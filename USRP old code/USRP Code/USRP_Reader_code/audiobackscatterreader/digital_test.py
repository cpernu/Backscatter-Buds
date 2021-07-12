#!/usr/bin/env python

# Copyright (c) 2015, Bryce Kellogg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its contributors
#     may be used to endorse or promote products derived from this software without
#     specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
#  OF SUCH DAMAGE.

from gnuradio import gr
from gnuradio import uhd
from gnuradio import blocks
from gnuradio import analog

import sys

import backscatter

class my_top_block(gr.top_block):
    def __init__(self, usrp_tx_addr, usrp_rx_addr):
        gr.top_block.__init__(self)

        sampRate = 2e6
        bitRate = 328
        freq = 915e6
       
        ##################
        # TX and Speaker #
        ##################

        # USRP
        usrp_tx = uhd.single_usrp_sink('addr=' + usrp_tx_addr, uhd.io_type_t.COMPLEX_FLOAT32,1)
        usrp_tx.set_samp_rate(sampRate)
        #usrp_tx.set_clock_source("external", 0)
        usrp_tx.set_center_freq(freq, 0)
        usrp_tx.set_antenna('TX/RX',0)
        #usrp_tx.set_gain(30.0);

        # Blocks/Connections
        self.cmd_tx = backscatter.tx(sampRate, bitRate)
        self.f_to_c = blocks.float_to_complex()

        self.connect(self.cmd_tx, self.f_to_c, usrp_tx)

        ##############
        # RX and Mic #
        ##############

        # USRP
        #usrp_rx = uhd.single_usrp_source('addr=' + usrp_rx_addr, uhd.io_type_t.COMPLEX_FLOAT32,1)
        #usrp_rx.set_clock_source("mimo", 0)
        #usrp_rx.set_time_source("mimo", 0)
        #usrp_rx.set_samp_rate(sampRate)
        #usrp_rx.set_center_freq(freq, 0)
        #usrp_rx.set_antenna('TX/RX',0)
        #usrp_rx.set_gain(20.0);

        # Blocks
        #cmd_rx = backscatter.rx(sampRate, bitRate, self.Tag_RX_CMD)
        #filesink = blocks.file_sink(gr.sizeof_gr_complex, "./data/data.usrp")

        # Connections
        #self.connect(usrp_rx, cmd_rx)
        #self.connect(usrp_rx, filesink)

    #############
    # Tag Comms #
    #############
    def Tag_RX_CMD(self, tagID, payload):
        if tagID == None or payload == None:
            print("ERROR: CRC")
            return

        print("Receiving:")
        print(" ID : " + str(tagID))
        print(" MSG: " + payload)
        print(" LEN: " + str(len(payload)))
       
    def Tag_TX_CMD(self, tagID, payload):
        print("Sending:")
        print(" ID : " + str(tagID))
        print(" MSG: " + payload)
        print(" LEN: " + str(len(payload)))
        #self.setCMD()
        self.cmd_tx.send(tagID, payload)
        #self.setCW()

def main():
    # Arguments
    if len(sys.argv) != 3:
        print "Usage: ", sys.argv[0], "<USRP TX IP> <USRP RX IP>"
        exit(1)

    usrp_tx_addr = sys.argv[1]
    usrp_rx_addr = sys.argv[2]

    # Construct and initialize Gnuradio top block
    global tb
    tb = my_top_block(usrp_tx_addr, usrp_rx_addr)
    tb.start()

    # Begin program loop
    while 1:
        tb.Tag_TX_CMD(5, 'X')
        c = raw_input("'q' to quit\n")
        if c == "q":
            tb.stop()
            break

if __name__ == '__main__':
    main()
