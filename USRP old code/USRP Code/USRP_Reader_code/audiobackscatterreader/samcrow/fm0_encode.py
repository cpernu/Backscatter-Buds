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
import itertools
from gnuradio import gr

class fm0_encode(gr.interp_block):
    """
    An FM0 encoder

    Takes a data signal of int8s, containing 0 and 1 values

    Outputs an FM0-encoded stream of 0 and 1 values
    """
    def __init__(self):
        # The last output value, 0 or 1
        self.previous = 1

        gr.interp_block.__init__(self,
            name="fm0_encode",
            in_sig=[numpy.int8],
            # Interpolation of 2: 2 output samples for each input
            out_sig=[numpy.int8], interp = 2)

    def work(self, input_items, output_items):
        signal = input_items[0]
        out = output_items[0]

        for i, signalbit in enumerate(signal):
            # Use the mapping defined in the EPC specification:
            # 0 => period with transition
            # 1 => period without transition
            if signalbit:
                # Two samples opposite of previous
                inverted = invert(self.previous)
                out[2 * i] = inverted
                out[(2 * i) + 1] = inverted
                self.previous = inverted
            else:
                # One sample the opposite of previous, then one previous
                out[2 * i] = invert(self.previous);
                out[(2 * i) + 1] = self.previous;
                # self.previous does not change
        return len(out)

# Inverts a bit. Converts 1 to 0 and 0 to 1.
def invert(b):
    return int(not b)

"""
Encodes a sequence of 1s and 0s in FMO

Assumes that the signal is 1 before the start of data.

data: An array-like object containing zero or more 1s and 0s
data must not conain any values other than 0 or 1.

Returns an array with double the length of data, containing its FM0-encoded form

"""
def procedural_fm0_encode(data):
    previous = 0
    result = [0] * (2 * len(data))
    for i, signalbit in enumerate(data):
        # Use the mapping defined in the EPC specification:
        # 0 => period with transition
        # 1 => period without transition
        if signalbit:
            # Two samples opposite of previous
            inverted = invert(previous)
            result[2 * i] = inverted
            result[2 * i + 1] = inverted
            previous = inverted
        else:
            # One sample the opposite of previous, then one previous
            result[2 * i] = invert(previous);
            result[2 * i + 1] = previous;
            # previous does not change
    return result
