
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import filter

from msg_rx import msg_rx

import correlate

"""
Thresholds a complex input sends it to a msg_rx

Output 0: Filtered signal (real part), threshold (complex part)
Output 1: Output of matched filter
Output 2: Threshold result

"""
class msg_rx_analog_matched(gr.hier_block2):
    def __init__(self, sample_rate, bit_rate, tag_callback):
        gr.hier_block2.__init__(self, "msg_rx_analog",
                                input_signature = gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                output_signature = gr.io_signature(3, 3, gr.sizeof_gr_complex))

        initial_taps = filter.firdes.high_pass_2(
            gain = 1,
            sampling_freq = sample_rate,
            cutoff_freq = 3000,
            transition_width = 1000,
            attenuation_dB = 20)
        initial_high_pass = filter.fir_filter_ccf(decimation = 1, taps = initial_taps)
        print "Initial low-pass filter: %d taps" % len(initial_taps)

        to_magnitude = blocks.complex_to_mag()

        # Matched filter
        # Number of taps = sample rate / (bit rate * 2)
        matched_taps = [1] * 55
        matched_filter = filter.fir_filter_ccc(decimation = 1, taps = matched_taps)

        # Filter the AGC output to estimate the correct threshold
        threshold_taps = filter.firdes.low_pass_2(
            gain = 1,
            sampling_freq = sample_rate,
            cutoff_freq = 100,
            transition_width = 1000,
            attenuation_dB = 30)
        print 'Threshold filter: %d taps' % len(threshold_taps)
        threshold_low_pass_filter = filter.fir_filter_fff(decimation = 1,
            taps = threshold_taps)

        thresh = blocks.threshold_ff(-0.05, 0.05)

        add_constant = blocks.add_const_cc(2.0 + 2.0j)

        rx = msg_rx(sample_rate, bit_rate, tag_callback)
        float_to_char = blocks.float_to_char()

        # Calculate correlation
        correlation_calc = correlate.correlation_calculator(sample_rate, bit_rate)

        self.connect(self,
            matched_filter,
            add_constant,
            to_magnitude)

        # Filter filtered AGC output
        self.connect(to_magnitude, threshold_low_pass_filter)
        # Subtract threshold filter output from AGC output
        threshold_subtract = blocks.sub_ff()
        self.connect(to_magnitude, (threshold_subtract, 0))
        self.connect(threshold_low_pass_filter, (threshold_subtract, 1))

        self.connect(threshold_subtract, thresh, float_to_char, rx)

        # Matched filter input output
        # self.connect(self, (self, 0))
        # Matched filter output output
        self.connect(matched_filter, (self, 1))

        # Group AGC output and threshold in a complex value
        group_complex = blocks.float_to_complex()
        self.connect(to_magnitude, (group_complex, 0))
        self.connect(threshold_low_pass_filter, (group_complex, 1))

        self.connect(group_complex, (self, 0))

        self.connect(thresh, blocks.float_to_complex(), (self, 2))
