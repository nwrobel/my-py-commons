'''
This module contains functionality for things that fall under no simple category: general 'utils'.
'''

from typing import List

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

def stringIsNullOrEmpty(inputString: str) -> bool:
    ''' 
    Checks whether or not a string is None or empty.
    ''' 
    if (not isinstance(inputString, str)):
        raise TypeError("inputString is invalid")
    else:
        return (inputString is None or not inputString)

def listIsNullOrEmpty(inputList: List) -> bool:
    ''' 
    Checks whether or not a list is None or empty.
    ''' 
    if (not isinstance(inputList, list)):
        raise TypeError("inputList is invalid")
    else:
        return (inputList is None or not inputList)

def convertBitsToKilobits(bits):
    '''
    Converts the given number of bits to kilobits.
    '''
    kilobits = round(bits / 1000)
    return kilobits

def getListDupes(inputList):
    '''
    Returns a set of the items in the list that are duplicates
    '''
    return set([x for x in inputList if inputList.count(x) > 1])

