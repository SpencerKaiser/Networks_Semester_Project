# CSE4344 - Networks
# CRC Implementation - This file contains functionality to encode/decode a packet using CRC

#GLOBAL VARIABLES
polynomial = "11000000000000101"        # Official CRC-16 poly = 0x8005 ~ 1000 0000 0000 0101 (includes 1 in high bi)
polyLength = len(polynomial)            # Number of bits to XOR against (17 bits)
placeholderBits = "0000000000000000"    # Bits to append to original packet BEFORE encoding (16 bits)
subPacketLength = 17


# FUNCTION: Receives packet header/data as input, returns packet with added CRC suffix
# INPUT: string representing binary packet (consists of 0's and 1's)
# OUTPUT: input string with added CRC suffix bits (16 bits)
def encode(packet):
    workingPacket = packet + placeholderBits            # Append placeholder bits before encoding
    pointer = subPacketLength                           # Pointer to location in workingPacket
    crc = placeholderBits                               # Zero out CRC bit variable
    subPacket = workingPacket[pointer-17:pointer]       # Zero out subPacket

    while pointer <= len(workingPacket):    # Iterate through packet XORing until remaining data fits in the CRC bit area
        # print "XORing some shit..."
        # print subPacket
        # print polynomial
        xorresult = int(subPacket, 2) ^ int(polynomial, 2)      # XOR subpacket against polynomial
        # print '{0:0{1}b}'.format(xorresult, subPacketLength)

        subPacket = '{0:b}'.format(xorresult)
        # print subPacket

        numBits = subPacketLength - len(subPacket)

        subPacket += workingPacket[pointer:pointer+numBits]

        # print subPacket
        pointer += numBits

        # print "\n"

    crc = subPacket.zfill(16)                           # Pads CRC bits with prefixed 0's to fit 16 bits
    # print crc
    return packet + crc


# FUNCTION: Receives packet header/data as input, returns packet with added CRC suffix
# INPUT: string representing encoded binary packet (consists of 0's and 1's)
# OUTPUT: boolean representing whether an error was detected (true = NO ERROR, false = ERROR)
def decode(packet):
    workingPacket = packet
    pointer = subPacketLength                           # Pointer to location in workingPacket
    subPacket = workingPacket[pointer-17:pointer]       # Zero out subPacket

    while pointer <= len(workingPacket):    # Iterate through packet XORing until remaining data fits in the CRC bit area
        # print "XORing some shit..."
        # print subPacket
        # print polynomial
        xorresult = int(subPacket, 2) ^ int(polynomial, 2)      # XOR subpacket against polynomial
        # print '{0:0{1}b}'.format(xorresult, subPacketLength)

        subPacket = '{0:b}'.format(xorresult)
        # print subPacket

        numBits = subPacketLength - len(subPacket)

        subPacket += workingPacket[pointer:pointer+numBits]

        # print subPacket
        pointer += numBits

        # print "\n"

    if int(subPacket) == 0:
        return True                                     # NO ERRORS
    else:
        return False                                    # ERRORS EXIST





#TESTING:
# num      = "1001010010101001010100101010101110101111111000001010101001010101010100101001010100101010010101010111010111111100"
# otherNum = "0011010010101001011110101010101110101110111000001010101001010101010000101001010100101010010101010111010111101111"

# falseEncode      = "10010100101010010101001010101011101011111110000010101010010101010101011010010101001010100101010101110101111111001110011110110110"
# otherFalseEncode = "10010100101010010101001010101011101011101110000010101010010101010101011010010101001010100101010101110101110111001110011110110110"

# encodedPacket = encode(num)
# print "\nFIRST TEST:"
# print encodedPacket
# print decode(encodedPacket)
# print "\nFalse Decode Test:"
# print decode(falseEncode)

# print "\n\nSECOND TEST"
# encodedPacket = encode(otherNum)
# print encodedPacket
# print decode(encodedPacket)
# print "\nFalse Decode Test:"
# print decode(otherFalseEncode)


