import crc
import hamming
import noise


with open('../data/packets.txt', 'r') as fin:
    for packet in fin:
        packet = packet.strip()

        print "Orig Packet:\t" + packet + "\r"
        halfEncodedPacket = crc.encode(packet)
        print "CRC Packet:\t\t" + halfEncodedPacket + "\r"
        encodedPacket = hamming.encode(halfEncodedPacket)
        print "Hamming Packet:\t" + encodedPacket + "\r"
        noisePacket = noise.gaussian(encodedPacket, 0.003)
        print "Noise Packet:\t" + noisePacket + "\r"
        halfDecodedPacket = hamming.decode(noisePacket)
        print "Hamming Decode:\t" + str(halfDecodedPacket) + "\r"
        if halfDecodedPacket:
            decodedPacket = crc.decode(halfDecodedPacket)
            print "Full Decode:\t" + str(decodedPacket) + "\n"
        else:
            print "Full Decode:\tFalse\n"


