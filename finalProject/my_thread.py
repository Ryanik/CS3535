#! /usr/bin/env/python

import threading

class my_thread(threading.Thread):

    def __init__(self,player,queue):
        threading.Thread.__init__(self)
        self.player = player
        self.queue = queue
        self._stopping = threading.Event()
    def run(self):
        while(self.stopping() != True):
            self.player.play(self.queue.get())
    def stopping(self):
        return self._stopping.isSet()
    def stop(self):
        self._stopping.set()