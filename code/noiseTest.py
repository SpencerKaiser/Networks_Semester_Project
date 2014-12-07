import noise
from random import random
import numpy
import sys

testNum = 1000
noiseRatio = 0.025
step = 0.0001

flips = 0


# with open("../data/testdrift.txt" , 'w') as fout:
#   noise = 0
#   avg = 0.0
#   for i in range(100000):
#     # noise = max(0, noise+numpy.random.normal(-0.1,0.4))
#     noise = max(0,random()*0.5-0.1)
#     avg = (avg+noise)/2
#   print avg
# sys.exit()
clean = 0

with open('../data/noiseTest.txt','w') as fout:
  for k in range(1):
    fout.write("="*120+'\n')
    fout.write("noise ratio: %s\n" % noiseRatio)
    fout.write("="*120+'\n\n')
    with open('../data/packets.txt','r') as fin:
      for i in range(testNum):
        packet = fin.readline().strip()
        packet = packet[:100]
        fout.write(packet+"\n")
        noisy = noise.burst(packet, noiseRatio)
        if packet == noisy: clean += 1
        for i,j in zip(packet,noisy):
          if i == j:
            fout.write(' ')
          else:
            fout.write("|")
            flips += 1
        fout.write("\n")
        fout.write(noisy+'\n'*3)
    noiseRatio += step

print float(flips)/testNum
print testNum - clean