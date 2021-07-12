
from gnuradio import gr
from gnuradio import uhd
from gnuradio import blocks


from msg_rx_analog_matched import msg_rx_analog_matched
from msg_rx_analog_correlate import msg_rx_analog_correlate
from msg_tx import msg_tx
from msg_rx import msg_rx
from audio_tx import audio_tx
from audio_rx import audio_rx

"""
A transport implementation that uses a USRP to communicate with a real device
"""
class usrp_transport:

    # Based on tests with a 20 dB amplifier 2017-06-05
    # USRP gain | actual transmit gain after amplifier
    # 0           20 dBm
    # 5           26 dBm
    # 10          30 dBm


    # Creates a transport implementation
    #
    # transmit_address should be the IP address of the USRP device to use for
    # transmitting.
    #
    # receive_address should be the IP address of the USRP device to use for
    # receiving.
    #
    # device_address should be a numerical address of the device to send to.
    # It must not be greater than 255.
    #
    # tag_id is the ID of the tag to send to
    #
    # The transport will initially be in digital mode.
    def __init__(self, transmit_address, receive_address, device_address):
        self.device_address = device_address
        self.top_block = gr.top_block()
        
        # USRP configuration for various modes
        # With the amplifier, transmit gains should be between 0 and 10
        self.config_digital = configuration()
        self.config_digital.tx_gain = 10.0
        self.config_digital.rx_gain = 0.0
        self.config_digital.rx_bandwidth = 1000.0
        self.config_digital.tx_sample_rate = 4000000
        self.config_digital.rx_sample_rate = 1000000
        self.config_digital.center_frequency = 912.002442e6
        
        self.config_talk = configuration()
        self.config_talk.tx_gain = 10.0
        self.config_talk.rx_gain = 0.0
        self.config_talk.rx_bandwidth = 1000.0
        self.config_talk.tx_sample_rate = 1000000
        self.config_talk.rx_sample_rate = 1000000
        self.config_talk.center_frequency = 912.002442e6
        
        self.config_listen = configuration()
        self.config_listen.tx_gain = 10.0
        self.config_listen.rx_gain = 0.0
        self.config_listen.rx_bandwidth = 40e6
        self.config_listen.tx_sample_rate = 1000000
        self.config_listen.rx_sample_rate = 1000000
        self.config_listen.center_frequency = 912.002442e6

        tx_bit_rate = 12500
        # Uplink bit rate is slightly off due to device timing issues
        rx_bit_rate = tx_bit_rate * 0.7273

        self.usrp_rx = uhd.usrp_source(
        	'addr=192.168.10.2',
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.usrp_rx.set_subdev_spec('B:0', 0)
        self.usrp_rx.set_antenna('TX/RX', 0)


        self.usrp_tx = uhd.usrp_sink(
        	'addr=192.168.10.2',
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.usrp_tx.set_subdev_spec('A:0', 0)
        self.usrp_tx.set_antenna('TX/RX', 0)

        # Digital receive mechanism
        self.msg_rx = msg_rx_analog_matched(
            self.config_digital.rx_sample_rate,
            rx_bit_rate,
            self._tag_callback)
        # Digital transmit mechanism
        self.msg_tx = msg_tx(self.config_digital.tx_sample_rate, tx_bit_rate)

        # Audio transmit mechanism
        self.audio_tx = audio_tx()
        # Audio receive mechanism
        self.audio_rx = audio_rx()

        self.receive_callback = None
        
        # Connect blocks and set up for digital mode
        self.configure_digital_mode()

    def start(self):
        self.top_block.start()

    # Sends the provided message to the device
    def send(self, message):
        self.msg_tx.send(self.device_address, message)

    # Connects the unused outputs of self.msg_rx to a null sink
    def connect_msg_rx_outputs(self):
        for i in range(self.msg_rx.output_signature().min_streams()):
            self.top_block.connect((self.msg_rx, i), blocks.null_sink(gr.sizeof_gr_complex))

    # Configures the USRP sink and source with settings from the provided
    # configuration object
    def configure_usrp(self, config):
        self.usrp_tx.set_gain(config.tx_gain)
        self.usrp_rx.set_gain(config.rx_gain)
        self.usrp_rx.set_bandwidth(config.rx_bandwidth)
        self.usrp_tx.set_samp_rate(config.tx_sample_rate)
        self.usrp_rx.set_samp_rate(config.rx_sample_rate)
        self.usrp_tx.set_center_freq(config.center_frequency)
        self.usrp_rx.set_center_freq(config.center_frequency)
    

    # Sets the transport mechanism to talk mode
    #
    # In this mode, the USRP transmits a constant stream of 1s.
    # The received signal is sent to the audio receive module
    # and the digital receive module.
    def configure_talk_mode(self):
        self.top_block.lock()
        self.top_block.disconnect_all()
        self.top_block.connect(self.usrp_rx, self.msg_rx)
        self.top_block.connect(self.msg_tx, self.usrp_tx)
        
        # Increase the amplitude of the signal to audio_rx
        signal_ratio = 10.0
        audio_signal_mult = blocks.multiply_const_cc(signal_ratio)
        self.top_block.connect(self.usrp_rx, audio_signal_mult, self.audio_rx)
        # self.top_block.connect(self.usrp_rx, self.audio_rx)
        
        self.configure_usrp(self.config_talk)
        
        self.connect_msg_rx_outputs()
        self.top_block.unlock()

    # Sets the transport mechanism to listen mode
    #
    # In this mode, the USRP transmits encoded audio.
    # The received signal is sent to the digital receive module.
    def configure_listen_mode(self):
        self.top_block.lock()
        self.top_block.disconnect_all()
        self.top_block.connect(self.usrp_rx, self.msg_rx)
        self.top_block.connect(self.audio_tx, self.usrp_tx)
        
        self.configure_usrp(self.config_listen)
        
        self.connect_msg_rx_outputs()
        self.top_block.unlock()

    # Sets the transport mechanism to digital mode
    #
    # In this mode, the USRP transmits a constant stream of 1s.
    # The received signal is sent to the digital receive module.
    def configure_digital_mode(self):
        self.top_block.lock()
        self.top_block.disconnect_all()
        self.top_block.connect(self.usrp_rx, self.msg_rx)
        self.top_block.connect(self.msg_tx, self.usrp_tx)
        
        self.configure_usrp(self.config_digital)
        
        self.connect_msg_rx_outputs()
        self.top_block.unlock()

    def set_receive_callback(self, callback):
        self.receive_callback = callback

    def _tag_callback(self, device_id, payload):
        if self.receive_callback != None and device_id != None and device_id != 0:
            print("!!! RECEIVE from %d" % device_id)
            if device_id == self.device_address:
                self.receive_callback(payload)
            else:
                print 'Received frame from unexpected device ' + str(device_id)

# USRP configuration
class configuration:
    def __init__(self):
        # Defaults
        self.tx_gain = 0.0
        self.rx_gain = 0.0
        self.rx_bandwidth = 0.0
        self.tx_sample_rate = 1000000
        self.rx_sample_rate = 1000000
        self.center_frequency = 912.002442e6

"""
A transport mechanism used for testing
"""
class test_transport:
    def __init__(self):
        self.receive_callback = None
        self.test_receive_callback = None

    def start(self):
        pass

    def send(self, message):
        if self.test_receive_callback != None:
            self.test_receive_callback(message)

    def set_receive_callback(self, callback):
        self.receive_callback = callback

    # Intended for use in tests
    # Sends a message from the device to the state machine
    def test_send(self, payload):
        if self.receive_callback != None:
            self.receive_callback(payload)

    # Intended for use in tests
    # Sets a callback to be notified when the state machine sends a message
    def test_set_receive_callback(self, callback):
        self.test_receive_callback = callback
