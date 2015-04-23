#! /usr/bin/env/python

import echonest.remix.audio as audio
import pprint
# sorting2 
# Appstate Computer Science Music Informatics course 3535
# Spring 2015
# Author Ryan Yanik

"""
    sorting2.py will take all of the segments in a song and sort them by the
    most dominate pitch per segment, staring with what ever pitch you want 
    0-11, 0 being C and wraping around i.e. if you choose 5 it will sort
    like 5,6,7,8,9,10,11,0,1,2,3,4

"""
usage = """
    python sorting2.py <Input File> <0-11> (optional default 0> <Output File Name>(optional)
"""

def main(input_file, output_file, start_note):
    audiofile = audio.LocalAudioFile(input_file)
    segments = audiofile.analysis.segments
    pitches = audiofile.analysis.segments.pitches
    
    sorted_segments = sort(pitches, segments, start_note)
     
    out = audio.getpieces(audiofile, sorted_segments)
    out.encode(output_file)        

def sort(pitch_list,segment_list, start_note):
   
    # save for later if doesn't work goes in max_pitch_list init
    # [pitch_dict[0] for i in range(len(pitch_list))

    pitch_dict = [{'pitch_vector': pitch_list[0], 'index': 0}  for x in range(len(pitch_list))]
    max_pitch_list = [[] for x in range(12)]
    count = [0 for i in range(12)]

    #tracking the original index of the pitch vector
    for i in range(len(pitch_list)):
        pitch_dict[i] = {'pitch_vector': pitch_list[i], 'index': i}
 
    # sorting out which pitch is highest
    for i in range(len(pitch_dict)):
        max_pitch_list[pitch_dict[i].get('pitch_vector',0).index(max(pitch_dict[i].get('pitch_vector',0)))].append( pitch_dict[i])
        count[pitch_dict[i].get('pitch_vector',0).index(max(pitch_dict[i].get('pitch_vector',0)))]+=1

    # bubble sorting pitches so the highest amount of pitch is first
    for i in range(12):
        for j in range(count[i]):
            for k in range(count[i]-1-j):
                if max(max_pitch_list[i][k].get('pitch_vector',0)) > max(max_pitch_list[i][k+1].get('pitch_vector',0)):
                    max_pitch_list[i][k], max_pitch_list[i][k+1] = max_pitch_list[i][k+1], max_pitch_list[i][k]

    counter = int(start_note)
    i = 0
    # save code 0 for x in range(len(pitch_list))
    sorted_pitch_indices = []
    sorted_segments = [segment_list[42] for x in segment_list]
    while i < 12:
        for j in range(len(max_pitch_list[counter])):
            sorted_pitch_indices.append(max_pitch_list[counter][j].get('index',0))
        counter+=1
        if counter == 12:
            counter = 0
        i+=1
    
    for i in range(len(segment_list)):
        sorted_segments[i] = segment_list[sorted_pitch_indices[i]]
    
    return sorted_segments


def create_output_file(input_file):
    
    return input_file[:len(input_file)-4] + "_sorted2.mp3"


if __name__ == '__main__':
    import sys
    try:
        input_file = sys.argv[1]
    except:
        print usage
        sys.exit(-1) 
    if len(sys.argv) < 4:
        output_file = create_output_file(input_file)
    else:
        output_file = sys.argv[3]
    if len(sys.argv) < 3:
        start_note = 0
    else:
        start_note = sys.argv[2]
    main(input_file, output_file, start_note)






