#!/usr/bin/env python

from gnuradio import gr
from gnuradio import wxgui
from gnuradio import blocks
from gnuradio import analog
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from msg_tx import msg_tx


class send_test(grc_wxgui.top_block_gui):
    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title = "Send test")

        # self.tx = msg_tx(2, 1)
        self.scope = scopesink2.scope_sink_f(self.GetWin())
        # self.convert = blocks.char_to_float()
        #
        # self.connect(self.tx, self.convert)
        # self.connect(self.convert, self.scope)
        self.const = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.throttle = blocks.throttle(gr.sizeof_float, 10)

        self.Add(self.scope.win)

        self.connect(self.const, self.throttle)
        self.connect(self.throttle, self.scope)

    def send(self, tag, message):
        pass
        # self.tx.send(tag, message)

def main():
    tb = send_test()
    tb.Start(True)
    tb.Wait()

if __name__ == "__main__":
    main()
