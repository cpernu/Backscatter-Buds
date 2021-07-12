import numpy
import collections
import itertools
from gnuradio import gr
import backscatter_frame


class framer(gr.sync_block):

    # When checking for the preamble, ignore this many bits at the beginning
    # to allow for initial inaccurate decoding
    PREAMBLE_IGNORE_BITS = 4

    """
    """
    def __init__(self, tag_callback):
        gr.sync_block.__init__(self,
            name="backscatter_framer",
            in_sig=[numpy.int8],
            out_sig=[])

        self.tag_callback = tag_callback

        self.preamble_ref = collections.deque(backscatter_frame.getPreamble())
        self.preamble = collections.deque([], len(backscatter_frame.getPreamble()))
        self.header = collections.deque([])
        self.payload = collections.deque([])


    def work(self, input_items, output_items):
        in0 = input_items[0]

        for bit in in0:
            preamble_slice = itertools.islice(self.preamble,
                framer.PREAMBLE_IGNORE_BITS,
                len(self.preamble))
            preamble_ref_slice = itertools.islice(self.preamble_ref,
                framer.PREAMBLE_IGNORE_BITS,
                len(self.preamble_ref))

            if list(preamble_slice) == list(preamble_ref_slice):
                if len(self.header) == backscatter_frame.getHeaderLen():
                    if len(self.payload) == backscatter_frame.getPayloadLen(list(self.header)):
                        deframed = backscatter_frame.deframe(list(self.header), list(self.payload))
                        if deframed != (None, None):
                            self.tag_callback(*deframed)
                        self.payload.clear()
                        self.header.clear()
                        self.preamble.clear()
                    else:
                        self.payload.append(bit)
                else:
                    self.header.append(bit)
            else:
                self.preamble.append(bit)

        if len(self.header) == backscatter_frame.getHeaderLen() and len(self.payload) == backscatter_frame.getPayloadLen(list(self.header)):
            (tag_id, payload) = backscatter_frame.deframe(list(self.header), list(self.payload))
            if tag_id != None and payload != None:
                self.tag_callback(tag_id, payload)
                # Added for use in GNURadio companion, where adding a callback is not easy
                print "======================== Received =============================="
                print "Tag ID: " + str(bytearray(tag_id))
                print "Payload: " + str(bytearray(payload))
                print "======================== Received =============================="

            self.payload.clear()
            self.header.clear()
            self.preamble.clear()
            
        
        # For correlate testing only: Call the tag callback
        # if a preamble stream tag is present
        
        # Find any tags in in0
        tags = self.get_tags_in_window(0, 0, len(in0))
        if len(tags) > 0:
            print "Got tag"
            self.tag_callback(5, '')

        return len(in0)
