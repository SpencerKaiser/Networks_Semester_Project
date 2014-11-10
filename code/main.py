import hamming
import crc

def main():
    print("garbage")
    packets = open('../data/packets.txt', 'r')

    badDecodes = 0

    for packet in packets:
        packet = packet[0:len(packet)-1]        
        encodedPacket = crc.encode(packet)
        if crc.decode(encodedPacket) == False:
            badDecodes

    print "Number of Bad Decodes: "+str(badDecodes)
        


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