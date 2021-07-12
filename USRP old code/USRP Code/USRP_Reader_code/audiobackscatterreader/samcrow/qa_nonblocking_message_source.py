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

import time
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from nonblocking_message_source import nonblocking_message_source

class qa_nonblocking_message_source (gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block ()

    def tearDown(self):
        self.tb = None

    def test_empty(self):
        # set up fg
        source = nonblocking_message_source()
        sink = blocks.vector_sink_b()
        self.tb.connect(source, sink)

        source.send(255)
        print("Starting")
        self.tb.start()
        print("Started, waiting")
        time.wait(1)
        print("Stopping")
        self.tb.stop()
        print("Stopped")

        # check data
        self.assertEqual((255), sink.data())


if __name__ == '__main__':
    gr_unittest.run(qa_nonblocking_message_source, "qa_nonblocking_message_source.xml")
