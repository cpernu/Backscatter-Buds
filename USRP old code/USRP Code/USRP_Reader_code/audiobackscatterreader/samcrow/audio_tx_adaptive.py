# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Adaptive audio downlink
# Generated: Fri May 26 11:51:23 2017
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes


class audio_tx_adaptive(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "Adaptive audio downlink",
            gr.io_signature(0, 0, 0),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Variables
        ##################################################
        self.usrp_samp_rate = usrp_samp_rate = 1000000
        self.audio_samp_rate = audio_samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=125,
                decimation=6,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, audio_samp_rate, 20, 5, firdes.WIN_HAMMING, 6.76))
        self.carrier_source = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vff((0.707106, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.5, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_source_0 = audio.source(audio_samp_rate, "skype_monitor", True)
        self.audio_absolute_value = blocks.abs_ff(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_absolute_value, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_absolute_value, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.carrier_source, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_2, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self, 0))    

    def get_usrp_samp_rate(self):
        return self.usrp_samp_rate

    def set_usrp_samp_rate(self, usrp_samp_rate):
        self.usrp_samp_rate = usrp_samp_rate

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, 20, 5, firdes.WIN_HAMMING, 6.76))
