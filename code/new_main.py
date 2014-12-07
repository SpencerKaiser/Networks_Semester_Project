from sys import argv
import csv
import hamming
import crc
import noise
import rs
import converter

# if len(argv) == 2:
#     noiseRatio = float(argv[1])
#     if noiseRatio < 0 or noiseRatio > 1:
#         print "Noise ration must be between 0 and 1"
#         exit(0)
# else:
#     noiseRatio = 0.003

noiseRatio = .0000

with open('../data/output.csv', 'w') as fout:
    # header = ["algorithm", "noise", "transmissions", "retransmissions", "corrections", "badReads"]
    header = ["Noise Ratio", "CRC RT G", "Hamming RT G", "Hamming+CRC RT G", "RS 16 RT G", "RS 32 RT G",
                "CRC RT B", "Hamming RT B", "Hamming+CRC RT B", "RS 16 RT B", "RS 32 RT B"]
    csvOut = csv.DictWriter(fout, fieldnames=header)
    csvOut.writeheader()
    print str(header)

    while noiseRatio <= .025:
        rowData = {}
        rowData["Noise Ratio"] = noiseRatio

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            for packet in fin:
                packet = packet.strip()
                crcEncodedPacket = crc.encode(packet)
                success = False
                while not success:
                    crcNoisePacket = noise.gaussian(crcEncodedPacket, noiseRatio)
                    numTrans += 1
                    success = True
                    if crc.decode(crcNoisePacket) == False:
                        numRT += 1
                        success = False
                    elif crcEncodedPacket != crcNoisePacket:
                        badReads += 1

        rowData["CRC RT G"] = round(float(numRT / numTrans), 1)

        print "CRC RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            for packet in fin:
                packet = packet.strip()
                crcEncodedPacket = crc.encode(packet)
                success = False
                while not success:
                    crcNoisePacket = noise.burst(crcEncodedPacket, noiseRatio)
                    numTrans += 1
                    success = True
                    if crc.decode(crcNoisePacket) == False:
                        numRT += 1
                        success = False
                    elif crcEncodedPacket != crcNoisePacket:
                        badReads += 1

        rowData["CRC RT B"] = round(float(numRT / numTrans), 1)

        print "CRC RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            for packet in fin:
                packet = packet.strip()
                hammingEncodedPacket = hamming.encode(packet)
                success = False
                while not success:
                    hammingNoisePacket = noise.gaussian(hammingEncodedPacket, noiseRatio)
                    numTrans += 1
                    hammingDecodedPacket = hamming.decode(hammingNoisePacket)
                    if hammingEncodedPacket == hammingNoisePacket:  # No interference
                        success = True
                    elif hammingDecodedPacket == packet:  # Correction was good
                        success = True
                        corrections += 1
                    elif hammingDecodedPacket == False:  # Could not correct
                        numRT += 1
                    else:  # Bad correction
                        badReads += 1

        rowData["Hamming RT G"] = round(float(numRT / numTrans), 1)

        print "Hamming RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            for packet in fin:
                packet = packet.strip()
                hammingEncodedPacket = hamming.encode(packet)
                success = False
                while not success:
                    hammingNoisePacket = noise.gaussian(hammingEncodedPacket, noiseRatio)
                    numTrans += 1
                    hammingDecodedPacket = hamming.decode(hammingNoisePacket)
                    if hammingEncodedPacket == hammingNoisePacket:  # No interference
                        success = True
                    elif hammingDecodedPacket == packet:  # Correction was good
                        success = True
                        corrections += 1
                    elif hammingDecodedPacket == False:  # Could not correct
                        numRT += 1
                    else:  # Bad correction
                        badReads += 1

        rowData["Hamming RT B"] = round(float(numRT / numTrans), 1)
        print "HCRC G\r"

        print "Hamming RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            for packet in fin:
                packet = packet.strip()

                halfEncodedPacket = crc.encode(packet)
                encodedPacket = hamming.encode(halfEncodedPacket)
                success = False
                while not success:
                    noisePacket = noise.gaussian(encodedPacket, noiseRatio)
                    halfDecodedPacket = hamming.decode(noisePacket)
                    success = True
                    numTrans += 1
                    if halfDecodedPacket:
                        decodedPacket = crc.decode(halfDecodedPacket)

                        if noisePacket == encodedPacket:
                            continue
                        elif decodedPacket is True:
                            corrections += 1
                        elif decodedPacket is False:
                            numRT += 1
                            success = False
                        else:
                            badReads += 1

                    else:
                        numRT += 1
                        success = False

        rowData["Hamming+CRC RT G"] = round(float(numRT / numTrans), 1)

        print "HCRC G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            for packet in fin:
                packet = packet.strip()

                halfEncodedPacket = crc.encode(packet)
                encodedPacket = hamming.encode(halfEncodedPacket)
                success = False
                while not success:
                    noisePacket = noise.burst(encodedPacket, noiseRatio)
                    halfDecodedPacket = hamming.decode(noisePacket)
                    success = True
                    numTrans += 1
                    if halfDecodedPacket:
                        decodedPacket = crc.decode(halfDecodedPacket)

                        if noisePacket == encodedPacket:
                            continue
                        elif decodedPacket is True:
                            corrections += 1
                        elif decodedPacket is False:
                            numRT += 1
                            success = False
                        else:
                            badReads += 1

                    else:
                        numRT += 1
                        success = False

        rowData["Hamming+CRC RT B"] = round(float(numRT / numTrans), 1)

        print "HCRC B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            reedsol = rs.RSCoder(128, 112)
            for packet in fin:
                packet = packet.strip()
                encodedPacket = reedsol.encode(packet)
                success = False
                while not success:
                    noisePacket = noise.gaussian_RS(encodedPacket, noiseRatio)
                    numTrans += 1
                    success = True
                    decodedPacket = reedsol.decode(noisePacket)

                    if noisePacket[0:112] == packet:
                        continue
                    elif decodedPacket == packet:
                        corrections += 1
                    elif decodedPacket != packet:
                        numRT += 1
                        success = False
                    else:
                        badReads += 1

        rowData["RS 16 RT G"] = round(float(numRT / numTrans), 1)

        print "RS 16 RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            reedsol = rs.RSCoder(128, 112)
            for packet in fin:
                packet = packet.strip()
                encodedPacket = reedsol.encode(packet)
                success = False
                while not success:
                    noisePacket = noise.burst_RS(encodedPacket, noiseRatio)
                    numTrans += 1
                    success = True
                    decodedPacket = reedsol.decode(noisePacket)

                    if noisePacket[0:112] == packet:
                        continue
                    elif decodedPacket == packet:
                        corrections += 1
                    elif decodedPacket != packet:
                        numRT += 1
                        success = False
                    else:
                        badReads += 1

        rowData["RS 16 RT B"] = round(float(numRT / numTrans), 1)

        print "RS 16 RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            reedsol = rs.RSCoder(144, 112)
            for packet in fin:
                packet = packet.strip()
                encodedPacket = reedsol.encode(packet)
                success = False
                while not success:
                    noisePacket = noise.gaussian_RS(encodedPacket, noiseRatio)
                    numTrans += 1
                    success = True
                    decodedPacket = reedsol.decode(noisePacket)

                    if noisePacket[0:112] == packet:
                        continue
                    elif decodedPacket == packet:
                        corrections += 1
                    elif decodedPacket != packet:
                        numRT += 1
                        success = False
                    else:
                        badReads += 1

        rowData["RS 32 RT G"] = round(float(numRT / numTrans), 1)

        print "RS 32 RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        with open('../data/packets.txt', 'r') as fin:
            reedsol = rs.RSCoder(144, 112)
            for packet in fin:
                packet = packet.strip()
                encodedPacket = reedsol.encode(packet)
                success = False
                while not success:
                    noisePacket = noise.burst_RS(encodedPacket, noiseRatio)
                    numTrans += 1
                    success = True
                    decodedPacket = reedsol.decode(noisePacket)

                    if noisePacket[0:112] == packet:
                        continue
                    elif decodedPacket == packet:
                        corrections += 1
                    elif decodedPacket != packet:
                        numRT += 1
                        success = False
                    else:
                        badReads += 1

        rowData["RS 32 RT B"] = round(float(numRT / numTrans), 1)

        print "RS 32 RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        csvOut.writerow(rowData)
        print str(rowData)
        noiseRatio += .00025