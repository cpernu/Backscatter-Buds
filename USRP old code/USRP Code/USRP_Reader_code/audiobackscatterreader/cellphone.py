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

from grc_gnuradio import blks2

import sys
import socket
import time
import thread
from bitarray import bitarray

import Skype4Py

import backscatter

state = "CW"

class my_top_block(gr.top_block):
    def __init__(self, usrp_tx_addr, usrp_rx_addr):
        gr.top_block.__init__(self)

        sampRate = 2e6
        bitRate = 100e3
        freq = 915e6
       
        ##################
        # TX and Speaker #
        ##################

        # USRP
        usrp_tx = uhd.single_usrp_sink('addr=' + usrp_tx_addr, uhd.io_type_t.COMPLEX_FLOAT32,1)
        #usrp_tx.set_clock_source("external", 0)
        usrp_tx.set_samp_rate(sampRate)
        usrp_tx.set_center_freq(freq, 0)
        usrp_tx.set_antenna('TX/RX',0)
        usrp_tx.set_gain(31)


        # Blocks
        self.cmd_tx = backscatter.tx(sampRate, bitRate)
        self.sel_tx = blks2.selector(gr.sizeof_float, 2, 1, 0, 0) # Mux

        # Connections
        #self.connect(self.cmd_tx, (self.sel_tx, 1))
        self.connect(self.cmd_tx, blocks.float_to_complex(), usrp_tx)

        ##############
        # RX and Mic #
        ##############

        # USRP
        usrp_rx = uhd.single_usrp_source('addr=' + usrp_rx_addr, uhd.io_type_t.COMPLEX_FLOAT32,1)
        usrp_rx.set_clock_source("mimo", 0)
        usrp_rx.set_time_source("mimo", 0)
        usrp_rx.set_samp_rate(sampRate)
        usrp_rx.set_center_freq(freq, 0)
        usrp_rx.set_antenna('TX/RX',0)
        usrp_rx.set_gain(0.0);

        # Blocks
        cmd_rx = backscatter.rx(sampRate, bitRate, self.Tag_RX_CMD)
        filesink = blocks.file_sink(gr.sizeof_gr_complex, "data.usrp")

        # Connections
        #self.connect(usrp_rx, cmd_rx)
        self.connect(usrp_rx, filesink)

    def usrp_msg_hendler(msg_type, msg):
        print(msg)

    ######################################
    # Switching between CW/CMD and Audio #
    ######################################
    def setMode(self, mode):
        self.stop()
        self.wait()
        self.sel_tx.set_input_index(mode)
        self.start()

    ###########################
    # RPC Comms to Other Side #
    ###########################
    def RPC_ListenStart(self):
        """
        Initiates the speaker on the tag.
        
        Sends a ListenStart command and waits
        for an ack. If not acked, returns False.
        If acked, sets mode to UDP and returns True

        Note that ListenStart is only allowed
        when we are in the CW state.
        """
        global state, ack
        # Listening is only allowed
        # in the CW state
        if state != "CW":
            return False

        # Send Listen_Start_CMD and wait for ack
        ack = False
        self.send_ListenStart()
        timeout = time.time() + 2
        while time.time() < timeout:
            time.sleep(0.1)
            if ack:
                state = "LISTEN"
                self.setMode_UDP()
                return True

        # No Ack
        state = "CW"
        return False

    #############
    # Tag Comms #
    #############
    def Tag_RX_CMD(self, tagID, payload):

        if tagID == None or payload == None:
            print("ERROR: CRC")
            return

        print("TagID: " + str(tagID))

        # Process Payload
        if len(payload) < 1:
            print("ERROR: no payload")
            return
        elif len(payload) > 1:
            print("Calling...")
            #pass # call number
        else:
            print("Payload: " + str(ord(payload)))
        return
        global skype, call

        if cmd == "CALL":
            try:
                pass
                #call = skype.PlaceCall(args[0])
            except Skype4Py.SkypeError as e:
                print("SKYPE ERROR: " + e[1])
        elif cmd == "ENDCALL":
            try:
                pass
                #call.Finish()
            except Skype4Py.SkypeError as e:
                print("SKYPE ERROR: " + e[1])
        else:
            print("ERROR: unknown cmd: " + cmd)

       
    def Tag_TX_CMD(self, tagID, payload):
        print("MSG: " + payload)
        print("LEN: " + str(len(payload)))
        self.cmd_tx.send(tagID, payload)

def SkypeOnCall(call, status):
    global tb

    SkypeIncoming = (Skype4Py.cltIncomingPSTN, Skype4Py.cltIncomingP2P)
    SkypeOutgoing = (Skype4Py.cltOutgoingPSTN, Skype4Py.cltOutgoingP2P)
    SkypeRinging = (Skype4Py.clsRouting, Skype4Py.clsRinging)
    SkypeDone = (Skype4Py.clsRefused, Skype4Py.clsUnplaced, Skype4Py.clsFailed, Skype4Py.clsFinished)
    SkypeInProgress = (Skype4Py.clsInProgress, Skype4Py.clsOnHold)

    if call.Type in SkypeIncoming:
        if status in SkypeRinging:
            # TODO: send call to tag
            # TODO: connect audio
            tb.Tag_TX_CMD(5, 'X')
            print("Incoming call: " + status)
        elif status in SkypeInProgress:
            # TODO: connect audio
            print("Incoming call: " + status)
        elif status in SkypeDone:
            # TODO: send ENDCALL
            print("Incoming call: " + status)
        else:
            print("UNKNOWN: Incoming Call: " + status)

    elif call.Type in SkypeOutgoing:
        if status in SkypeRinging + SkypeInProgress:
            # TODO: connect audio
            print("Outgoing Call: " + status)
        elif status in SkypeDone:
            # TODO: send ENDCALL
            print("Outgoing Call: " + status)
        else:
            print("UNKNOWN: Outgoing Call: " + status)


def main():
    # Arguments
    if len(sys.argv) != 3:
        print "Usage: ", sys.argv[0], "<USRP TX IP> <USRP RX IP>"
        exit(1)

    usrp_tx_addr = sys.argv[1]
    usrp_rx_addr = sys.argv[2]

    # Initialize Skype
    #global skype
    #skype = Skype4Py.Skype()
    #if not skype.Client.IsRunning:
    #    print("ERROR: Please start Skype.")
    #    return -1

    #skype.Attach()
    #skype.OnCallStatus = SkypeOnCall
    #print("Skype Initialized")

    # Construct and initialize Gnuradio top block
    global tb
    tb = my_top_block(usrp_tx_addr, usrp_rx_addr)
    tb.start()

    # Begin program loop
    while 1:
        c = raw_input("'q' to quit\n")
        if c == "q":
            tb.stop()
            break
        else:
            tb.Tag_TX_CMD(5, 'X')



if __name__ == '__main__':
    main()
