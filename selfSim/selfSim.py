#! /usr/bin/env/python

import echonest.remix.audio as audio
import math
import matplotlib.pyplot as plt
from scipy.spatial import distance as d
# Music Similarity matrix
# Appstate Computer Science Music informatics Course 3535
# Spring 2015
# Author Ryan Yanik

usage = """
    python selfSim.py <input_file>
"""

def main(input_file):
    audiofile = audio.LocalAudioFile(input_file)
    pitches = audiofile.analysis.segments.pitches
    timbre = audiofile.analysis.segments.timbre

    pitch_sim = [[0 for x in range(len(pitches))] for x in range (len(pitches))]
    timbre_sim = [[0 for x in range(len(timbre))] for x in range(len(timbre))]

    for i in range(len(pitches)):
        for j in range(len(pitches)):
	        pitch_sim[i][j] = compare(pitches[i], pitches[j])
    for i in range(len(timbre)):
	    for j in range(len(timbre)):
	        timbre_sim[i][j] = compare(timbre[i], timbre[j])
    plt.imshow(pitch_sim)
    plt.show()
    plt.imshow(timbre_sim)
    plt.show()

def compare(list_one, list_two):

    #ans = 0

    #for i in range(len(list_one)):
	#ans += (list_one[i] - list_two[i])**2

    return d.euclidean(list_one,list_two)#math.sqrt(ans)

if __name__ == '__main__':
    import sys
    try:
	input_file = sys.argv[1]
    except:
	print usage
        sys.exit(-1)
    main(input_file)

