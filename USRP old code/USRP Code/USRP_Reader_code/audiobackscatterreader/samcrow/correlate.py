
from gnuradio import gr
import numpy
import collections
import itertools
import time

import backscatter_frame
import msg_tx_source
import fm0_encode

# Creates a template for correlating the preamble of a message
#
# The returned value is a list of numbers that can be correlated with a
# complex signal at the provided bit rate.
def create_correlate_template(sample_rate, bit_rate):
    # Don't need matched filter
    # FM0 encode, repeat
    preamble_bits = backscatter_frame.getPreamble()
    fm0_encoded = fm0_encode.procedural_fm0_encode(preamble_bits)
    # Put several 0s at the beginning
    fm0_encoded = ([0] * len(fm0_encoded)) + fm0_encoded
    samples_per_half_bit = int(sample_rate / bit_rate) / 2
    return msg_tx_source.repeat_bits(samples_per_half_bit, fm0_encoded)

# Compares the incoming complex signal to a correlation template to detect
# the preamble of a message
#
# Outputs a complex correlation value. When the correlation is at maximum,
# the last sample of the signal corresponding to the template most likely
# recently arrived.
#
class correlation_calculator(gr.sync_block):
    def __init__(self, sample_rate, bit_rate):
        gr.sync_block.__init__(self, name = "correlation_calculator",
            in_sig = [numpy.complex64],
            out_sig = [numpy.complex64])
        self.template = create_correlate_template(sample_rate, bit_rate)
        print "Template length: %d samples" % len(self.template)
        # Window over a range of most recent samples
        # Samples are added to the right and automatically discarded from
        # Long enough for 2 preambles
        self.window = collections.deque(itertools.repeat(0, len(self.template)),
            maxlen = len(self.template))
        # The current correlation over self.window
        self.correlation = 0 + 0j

        # Recalculate the correlation approximately every [this many] samples
        self.calculate_interval = int(40 * sample_rate / bit_rate)


    def work(self, input_items, output_items):
        signal = input_items[0]
        correlation_out = output_items[0]
        input_count = min(len(signal), len(correlation_out))
        start_time = time.time()
        for i in range(input_count):
            self.window.append(signal[i])

            # Only recalculate the correlation periodically
            if i % self.calculate_interval == 0:
                correlation = self.calculate_correlation()
                correlation_out[i] = correlation
            else:
                correlation_out[i] = correlation_out[i - 1]

        end_time = time.time()
        samples_per_second = float(input_count) / (end_time - start_time)
        # print "%f samples/second" % samples_per_second
        return input_count

    # Calculates the correlation between self.template and a window
    # of signal (self.window). The window must have the same length as
    # self.template. The window must contain complex samples in the order that
    # this block received them.
    #
    # This function returns a float (non-complex).
    def calculate_correlation(self):
        return numpy.correlate(self.template, self.window)


if __name__ == "__main__":
    sample_rate = 1e6
    bit_rate = 12500
    calculator = correlation_calculator(sample_rate, bit_rate)
