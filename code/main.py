import hamming
import crc


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

        while success == False:                           # Continue until the packet is accurately received
            # TODO: PASS TO NOISE FUNCTION HERE
            crcNoisePacket = crcEncodedPacket

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

        while success == False:                           # Continue until the packet is accurately received
            # TODO: PASS TO NOISE FUNCTION HERE
            hammingNoisePacket = hammingEncodedPacket

            hammingTransmissions += 1
            success = True
            
            if hamming.decode(hammingNoisePacket) == False:       # If error(s) exist
                hammingRetransmissions += 1
                success = False
            elif hammingEncodedPacket != hammingNoisePacket:      # Error occured and CRC didn't catch it
                hammingUndetectedErrors += 1


    # SUMMARY
    print "\n"

    print "CRC ANALYSIS:"
    print "\tTransmissions: "+str(crcTransmissions)
    print "\tRetransmissions: "+str(crcRetransmissions)+" ~ "+str(crcRetransmissions/crcTransmissions*100)+"%"
    print "\tUndetected Errors: "+str(crcUndetectedErrors)
    
    print "\n"

    print "HAMMING ANALYSIS"
    print "\tTransmissions: "+str(hammingTransmissions)
    print "\tRetransmissions: "+str(hammingRetransmissions)+" ~ "+str(hammingRetransmissions/hammingTransmissions*100)+"%"
    print "\tCorrections: "+str(hammingCorrections)
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