'''
com.nwrobel.misc

This module contains functionality for things that fall under no simple category: general 'utils'.
'''

def stringStartsWith(inputString, startsWith):
    startsWithLength = len(startsWith)
    if (inputString[0:startsWithLength] == startsWith):
        return True
    else:
        return False