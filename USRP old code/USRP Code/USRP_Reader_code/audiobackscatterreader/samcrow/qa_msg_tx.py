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
from msg_tx import msg_tx
import time

class qa_msg_tx (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block()

    def tearDown (self):
        self.tb = None

    def test_one_byte_zero(self):
        # Do not use self.tb, to avoid freezing (deadlock) in teardown
        top = gr.top_block()
        sink = blocks.vector_sink_b()
        # Configure for 1 sample per half-bit (no repeating)
        mtx = msg_tx(2, 1)
        top.connect(mtx, sink)

        top.start()
        mtx.send(0, "\x00")
        time.sleep(0.1)
        top.stop()
        data = sink.data()
        expected = (
            # TODO
        )
        self.assertEqual(expected, data)



if __name__ == '__main__':
    gr_unittest.run(qa_msg_tx, "qa_msg_tx.xml")
