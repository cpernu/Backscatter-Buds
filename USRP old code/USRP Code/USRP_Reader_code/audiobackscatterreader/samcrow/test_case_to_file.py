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

"""
Writes test data to a complex binary file
"""

from gnuradio import gr
from gnuradio import blocks
from msg_rx import msg_rx

sampRate = 2000000
bitRate = 100000

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
    # Payload: 0x72
    0, 0, 1, 1,
    0, 0, 0, 0,
    1, 1, 1, 1,
    0, 0, 0, 0,
    1, 1, 0, 0,
    1, 1, 0, 0,
    1, 1, 1, 1,
    0, 0, 1, 1,
    # Checksum = 0xFF + 1 + 1 + 0x72 = 0x73
    0, 0, 1, 1,
    0, 0, 0, 0,
    1, 1, 1, 1,
    0, 0, 0, 0,
    1, 1, 0, 0,
    1, 1, 0, 0,
    1, 1, 1, 1,
    0, 0, 0, 0,
    # Ending
    1, 1, 1, 1,
))


# Source has 4 samples per bit
# Duplicate samples to get the correct sample rate and bit rate
duplicate_factor = sampRate / bitRate / 4
repeat = blocks.repeat(gr.sizeof_gr_complex, duplicate_factor)

# File output
file = blocks.file_sink(gr.sizeof_gr_complex, "test_data")

tb = gr.top_block()
tb.connect(source, repeat, file)
tb.run()
