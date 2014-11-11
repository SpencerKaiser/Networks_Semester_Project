import hamming
import crc
import noise
from sys import argv


def main(noiseRatio):
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
            crcNoisePacket = noise.gaussian(crcEncodedPacket, noiseRatio)

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
            hammingNoisePacket = noise.gaussian(hammingEncodedPacket, noiseRatio)

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

    print "NOISE RATIO: %s\n" % noiseRatio

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

    # Write data to file
    with open("../data/crcOut.txt",'a') as fout:
        fout.write("(%s,%s)"%(noiseRatio,round(float(crcRetransmissions)/float(crcTransmissions)*100, 2)))
    with open("../data/hammingOut.txt",'a') as fout:
        fout.write("(%s,%s)"%(noiseRatio,round(float(hammingRetransmissions)/float(hammingTransmissions)*100, 2)))
        


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

if len(argv) == 2:
    noiseRatio = float(argv[1])
    if noiseRatio < 0 or noiseRatio > 1:
        print "Noise ration must be between 0 and 1"
        exit(0)
    else:
        noiseRatio = 0.003
# main(noiseRatio)



