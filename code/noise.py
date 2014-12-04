# CSE4344 - Networks
# Luke Oglesbee

import numpy as np
from random import random, randint
from sys import stdout

__verbose = False

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

def drift(signal, noise_ratio, max_delta=0.2):
    """Put singal through drift noise fitler"""
    if noise_ratio < 0 or noise_ratio > 1:
        print "noise_ratio must be between 0 and 1"
        return False
    # Generate noise
    noise = [0]*len(signal)
    noise[0] = random()*noise_ratio
    for i in range(1,len(signal)):
        noise[i] += noise[i-1]+(random()-random()+random()-random())*max_delta
    flip = map(lambda x: x > 1-noise_ratio, noise)
    # print noise
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

def gaussian_RS(signal, noise_ratio):

    noise = ['']*len(signal)
    for i in range(0, len(noise)):
        rand = random()
        if rand <= noise_ratio:
            noise[i] = '-'
        else:
            noise[i] = signal[i]

    return "".join(str(x) for x in noise)


def burst_RS(signal, noise_ratio, max_bit_flip=16):
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
            output.append('-')
        else:
            output.append(s)
    if __verbose:
        for f in flip:
            if f:
                stdout.write("|")
            else:
                stdout.write(" ")
        print ""
    return "".join(str(x) for x in output)
    # noise = ['']*len(signal)
    # for i in range(0, len(noise)):
    #     rand = random()
    #     if rand <= noise_ratio:
    #         burstLen = randint(1, max_bit_flip)
    #         for j in range(0, burstLen):
    #             noise[i+j] = '-'
    #         i += burstLen
    #     else:
    #         noise[i] = signal[i]
    #
    # return "".join(str(x) for x in noise)

def drift_RS(signal, noise_ratio, max_delta=0.2):
    """Put singal through drift noise fitler"""
    if noise_ratio < 0 or noise_ratio > 1:
        print "noise_ratio must be between 0 and 1"
        return False
    # Generate noise
    noise = [0]*len(signal)
    noise[0] = random()*noise_ratio
    for i in range(1,len(signal)):
        noise[i] += noise[i-1]+(random()-random()+random()-random())*max_delta
    flip = map(lambda x: x > 1-noise_ratio, noise)
    # print noise
    output = []
    for f,s in zip(flip, signal):
        if f:
            output.append('-')
        else:
            output.append(s)
    if __verbose:
        for f in flip:
            if f:
                stdout.write("|")
            else:
                stdout.write(" ")
        print ""
    return "".join(str(x) for x in output)


