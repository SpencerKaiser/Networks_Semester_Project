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
  hammingGuassian = {}
  hammingGuassian["algorithm"] = "plain CRC"
  hammingGuassian["noise"] = "drift"
  hammingGuassian["transmissions"] = 0
  hammingGuassian["retransmissions"] = 0
  hammingGuassian["corrections"] = 0
  hammingGuassian["badReads"] = 0
  with open('../data/packets.txt','r') as fin:
    for packet in fin:
      packet = packet.strip()
      hammingEncodedPacket = hamming.encode(packet)
      success = False
      while not success:
        hammingNoisePacket = noise.gaussian(crcEncodedPacket, noiseRatio)
        hammingGuassian["transmissions"] += 1
        success = True
        decodedHammingPacket = hamming.decode(hammingNoisePacket)
        if not decodedHammingPacket:
          hammingGuassian["retransmissions"] += 1
          success = False
        elif hammingNoisePacket != hammingEncodedPacket:
          hammingGuassian["corrections"] +=1
  csvOut.writerow(hammingGuassian)
























