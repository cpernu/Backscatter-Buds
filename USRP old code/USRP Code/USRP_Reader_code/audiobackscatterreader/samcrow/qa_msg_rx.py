#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from msg_rx import msg_rx

class qa_msg_rx (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block()

    def tearDown (self):
        self.tb = None

    """
    Format:
    Preamble: 2 bytes: 0, 3
    Tag ID: 1 byte
    Message length: 1 byte
    Message ID (or something): 1 byte
    Payload: message length bytes
    Checksum: 1 byte

    The checksum is the sum of the tag ID, length, message ID, and each payload byte

    In each byte, the most significant bit is first.
    """

    def testZeroFrame(self):
        # Workaround for capturing, which Python 2 does not fully support
        out_tag_id = [None]
        out_payload = [None]
        def frame_callback(tag_id, payload):
            print "Frame callback"
            out_tag_id[0] = tag_id
            out_payload[0] = payload

        source = blocks.vector_source_c((
            # A few samples to start
            0, 0, 0, 0,
            # One byte with a value of 0
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            # One byte with a value of 3
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            # Tag ID byte: 0xFF
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            # Length: 1
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 1, 1,
            # Message ID: 0
            0, 0, 1, 1,
            0, 0, 1, 1,
            0, 0, 1, 1,
            0, 0, 1, 1,
            0, 0, 1, 1,
            0, 0, 1, 1,
            0, 0, 1, 1,
            0, 0, 1, 1,
            # Payload: 0x72
            0, 0, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 1, 1,
            0, 0, 1, 1,
            # Checksum = 0xFF + 1 + 0 + 0x72 = 0x72
            0, 0, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 1, 1,
            0, 0, 1, 1,
            # Ending
            0, 0, 0, 0,
        ))

        rx_block = msg_rx(4, 2, frame_callback)
        self.tb.connect(source, rx_block)
        self.tb.run()

        self.assertEqual(out_tag_id[0], 0xFF)
        self.assertEqual(out_payload[0], chr(0x72))



if __name__ == '__main__':
    gr_unittest.run(qa_msg_rx, "qa_msg_rx.xml")
