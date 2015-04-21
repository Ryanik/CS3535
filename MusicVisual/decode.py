#! /usr/bin/env/python

import pprint
import cPickle as pickle
import musicVis as mV
import matplotlib.pyplot as plt


usage = """
        python decode.py <pickle_file_name> <anchor_chord> <size>
        """

def main(map_pickle_file,anchor_chord,output_file_name):

    print map_pickle_file
    mV.set_note_chords(1)
    map = decodeMap(map_pickle_file)
    mV.init_s_patterns(1)
    mV.init_r_patterns()
    mV.init_o_patterns()
    chord_index = mV.get_chord_index(anchor_chord,1)
    chord = mV.get_chord(chord_index)
    distance_map = mV.distance_map(chord,map)
    mV.label_map(map,1)
    plt.imshow(distance_map,interpolation = 'nearest')
    plt.savefig('./Figures/' + output_file_name + '.png', bbox_inches='tight')

def decodeMap(map_pickle_file):

    with open(map_pickle_file,'rb') as file1:
        map = pickle.load(file1)
    return map


if __name__ == '__main__':
    import sys
    try:
        map_pickle_file = sys.argv[1]
        anchor_chord = sys.argv[2]
        output_file_name = sys.argv[3]
    except:
        print usage
        sys.exit(-1)
    main(map_pickle_file, anchor_chord,output_file_name)
