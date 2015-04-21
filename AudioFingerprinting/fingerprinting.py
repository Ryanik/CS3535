#! /usr/bin/env/python

import pprint
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import signal as sig
import scipy.io.wavfile as wav
import wave

def main (input_file):

    spf = wave.open(input_file,'r')
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, "Int16")
    signal = signal/float(max(signal))
    fs = spf.getframerate()
    signal = make_stereo_mono(signal)
    signal = np.reshape(signal,(2646000,1))
    Time=np.linspace(0,len(signal)/fs,num=len(signal))
    plt.figure(1)
    plt.plot(Time,signal)
    plt.show()

def make_stereo_mono(stereo):
    stereo = np.reshape(stereo,(len(stereo)/2,2))
    return np.array([(stereo[:,0] + stereo[:,1]) / 2])

if __name__ == '__main__':
    import sys
    try:
        input_file = sys.argv[1]
    except:
        print "error"
        sys.exit(-1)
    main(input_file)
