from gnuradio import gr
import numpy
import collections
import itertools
import cmath
import pmt

import correlate

#
# Accepts a complex signal, a complex correlation signal, and a float
# thresholded correlation signal
# Outputs a float normalized signal.
#
# When the thresholded correlation signal transitions from 0 to 1
# (likely corresponding to the last sample of the preamble of a message), this
# block:
#
# 1. Calculates the phase of the complex correlation value
# 2. Creates a complex value with a phase equal to the negative phase of the
# complex correlation
# 3. Multiplies the signal by that value and ignores the complex part of the
# result to get a float signal
# 4. Calculates the minimum and maximum of the float signal and calculates a
# threshold from the average of the minimum and maximum values
#
# The resulting float signal is output on output 0. The threshold is output
# on output 1.
#
# The signal and correlation signal must be synchronized for this block to
# work correctly.
#
# The threshold is updated on each preamble, and held constant at other times.
#
class correlate_threshold(gr.sync_block):
    def __init__(self, sample_rate, bit_rate):
        gr.sync_block.__init__(self, name = "correlate_threshold",
            # Input 0: Signal, input 1: correlation, input 2: correlation threshold
            in_sig = [numpy.complex64, numpy.complex64, numpy.float32],
            # Output 0: float signal, output 1: threshold
            out_sig = [numpy.float32, numpy.float32])
        # The number of samples in the preamble
        preamble_length = len(correlate.create_correlate_template(sample_rate, bit_rate))
        # Store the most recent samples for analysis
        self.signal_window = collections.deque(itertools.repeat(0, preamble_length),
            maxlen = preamble_length)

        # The previous value of the thresholded correlation input (0 or 1)
        self.previous_thresholded = 0.0

        # Complex value, with which the signal is multiplied
        self.inverse_phase = 0 + 0j

        # Threshold to output, recalculated periodically
        self.threshold = 0.0

    def work(self, input_items, output_items):
        in_signal = input_items[0]
        in_correlation = input_items[1]
        in_thresholded = input_items[2]
        out_signal = output_items[0]
        out_threshold = output_items[1]

        sample_count = min(len(in_signal), len(in_correlation), len(out_normalized))

        for i in range(sample_count):
            if in_thresholded[i] > self.previous_thresholded:


                print "High correlation: %s" % in_correlation[i]
                correlation_phase = cmath.phase(in_correlation[i])
                # Create a complex value from r = 1, phi = -correlation_phase
                self.inverse_phase = cmath.rect(1.0, -correlation_phase)
                # Find min/max of (signal window * inverse phase) for thresholding
                (min_real, max_real) = self.min_max_real_signal()
                self.threshold = (min_real + max_real) / 2.0

                # Add a tag to the stream with the updated normalization
                self.add_item_tag(
                    0, # Output 0
                    self.nitems_written(0) + i, # Absolute offset in stream
                    pmt.intern("preamble"), # key
                    pmt.cons(pmt.intern("threshold"), pmt.from_float(self.threshold))) # value


            # Add a signal sample to the signal window and get the value at the
            # other end that it pushed out
            delayed_sample = push_pop(self.signal_window, in_signal[i])
            # Provide output, multiplied by the
            # inverse phase value and the normalization factor
            inverse_phased = delayed_sample * self.inverse_phase
            out_signal[i] = inverse_phased.real
            # Output threshold
            out_threshold[i] = self.threshold

            # Store thresholded correlation
            self.previous_thresholded = in_thresholded[i]

        return sample_count


    # Finds the minimum and maximum values of the real part of
    # (self.signal_window * self.inverse_phase)
    # and returns it them
    def min_max_real_signal(self):
        max_value = None
        min_value = None
        for sample in self.signal_window:
            real_value = abs((sample * self.inverse_phase).real)
            if max_value == None or real_value > max_value:
                max_value = real_value
            if min_value == None or real_value < min_value:
                min_value = real_value
        if max_value == None or min_value == None:
            raise RuntimeError("No maximum/minimum real value of signal sample")
        return (min_value, max_value)


# Pushes the provided value to the right of the provided deque
# and returns the leftmost element of the queue.
def push_pop(deque, value):
    leftmost = deque.popleft()
    deque.append(value)
    return leftmost


if __name__ == "__main__":
    sample_rate = 1e6
    bit_rate = 12500
    threshold = correlate_threshold(sample_rate, bit_rate)
