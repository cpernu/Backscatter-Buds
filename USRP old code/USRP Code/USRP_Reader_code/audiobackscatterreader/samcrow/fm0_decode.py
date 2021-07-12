import numpy
import sys
from gnuradio import gr

class fm0_decode(gr.basic_block):
    # State constants

    # Initial state. An input transition causes a change to STATE_MAIN.
    STATE_IDLE = 0
    # Have observed a transition. An input transition after 1/2 period causes a
    # change to STATE_HALF_BIT. An input transition after 1 period causes an
    # output of 1. No input transition after 2 periods causes a transition to
    # STATE_IDLE.
    STATE_MAIN = 1
    # Half done reading a zero bit. An input transition after 1/2 period causes
    # a change to STATE_MAIN and an output of 0. An input transition after 1
    # period or longer indicates an error and causes a transition to STATE_IDLE.
    STATE_HALF_BIT = 2

    """
    sampRate: Sample rate, samples per second
    bitRate: Number of bits per second
    """
    def __init__(self, sampRate, bitRate):
        gr.basic_block.__init__(self,
            name="backscatter_fm0_decode",
            in_sig=[numpy.int8],
            out_sig=[numpy.int8])

        # Number of samples in one bit/clock cycle
        self.period_samples = int(sampRate / bitRate)
        # Number of samples in half a bit
        self.half_period_samples = self.period_samples / 2
        # Variables
        # State
        self.state = fm0_decode.STATE_IDLE
        # Number of samples since last transition
        # 0 when self.state == STATE_IDLE
        self.samples_since_transition = 0
        # Value of the last sample received
        self.prev_sample = 0

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # Track the number of output bits produced
        i = 0

        for sample in in0:
            if (sample != self.prev_sample):
                # Transition
                threshold = (self.period_samples + self.half_period_samples) / 2
                if (self.state == fm0_decode.STATE_IDLE):
                    self.state = fm0_decode.STATE_MAIN
                elif (self.state == fm0_decode.STATE_MAIN):
                    # Distinguish between period and half-period transitions
                    if (self.samples_since_transition > threshold):
                        # Full-period transition
                        # Output 1
                        # print "fm0_decode: Decoded 1 bit"
                        
                        # Avoid overwriting output
                        if (i >= len(out)):
                            break
                        out[i] = 1
                        i += 1
                        # Stay in this state
                    else:
                        # Half-period transition
                        self.state = fm0_decode.STATE_HALF_BIT

                elif (self.state == fm0_decode.STATE_HALF_BIT):
                    # Half-period transition, output 0
                    # print "fm0_decode: Decoded 0 bit"
                    # Avoid overwriting output
                    if (i >= len(out)):
                        break
                    out[i] = 0
                    i += 1
                    self.state = fm0_decode.STATE_MAIN

                self.samples_since_transition = 0
            else:
                # No transition
                if (self.state == fm0_decode.STATE_IDLE):
                    pass
                elif (self.state == fm0_decode.STATE_MAIN):
                    self.samples_since_transition += 1
                    if (self.samples_since_transition > 2 * self.period_samples):
                        # print "fm0_decode in STATE_MAIN: No transition after 2 periods"
                        self.samples_since_transition = 0
                        self.state = fm0_decode.STATE_IDLE
                elif (self.state == fm0_decode.STATE_HALF_BIT):
                    self.samples_since_transition += 1
                    if (self.samples_since_transition > self.period_samples):
                        # print "fm0_decode in STATE_HALF_BIT: No transition after 1 period"
                        self.samples_since_transition = 0
                        self.state = fm0_decode.STATE_IDLE

            # Update last sample
            self.prev_sample = sample;

        # Consume all inputs
        self.consume_each(len(in0))
        return i
