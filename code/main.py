import hamming
import crc
import noise


def main():
    packets = open('../data/packets.txt', 'r')

    # CRC VARIABLES
    crcTransmissions = 0
    crcRetransmissions = 0
    crcUndetectedErrors = 0

    # HAMMING VARIABLES
    hammingTransmissions = 0
    hammingRetransmissions = 0
    hammingCorrections = 0
    hammingUndetectedErrors = 0

    # PACKET ANALYSIS
    for packet in packets:
        packet = packet[:len(packet)-1]        # Remove the return carriage

        # CRC
        success = False
        crcEncodedPacket = crc.encode(packet)

        while not success:                           # Continue until the packet is accurately received
            crcNoisePacket = noise.gaussian(crcEncodedPacket, 0.003)

            crcTransmissions += 1
            success = True
            
            if crc.decode(crcNoisePacket) == False:       # If error(s) exist
                crcRetransmissions += 1
                success = False
            elif crcEncodedPacket != crcNoisePacket:      # Error occured and CRC didn't catch it
                crcUndetectedErrors += 1

        # HAMMING
        success = False
        hammingEncodedPacket = hamming.encode(packet)

        while not success:                           # Continue until the packet is accurately received
            hammingNoisePacket = noise.gaussian(hammingEncodedPacket, 0.003)

            hammingTransmissions += 1
            success = True

            decodedHammingPacket = hamming.decode(hammingNoisePacket)
            if not decodedHammingPacket:                        # Hamming decode failed - too many bit flips
                hammingRetransmissions += 1
                success = False
            elif hammingNoisePacket != hammingEncodedPacket:    # If a bit(s) was flipped & the result came back as true
                hammingCorrections += 1

    # SUMMARY
    print "\n"

    print "CRC ANALYSIS:"
    print "\tTransmissions: "+str(crcTransmissions)
    retransmissionRate = round(float(crcRetransmissions)/float(crcTransmissions)*100, 2)
    print "\tRetransmissions: "+str(crcRetransmissions)+" ~ "+str(retransmissionRate)+"%"
    print "\tUndetected Errors: "+str(crcUndetectedErrors)
    
    print "\n"

    print "HAMMING ANALYSIS"
    print "\tTransmissions: "+str(hammingTransmissions)
    retransmissionRate = round(float(hammingRetransmissions)/float(hammingTransmissions)*100, 2)

    print "\tRetransmissions: "+str(hammingRetransmissions)+" ~ "+str(retransmissionRate)+"%"
    print "\tCorrected Packets: "+str(hammingCorrections)
    print "\tUndetected Errors: "+str(hammingUndetectedErrors)

    print "\n"


        


        # print("b")
        # hammingPacket = hamming.encode(packet)
        #
        # hammingSuccess = false;
        # while(!hammingSuccess):
        #   # hammingNoise = noise(hammingPacket, 0.005)
        #
        # reedSolomonPacket = rs.encode(packet)
        # reedSolomonNoise = noise(reedSolomonPacket, 0.005)
        #
        # otherPacket = other.encode(packet)
        # otherNoise = noise(otherPacket, 0.005)

main()