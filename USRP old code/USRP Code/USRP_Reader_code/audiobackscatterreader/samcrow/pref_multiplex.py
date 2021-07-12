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

class pref_multiplex(gr.basic_block):
    """
    Accepts one input.
    If any samples are available on input 0, they are output. Otherwise,
    0s are output. (temporarily changed from 1s to 0s for testing)
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="pref_multiplex",
            in_sig=[numpy.int8],
            out_sig=[numpy.int8])


    def forecast(self, noutput_items, ninput_items_required):
        # Do not require any input
        ninput_items_required[0] = 0

    def general_work(self, input_items, output_items):
        if len(input_items[0]) > 0:
            # Have some input, copy it to output
            copy_count = min(len(output_items[0]), len(input_items[0]))
            for i in range(copy_count):
                output_items[0][i] = input_items[0][i]
            self.consume(0, copy_count)
            print "pref_multiplex: processed %d (some input)" % copy_count
            return copy_count
        else:
            # No input, fill output with 0s
            for i in range(len(output_items[0])):
                output_items[0][i] = 0
            print "pref_multiplex: processed %d (no input)" % len(output_items[0])
            return len(output_items[0]);

