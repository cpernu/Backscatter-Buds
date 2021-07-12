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
import struct
from gnuradio import gr
from gnuradio import blocks
from fm0_encode import fm0_encode
from msg_tx_source import msg_tx_source
import backscatter_frame


class msg_tx(gr.hier_block2):
    """
    Encodes and outputs messages

    Outputs a sequence of 0/1 values suitable for sending at the provided
    sample rate.
    """
    def __init__(self, sample_rate, bit_rate):
        gr.hier_block2.__init__(self,
            name = "msg_tx",
            input_signature = gr.io_signature(0, 0, 0),
            output_signature = gr.io_signature(1, 1, gr.sizeof_gr_complex))

        # Begin blocks for message data path
        # Message source
        self.msg = msg_tx_source(sample_rate, bit_rate)

        # Connections
        self.connect(self.msg,self)

    """
    Sends a message.
    tag is the ID of the tag to send to.

    The message should be a string or something that can be converted into
    a string.
    """
    def send(self, tag, message):
        print "Sending message with tag %d" % tag
        encoded = backscatter_frame.frame(tag, message)
        self.msg.send_message(encoded)
