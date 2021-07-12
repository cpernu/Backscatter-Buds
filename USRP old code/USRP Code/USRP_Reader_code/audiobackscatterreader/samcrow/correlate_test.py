
from gnuradio import gr

import correlate
import correlate_threshold

class correlate_test(gr.top_block):
    def __init__(self, sample_rate, bit_rate):
        gr.top_block.__init__(self)
