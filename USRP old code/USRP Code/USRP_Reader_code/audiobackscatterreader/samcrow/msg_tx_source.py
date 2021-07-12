
import numpy
import pmt
from gnuradio import gr
from gnuradio import blocks
import numpy
import time
import collections
import itertools

from fm0_encode import procedural_fm0_encode

"""
Receives frames on the message port 'message' and outputs them on a stream.

When no messages are available, this outputs a constant stream of 1s.

Message samples and 1s are output on port 0.

To transmit a message:

```
source = msg_tx_source()
source.send_message("Hello")
```

"""
class msg_tx_source(gr.basic_block):

    # The number of bit intervals to add after each message for separation
    PADDING_BITS = 4
    # The output provided when no messages are available
    IDLE_SIGNAL = 1

    def __init__(self, sample_rate, bit_rate):
        gr.basic_block.__init__(self,
            name="msg_tx_source",
            in_sig=[],
            out_sig=[numpy.complex64])


        # Calculate samples per bit
        # Divided by 2 because 2 samples are used for each bit
        self.samples_per_half_bit = int(sample_rate / bit_rate) / 2
        print "%d samples per half bit" % self.samples_per_half_bit

        # Register port
        self.message_port_register_in(pmt.intern("message"))
        self.set_msg_handler(pmt.intern("message"), lambda (message): self.handle_message(message))

        # Queue of samples from messages waiting to be sent
        # Leftmost samples will be output first
        self.samples_waiting = collections.deque()

    def forecast(self, noutput_items, ninput_items_required):
        # Do not require any input
        ninput_items_required[0] = 0

    def general_work(self, input_items, output_items):
        out0 = output_items[0]
        if len(self.samples_waiting) == 0:
            # Send 1s
            out0.fill(msg_tx_source.IDLE_SIGNAL)
            return len(out0)

        else:
            # Send samples from the queue
            sample_count = min(len(self.samples_waiting), len(out0))
            for i in range(sample_count):
                out0[i] = self.samples_waiting.popleft()
            return sample_count

    # The message passing mechanism calls this function. Client code should not
    # call it.
    def handle_message(self, message):
        message = pmt.symbol_to_string(message)
        if len(message) > 0:
            # FM0 encode bits
            message = procedural_fm0_encode(unpack_bits(bytearray(message)))
            # Repeat bits
            message = repeat_bits(self.samples_per_half_bit, message)
            # Add message bits and in-between-message signal to sample queue
            self.samples_waiting.extend(message)
            # If the last sample of message is 1, there will be no transition at the
            # end of the last bit and the receiving device will not be able to
            # receive the message. Workaround: Add 2 samples of 0
            if message[-1] == 1:
                self.samples_waiting.extend([0, 0])
            self.samples_waiting.extend([msg_tx_source.IDLE_SIGNAL]
                * (msg_tx_source.PADDING_BITS * 2 * self.samples_per_half_bit))
        else:
            print "msg_tx_source: cannot send empty message"


    """
    Sends a message through this block

    The message must be something that can be converted into a string.

    This function may be called from any thread.
    """
    def send_message(self, message):
        port = pmt.intern("message")
        message = pmt.string_to_symbol(str(message))
        self.to_basic_block()._post(port, message)

# Accepts and array of 1s and 0s
# Returns a new array with each value in bits repeated samples_per_half_bit
# times
def repeat_bits(samples_per_half_bit, bits):
    result = [0] * (len(bits) * samples_per_half_bit)
    for i in range(len(bits)):
        for j in range(samples_per_half_bit):
            result[i * samples_per_half_bit + j] = bits[i]
    return result


# Unpacks an array of bytes into an array of bits, with the most significant
# bit first
def unpack_bits(message):
    result = [0] * (8 * len(message))
    for i, byte in enumerate(message):
        for j in range(0, 8):
            result[8 * i + j] = (byte >> (7 - j)) & 1
    return result

# Test
if __name__ == '__main__':
    top = gr.top_block()
    source = msg_tx_source()
    null_sink = blocks.null_sink(gr.sizeof_char)
    top.connect(source, null_sink)

    print 'Starting'
    top.start()
    print 'Started'

    while True:
        try:
            time.sleep(1)
            source.send_message("Hello world!")
        except KeyboardInterrupt:
            break

    top.stop()
    top.wait()
