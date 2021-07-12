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
from pie_encode import pie_encode

class qa_pie_encode (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_all_zero (self):
        # set up fg
        signal = (0, 0, 0, 0, 0, 0, 0, 0)

        signal_src = blocks.vector_source_b(signal)
        encode = pie_encode()
        self.tb.connect(signal_src, encode)
        sink = blocks.vector_sink_b()
        self.tb.connect(encode, sink)

        self.tb.run()
        expected_result = (0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1,
                           0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1)
        result = sink.data()
        # check data
        self.assertEqual(expected_result, result)
    #
    # def test_all_one (self):
    #     # set up fg
    #     # 4 clock periods
    #     clock = (0, 1, 0, 1, 0, 1, 0, 1)
    #     signal = (1, 1, 1, 1, 1, 1, 1, 1)
    #
    #     clock_src = blocks.vector_source_b(clock)
    #     signal_src = blocks.vector_source_b(signal)
    #     encode = fm0_encode()
    #     self.tb.connect(clock_src, (encode, 0))
    #     self.tb.connect(signal_src, (encode, 1))
    #     sink = blocks.vector_sink_b()
    #     self.tb.connect(encode, sink)
    #
    #     self.tb.run()
    #     expected_result = (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1)
    #     result = sink.data()
    #     # check data
    #     self.assertEqual(expected_result, result)
    #
    #
    # def test_complex (self):
    #     # set up fg
    #     # 4 clock periods
    #     clock = (0, 1, 0, 1, 0, 1, 0, 1)
    #     signal = (0, 0, 1, 1, 1, 0, 1, 0)
    #
    #     clock_src = blocks.vector_source_b(clock)
    #     signal_src = blocks.vector_source_b(signal)
    #     encode = fm0_encode()
    #     self.tb.connect(clock_src, (encode, 0))
    #     self.tb.connect(signal_src, (encode, 1))
    #     sink = blocks.vector_sink_b()
    #     self.tb.connect(encode, sink)
    #
    #     self.tb.run()
    #     expected_result = (0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1)
    #     result = sink.data()
    #     # check data
    #     self.assertEqual(expected_result, result)


if __name__ == '__main__':
    gr_unittest.run(qa_pie_encode, "qa_pie_encode.xml")
