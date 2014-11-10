import hamming


def main():
    print("garbage")
    packets = open('../data/packets.txt', 'r')

    for packet in packets:
        print("b")
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