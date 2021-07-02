'''
com.nwrobel.system

This module contains functionality related to operating systems and their operations.
'''

import os

def thisMachineIsWindowsOS():
    '''
    Determines whether or not the OS currently running this Python script is Windows or not.
    '''
    if (os.name == 'nt'):
        return True
    else:
        return False