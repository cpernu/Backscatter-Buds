#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
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
from gnuradio import blocks
from gnuradio import analog
from gnuradio import digital
from gnuradio import filter
from grc_gnuradio import blks2

import numpy
import Queue
import collections
from bitarray import bitarray
import struct

class tx(gr.hier_block2):
    def __init__(self, sampRate, bitRate):
        gr.hier_block2.__init__(self, "backscatter_tx",
                                gr.io_signature(0, 0, 0),
                                gr.io_signature(1, 1, gr.sizeof_float))

        self.sampPerChip = int(sampRate / (bitRate) / 2)

        # Digital Commands
        self.msg = blocks.message_source(gr.sizeof_char, 2)
        self.unpack = blocks.unpack_k_bits_bb(8)
        self.fm0_encode = fm0_encode()
        self.repeat = blocks.repeat(gr.sizeof_char, self.sampPerChip)

        # CW for Power
        self.cw = analog.sig_source_f(sampRate, analog.GR_CONST_WAVE, 0, ampl=1, offset=0)

        # Connections
        self.connect(self.msg, self.unpack, self.fm0_encode, self.repeat, blocks.char_to_float(), self)

    def send(self, tagID, payload):
        msg = abc.frame(tagID, payload)
        self.msg.msgq().insert_tail(gr.message_from_string(msg))


class fm0_encode(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(self,
            name="backscatter_fm0_encode",
            in_sig=[numpy.int8],
            out_sig=[numpy.int8])

        self.set_output_multiple(128)


    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        if (len(in0) == 0):
            out[:] = [1]
            return 1

        i = 0
        out[-1] = 1
        for bit in in0:
            out[i] = int(not out[i-1])
            out[i+1] = int(out[i] == bit)
            i += 2

        if len(in0):
            out[i] = int(not out[i-1])
            out[i+1] = 1
            i += 2

        self.consume_each(len(in0))
        return i


class rx(gr.hier_block2):
    def __init__(self, sampRate, bitRate, tag_callback):
        gr.hier_block2.__init__(self, "backscatter_tx",
                                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                                gr.io_signature(0, 0, 0))

        # TODO: add skip head block to fix startup issue.

        agc = analog.agc2_cc(attack_rate=1.6, decay_rate=5e-5, reference=1, gain=1.0)
        thresh_middle=0.5
        thresh = blocks.threshold_ff(thresh_middle-0.02,thresh_middle+0.02)
        fm0decode = fm0_decode(sampRate, bitRate)
        self.framer = framer(tag_callback)
            
        filesink = blocks.file_sink(gr.sizeof_gr_complex, "./data/data.usrp")

        self.connect(self, agc, blocks.complex_to_mag_squared(), thresh, blocks.float_to_char(), fm0decode, self.framer)
        self.connect(agc, filesink)


class fm0_decode(gr.basic_block):
    """
    """
    def __init__(self, sampRate, bitRate):
        gr.basic_block.__init__(self,
            name="backscatter_fm0_decode",
            in_sig=[numpy.int8],
            out_sig=[numpy.int8])


        self.sampPerChip = int((sampRate / bitRate) / 2)
        
        self.prevSamp = 0
        self.numSamp = 0
        self.halfbitprev = 0

        self.numbits = 0


    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        halfbit = self.sampPerChip
        fullbit = 2 * halfbit
        wiggle = 5

        i = 0
        for samp in in0:
            if samp != self.prevSamp:
                # Full Bit
                if (fullbit - wiggle) <= self.numSamp <= (fullbit + wiggle):
                    self.halfbitprev = 0
                    out[i] = 1
                    i += 1

                # Half Bit
                elif (halfbit - wiggle) <= self.numSamp <= (halfbit + wiggle):
                    if self.halfbitprev:
                        self.halfbitprev = 0
                        out[i] = 0
                        i += 1
                    else:
                        self.halfbitprev = 1
                self.numSamp = 0

            self.numSamp += 1
            self.prevSamp = samp

        self.consume_each(len(in0))
        return i



class framer(gr.sync_block):
    """
    """
    def __init__(self, tag_callback):
        gr.sync_block.__init__(self,
            name="backscatter_framer",
            in_sig=[numpy.int8],
            out_sig=[])

        self.tag_callback = tag_callback

        self.preamble_ref = collections.deque(abc.getPreamble())
        self.preamble = collections.deque([], len(abc.getPreamble()))
        self.header = collections.deque([])
        self.payload = collections.deque([])


    def work(self, input_items, output_items):
        in0 = input_items[0]

        for bit in in0:
            if self.preamble == self.preamble_ref:
                if len(self.header) == abc.getHeaderLen():
                    if len(self.payload) == abc.getPayloadLen(list(self.header)):
                        self.tag_callback(*abc.deframe(list(self.header), list(self.payload)))
                        self.payload.clear()
                        self.header.clear()
                        self.preamble.clear()
                    else:
                        self.payload.append(bit)
                else:
                    self.header.append(bit)
            else:
                self.preamble.append(bit)

        if len(self.header) == abc.getHeaderLen() and len(self.payload) == abc.getPayloadLen(list(self.header)):
            self.tag_callback(*abc.deframe(list(self.header), list(self.payload)))
            self.payload.clear()
            self.header.clear()
            self.preamble.clear()

        return len(in0)

msgID = 0
class abc():
    """
    Holds utils for building and decoding
    messages in the ambient backscatter format.
    """

    @staticmethod
    def frame(tagID, payload):
        preamble0 = 0
        preamble1 = 3

        msgLen = len(payload)
        checksum = abc.calc_checksum(tagID, msgLen, 1, payload)

        msg = struct.pack("BBBBB" + str(msgLen) + "sB", preamble0, preamble1, tagID, msgLen, 1, payload, checksum)

        #print(len(payload))

        #print(':'.join(x.encode('hex') for x in msg))
        
        return msg

    @staticmethod
    def deframe(header, raw_payload):
        tagID, msgLen = struct.unpack("BB", bitarray(header).tobytes())
        #print("---------------------------------------")
        #print("TagID: " + str(tagID))
        #print("MsgLen: " + str(msgLen))

        payload, tag_checksum = struct.unpack(str(msgLen) + "s" + "B", bitarray(raw_payload).tobytes())
        local_checksum = abc.calc_checksum(tagID, msgLen, payload)

        #print("Payload: " + str(ord(payload[0])))
        #print(bitarray(raw_payload))
        #print("CRC: " + str(tag_checksum))
        #print("Local CRC: " + str(local_checksum))
    
        if local_checksum != tag_checksum:
            return (None, None)

        return (tagID, payload)

    @staticmethod
    def getPreamble():
        return (0,0,0,0,0,0,1,1)

    @staticmethod
    def getHeaderLen():
        return 2*8

    @staticmethod
    def getPayloadLen(header):
        return 8*struct.unpack_from("B", bitarray(header[8:16]).tobytes())[0] + 8

    @staticmethod
    def calc_checksum(tagID, msgLen, msgID, payload):
        payload_sum = sum(struct.unpack("B"*msgLen, payload))
        header_sum = tagID + msgLen + msgID
        return (payload_sum+header_sum)%256
