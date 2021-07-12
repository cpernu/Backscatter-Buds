
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import filter

from msg_rx import msg_rx

"""
Thresholds a complex input sends it to a msg_rx

Output 0: Input to AGC
Output 1: Output of AGC (real part), filtered threshold (imaginary part)
Output 2: Threshold result

"""
class msg_rx_analog(gr.hier_block2):
    def __init__(self, sample_rate, bit_rate, tag_callback):
        gr.hier_block2.__init__(self, "msg_rx_analog",
                                input_signature = gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                output_signature = gr.io_signature(3, 3, gr.sizeof_gr_complex))

        # TODO: add skip head block to fix startup issue.
        
        taps = filter.firdes.low_pass_2(
            gain = 1,
            sampling_freq = sample_rate,
            cutoff_freq = 75000,
            transition_width = 1000,
            attenuation_dB = 40)
        low_pass_filter = filter.fir_filter_ccf(decimation = 1, taps = taps)
        print "Initial low-pass filter: %d taps" % len(taps)

        to_magnitude = blocks.complex_to_mag()
        agc = analog.agc2_ff(attack_rate = 0.01,
            decay_rate = 3e-3,
            reference = 1,
            gain = 1)
        
        
        post_agc_taps = filter.firdes.low_pass_2(
            gain = 1,
            sampling_freq = sample_rate,
            cutoff_freq = 50000,
            transition_width = 10000,
            attenuation_dB = 40)
        post_agc_low_pass_filter = filter.fir_filter_fff(decimation = 1,
            taps = post_agc_taps)
        print 'Post-AGC filter: %d taps' % len(post_agc_taps)
            
        # Filter the AGC output to estimate the correct threshold
        threshold_taps = filter.firdes.low_pass_2(
            gain = 0.98,
            sampling_freq = sample_rate,
            cutoff_freq = 75,
            transition_width = 1000,
            attenuation_dB = 20)
        print 'Threshold filter: %d taps' % len(threshold_taps)
        threshold_low_pass_filter = filter.fir_filter_fff(decimation = 1,
            taps = threshold_taps)
        
        thresh = blocks.threshold_ff(0.05, 0.08)
        
        add_constant = blocks.add_const_cc(0.1 + 0.1j)

        rx = msg_rx(sample_rate, bit_rate, tag_callback)
        float_to_char = blocks.float_to_char()

        self.connect(self,
            low_pass_filter,
            add_constant,
            to_magnitude,
            agc,
            post_agc_low_pass_filter)
        
        # Filter filtered AGC output
        self.connect(post_agc_low_pass_filter, threshold_low_pass_filter)
        # Subtract threshold filter output from AGC output
        threshold_subtract = blocks.sub_ff()
        self.connect(post_agc_low_pass_filter, (threshold_subtract, 0))
        self.connect(threshold_low_pass_filter, (threshold_subtract, 1))
        
        self.connect(threshold_subtract, thresh, float_to_char, rx)
        
        self.connect(to_magnitude, blocks.float_to_complex(), (self, 0))
        
        # Group AGC output and threshold in a complex value
        group_complex = blocks.float_to_complex()
        self.connect(post_agc_low_pass_filter, (group_complex, 0))
        self.connect(threshold_low_pass_filter, (group_complex, 1))
        
        self.connect(group_complex, (self, 1))
        
        self.connect(thresh, blocks.float_to_complex(), (self, 2))
        
        
        
