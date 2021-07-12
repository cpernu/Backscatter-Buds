
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import filter

from msg_rx import msg_rx

import correlate
import correlate_threshold

"""
Thresholds a complex input sends it to a msg_rx

Uses correlation to detect preambles

On the thresholded signal sent to the msg_rx block, a stream tag with a key
of "preamble" appears at the beginning of every message.


"""
class msg_rx_analog_correlate(gr.hier_block2):
    def __init__(self, sample_rate, bit_rate, tag_callback):
        gr.hier_block2.__init__(self, "msg_rx_analog",
                                input_signature = gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                output_signature = gr.io_signature(0, 0, gr.sizeof_gr_complex))

        # Matched filter
        # Number of taps = sample rate / (bit rate * 2)
        matched_taps = [1] * 55
        matched_filter = filter.fir_filter_ccc(decimation = 1, taps = matched_taps)

        # Calculate correlation
        correlation_calc = correlate.correlation_calculator(sample_rate, bit_rate)
        # Connections from correlation calculator to correlation threshold
        # processor
        correlation_to_mag = blocks.complex_to_mag()
        correlation_mag_threshold = blocks.threshold_ff(100, 200)
        # Correlation threshold processor
        correlate_threshold_block = correlate_threshold.correlate_threshold(sample_rate, bit_rate)
        
        
        # Threshold for signal after correlation threshold processor
        signal_threshold = blocks.threshold_ff(0.5, 0.5)
       
        rx = msg_rx(sample_rate, bit_rate, tag_callback)
        float_to_char = blocks.float_to_char()
        
        # Connections
        # input -> matched filter -> correlation calculator
        self.connect(self,
            matched_filter,
            correlation_calc)
        # Correlate input
        self.connect(correlation_calc, (correlate_threshold_block, 1))
        # Magnitude of correlation to correlation threshold processor
        # thresholded input
        self.connect(correlation_calc,
            correlation_to_mag,
            correlation_mag_threshold,
            (correlate_threshold_block, 2))
        # Signal from matched filter to correlation threshold processor input 0
        self.connect(matched_filter, (correlate_threshold_block, 0))

        # Correlation threshold processor -> signal threshold
        self.connect(correlate_threshold_block, signal_threshold)
        
        # Threshold of signal to receive mechanism
        self.connect(signal_threshold, float_to_char, rx)

