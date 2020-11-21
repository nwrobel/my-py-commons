def stringStartsWith(inputString, startsWith):
    startsWithLength = len(startsWith)
    if (inputString[0:startsWithLength] == startsWith):
        return True
    else:
        return False