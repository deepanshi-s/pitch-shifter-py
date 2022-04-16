# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 04:00:39 2022

@author: Admin
"""

#!/usr/bin/env python
##
# pitch-shifter-cli.py: Pitch Shifter Command Line Tool
# 
# Author(s): Chris Woodall <chris@cwoodall.com>
# MIT License 2015-2021 (c) Chris Woodall <chris@cwoodall.com>
##
import argparse
import matplotlib.pyplot as pp
import numpy as np
import scipy
import scipy.interpolate
import scipy.io.wavfile
import sys
import logging

from stft import *
from vocoder import *
from utilities import *
from resampler import linear_resample

logging.basicConfig(filename='pitchshifter-cli.log', filemode='w', level=logging.DEBUG)


def pitchShifter(wavFile, pitch, out, startTime = 0, endTime= -1, overlap = .9, chunk_size = 4096, blend = 1):
    # Try to open the wav file and read it
    try:
        source = scipy.io.wavfile.read(wavFile)
        print("here")
    except:
        print("File {0} does not exist".format(wavFile))
        sys.exit(-1)
    time = source[1].shape[0] / source[0]
    
    
    print(source[1].shape, time)
    
    start_time = 0
    end_time = source[1].shape[0]
    
    concat = False
    
    if(startTime != 0):
        start_time = int(startTime*source[0])
        concat = True
    
    if(endTime != -1):
        end_time = int(endTime*source[0])
    
    
    
        
    
    RESAMPLING_FACTOR = 2**(pitch/12)
    HOP = int((1-overlap)*chunk_size)
    HOP_OUT = int(HOP*RESAMPLING_FACTOR)
    
    audio_samples = source[1].tolist()
    
    
    print(HOP, HOP_OUT, chunk_size)
    rate = source[0]
    mono_samples = stereoToMono(audio_samples)
    signal = mono_samples[start_time:end_time]
    frames = stft(signal, chunk_size, HOP)
    vocoder = PhaseVocoder(HOP, HOP_OUT)
    adjusted = [frame for frame in vocoder.sendFrames(frames)]

    merged_together = istft(adjusted, chunk_size, HOP_OUT)

    
    resampled = linear_resample(merged_together, 
                                   len(signal))
    final = resampled * blend + (1-blend) * signal

    
    
    print(start_time, end_time)
    print(mono_samples[:start_time].shape, final.shape, mono_samples[end_time:].shape)
    if (concat == True):
        finalSig = np.concatenate((mono_samples[:start_time], final, mono_samples[end_time:]))
    else:
        finalSig = final
    
    print(finalSig.shape)
    
    
    output = scipy.io.wavfile.write(out, rate, np.asarray(finalSig, dtype=np.int16))
    