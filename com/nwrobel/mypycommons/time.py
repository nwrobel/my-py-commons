'''
mlu.common.time

Module containing "common" functionality related to time and timestamp logic.
'''

from datetime import datetime, timedelta
from pytimeparse.timeparse import timeparse

def isValidTimestamp(timestamp):
    '''
    Checks whether or not the given epoch timestamp (float value, can contain fractions of second)
    represents a valid time. A valid time is defined as the following:
    - After or equal to 1900-01-01 00:00:00
    - Less than or equal to the current date/time

    @params
    timestamp: (int or float) the epoch timestamp
    '''
    if (not isinstance(timestamp, int)) and (not isinstance(timestamp, float)):
        return False

    lowerThresholdDatetime = datetime(year=1900, month=1, day=1)
    upperThresholdDatetime = datetime.now()
    testValueDatetime = datetime.fromtimestamp(timestamp)

    isValid = (lowerThresholdDatetime <= testValueDatetime <= upperThresholdDatetime)
    return isValid

def convertDateTimeToTimestamp(dateTime: datetime) -> float:
    '''
    Converts a datetime object into an epoch timestamp (float)
    '''
    return datetime.timestamp(dateTime)

def formatDatetimeForDisplay(datetime: datetime) -> str:
    ''' 
    Converts a datetime object into a human-readable string.
    Format is: YYYY-MM-DD HH-MM-SS (ex: "2012-01-27 02:29:33")
    ''' 
    return datetime.strftime("%Y-%m-%d %H:%M:%S")

def getDateTimeFromFormattedTime(formattedTime: str) -> datetime:
    '''
    Converts the given formatted time string, formatted as YYYY-MM-DD HH-MM-SS (ex: "2012-01-27 02:29:33")
    from this string format into a datetime.

    @params
    formattedTime: (str) the pretty formatted time string to convert
    '''
    dateTime = datetime.strptime(formattedTime, "%Y-%m-%d %H:%M:%S")
    return dateTime

def getTimedeltaFromFormattedDuration(formattedTime: str) -> timedelta:
    '''
    Given a duration formatted like "0:03:01" create a timedelta object
    '''
    seconds = timeparse(formattedTime)
    return timedelta(seconds=seconds)

def applyDeltaYearsToTimestamp(startTimestamp, years):
    '''
    Given a starting time timestamp and a number of years, this returns a new epoch timestamp which represents
    that time X years before or after the given timestamp. Years can be positive to add time or 
    negative to subtract time. 

    @params
    startTimestamp: (int or float) the starting epoch timestamp
    years: (int) number of years time to add
    '''
    startDt = datetime.fromtimestamp(startTimestamp)
    newDt = startDt + datetime.timedelta(years=years)
    newTimestamp = datetime.timestamp(newDt)

    return newTimestamp

def applyDeltaSecondsToTimestamp(startTimestamp, seconds):
    '''
    Given a starting time timestamp and a number of seconds, this returns a new epoch timestamp which represents
    that time X seconds before or after the given timestamp. Years can be positive to add time or 
    negative to subtract time. 

    @params
    startTimestamp: (int or float) the starting epoch timestamp
    seconds: (int) number of seconds time to add
    '''
    startDt = datetime.fromtimestamp(startTimestamp)
    newDt = startDt + datetime.timedelta(seconds=seconds)
    newTimestamp = datetime.timestamp(newDt)

    return newTimestamp

def convertDurationToTimestamp(seconds):
    '''
    Converts the given duration, represented in seconds, into the duration represented as epoch 
    timestamp duration/time delta.

    @params
    seconds: (int) number of seconds of duration to convert
    '''
    secondsDt = datetime.timedelta(seconds=seconds)
    secondsTimestamp = datetime.timestamp(secondsDt)
    return secondsTimestamp


def getCurrentYear():
    '''
    Returns the 4 digit integer value of the current calendar year.
    '''
    currentYear = (datetime.now()).year  
    return int(currentYear) 


def getCurrentTimestamp():
    '''
    Returns the current time as an epoch timestamp.
    '''
    dt = datetime.now()
    return datetime.timestamp(dt)

def getCurrentFormattedTime():
    '''
    Returns the current time, formatted to look pretty for display purposes.
    Output format example: "2012-01-27 02:29:33". Hours will be represented on a
    24-hour clock. 
    
    Since epoch timestamps are given in time relative to GMT, the formatted time 
    returned will be adjusted according to the current timezone by adding hours, so that the correct
    time according to the current location is returned.
    
    If the given epoch timestamp contains a fractional (decimal) part, it will be rounded to remove 
    it so it can be displayed in the output format YYYY-MM-DD HH-MM-SS. 

    Timestamps in this format are not meant to be used for precise calculations. Instead, use the
    original epoch timestamp values, which may include fractional/decimal seconds. 
    '''
    return formatDatetimeForDisplay(datetime.now())

def getCurrentTimestampForFilename():
    '''
    Returns the current time, formatted in such a way as to allow it to be used as a string in file
    names. This is useful for applying archive timestamps to files through their name.

    Example output: "2012-01-27 02.29.33"
    '''
    timeFmt = getCurrentFormattedTime().replace(':', '.')
    timeFilename = "{}".format(timeFmt)
    return timeFilename




    
