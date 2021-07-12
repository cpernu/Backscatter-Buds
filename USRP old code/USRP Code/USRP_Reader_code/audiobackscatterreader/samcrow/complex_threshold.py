from gnuradio import gr
import numpy
import collections
import itertools


#
# Thresholds a complex signal with a complex threshold
#
# A sample is considered above the threshold if the sum of its real and imaginary
# parts are greater than the sum of the threshold's real and imaginary parts
#
# Outputs 1 for each sample above the threshold and 0 for each sample below
# the threshold.
#
class complex_threshold(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self, name = "complex_threshold",
            # Input 0: Signal, input 1: threshold
            in_sig = [numpy.complex64, numpy.complex64],
            # Output 0: threshold result
            out_sig = [numpy.int8])
        # TODO: Hysteresis?

    def work(self, input_items, output_items):
        signal = input_items[0]
        threshold = input_items[1]
        result = output_items[0]

        sample_count = min(len(signal), len(threshold), len(result))
        for i in range(sample_count):
            threshold_sum = sum_real_imag(threshold[i])
            if sum_real_imag(signal[i]) > threshold_sum:
                result[i] = 1
            else:
                result[i] = 0

        return sample_count

def sum_real_imag(complex_value):
    return complex_value.real + complex_value.imag

if __name__ == "__main__":
    sample_rate = 1e6
    bit_rate = 12500
    threshold = complex_threshold()
