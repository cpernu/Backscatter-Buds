

from msg_tx import msg_tx
from fm0_encode import fm0_encode
from gnuradio import gr, blocks
from gnuradio import wxgui
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
import time
import threading

class msg_tx_test(grc_wxgui.top_block_gui):
    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Transmit Test")

        sampRate = 2e6
        bitRate = 328

        self.scope = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Transmit Scope",
            sample_rate = sampRate,
            v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Value")

        self.Add(self.scope.win)
        self.mtx = msg_tx(sampRate, bitRate)
        self.convert = blocks.char_to_float(1)
        self.connect(self.mtx, self.convert)
        self.connect(self.convert, self.scope)

    def send(self, tag, payload):
        self.mtx.send(tag, payload)

def main():
    top = msg_tx_test()
    top.Start(True)

    def run():
        while True:
            print "Sending"
            top.send(0, "\x00")
            print "Sent"
            time.sleep(1)

    thread = threading.Thread(group = None, target = run)
    thread.start()

    top.Wait()

if __name__ == "__main__":
    main()
