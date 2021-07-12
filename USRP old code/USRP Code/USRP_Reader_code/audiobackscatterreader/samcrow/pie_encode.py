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

import numpy
from gnuradio import gr

class pie_encode(gr.basic_block):
    """
    Encodes a stream of bytes using pulse interval encoding.

    Each sample with a value of 1 received is converted into a 0 followed by
    a 1. Each sample with a value of 0 is converted into a 0 followed by two 1s.
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="pie_encode",
            in_sig=[numpy.int8],
            out_sig=[numpy.int8])

    def forecast(self, noutput_items, ninput_items_required):
        # Assume all bits will be 1
        # Require one input per two outputs
        ninput_items_required[0] = noutput_items / 2

    def general_work(self, input_items, output_items):
        i = 0
        for value in input_items[0]:
            # Check that this input value will
            if (i + 2) >= len(output_items[0]):
                break
            output_items[0][i] = 0
            output_items[0][i + 1] = 1
            i += 2
            if not value:
                output_items[0][i] = 1
                i += 1
            # Consume one input value
            self.consume(0, 1)

        return i
