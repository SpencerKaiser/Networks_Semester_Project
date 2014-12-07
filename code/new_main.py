from sys import argv
import csv
import hamming
import crc
import noise
import rs
import converter

# if len(argv) == 2:
#     noiseRatio = float(argv[1])
#     if noiseRatio < 0 or noiseRatio > 1
#         print "Noise ration must be between 0 and 1"
#         exit(0)
# else:
#     noiseRatio = 0.003

noiseRatio = 0.0
noiseStep = .0005
noiseLimit = .025

# CREATE CSV FILES AND BEGIN OUTER LOOP
with open('../data/output.csv', 'w') as fout, open('../data/gaussian.csv', 'w') as gaussianFile, open('../data/burst.csv', 'w') as burstFile:
    header = ["Noise Ratio", "CRC RT G", "Hamming RT G", "Hamming+CRC RT G", "RS 16 RT G", "RS 32 RT G",
                "CRC RT B", "Hamming RT B", "Hamming+CRC RT B", "RS 16 RT B", "RS 32 RT B"]
    csvOut = csv.DictWriter(fout, fieldnames=header)
    csvOut.writeheader()

    header = ["Noise Ratio",
              "CRC T", "CRC RT",
              "Hamming T", "Hamming RT", "Hamming BRs",
              "Hamming+CRC T", "Hamming+CRC RT", "Hamming+CRC BRs", "Hamming+CRC Corr",
              "RS 16 T", "RS 16 RT", "RS 16 Corr",
              "RS 32 T", "RS 32 RT", "RS 32 Corr"]

    gaussianStats = csv.DictWriter(gaussianFile, fieldnames=header)
    gaussianStats.writeheader()

    burstStats = csv.DictWriter(burstFile, fieldnames=header)
    burstStats.writeheader()

    # PRINT NOISE INFORMATION
    print "Noise Ratio (INIT): " + str(noiseRatio)
    print "Noise Step: " + str(noiseStep)
    print "Noise Limit: " + str(noiseLimit) + "\n\n"

    # BEGIN ANALYSIS
    while noiseRatio < noiseLimit + .0001:      # This is to account for erroneous data added to the float value
        rowData = {}
        rowData["Noise Ratio"] = noiseRatio

        gaussianRow = {}
        gaussianRow["Noise Ratio"] = noiseRatio

        burstRow= {}
        burstRow["Noise Ratio"] = noiseRatio

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # CRC - Gaussian
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

        rowData["CRC RT G"] = round(float(numRT) / numTrans, 4)

        gaussianRow["CRC T"] = numTrans
        gaussianRow["CRC RT"] = numRT

        print "CRC RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # CRC - Burst
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

        rowData["CRC RT B"] = round(float(numRT) / numTrans, 4)

        burstRow["CRC T"] = numTrans
        burstRow["CRC RT"] = numRT

        print "CRC RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # Hamming - Gaussian
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
                        success = True

        rowData["Hamming RT G"] = round(float(numRT) / numTrans, 4)

        gaussianRow["Hamming T"] = numTrans
        gaussianRow["Hamming RT"] = numRT
        gaussianRow["Hamming BRs"] = badReads

        print "Hamming RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # Hamming - Burst
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
                        success = True

        rowData["Hamming RT B"] = round(float(numRT) / numTrans, 4)

        burstRow["Hamming T"] = numTrans
        burstRow["Hamming RT"] = numRT
        burstRow["Hamming BRs"] = badReads

        print "Hamming RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # Hamming+CRC - Gaussian
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

        rowData["Hamming+CRC RT G"] = round(float(numRT) / numTrans, 4)

        gaussianRow["Hamming+CRC T"] = numTrans
        gaussianRow["Hamming+CRC RT"] = numRT
        gaussianRow["Hamming+CRC BRs"] = badReads
        gaussianRow["Hamming+CRC Corr"] = corrections

        print "HCRC G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # Hamming+CRC - Burst
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

        rowData["Hamming+CRC RT B"] = round(float(numRT) / numTrans, 4)

        burstRow["Hamming+CRC T"] = numTrans
        burstRow["Hamming+CRC RT"] = numRT
        burstRow["Hamming+CRC BRs"] = badReads
        burstRow["Hamming+CRC Corr"] = corrections

        print "HCRC B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        #RS 16 - Gaussian
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

        rowData["RS 16 RT G"] = round(float(numRT) / numTrans, 4)

        gaussianRow["RS 16 T"] = numTrans
        gaussianRow["RS 16 RT"] = numRT
        gaussianRow["RS 16 Corr"] = corrections

        print "RS 16 RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # RS 16 - Burst
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

        rowData["RS 16 RT B"] = round(float(numRT) / numTrans, 4)

        burstRow["RS 16 T"] = numTrans
        burstRow["RS 16 RT"] = numRT
        burstRow["RS 16 Corr"] = corrections

        print "RS 16 RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # RS 32 - Gaussian
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

        rowData["RS 32 RT G"] = round(float(numRT) / numTrans, 4)

        gaussianRow["RS 32 T"] = numTrans
        gaussianRow["RS 32 RT"] = numRT
        gaussianRow["RS 32 Corr"] = corrections

        print "RS 32 RT G\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        numTrans = 0
        numRT = 0
        badReads = 0
        corrections = 0

        # RS 32 - Burst
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

        rowData["RS 32 RT B"] = round(float(numRT) / numTrans, 4)

        burstRow["RS 32 T"] = numTrans
        burstRow["RS 32 RT"] = numRT
        burstRow["RS 32 Corr"] = corrections

        print "RS 32 RT B\r"
        print "\tNumTrans:\t" + str(numTrans)
        print "\tNumRT:\t" + str(numRT)
        print "\tCorrections:\t" + str(corrections)
        print "\tBadReads:\t" + str(badReads)

        csvOut.writerow(rowData)
        gaussianStats.writerow(gaussianRow)
        burstStats.writerow(burstRow)

        print str(rowData) + "\n"
        print str(gaussianRow) + "\n"
        print str(burstRow) + "\n"

        noiseRatio += noiseStep