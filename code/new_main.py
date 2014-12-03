from sys import argv
import csv
import hamming
import crc
import noise

if len(argv) == 2:
  noiseRatio = float(argv[1])
  if noiseRatio < 0 or noiseRatio > 1:
    print "Noise ration must be between 0 and 1"
    exit(0)
else:
  noiseRatio = 0.003

with open('../data/trial1.csv','w') as fout:
  header=["algorithm","noise","transmissions","retransmissions","corrections","badReads"]
  csvOut =csv.DictWriter(fout, fieldnames=header)
  csvOut.writeheader() 

  #Plain CRC with gaussian noise
  crcGaussian = {}
  crcGaussian["algorithm"] = "plain CRC"
  crcGaussian["noise"] = "white"
  crcGaussian["transmissions"] = 0
  crcGaussian["retransmissions"] = 0
  crcGaussian["corrections"] = 0
  crcGaussian["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      crcEncodedPacket = crc.encode(packet)
      success = False
      while not success:
        crcNoisePacket = noise.gaussian(crcEncodedPacket, noiseRatio)
        crcGaussian["transmissions"] += 1
        success = True
        if crc.decode(crcNoisePacket) == False:
          crcGaussian["retransmissions"] += 1
          success = False
        elif crcEncodedPacket != crcNoisePacket:
          crcGaussian["badReads"] +=1
  csvOut.writerow(crcGaussian)

  #Plain CRC with burst noise
  crcBurst = {}
  crcBurst["algorithm"] = "plain CRC"
  crcBurst["noise"] = "burst"
  crcBurst["transmissions"] = 0
  crcBurst["retransmissions"] = 0
  crcBurst["corrections"] = 0
  crcBurst["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      crcEncodedPacket = crc.encode(packet)
      success = False
      while not success:
        crcNoisePacket = noise.burst(crcEncodedPacket, noiseRatio)
        crcBurst["transmissions"] += 1
        success = True
        if crc.decode(crcNoisePacket) == False:
          crcBurst["retransmissions"] += 1
          success = False
        elif crcEncodedPacket != crcNoisePacket:
          crcBurst["badReads"] +=1
  csvOut.writerow(crcBurst)

  #Plain CRC with drift noise
  crcDrift = {}
  crcDrift["algorithm"] = "plain CRC"
  crcDrift["noise"] = "drift"
  crcDrift["transmissions"] = 0
  crcDrift["retransmissions"] = 0
  crcDrift["corrections"] = 0
  crcDrift["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      crcEncodedPacket = crc.encode(packet)
      success = False
      while not success:
        crcNoisePacket = noise.drift(crcEncodedPacket, noiseRatio)
        crcDrift["transmissions"] += 1
        success = True
        if crc.decode(crcNoisePacket) == False:
          crcDrift["retransmissions"] += 1
          success = False
        elif crcEncodedPacket != crcNoisePacket:
          crcDrift["badReads"] +=1
  csvOut.writerow(crcDrift)

  #Hamming with Gaussian noise
  row = {}
  row["algorithm"] = "hamming"
  row["noise"] = "gaussian"
  row["transmissions"] = 0
  row["retransmissions"] = 0
  row["corrections"] = 0
  row["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      hammingEncodedPacket = hamming.encode(packet)
      success = False
      while not success:
        hammingNoisePacket = noise.gaussian(hammingEncodedPacket, noiseRatio)
        row["transmissions"] += 1
        hammingDecodedPacket = hamming.decode(hammingNoisePacket)
        if hammingEncodedPacket == hammingNoisePacket: # No interference
          success = True
        elif hammingDecodedPacket == packet: # Correction was good
          success = True
          row["corrections"] += 1
        elif hammingDecodedPacket == False: # Could not correct
          row["retransmissions"] += 1
        else: # Bad correction
          row["badReads"] +=1
  csvOut.writerow(row)

  #Hamming with Burst noise
  row = {}
  row["algorithm"] = "hamming"
  row["noise"] = "burst"
  row["transmissions"] = 0
  row["retransmissions"] = 0
  row["corrections"] = 0
  row["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      hammingEncodedPacket = hamming.encode(packet)
      success = False
      while not success:
        hammingNoisePacket = noise.burst(hammingEncodedPacket, noiseRatio)
        row["transmissions"] += 1
        hammingDecodedPacket = hamming.decode(hammingNoisePacket)
        if hammingEncodedPacket == hammingNoisePacket: # No interference
          success = True
        elif hammingDecodedPacket == packet: # Correction was good
          success = True
          row["corrections"] += 1
        elif hammingDecodedPacket == False: # Could not correct
          row["retransmissions"] += 1
        else: # Bad correction
          row["badReads"] +=1
          success = True
  csvOut.writerow(row)

  #Hamming with Drift noise
  row = {}
  row["algorithm"] = "hamming"
  row["noise"] = "drift"
  row["transmissions"] = 0
  row["retransmissions"] = 0
  row["corrections"] = 0
  row["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      hammingEncodedPacket = hamming.encode(packet)
      success = False
      while not success:
        hammingNoisePacket = noise.drift(hammingEncodedPacket, noiseRatio)
        row["transmissions"] += 1
        hammingDecodedPacket = hamming.decode(hammingNoisePacket)
        if hammingEncodedPacket == hammingNoisePacket: # No interference
          success = True
        elif hammingDecodedPacket == packet: # Correction was good
          success = True
          row["corrections"] += 1
        elif hammingDecodedPacket == False: # Could not correct
          row["retransmissions"] += 1
        else: # Bad correction
          row["badReads"] +=1
          success = True
  csvOut.writerow(row)

  # CRC to hamming with guassian noise
  row = {}
  row["algorithm"] = "CRC to hamming"
  row["noise"] = "gaussian"
  row["transmissions"] = 0
  row["retransmissions"] = 0
  row["corrections"] = 0
  row["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      halfEncodedPacket = crc.encode(packet)
      encodedPacket = hamming.encode(halfEncodedPacket)
      success = False
      while not success:
        noisePacket = noise.gaussian(encodedPacket, noiseRatio)
        row["transmissions"] += 1
        halfDecodedPacket = hamming.decode(noisePacket)
        if halfDecodedPacket:
          decodedPacket = crc.decode(halfDecodedPacket)
        else:
          decodedPacket = False

  csvOut.writerow(row)
























