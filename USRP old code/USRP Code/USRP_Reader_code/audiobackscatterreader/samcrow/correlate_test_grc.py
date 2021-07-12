#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Correlate Test Grc
# Generated: Fri Jun  9 11:31:34 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from correlate import correlation_calculator
from correlate_threshold import correlate_threshold
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from msg_rx import msg_rx
from optparse import OptionParser
import sip
import sys
import time


class correlate_test_grc(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Correlate Test Grc")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Correlate Test Grc")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "correlate_test_grc")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.time_sink_seconds = time_sink_seconds = 0.5
        self.sample_rate = sample_rate = 1000000
        self.cf = cf = 912.002442e6
        self.bit_rate = bit_rate = 9091

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_subdev_spec("B:0", 0)
        self.uhd_usrp_source_0.set_samp_rate(sample_rate)
        self.uhd_usrp_source_0.set_center_freq(cf, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0.set_bandwidth(1000, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_subdev_spec("A:0", 0)
        self.uhd_usrp_sink_0.set_samp_rate(sample_rate)
        self.uhd_usrp_sink_0.set_center_freq(cf, 0)
        self.uhd_usrp_sink_0.set_gain(1, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(40e6, 0)
        self.qtgui_time_sink_x_1_0_0 = qtgui.time_sink_f(
        	int(time_sink_seconds * sample_rate), #size
        	sample_rate, #samp_rate
        	"Thresholded", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1_0_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "preamble")
        self.qtgui_time_sink_x_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_0_0.enable_control_panel(True)
        
        if not True:
          self.qtgui_time_sink_x_1_0_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_0_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	int(time_sink_seconds * sample_rate), #size
        	sample_rate, #samp_rate
        	"Normalized", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "preamble")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_control_panel(True)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.msg_rx_0 = msg_rx(sample_rate, bit_rate, lambda header, payload: None)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, ([1] * 55))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.correlation_calculator_0 = correlation_calculator(sample_rate, bit_rate)
        self.correlate_threshold_0 = correlate_threshold(sample_rate, bit_rate)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(-0.5, -0.5, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(100, 200, 0)
        self.blocks_float_to_complex_1_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_sink_0_1_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "thresholded.dat", False)
        self.blocks_file_sink_0_1_0.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_gr_complex*1, "normalized.dat", False)
        self.blocks_file_sink_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "matched_filter.dat", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "correlation.dat", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_float_to_char_0, 0), (self.msg_rx_0, 0))    
        self.connect((self.blocks_float_to_complex_1, 0), (self.blocks_file_sink_0_1, 0))    
        self.connect((self.blocks_float_to_complex_1_0, 0), (self.blocks_file_sink_0_1_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.correlate_threshold_0, 2))    
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_char_0, 0))    
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_complex_1_0, 0))    
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.qtgui_time_sink_x_1_0_0, 0))    
        self.connect((self.correlate_threshold_0, 0), (self.blocks_float_to_complex_1, 0))    
        self.connect((self.correlate_threshold_0, 0), (self.blocks_threshold_ff_0_0, 0))    
        self.connect((self.correlate_threshold_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.correlation_calculator_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.correlation_calculator_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.correlation_calculator_0, 0), (self.correlate_threshold_0, 1))    
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.correlate_threshold_0, 0))    
        self.connect((self.fir_filter_xxx_0, 0), (self.correlation_calculator_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.fir_filter_xxx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "correlate_test_grc")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_time_sink_seconds(self):
        return self.time_sink_seconds

    def set_time_sink_seconds(self, time_sink_seconds):
        self.time_sink_seconds = time_sink_seconds

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.qtgui_time_sink_x_1.set_samp_rate(self.sample_rate)
        self.qtgui_time_sink_x_1_0_0.set_samp_rate(self.sample_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.sample_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.sample_rate)

    def get_cf(self):
        return self.cf

    def set_cf(self, cf):
        self.cf = cf
        self.uhd_usrp_source_0.set_center_freq(self.cf, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.cf, 0)
        self.uhd_usrp_sink_0.set_center_freq(self.cf, 1)

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate


def main(top_block_cls=correlate_test_grc, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
