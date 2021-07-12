# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Audio downlink transmitter
# Generated: Wed May 31 16:52:33 2017
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes


class audio_tx(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "Audio downlink transmitter",
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
        self.fractional_resampler_xx_0 = filter.fractional_resampler_ff(0, float(audio_samp_rate) /float(usrp_samp_rate))
        self.carrier_source = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vff((0.707106, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((0.5, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((1, ))
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(usrp_samp_rate * 0.00001), 1.11111e-1, 4000)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_source_0 = audio.source(audio_samp_rate, "skype_monitor", True)
        self.audio_absolute_value = blocks.abs_ff(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_absolute_value, 0), (self.blocks_moving_average_xx_0, 0))    
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.fractional_resampler_xx_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self, 0))    
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_multiply_const_vxx_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_absolute_value, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.carrier_source, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.fractional_resampler_xx_0, 0), (self.blocks_float_to_complex_0, 0))    

    def get_usrp_samp_rate(self):
        return self.usrp_samp_rate

    def set_usrp_samp_rate(self, usrp_samp_rate):
        self.usrp_samp_rate = usrp_samp_rate
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.usrp_samp_rate * 0.00001), 1.11111e-1)
        self.fractional_resampler_xx_0.set_resamp_ratio(float(self.audio_samp_rate) /float(self.usrp_samp_rate))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.fractional_resampler_xx_0.set_resamp_ratio(float(self.audio_samp_rate) /float(self.usrp_samp_rate))
