'''
com.nwrobel.system

This module contains functionality related to operating systems and their operations.
'''

import os

def thisMachineIsWindowsOS():
    if (os.name == 'nt'):
        return True
    else:
        return False