

from msg_tx import msg_tx
from gnuradio import gr, blocks, analog
from gnuradio import uhd
from PyQt4 import Qt
from gnuradio import qtgui
import sys, sip, os
import time
import threading

class msg_tx_test(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        # Increasing the sample rate above 1 Msps reduces latency
        # At 8 Msps, the UHD software displays a warning.
        sampRate = 4000000
        bitRate = 12500
        freq = 912.002442e6

        # USRP
        usrp_tx = uhd.single_usrp_sink('addr=192.168.10.2', uhd.io_type_t.COMPLEX_FLOAT32,1)
        usrp_tx.set_subdev_spec('A:0', 0)
        usrp_tx.set_samp_rate(sampRate)
        usrp_tx.set_center_freq(freq, 0)
        usrp_tx.set_gain(10)
        usrp_tx.set_antenna('TX/RX', 0)

        self.mtx = msg_tx(sampRate, bitRate)

        self.connect(self.mtx, usrp_tx)

        # file_sink = blocks.file_sink(gr.sizeof_gr_complex, "transmit_test")
        # self.connect(self.to_complex, file_sink)

        # Instrumentation
        self.time_sink = qtgui.time_sink_c(120 * int(sampRate / bitRate),
          sampRate, "Send test")
        self.snk_win = sip.wrapinstance(self.time_sink.pyqwidget(), Qt.QWidget)
        self.snk_win.show()

        self.connect(self.mtx, self.time_sink)

    def send(self, tag, payload):
        self.mtx.send(tag, payload)

def main():
    print "PID %d" % os.getpid()
    qapp = Qt.QApplication(sys.argv)

    top = msg_tx_test()
    top.start()

    thread_running = True
    def run():
        while thread_running:
            print "Press return to send a message"
            raw_input()
            top.send(5, "\x11")

    thread = threading.Thread(group = None, target = run)
    thread.start()

    qapp.exec_()

    # while True:
    #     # print "Sending"
    #     # top.send(5, '\x10')
    #     time.sleep(1)

    top.stop()
    thread_running = False
    top.wait()

if __name__ == "__main__":
    main()
