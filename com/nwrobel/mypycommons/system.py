import os

def thisMachineIsWindowsOS():
    if (os.name == 'nt'):
        return True
    else:
        return False