# CSE4344 - Networks
# Luke Oglesbee

import numpy as np
from sys import stdout

__verbose = False

def gaussian(signal, noise_ratio):
    """Put signal through gaussian white noise fitler"""
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