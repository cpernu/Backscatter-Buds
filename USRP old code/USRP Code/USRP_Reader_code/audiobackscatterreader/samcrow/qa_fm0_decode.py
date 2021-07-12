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
from fm0_decode import fm0_decode

class qa_fm0_decode (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    # All test inputs start with at least one zero, and then transition to 1

    def run_decode(self, input, expected_output):
        signal_src = blocks.vector_source_b(input)
        decode = fm0_decode(4, 2)
        self.tb.connect(signal_src, decode)
        sink = blocks.vector_sink_b()
        self.tb.connect(decode, sink)
        self.tb.run()
        result = sink.data()
        self.assertEqual(expected_output, result)

    def test_nothing(self):
        self.run_decode((0, 0, 0, 0, 0, 0, 0, 0), ())

    def test_all_one(self):
        input = (0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0,
            1, 1, 1, 1,
            0, 0, 0, 0, 1
        )
        self.run_decode(input, (1, 1, 1, 1, 1, 1, 1, 1))

    def test_all_zero(self):
        input = (0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0,
            1, 1, 0, 0, 1
        )
        self.run_decode(input, (0, 0, 0, 0, 0, 0, 0, 0))


    def test_mixed(self):
        input = (0,
                1, 1, 0, 0, # 0
                1, 1, 1, 1, # 1
                0, 0, 1, 1, # 0
                0, 0, 1, 1, # 0
                0, 0, 1, 1, # 0
                0, 0, 0, 0, # 1
                1, 1, 0, 0, # 0
                1, 1, 1, 1, 0) # 1, Last element provides an ending transition
        self.run_decode(input, (0, 1, 0, 0, 0, 1, 0, 1))

if __name__ == '__main__':
    gr_unittest.run(qa_fm0_decode, "qa_fm0_decode.xml")
