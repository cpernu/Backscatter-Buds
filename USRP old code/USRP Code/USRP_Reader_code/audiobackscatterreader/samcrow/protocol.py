
import struct

# Protocol definitions
#
# Each message has a 1-byte key, followed by zero or more payload bytes

# Message key for a call (containing a number to call)
# The device sends a message of this type to the reader to start a call
#
# The message contains a 10-digit phone number. The number is split into
# bytes as follows:
# * Digits 1-2
# * Digits 3-4
# * Digits 5-6
# * Digits 7-8
# * Digits 9-10
#
# To call the number 352 849 3201, the device would send the bytes
# 35 28 49 32 01.
#
KEY_CALL = 0x10
# Message key for call acknowledgments, sent from the reader
KEY_CALL_ACK = 0x11
# Message key for a call action message, sent from the reader to notify
# the device that a call is about to begin
KEY_CALL_ACTION = 0x15
# Call action acknowledgments, sent from the device
KEY_CALL_ACTION_ACK = 0x16
# Message key for a listen message, sent from the device to request that
# the user listen to audio from the caller
KEY_LISTEN = 0x20
# Listen acknowledgments
KEY_LISTEN_ACK = 0x21
# Key for a talk message, sent from the device to switch to talk mode
KEY_TALK = 0x30
# Talk acknowledgment
KEY_TALK_ACK = 0x31
# Key for a hang up message, sent from the device to end the call
KEY_HANG_UP = 0x40
# Hang up acknowledgment
KEY_HANG_UP_ACK = 0x41

# Builds a message with the provided key and body
#
# key: One of the key constants defined in this module
# body: A byte array containing the body of the message
#
# Returns a str representing a message
def build_message(key, body = bytearray()):
    return struct.pack('b' + str(len(body)) + 's', key, str(body))

# Parses a message
#
# Accepts a bytearray
#
# Returns a message ID and a possibly empty body bytearray. Raises something
# if the provided frame content is empty.
def parse_message(frame_content):
    if len(frame_content) == 0:
        # raise RuntimeError("Empty message")
        # Lenient for testing
        return 0, bytearray()
    else:
        body_length = len(frame_content) - 1
        key, body_str = struct.unpack('b' + str(body_length) + 's', str(frame_content))
        return key, bytearray(body_str)

# Converts an array of bytes into a phone number
def parse_phone_number(body):
    print "Parsing phone number from body " + body
    for byte in body:
        print "Body byte: %d" % byte
    if len(body) != 5:
        raise "Incorrect body length for phone number"
    else:
        digit1 = body[0] >> 4
        digit2 = body[0] & 0xF
        digit3 = body[1] >> 4
        digit4 = body[1] & 0xF
        digit5 = body[2] >> 4
        digit6 = body[2] & 0xF
        digit7 = body[3] >> 4
        digit8 = body[3] & 0xF
        digit9 = body[4] >> 4
        digit10 = body[4] & 0xF
        
        return digit10 + digit9 * 10 + digit8 * 100 + digit7 * 1000 + digit6 * 10000 + digit5 * 100000 + digit4 * 1000000 + digit3 * 10000000 + digit2 * 100000000 + digit1 * 1000000000
