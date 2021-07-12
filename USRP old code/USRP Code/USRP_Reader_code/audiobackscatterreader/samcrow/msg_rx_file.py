

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr

from msg_rx_analog import msg_rx_analog

class msg_rx_file(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        samp_rate = 2000000
        # This appears to be the actual bit rate of the recorded data
        # (84 samples per bit)
        bit_rate = 23809

        in_file = blocks.file_source(gr.sizeof_gr_complex, '../../Capture2/test3-data')
        throttle = blocks.throttle(gr.sizeof_gr_complex, samp_rate)
        
        rx = msg_rx_analog(samp_rate, bit_rate, receive_callback)
        self.connect(in_file, throttle, rx)


def receive_callback(tag_id, payload):
    print "Received"

def main():
    top = msg_rx_file()
    top.run()

if __name__ == "__main__":
    main()
