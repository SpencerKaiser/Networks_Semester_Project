# CSE4344 - Networks
# Luke Oglesbee

import numpy as np
from sys import stdout

__verbose = True

def gaussian(signal, noise_ratio):
    """Put signal through gaussian white noise filter"""
    if noise_ratio < 0 or noise_ratio > 1:
        print "noise_ratio must be between 0 and 1"
        return False
    # Generate noise
    noise = np.random.rand(len(signal))
    flip = map(lambda x: x < noise_ratio, noise)
    output = []
    for f,s in zip(flip, signal):
        if f:
            output.append((int(s)+1)%2)
        else:
            output.append(int(s))
    # print flip
    if __verbose:
        for f in flip:
            if f:
                stdout.write("|")
            else:
                stdout.write(" ")
        print ""
    return "".join(str(x) for x in output)

def burst(signal, noise_ratio, max_bit_flip=16):
    """Put signal through burst noise filter"""
    if noise_ratio < 0 or noise_ratio > 1:
        print "noise_ratio must be between 0 and 1"
        return False
    # Generate noise
    noise = np.random.rand(len(signal))
    length = [int(x*max_bit_flip) for x in np.random.rand(len(signal))]
    flip = map(lambda x: x < noise_ratio, noise)
    i = 0
    while i < len(flip):
        if flip[i]:
            j = i
            i += length[i]
            while j < len(flip) and j < i:
                flip[j] = True
                j += 1
        i += 1
    output = []
    for f,s in zip(flip, signal):
        if f:
            output.append((int(s)+1)%2)
        else:
            output.append(int(s))
    if __verbose:
        for f in flip:
            if f:
                stdout.write("|")
            else:
                stdout.write(" ")
        print ""
    return "".join(str(x) for x in output)



    