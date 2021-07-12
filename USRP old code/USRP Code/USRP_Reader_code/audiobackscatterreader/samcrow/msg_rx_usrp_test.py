

from gnuradio import gr, blocks, analog
from gnuradio import uhd
from PyQt4 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sys, sip
from msg_rx_analog import msg_rx_analog
from msg_rx_analog_matched import msg_rx_analog_matched
from audio_tx_adaptive import audio_tx_adaptive

# Mode constants
TX_ONES = 1
TX_AUDIO = 2

# Mode selection
TX_MODE = TX_ONES

class msg_tx_test(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)
        
        write_to_files = False

        samp_rate = 1000000
        bitRate = 9091
        freq = 912.002442e6
        bandwidth = 1000
        
        # USRP gain | actual transmit gain after amplifier
        # 0           20 dBm
        # 5           26 dBm
        # 10          30 dBm
        
        tx_gain = 10 # maximum 31.5
        rx_gain = 0
        
        # USRP
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('addr=192.168.10.2', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_subdev_spec('B:0', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_bandwidth(bandwidth, 0)
        
        
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('addr=192.168.10.2', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_subdev_spec('A:0', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(bandwidth, 0)
        
        if TX_MODE == TX_ONES:
            # Transmit constant 1
            analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)
            self.connect((analog_const_source_x_0, 0), (self.uhd_usrp_sink_0, 0))
        if TX_MODE == TX_AUDIO:
            audio = audio_tx_adaptive()
            self.connect(audio, self.uhd_usrp_sink_0)
            

        # Instrumentation
        
        self.raw_sink = qtgui.time_sink_c(60 * int(samp_rate / bitRate), samp_rate, "Raw")
        self.raw_sink_win = sip.wrapinstance(self.raw_sink.pyqwidget(), Qt.QWidget)
        self.raw_sink_win.show()
        
        self.post_matched_sink = qtgui.time_sink_c(60 * int(samp_rate / bitRate), samp_rate, "Post-matched filter")
        self.post_matched_sink_win = sip.wrapinstance(self.post_matched_sink.pyqwidget(), Qt.QWidget)
        self.post_matched_sink_win.show()
        
        self.post_agc_sink = qtgui.time_sink_c(60 * int(samp_rate / bitRate), samp_rate, "Filtered/threshold")
        self.post_agc_sink_win = sip.wrapinstance(self.post_agc_sink.pyqwidget(), Qt.QWidget)
        self.post_agc_sink_win.show()
        
        self.thresholded_sink = qtgui.time_sink_c(60 * int(samp_rate / bitRate), samp_rate, "Thresholded")
        self.thresholded_sink_win = sip.wrapinstance(self.thresholded_sink.pyqwidget(), Qt.QWidget)
        self.thresholded_sink_win.show()
        
        # FFT
        freq_sink = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"FFT", #name
        	1 #number of inputs
        )
        freq_sink_win = sip.wrapinstance(freq_sink.pyqwidget(), Qt.QWidget)
        freq_sink_win.show()
        

        rx = msg_rx_analog_matched(samp_rate, bitRate, receive_callback)
        self.connect(self.uhd_usrp_source_0, rx)
        self.connect((rx, 0), self.post_agc_sink)
        self.connect((rx, 1), self.post_matched_sink)
        self.connect(self.uhd_usrp_source_0, self.raw_sink)
        self.connect((rx, 2), self.thresholded_sink)
        self.connect((rx, 0), freq_sink)
        
        # Files
        if write_to_files:
            signal_threshold_file = blocks.file_sink(gr.sizeof_gr_complex, "signal_threshold.dat")
            # post_filter_file = blocks.file_sink(gr.sizeof_gr_complex, "post_matched_filter.dat")
            thresholded_file = blocks.file_sink(gr.sizeof_gr_complex, "thresholded.dat")
            raw_file = blocks.file_sink(gr.sizeof_gr_complex, "raw.dat")
            self.connect(self.uhd_usrp_source_0, raw_file)
            self.connect((rx, 0), signal_threshold_file)
            # self.connect((rx, 1), post_filter_file)
            self.connect((rx, 2), thresholded_file)
            


def receive_callback(header, payload):
    if header != None and payload != None:
        print "======================== Received =============================="
        print str(bytearray(header))
        print str(bytearray(payload))
        print "======================== Received =============================="


def main():
    qapp = Qt.QApplication(sys.argv)

    top = msg_tx_test()
    top.start()

    qapp.exec_()
    top.stop()

if __name__ == "__main__":
    main()
