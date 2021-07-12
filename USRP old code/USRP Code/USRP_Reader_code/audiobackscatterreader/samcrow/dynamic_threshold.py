from gnuradio import gr
import numpy

"""

Thresholds an input according to the value of another input

Input 0 is the signal input. Input 1 is the threshold input.

If the signal input is less than the threshold input, the block
outputs 0. Otherwise, it outputs 1.

"""
class dynamic_threshold_ff(gr.sync_block):

    """
    Creates a threshold block

    hysteresis: the difference between the increasing threshold and the decreasing
    threshold
    """
    def __init__(self, hysteresis = 0.1):
        gr.sync_block.__init__(self,
            name="dynamic_threshold_ff",
            in_sig=[numpy.float, numpy.float],
            out_sig=[numpy.float])
        self.hysteresis = hysteresis
        # Most recent output, 0 or 1, for hysteresis
        self.current_output = 0

    def work(self, input_items, output_items):
        signal = input_items[0]
        threshold = input_items[1]
        output = output_items[0]
        item_count = min(len(signal), len(threshold))

        for i in range(item_count):
            if signal[i] > (threshold[i] + self.hysteresis / 2.0):
                self.current_output = 1
            elif signal[i] < (threshold[i] - self.hysteresis / 2.0):
                self.current_output = 0

            output[i] = self.current_output      
        return item_count
