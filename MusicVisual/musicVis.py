#! /usr/bin/env/python

import pprint
import math
import random as r
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.spatial import distance as d
import cPickle as pickle

# Music Visualization
# Appstate Computer Science Music Informatics course 3535
# Spring 2015
# Author Ryan Yanik

"""
   musicVis is a visualization of the closeness of different chords 
"""

usage = """
    python musicVis.py <anchor chord>(i.e. CM, Cm, Co, CM7, ect...) <number of iterations> <Large?> (0,1)(default is 0) <crashed?> (1,0)
"""
notes = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
chords = ['M','m','o','+','M7','m7','x7','07','+7','m-7','o7']
note_chords = []
chord_indices = []

o_patterns = []
s_patterns = []
r_patterns = []

numpy_o_patterns = np.array(o_patterns)

num_inputs = 0

def main(anchor_chord, num_it,size,crashed):

    if(init_s_patterns(size) == -1):
        print "init_s_patterns failed"
        exit(-1)
    if(init_r_patterns() == -1):
        print "init_r_patterns failed"
        exit(-1)
    if(init_o_patterns() == -1):
        print "init_o_patterns failed"
        exit(-1)

    chord_index = get_chord_index(anchor_chord,size)
    chord = get_chord(chord_index)

    numpy_o_patterns = np.array(o_patterns)

    map = make_map(chord,num_it,size,crashed)
    print "map done"
    distance = distance_map(chord,map)
    print "distance done"
    label_map(map,size)
    print "labeling done"

    plt.imshow(distance,interpolation = 'nearest')
    plt.show()

def init_s_patterns(size):

    global s_patterns

    num_chords = 0

    if(size is 1):
        s_patterns = [[0 for i in range(12)] for i in range(132)]

        s_patterns[0] = [1,0,0,0,1,0,0,1,0,0,0,0]
        s_patterns[1] = [1,0,0,1,0,0,0,1,0,0,0,0]
        s_patterns[2] = [1,0,0,1,0,0,1,0,0,0,0,0]
        s_patterns[3] = [1,0,0,0,1,0,0,0,1,0,0,0]
        s_patterns[4] = [1,0,0,0,1,0,0,1,0,0,0,1]
        s_patterns[5] = [1,0,0,1,0,0,0,1,0,0,1,0]
        s_patterns[6] = [1,0,0,0,1,0,0,1,0,0,1,0]
        s_patterns[7] = [1,0,0,1,0,0,1,0,0,0,1,0]
        s_patterns[8] = [1,0,0,0,1,0,0,0,1,0,0,1]
        s_patterns[9] = [1,0,0,1,0,0,0,1,0,0,0,1]
        s_patterns[10] = [1,0,0,1,0,0,1,0,0,1,0,0]

        num_chords = 11
        set_num_inputs(132)

    else:
        s_patterns = [[0 for i in range(12)] for i in range(24)]

        s_patterns[0] = [1,0,0,0,1,0,0,1,0,0,0,0]
        s_patterns[1] = [1,0,0,1,0,0,0,1,0,0,0,0]

        num_chords = 2
        set_num_inputs(24)

    for i in range(len(s_patterns)):
        if(i > (num_chords - 1)):
            s_patterns[i] = s_patterns[i%num_chords]

    note = 0
    for i in range(len(s_patterns)):
        if(i > (num_chords - 1)):
            if i % num_chords == 0:
                note+=1
            s_patterns[i] = shift(note,s_patterns[i])

    count = 0
    for i in range(len(s_patterns)):
        if(i % num_chords == 0):
            count+=1

    if(len(s_patterns) == 0):
        return -1
    else:
        return 0

def init_r_patterns():

    global r_patterns

    r_patterns = [[0 for i in range(12)] for i in range(len(s_patterns))]

    note_r_patterns = [[0 for i in range(12)] for i in range(12)]

    note_r_patterns[0] = [1,0,.25,0,0,.5,0,0,.33,.1,.2,0]

    for i in range(12):
        if i > 0:
            note_r_patterns[i] = shift(1,note_r_patterns[i-1])

    for r in range(len(s_patterns)):
        for c in range(12):
            if(s_patterns[r][c] == 1):
                for i in range(12):
                    r_patterns[r][i] += note_r_patterns[c][i]
    if(len(r_patterns) == 0):
        return -1
    else:
        return 0

def init_o_patterns():

    global o_patterns

    o_patterns = [[0 for i in range(12)] for i in range(len(r_patterns))]

    for r in range(len(r_patterns)):
        for c in range(12):
            o_patterns[r][c] = O_algorithm(r_patterns[r][c],r_patterns[r])

    if(len(o_patterns) == 0):
        return -1
    else:
        return 0

def make_map(anchor_chord,num_it,size,crashed):

    map = [[[r.random() for i in range(12)] for i in range(size_of_map())]for i in range(size_of_map())]
    new_map = np.array(map)

    distance = [[0 for i in range(len(new_map))] for j in range(len(new_map))]

    learning_rate = .02
    count = 1
    count_down_two = get_num_inputs()
    count_down = num_it

    if(crashed and size == 0):
        with open('./crash_info/small/map.p', 'rb') as file1:
            new_map = pickle.load(file1)
        with open('./crash_info/small/count.p','rb') as file2:
            count = pickle.load(file2)
            count_down = num_it - count
        with open('./crash_info/small/num_it.p','rb') as file3:
            num_it = pickle.load(file3)
    elif(crashed and size == 1):
        with open('./crash_info/large/map.p', 'rb') as file1:
            new_map = pickle.load(file1)
        with open('./crash_info/large/count.p','rb') as file2:
            count = pickle.load(file2)
            count_down = num_it - count
        with open('./crash_info/large/num_it.p','rb') as file3:
            num_it = pickle.load(file3)

    random_chord_index = r.randint(0,len(o_patterns)-1)
    chord = get_chord(random_chord_index)
    bmu_index = best_matching_unit_on_map(chord,new_map)

    while count <= num_it:
        print ".........."
        print count_down
        print ".........."
        for i in range(get_num_inputs()):
            print count_down_two

            update(new_map,bmu_index,count,learning_rate,chord)

            random_chord_index = r.randint(0,len(o_patterns)-1)
            chord = get_chord(random_chord_index)
            bmu_index = best_matching_unit_on_map(chord,new_map)

            count_down_two -= 1
        if(size == 1 and count % 10 == 0):
            file_name = './steps/map' + str(count) + '.p'
            with open(file_name, 'wb') as picklepicture:
                pickle.dump(new_map,picklepicture)
        if(size == 0):
            with open('./crash_info/small/map.p', 'wb') as file:
                pickle.dump(new_map, file)
            with open('./crash_info/small/count.p', 'wb') as file2:
                pickle.dump(count, file2)
            with open('./crash_info/small/num_it.p','wb') as file3:
                pickle.dump(num_it,file3)
        else:
            with open('./crash_info/large/map.p', 'wb') as file:
                pickle.dump(new_map, file)
            with open('./crash_info/large/count.p', 'wb') as file2:
                pickle.dump(count, file2)
            with open('./crash_info/large/num_it.p','wb') as file3:
                pickle.dump(num_it,file3)

        count_down_two = get_num_inputs()
        count= count + 1
        count_down = count_down - 1
    return new_map

def update(map,bmu_index,it_count,learning_rate,chord):

    new_chord = np.array(chord)
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j] = map[i][j] + neighborhood(bmu_index,[i,j],it_count) * learning_rate * (new_chord - map[i][j])

def sum_distance(map):

    sum = 0
    bmu = [0,0]
    for i in range(len(o_patterns)):
        bmu = best_matching_unit_on_map(o_patterns[i],map)
        sum += compare(o_patterns[i],map[bmu[0]][bmu[1]])
    return sum

def distance_map(anchor_chord,map):

    distance_map = [[0 for i in range(len(map))] for j in range(len(map))]

    for i in range(len(map)):
        for j in range(len(map[i])):
            distance_map[i][j] = compare(anchor_chord,map[i][j])
    return distance_map

def set_note_chords(size):

    global chord_indices
    global note_chords

    if size is 1:
        num_chords = 11
    else:
        num_chords = 2

    count = 0
    for i in range(12):
        for j in range(num_chords):
            chord_indices.append({"chord" : (notes[i] + chords[j]), "index": count})
            count += 1

    for i in chord_indices:
        note_chords.append(i.get("chord"))

def get_chord_index(chord_string,size):

    if len(chord_indices) == 0:
        set_note_chords(size)

    for i in chord_indices:
        if(i.get("chord") == chord_string):
            return i.get("index")

def best_matching_unit_on_map(chord, map):

    bmu_cord = [-1,-1]
    bmu = 1000000000

    for r in range(len(map)):
        for c in range(len(map[r])):
            if(compare(map[r][c], chord) < bmu):
                bmu = compare(map[r][c], chord)
                bmu_cord = [r,c]
    return bmu_cord

def label_map(map,size):

    global note_chords

    for i in range(len(o_patterns)):
        chord_index = get_chord_index(note_chords[i],size)
        chord = get_chord(chord_index)
        bmu = best_matching_unit_on_map(chord,map)
        plt.text(bmu[1],bmu[0],note_chords[i])
    return map

def size_of_map():

    size = int(len(o_patterns) - (len(o_patterns)/6))
    return size

def get_chord(chord_index):

    return o_patterns[chord_index]

def neighborhood(u,v,s):

    neighborhood = (math.e)**-((distance(u,v)**2)/(2*(stddev(s)**2)))
    return neighborhood

def distance(cord1, cord2):

    if(len(cord1) != 2 or len(cord2) != 2):
        print "Cords out of bounds"
        exit(-1)

    return math.sqrt(min(math.fabs(cord1[0] - cord2[0]), size_of_map() - math.fabs(cord1[0] - cord2[0]))**2 +
                min(math.fabs(cord1[1] - cord2[1]), size_of_map() - math.fabs(cord1[1] - cord2[1]))**2)
def stddev(s):

    stddev = ((size_of_map() - 1) - (s/(size_of_map()-1)))/3
    return stddev

def compare(list_one, list_two):

    if len(list_one) != 12 or len(list_two) != 12:
        exit(-1)
    else:
        dst = d.euclidean(list_one,list_two)

    return dst

def O_algorithm(R,lst):

    sum = 0
    r_max = max(lst)
    first_term = R/r_max

    for i in range(12):
        sum += lst[i] / r_max

    second_term = 1 / math.sqrt(sum)

    return first_term * second_term

def shift(key, array):
    return array[-key:] + array[:-key]

def set_num_inputs(num_in):
    global num_inputs
    num_inputs = num_in

def get_num_inputs():
    return num_inputs

if __name__ == '__main__':
    import sys
    try:
        anchor_chord = sys.argv[1]
        num_it = int(sys.argv[2])
    except:
        print usage
        sys.exit(-1)
    if(len(sys.argv) == 4):
        size = int(sys.argv[3])
    elif(len(sys.argv) == 5):
        size = int(sys.argv[3])
        crashed = int(sys.argv[4])
    else:
        size = 0
        crashed = 0
    main(anchor_chord, num_it,size,crashed)

