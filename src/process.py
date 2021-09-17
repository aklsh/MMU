'''
MMU Simulator in python
Assignment 3, Computer Architecture
Authors: Akilesh K, Arjun Menon V
Sept 2021
Class Definition for the process module

NOTES: - function for pagewalk must include kernelMem and userMem objects as arguments
         (e.g.- for accessing entry no. 60 of PD for a process, use kernelMem.mem[pid][60])
'''
class proc:
    def __init__(self, pid):
        self.pid = pid
