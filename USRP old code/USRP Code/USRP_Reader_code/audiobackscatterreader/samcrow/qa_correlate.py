#!/usr/bin/env python

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import correlate

# Tests are not up-to-date. Most of them incorrectly fail.
class qa_correlate (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block()

    def tearDown (self):
        self.tb = None

    def run_test(self, input, expected_output):
        signal_src = blocks.vector_source_c(input)
        correlate_block = correlate.correlation_calculator(4, 2)
        self.tb.connect(signal_src, correlate_block)
        sink = blocks.vector_sink_f()
        self.tb.connect(correlate_block, sink)
        self.tb.run()
        result = sink.data()
        self.assertEqual(expected_output, result)

    def test_nothing(self):
        self.run_test((), ())

    def test_few_bits(self):
        self.run_test((0, 1, 0, 1, 0, 1), (0.0,) * 6)

    def test_exact_match(self):
        encoded_preamble = (1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1,
            1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0)
        # Expected corelation is the number of 1 samples in the template
        self.run_test(encoded_preamble, (16.0,))

    def test_exact_match_then_decline(self):
        encoded_preamble = (1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1,
            1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
            # Post-preamble section
            0, 0, 0, 0)
        self.run_test(encoded_preamble, (14.0,))

if __name__ == '__main__':
    gr_unittest.run(qa_correlate, "qa_correlate.xml")
