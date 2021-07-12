
import numpy
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from fm0_decode import fm0_decode
from framer import framer

"""
Accepts chars and decodes them as messages
"""
class msg_rx(gr.hier_block2):
    def __init__(self, sample_rate, bit_rate, tag_callback):
        gr.hier_block2.__init__(self, "msg_rx",
                                input_signature = gr.io_signature(1, 1, gr.sizeof_char),
                                output_signature = gr.io_signature(0, 0, 0))
                                
        fm0decode = fm0_decode(sample_rate, bit_rate)
        frame_framer = framer(tag_callback)

        self.connect(self,
            fm0decode,
            frame_framer)
