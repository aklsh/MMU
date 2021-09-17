'''
MMU Simulator in python
Assignment 3, Computer Architecture
Authors: Akilesh K, Arjun Menon V
Sept 2021
Class Definition for the process module

NOTES: - function for pagewalk must include kernelMem and userMem objects as arguments
         (e.g.- for accessing entry no. 60 of PD for a process, use kernelMem.mem[pid][60])
       - update kernelMem.valid[frameNo][entry] when a page or page table location is written to
         kernelMem.mem; similarly when a frame is replaced, the victim_frame Number is returned,
         update the valid field in the Page Table or Page Directory (call kernelMem.invalidate_entry())
'''
class proc:
    def __init__(self, pid):
        self.pid = pid
