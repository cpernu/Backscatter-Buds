
import sys
import time
from gnuradio import gr
from gnuradio import uhd
from gnuradio import analog
from msg_tx import msg_tx
import protocol
from transport import usrp_transport

import Skype4Py

def skype_on_call(call, status, state_machine):
    SkypeOutgoing = (Skype4Py.cltOutgoingPSTN, Skype4Py.cltOutgoingP2P)
    SkypeRinging = (Skype4Py.clsRouting, Skype4Py.clsRinging)
    SkypeInProgress = (Skype4Py.clsInProgress, Skype4Py.clsOnHold)
    SkypeDone = (Skype4Py.clsFinished, Skype4Py.clsCancelled)
    
    print "call.Type: %s" % call.Type
    print "status: %s" % status

    if call.Type in SkypeOutgoing:
        if status == Skype4Py.clsRinging or status == Skype4Py.clsInProgress \
            and state_machine.state == state_machine.STATE_CALL_STARTED:
            print("Outgoing Call: " + status)
            print "======================= Listen mode ============================"
            state_machine.state = state_machine.STATE_LISTEN
            state_machine.transport.configure_listen_mode()

# Sends the provided message count times using the provided
# state machine, waiting interval seconds between messages
def send_repeated_message(message, interval, count, state_machine):
    for i in range(count):
        state_machine.send(message)
        time.sleep(interval)

class state_machine:

    # Initial state (waiting for a call request from the device)
    STATE_CALL_WAITING = 0
    # Call started, sending messages to the device to notify it
    STATE_CALL_STARTED = 1
    # Sending audio to the device, allowing the user to lisent
    STATE_LISTEN = 2
    # Receiving audio from the device
    STATE_TALK = 3
    
    
    # The number of acknowledgments to send to the device
    ACK_COUNT = 128
    # The interval in seconds to wait between sending acknowledgments
    ACK_INTERVAL = 0.01


    # Creates a state machine
    #
    # transport is a transport layer implementation to use
    def __init__(self, transport):
        
        # Skype can be disabled for testing
        # When Skype is disabled, the state machine will not leave
        # STATE_CALL_WAITING
        self.enable_skype = False
        # Automatically proceed into talk mode, without any actual
        # device required, for testing
        self.proceed_to_talk_mode = False
        # Automatically proceed into listen mode
        self.proceed_to_listen_mode = False
        
        # Flags for desire to transition to talk and listen modes
        # (When messages are received, the callback is called from a block's
        # work function, so the graph can't be reconfigured directly there.)
        self.want_talk_mode = False
        self.want_listen_mode = False
    
        self.transport = transport
        self.transport.set_receive_callback(self.tag_callback)
        self.transport.configure_digital_mode()
        # Set up call waiting state
        self.state = state_machine.STATE_CALL_WAITING
        if self.enable_skype:
            # Skype connection
            self.skype = Skype4Py.Skype()
            if not self.skype.Client.IsRunning:
                self.skype.Client.start()
            self.skype.OnCallStatus = lambda call, status: skype_on_call(call, status, self)
            self.skype.Attach()
        self.call = None

    # Runs the state machine
    def run(self):
        print "run()"
        self.transport.start()
        print "Transport started"
        while True:
            if self.state == state_machine.STATE_CALL_WAITING:
                if self.proceed_to_talk_mode or self.proceed_to_listen_mode:
                    # Testing only: Transition to call started state
                    self.message_callback(protocol.KEY_CALL, bytearray([0x35, 0x28, 0x49, 0x32, 0x01]))
                # Keep waiting for a call message
                pass
            elif self.state == state_machine.STATE_CALL_STARTED:
                pass
            elif self.state == state_machine.STATE_LISTEN:
                if self.proceed_to_talk_mode:
                    # Testing only: Transition to talk state
                    self.message_callback(protocol.KEY_TALK, bytearray())
                if self.want_talk_mode:
                    self.want_talk_mode = False
                    
                    # In listen mode, the digital transmit block is disconnected.
                    # Must switch to talk mode immediately so that the
                    # acknowledgments can be sent
                    print "======================= Talk mode ============================"
                    self.state = state_machine.STATE_TALK
                    self.transport.configure_talk_mode()


                    # Send several acknowledgments
                    message = protocol.build_message(protocol.KEY_TALK_ACK)
                    for i in range(state_machine.ACK_COUNT):
                        print 'Sending talk acknowledgment'
                        self.send(message)
                        time.sleep(state_machine.ACK_INTERVAL)

            elif self.state == state_machine.STATE_TALK:
                if self.want_l8isten_mode:
                    self.want_listen_mode = False
                    
                    # Send several acknowledgments
                    message = protocol.build_message(protocol.KEY_LISTEN_ACK)
                    for i in range(state_machine.ACK_COUNT):
                        print 'Sending listen acknowledgment'
                        self.send(message)
                        time.sleep(state_machine.ACK_INTERVAL)
                    # Wait for messages to get through the graph
                    time.sleep(2)
                    print "======================= Listen mode ============================"
                    self.state = state_machine.STATE_LISTEN
                    self.transport.configure_listen_mode()
            else:
                print 'Invalid state ' + str(self.state)
            time.sleep(0.1)

    # Handles incoming frames from the device
    def tag_callback(self, frame_body):
        key, body = protocol.parse_message(frame_body)
        self.message_callback(key, body)

    # Handles incoming application-layer messages
    #
    # key: A number containing the message key
    # body: An array of zero or more bytes containing the message body
    def message_callback(self, key, body):
        print "Got message with key 0x%x"  % key
        if key == protocol.KEY_CALL and self.state == state_machine.STATE_CALL_WAITING:
        
        
            # Send several call acknowledgments
            message = protocol.build_message(protocol.KEY_CALL_ACK)
            for i in range(1):
                print 'Sending call acknowledgment at time %f' % time.time()
                self.send(message)
                time.sleep(state_machine.ACK_INTERVAL)

            phone_number = protocol.parse_phone_number(body)
            # Skype expects an 11-digit phone number with a country code at
            # the beginning
            # Assume that the number is United States-based
            # Prepend 1
            phone_number = "+1" + str(phone_number)
            print "Calling " + str(phone_number)
            if self.enable_skype:
                # For testing, call another Skype account instead of a phone number
                # self.call = self.skype.PlaceCall(str(phone_number))
                # self.call = self.skype.PlaceCall("yomeilingwu")
                
                # Wait for confirmation
                print "Continue? (q to quit)"
                command = raw_input()
                if command == 'q':
                    sys.exit()
                
                self.call = self.skype.PlaceCall(str(phone_number))
                self.state = state_machine.STATE_CALL_STARTED
                

        elif key == protocol.KEY_LISTEN and self.state == state_machine.STATE_TALK:
            # Switch to listen mode
            print "Switching to listen mode"
            self.want_listen_mode = True

        elif key == protocol.KEY_TALK and self.state == state_machine.STATE_LISTEN:
            # Switch to talk mode
            print "Switching to talk mode"
            self.want_talk_mode = True

        # Send an acknowledgment for a request to switch to listen/talk mode
        # if already in that mode
        elif key == protocol.KEY_TALK and self.state == state_machine.STATE_TALK:
            message = protocol.build_message(protocol.KEY_TALK_ACK)
            self.send(message)

        # Respond to hang up messages if in a call or if a call has recently
        # ended
        elif key == protocol.KEY_HANG_UP and (self.in_call() or self.state == state_machine.STATE_CALL_WAITING):
            # End call and acknowledge
            print "Ending call"
            message = protocol.build_message(protocol.KEY_HANG_UP_ACK)
            self.send(message)
            if self.enable_skype and self.call != None:
                self.call.Finish()
                self.call = None
            self.state = state_machine.STATE_CALL_WAITING
            self.transport.configure_digital_mode()
        else:
            print "Unexpected message with key 0x%x in state %d" % (key, self.state)

    # Sends the provided message to the device
    #
    # Because this uses the gnuradio message passing mechanism, it is probably
    # safe to call from any thread.
    def send(self, message):
        self.transport.send(message)

    # Returns true if the state is STATE_TALK or STATE_LISTEN
    def in_call(self):
        return self.state == state_machine.STATE_TALK or self.state == state_machine.STATE_LISTEN


def main():
    if len(sys.argv) != 4:
        print 'Usage: %s receiver-address transmitter-address device-address' % sys.argv[0]
        return
    transmit_addr = sys.argv[1]
    receive_addr = sys.argv[2]
    device_address = int(sys.argv[3])

    transport = usrp_transport(transmit_addr, receive_addr, device_address)
    machine = state_machine(transport)
    machine.run()

if __name__ == '__main__':
    main()
