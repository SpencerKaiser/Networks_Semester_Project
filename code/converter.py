class Converter:

    __hexVals = {
        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "A",
        "1011": "B",
        "1100": "C",
        "1101": "D",
        "1110": "E",
        "1111": "F"
    }

    __bitVals = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"
    }

    def bitsToBytes(self, bitstream):
        formattedBitstream = ""
        bytestream = ""
        bitlen = len(bitstream)
        remainder = bitlen % 8
        if remainder is not 0:
            remainder = 8 - remainder

        for i in range(0, remainder):
            formattedBitstream += "0"
        formattedBitstream += bitstream
        formattedBitlen = len(formattedBitstream)

        loopCount = formattedBitlen / 4
        currentSegment = 0
        for i in range(0, loopCount):
            fourBit = formattedBitstream[currentSegment:currentSegment+4]
            bytestream += self.__hexVals.get(fourBit)
            currentSegment += 4

        return bytestream

    def bytesToBits(self, bytestream):

        bitstream = ""
        bytelen = len(bytestream)

        for i in range(0, bytelen):
            bitstream += self.__bitVals.get(bytestream[i])

        return bitstream


c = Converter()

initialStream = "110100110101111100110111"
bytestream = c.bitsToBytes(initialStream)
bitstream = c.bytesToBits(bytestream)

print "Initial:\t" + initialStream + "\r"
print "Bytestream:\t" + bytestream + "\r"
print "Bitstream:\t" + bitstream + "\r"


