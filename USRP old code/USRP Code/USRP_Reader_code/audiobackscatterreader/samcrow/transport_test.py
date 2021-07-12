from transport import test_transport
import state_machine
import threading
import protocol
import time

def main():
    transport = test_transport()

    def message_sent(message):
        pass
    transport.test_set_receive_callback(message_sent)

    machine = state_machine.state_machine(transport)

    def run_machine():
        machine.run()

    thread = threading.Thread(group = None, target = run_machine)
    thread.daemon = True
    thread.start()

    # Send some messages
    time.sleep(1)
    # Start a call
    transport.test_send(protocol.build_message(protocol.KEY_CALL, bytearray([12, 34, 56, 78, 90])))
    time.sleep(0.01)
    # Acknowledge that the call has started, enter listen mode
    transport.test_send(protocol.build_message(protocol.KEY_CALL_ACTION_ACK))

    time.sleep(0.1)
    # Talk mode
    transport.test_send(protocol.build_message(protocol.KEY_TALK))
    time.sleep(0.1)
    # Listen mode
    transport.test_send(protocol.build_message(protocol.KEY_LISTEN))

    time.sleep(0.1)
    # End call
    transport.test_send(protocol.build_message(protocol.KEY_HANG_UP))

    time.sleep(1)


if __name__ == '__main__':
    main()
