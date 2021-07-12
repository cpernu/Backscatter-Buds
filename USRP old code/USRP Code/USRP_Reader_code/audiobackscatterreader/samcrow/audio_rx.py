# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Audio uplink receive
# Generated: Fri Jun  2 13:47:26 2017
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes


class audio_rx(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "Audio uplink receive",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(0, 0, 0),
        )

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.cf = cf = 912e6

        ##################################################
        # Blocks
        ##################################################
        self.fractional_resampler_xx_0 = filter.fractional_resampler_ff(0, 1e6/48e3)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(1, firdes.band_pass(
        	1, 48e3, 300, 3400, 300, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "audio_rx_loopback", True)
        self.analog_agc2_xx_0 = analog.agc2_ff(0.08, 0.005, 0.1, 100)
        self.analog_agc2_xx_0.set_max_gain(10000)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.fractional_resampler_xx_0, 0))    
        self.connect((self.fractional_resampler_xx_0, 0), (self.band_pass_filter_0, 0))    
        self.connect((self, 0), (self.blocks_complex_to_mag_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_cf(self):
        return self.cf

    def set_cf(self, cf):
        self.cf = cf
