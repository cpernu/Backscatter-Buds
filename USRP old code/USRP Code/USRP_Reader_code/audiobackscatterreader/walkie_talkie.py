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
import SimpleXMLRPCServer
import xmlrpclib
import thread
from bitarray import bitarray

import backscatter

state = "CW"

class my_top_block(gr.top_block):
    def __init__(self, freq, usrp_tx_addr, usrp_rx_addr, server_addr, server_port, local_port, backchannel_port):
        gr.top_block.__init__(self)

        sampRate = 1e6
        bitRate = 666

        #######
        # RPC #
        #######

        self.rpc = xmlrpclib.ServerProxy("http://" + server_addr + ":" + str(backchannel_port))
       
        ##################
        # TX and Speaker #
        ##################

        # USRP
        usrp_tx = uhd.single_usrp_sink('addr=' + usrp_tx_addr, uhd.io_type_t.COMPLEX_FLOAT32,1)
        usrp_tx.set_clock_source("external", 0)
        usrp_tx.set_time_source("external", 0)
        usrp_tx.set_samp_rate(sampRate)
        usrp_tx.set_center_freq(freq, 0)
        usrp_tx.set_antenna('TX/RX',0)
        usrp_tx.set_gain(200);

        # Blocks
        self.cw_tx  = analog.sig_source_f(sampRate, analog.GR_CONST_WAVE, 0, ampl=1, offset=0)
        self.cmd_tx = backscatter.tx(sampRate, bitRate)
        self.udp_tx = blocks.udp_source(gr.sizeof_float, "0.0.0.0", server_port, 1472, False)
        self.sel_tx = blks2.selector(gr.sizeof_float, 3, 1, 0, 0) # Mux

        # Connections
        self.connect(self.cw_tx,  (self.sel_tx, 0))
        self.connect(self.cmd_tx, (self.sel_tx, 1))
        self.connect(self.udp_tx, (self.sel_tx, 2))
        self.connect(self.sel_tx, blocks.float_to_complex(), usrp_tx)

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
        usrp_rx.set_gain(200);

        # Blocks
        cmd_rx = backscatter.rx(sampRate, bitRate)
        udp_rx = blocks.udp_sink(gr.sizeof_float, server_addr, server_port) # Audio

        # Connections
        self.connect(usrp_rx, block.compex_to_mag(), cmd_rx)


    #######################
    # Sending data to tag #
    #######################

    def RPC_debug(self, cmd):
        print("DEBUG Sending: " + str(cmd))
        self.cmd_spkr.sendbits(backscatter.buildMsg())
        time.sleep(1)
        return True


    def send_ListenStart(self):
        self.cmd_spkr.sendbits(backscatter.getHeader() + backscatter.getID() + backscatter.getCMD("LISTEN"))
        time.sleep(1)
        
    def send_ListenStop(self):
        self.cmd_spkr.sendbits(backscatter.getHeader() + backscatter.getID() + backscatter.getCMD("LISTEN_STOP"))
        time.sleep(1)

    def send_Ack(self):
        self.cmd_spkr.sendbits(backscatter.getHeader() + backscatter.getID() + backscatter.getCMD("ACK"))
        time.sleep(1)

    ######################################
    # Switching between CW/CMD and Audio #
    ######################################
    def setMode_CMD(self):
        self.stop()
        self.wait()
        self.sel_spkr.set_input_index(0)
        self.start()

    def setMode_UDP(self):
        self.stop()
        self.wait()
        self.sel_spkr.set_input_index(1)
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

    def RPC_ListenStop(self):
        """
        Ends the speaker mode on the tag. Sends
        a ListenStop command, and returns True.

        Note that ListenStop is only allowed
        when we are in the LISTEN state.
        """
        global state
        print("RPC_ListenStop()")
        # Stopping listening in
        # only allowed in LISTEN state
        if state != "LISTEN":
            return False

        self.setMode_CMD()
        self.send_ListenStop()
        state = "CW"
        return True


    #############
    # Tag Comms #
    #############
    def Tag_CMD(self, bits):
        tagID = ord(bitarray(bits[0:8]).tobytes())
        msgLen = ord(bitarray(bits[8:16]).tobytes())
        msgID = ord(bitarray(bits[16:24]).tobytes())
        payload = bitarray(bits[24:-1]).tostring()

        print("Tag ID : " + str(tagID))
        print("MSG Len: " + str(msgLen))
        print("MSG ID : " + str(msgID))
        print("Payload: " + payload)

        if payload == "ACK":
            print("ACK")
            global ack
            ack = True
        elif payload == "TALK":
            print("TALK")
            self.Tag_TalkStart()
        elif payload == "TALK_STOP":
            print("TALK_STOP")
            self.Tag_TalkStop()
        elif payload == "LISTEN":
            print("DEBUG: Acking LISTEN")
            self.RPC_debug("ACK")
        else:
            print("ERR: " + payload)



    def Tag_TalkStart(self):
        res = self.rpc.RPC_ListenStart()
        if res:
            self.send_Ack()

    def Tag_TalkStop(self):
        self.rpc.RPC_ListenStop()

def startRPCServer(block, port):
    rpc_server = SimpleXMLRPCServer.SimpleXMLRPCServer(('death.cs.washington.edu', port), logRequests=False)
    rpc_server.register_function(block.RPC_ListenStart)
    rpc_server.register_function(block.RPC_ListenStop)
    rpc_server.register_function(block.RPC_debug)
    rpc_server.serve_forever()

def main():
    # Arguments
    if len(sys.argv) != 9:
        print "Usage: ", sys.argv[0], "<USRP IP 1> <USRP IP 2> <Server IP/Hostname> <Gnuradio Server Port> <Gnuradio Local Port> <Backchannel Server Port> <Backchannel Local Port> <Freq>"
        exit(1)

    usrp_tx_addr = sys.argv[1]
    usrp_rx_addr = sys.argv[2]
    server_addr = socket.gethostbyname(sys.argv[3])
    udp_server_port = int(sys.argv[4])
    udp_local_port = int(sys.argv[5])
    backchannel_server_port = int(sys.argv[6])
    backchannel_local_port = int(sys.argv[7])
    freq = float(sys.argv[8])

    # Construct and initialize Gnuradio top block
    tb = my_top_block(freq, usrp_tx_addr, usrp_rx_addr, server_addr, udp_server_port, udp_local_port, backchannel_server_port)
    tb.start()

    # Initilize backchannel RPC connection
    thread.start_new_thread(startRPCServer, (tb,backchannel_local_port))



    tb.cmd_tx.sendMsg("abcde")

    # Begin state machine
    global state
    while 1:
        if state == "CW":
            # Checking for changing states
            pass
        elif state == "SEND_LISTEN":
            # TODO: wait on ack/timeout
            state = "CW"

if __name__ == '__main__':
    main()
