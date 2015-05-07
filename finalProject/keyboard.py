#! /usr/bin/env/python

import echonest.remix.audio as audio
import pprint
import sys
import os
import string
import Player
import keypress
import my_thread
import Queue

usage = """
            python keyboard.py <input_file_name>
        """
key_binds = []

def main(input_file):

    audiofile = audio.LocalAudioFile(input_file)
    bars = audiofile.analysis.bars

    length = audiofile.duration
    average = length/(len(bars))
# average person types 40 words per minute
# average english word 5.1 letters long
# ( 40 * 5.1 )/60seconds = 3.4 letters per second
# the number of threads is based on the average length of a bar
# and the amount of keypresses that could be pressed in that time
    num_threads = int(average*3.4)
    print
    print "Song:\t", input_file
    print "Druation:\t",int(audiofile.duration/60),"minutes",int(audiofile.duration%60),"seconds"
    print "Number of bars:\t", len(bars)

    print "Press any of these keys"
    key_binds = key_bind_bars(bars,len(bars))

    key = keypress.KBHit()
    players = []
    for i in range(num_threads):
        p = Player.Player(audiofile)
        players.append(p)

    queue = Queue.Queue(1024)
    thread_list = []
    for i in range(num_threads):
        t = my_thread.my_thread(players[i],queue)
        t.start()
        thread_list.append(t)

    print "Press any key"
    play_bar(bars,key,queue)
    print "Done"
    for t in thread_list:
        t.stop()

# key_bind_bars creates a dictionary for each bar in the input song and assignes a key to that bar
# this is the method you would change if your input changes from keyboard to anything else
# for instance a midi keyboard
def key_bind_bars(bars,num_bars):

    global key_binds

    keys = string.printable
    keys = list(keys)
    if(num_bars<(len(keys)-5)):
        keys = keys[0:len(keys)-((len(keys)-num_bars))]
    else:
        keys = keys[0:len(keys)-5]
    print keys

    for i in range(len(keys)):
        key_binds.append({"Bar_number" : i,"Key" :keys[i]})

    return key_binds

def play_bar(bars,key,queue):
    bar_num = -1
    while 1:
        c = key.getch() #geting the character that was pressed
        if ord(c) == 27:
            break
        for i in key_binds:
            if(i.get("Key") == c):
                print c,"was pressed, playing bar number:",i.get("Bar_number")
                bar_num = i.get("Bar_number")
                queue.put(bars[bar_num])
        #ply.play(bars[bar_num])

if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
    except:
        print usage
    main(input_file)
