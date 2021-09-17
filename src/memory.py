'''
MMU Simulator in python
Assignment 3, Computer Architecture
Authors: Akilesh K, Arjun Menon V
Sept 2021
Class Definition for the memory module
Notes: - 'mem' array in memory objects of "user" type has granularity of 1 byte,
         while in objects of "kernel" type, the granularity is 4 bytes
'''
import numpy as np
import sys
print(sys.path)
from inc.opts import *
from queue import Queue as Q
class memory:
    def __init__(self, num_frames= 768, objtype= "user"):
        self.num_frames = num_frames
        self.objtype= objtype
        self.LRUctr = (-1)*np.ones(self.num_frames, dtype= int) #LRUctr = -1 when frame is free
        if(self.objtype == "user"):
            # Page Frames in User Space require granularity in bytes
            self.mem = np.zeros((self.num_frames, ENTRIES_PER_FRAME*ENTRY_SIZE), dtype= int)
            self.freeFrames = Q(self.num_frames)    # FIFO to track free frames
            for i in range(self.num_frames):
                self.freeFrames.put(i)          # initialise FIFO to include all page frames
        else:
            # Kernel Page Frames operate at granularity of PDE or PTE (= 4B)
            self.mem = np.zeros((self.num_frames, ENTRIES_PER_FRAME), dtype= int)
            # valid bit denotes whether the Page pointed to by the entry resides in mem
            self.valid = np.zeros((self.num_frames, ENTRIES_PER_FRAME), dtype= bool)
            self.freeFrames = Q(self.num_frames-NPROC)
            for i in range(NPROC, self.num_frames):
                self.freeFrames.put(i)          # page directories cannot be replaced
        return self
    #
    def updateLRU(self, hit_page):
        return 0
    def evictframe(self):
        return 0
