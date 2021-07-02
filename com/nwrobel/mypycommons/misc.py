'''
com.nwrobel.misc

This module contains functionality for things that fall under no simple category: general 'utils'.
'''

def stringStartsWith(inputString, startsWith):
    '''
    Returns true/false whether or not the given string starts with the given substring.

    @params
    inputString: the original input string
    startsWith: the string of characters to see if the original string begins with
    '''
    startsWithLength = len(startsWith)
    if (inputString[0:startsWithLength] == startsWith):
        return True
    else:
        return False