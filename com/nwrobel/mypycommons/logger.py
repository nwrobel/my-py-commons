'''
com.nwrobel.logger

Module containing functionality for configuring and retrieving logger instances, which can be used
as a better alternative to print statements for debugging, info, error, etc purposes.

'''

import logging
import inspect

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.file

class LogLevel:
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

def getLogger(loggerName):
    '''
    Returns a logger instance by name. Does the same as "logging.getLogger(loggerName)"
    '''
    return logging.getLogger(loggerName)

def configureLoggerWithBasicSettings(loggerName, logDir, logFilename=''):
    '''
    Configures the given logger instance, specified by name.
    Logger will send all log statements to the console and to a log file in the specified directory.

    Configuration applied: 
    - the logger will allow all messages to be passed to the handlers (debug or higher)
    - the logger has two handlers, which define how the messages should be output, which ones to output, etc:
        - a file handler, which writes all messages (debug or higher) to a log file
        - a stream (console output) handler, which outputs all messages (debug or higher) to the console/stdout

    @params:
    loggerName: name of the logger, used to retrieve the desired logger instance
    logDir: directory in which to store the log file
    logFilename: (optional) Name of the log file to which the file handler will output the log messages.
            By default, uses the name of the calling script + the .log file extension.
    '''
    loggerSpecified = getLogger(loggerName)

    # allow all messages of all levels to be passed to the handlers: the handlers will have their
    # own levels set, where they can individually decide which messages to print for a more granular
    # logging control
    loggerSpecified.setLevel(logging.DEBUG) 

    # If no log filename was given,
    # get the name of the module/file that called this function so we can use it to be the log file name
    if (not logFilename):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        callerModuleFilename = mypycommons.file.getFilename(module.__file__)

        logFilename = "{}.log".format(callerModuleFilename)

    # create a file handler which logs all messages by default by saving them to a log file
    logFilepath = mypycommons.file.joinPaths(logDir, logFilename)
    fh = logging.FileHandler(logFilepath, encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    # create console output handler which logs all messages (debug up through critical)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - [%(filename)s,  %(funcName)s()] - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    loggerSpecified.addHandler(fh)
    loggerSpecified.addHandler(ch)

def setLoggerConsoleOutputLogLevel(loggerName, logLevel):
    '''
    Modifies the configuration of the given logger by setting the minimum level of importance (log
    level) that log messages need to have in order to be logged to the console.
    
    @params:
    loggerName: name of the logger, used to retrieve the desired logger instance
    logLevel: a valid value from the LogLevel type enum class
    '''
    loggerSpecified = getLogger(loggerName)

    # Get the actual log level from the logging class, given the LogLevel type param
    level = _getLoggerLevel(logLevel)

    for handler in loggerSpecified.handlers:
        if (handler.__class__.__name__ == 'StreamHandler'):
            handler.setLevel(level)

def setLoggerFileOutputLogLevel(loggerName, logLevel):
    '''
    Modifies the configuration of the given logger by setting the minimum level of importance (log
    level) that log messages need to have in order to be logged to the log file.
    
    @params:
    loggerName: name of the logger, used to retrieve the desired logger instance
    logLevel: a valid value from the LogLevel type enum class
    '''
    loggerSpecified = getLogger(loggerName)

    # Get the actual log level from the logging class, given the LogLevel type param
    level = _getLoggerLevel(logLevel)

    for handler in loggerSpecified.handlers:
        if (handler.__class__.__name__ == 'FileHandler'):
            handler.setLevel(level)

def _getLoggerLevel(logLevel):
    if (logLevel == LogLevel.DEBUG):
        return logging.DEBUG

    elif (logLevel == LogLevel.INFO):
        return logging.INFO 

    elif (logLevel == LogLevel.WARNING):
        return logging.WARNING

    elif (logLevel == LogLevel.ERROR):
        return logging.ERROR

    else:
        raise TypeError("Invalid value given for parameter 'logLevel': it must be a value of the LogLevel enum class")