
import struct
from bitarray import bitarray

"""
Holds utils for building and decoding
messages in the ambient backscatter format.
"""

"""
Format:
Preamble: 2 bytes: 0, 3
Tag ID: 1 byte
Message length: 1 byte
Message ID (or something): 1 byte
Payload: message length bytes
Checksum: 1 byte

The checksum is the sum of the tag ID, length, message ID, and each payload byte

In each byte, the most significant bit is first.
"""

def frame(tagID, payload):

    # Downlink preamble 0x0003 is different from uplink preamble
    preamble0 = 0x00
    preamble1 = 0x03

    msgLen = len(payload)
    message_id = 0
    checksum = calc_checksum(tagID, msgLen, message_id, payload)

    msg = struct.pack("BBBBB" + str(msgLen) + "sB",
        preamble0,
        preamble1,
        tagID,
        msgLen,
        message_id,
        payload,
        checksum)

    return msg

def deframe(header, raw_payload):
    header_bytes = bytearray(bitarray(header).tobytes())
    raw_payload_bytes = bytearray(bitarray(raw_payload).tobytes())

    tagID, msgLen, message_id = struct.unpack("BBB", header_bytes)

    print "Header bytes:"
    for i in range(3):
        print "%02X" % header_bytes[i]
    print "Payload/checksum bytes:"
    for i in range(msgLen + 1):
        print "%02X" % raw_payload_bytes[i]


    print("---------------------------------------")
    print("TagID: " + str(tagID))
    print("MsgLen: " + str(msgLen))
    print("Message ID: " + str(message_id))
    print("---------------------------------------")

    payload, tag_checksum = struct.unpack(str(msgLen) + "s" + "B", raw_payload_bytes)
    local_checksum = calc_checksum(tagID, msgLen, message_id, payload)

    if (msgLen == 0):
        # Empty
        return (None, None)

    # print("Payload: " + str(ord(payload[0])))
    print("CRC: " + str(tag_checksum))
    print("Calculated CRC: " + str(local_checksum))

    if local_checksum != tag_checksum:
        print "Invalid checksum"
        return (None, None)
    print "Checksum OK"
    return (tagID, payload)

# Returns the preamble of digital uplink messages
#
# The returned value is a list of bits (not FM0 encoded).
def getPreamble():
    # 0xAAA0
    return (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0)

def getHeaderLen():
    return 3*8

def getPayloadLen(header):
    return 8*struct.unpack_from("B", bitarray(header[8:16]).tobytes())[0] + 8

def calc_checksum(tagID, msgLen, msgID, payload):
    payload_sum = sum(struct.unpack("B"*msgLen, payload))
    header_sum = tagID + msgLen + msgID
    return (payload_sum+header_sum)%256
