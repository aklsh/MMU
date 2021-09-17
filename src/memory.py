'''
MMU Simulator in python
Assignment 3, Computer Architecture
Authors: Akilesh K, Arjun Menon V
Sept 2021
Class Definition for the memory module
Notes: - 'mem' array in memory objects of "user" type has granularity of 1 byte,
         while in objects of "kernel" type, the granularity is 4 bytes
       - Assumption: First NPROC frames in kernel space are allocated to Page Directories
       - evictframe() returns victim frame number; use this to update PDEvalid or PTEvalid from pagewalk()
'''
from sys import exit
import numpy as np
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
            if (self.num_frames <= NPROC):
                print("Insufficient space allocated to MMU in Kernel Space, exiting!")
                exit(-1)
            # Kernel Page Frames operate at granularity of PDE or PTE (= 4B)
            self.mem = np.zeros((self.num_frames, ENTRIES_PER_FRAME), dtype= int)
            # valid bit denotes whether the Page pointed to by the entry resides in mem
            self.valid = np.zeros((self.num_frames, ENTRIES_PER_FRAME), dtype= bool)
            self.freeFrames = Q(self.num_frames-NPROC)
            for i in range(NPROC, self.num_frames):
                self.freeFrames.put(i)          # page directories cannot be replaced
    #
    def updateLRU(self, hit_page):
        curr_count = self.LRUctr[hit_page]
        if (curr_count == -1): # page was previously free, inc LRUctr of all active frames by 1
            if((self.objtype == "user") or (hit_page >= NPROC)): # PDframes not present in FIFO
                self.__updateFIFO(hit_page)
            for i in range(self.num_frames):
                if(self.LRUctr[i] != -1):
                    self.LRUctr[i] += 1
        else:
            for i in range(self.num_frames):
                # inc LRUctr of all frames that were used btw prev access to current frame and now
                if((self.LRUctr[i] != -1) and (self.LRUctr[i] < curr_count)):
                    self.LRUctr[i] += 1
        self.LRUctr[hit_page] = 0
        return 0
    def __updateFIFO(self, hit_page):
        # remove entry corr to hit_page from FIFO
        temp_size = self.freeFrames.qsize()
        temp = Q(temp_size)
        for i in range(temp_size):
            temp_val = self.freeFrames.get()
            if(temp_val != hit_page):
                temp.put(temp_val)
        for i in range(temp_size-1):
            self.freeFrames.put(temp.get())
        return 0
    def evictframe(self):
        # Call this ONLY IF FIFO is empty
        if (self.freeFrames.empty()):
            if (self.objtype == "user"):
                victim_frame = np.argmax(self.LRUctr)
                self.freeFrames.put(victim_frame)
                self.LRUctr[victim_frame] = -1
            else:
                victim_frame = np.argmax(self.LRUctr[NPROC:-1]) # do not evict Page Directory
                self.freeFrames.put(victim_frame)
                self.LRUctr[victim_frame] = -1
            return victim_frame
        return -1

    def invalidate_entry(self, targ_type, victim):
        if (self.objtype == "kernel"):
            if (targ_type == "user"): # update valid field in PTE
                frame, entry = np.where((self.mem[NPROC:][:] == victim)) # search amongst PTEs
                frame = frame[0]; entry = entry[0]
                self.valid[frame][entry] = 0    #invalidate
            else:
                frame, entry = np.where((self.mem[0:NPROC][:] == victim)) # search amongst PDEs
                frame = frame[0]; entry = entry[0]
                self.valid[frame][entry] = 0
            return 0
        return -1
