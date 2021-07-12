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
from fm0_encode import fm0_encode

class qa_fm0_encode (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def run_encode(self, input, expected):
        source = blocks.vector_source_b(input)
        encode = fm0_encode()
        sink = blocks.vector_sink_b()
        self.tb.connect(source, encode, sink)
        self.tb.run()
        self.assertEqual(expected, sink.data())

    def test_all_zero (self):
        # 4 clock periods
        self.run_encode((0, 0, 0, 0, 0, 0, 0, 0),
            (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1))

    def test_all_one (self):
        self.run_encode((1, 1, 1, 1, 1, 1, 1, 1),
            (0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1))


    def test_complex (self):
        self.run_encode((0, 0, 1, 1, 1, 0, 1, 0),
            (0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1))


if __name__ == '__main__':
    gr_unittest.run(qa_fm0_encode, "qa_fm0_encode.xml")
