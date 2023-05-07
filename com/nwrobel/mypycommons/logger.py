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

class CommonLogger:
    def __init__(self, loggerName: str, logDir: str, logFilename: str = ''):
        self.loggerName = loggerName
        self.logDir = logDir
        self.logFilename = logFilename
        self.logFilepath = ''

        if (not mypycommons.file.pathExists(self.logDir)):
            raise ValueError("Given logDir path does not exist")

        self._loggerObj = logging.getLogger(self.loggerName)
        self._configureWithBasicSettings()

    def getLogger(self):
        '''
        Returns a logger instance by name. Does the same as "logging.getLogger(loggerName)"
        '''
        return self._loggerObj

    def setConsoleOutputLogLevel(self, logLevel: LogLevel):
        '''
        Modifies the configuration of the logger by setting the minimum level of importance (log
        level) that log messages need to have in order to be logged to the console.
        '''
        level = self._getLoggerLevel(logLevel)

        for handler in self._loggerObj.handlers:
            if (handler.__class__.__name__ == 'StreamHandler'):
                handler.setLevel(level)

    def setFileOutputLogLevel(self, logLevel: LogLevel):
        '''
        Modifies the configuration of the logger by setting the minimum level of importance (log
        level) that log messages need to have in order to be logged to the log file.
        '''
        level = self._getLoggerLevel(logLevel)

        for handler in self._loggerObj.handlers:
            if (handler.__class__.__name__ == 'FileHandler'):
                handler.setLevel(level)

    def _configureWithBasicSettings(self):
        '''
        Configures the logger instance.
        Logger will send all log statements to the console and to a log file in the log directory.

        Configuration applied: 
        - the logger will allow all messages to be passed to the handlers (info or higher)
        - the logger has two handlers, which define how the messages should be output, which ones to output, etc:
            - a file handler, which writes messages to a log file
            - a stream (console output) handler, which outputs messages to the console/stdout
        '''
        # allow all messages of all levels to be passed to the handlers: the handlers will have their
        # own levels set, where they can individually decide which messages to print for a more granular
        # logging control
        self._loggerObj.setLevel(logging.INFO) 

        # If no log filename was given,
        # get the name of the module/file that called this function so we can use it to be the log file name
        if (not self.logFilename):
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            callerModuleFilename = mypycommons.file.getFilename(module.__file__)

            self.logFilename = "{}.log".format(callerModuleFilename)

        # create a file handler which logs all messages by default by saving them to a log file
        self.logFilepath = mypycommons.file.joinPaths(self.logDir, self.logFilename)
        fh = logging.FileHandler(self.logFilepath, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # create console output handler which logs all messages 
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - [%(filename)s,  %(funcName)s()] - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self._loggerObj.addHandler(fh)
        self._loggerObj.addHandler(ch)

    def _getLoggerLevel(self, logLevel: LogLevel):
        '''
        Get the actual log level from the logging class, given the LogLevel type param
        '''
        if (logLevel == LogLevel.DEBUG):
            return logging.DEBUG

        elif (logLevel == LogLevel.INFO):
            return logging.INFO 

        elif (logLevel == LogLevel.WARNING):
            return logging.WARNING

        elif (logLevel == LogLevel.ERROR):
            return logging.ERROR

        else:
            raise TypeError("Invalid value given for parameter 'logLevel': it must be a value of the com.nwrobel.mypycommons.logger2.LogLevel enum class")