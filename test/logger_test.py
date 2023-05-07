import os
import sys

# Add project root to PYTHONPATH so MLU modules can be imported
scriptPath = os.path.dirname(os.path.realpath(__file__))
projectRoot = os.path.abspath(os.path.join(scriptPath ,".."))
sys.path.insert(0, projectRoot)

import unittest
from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.logger
import com.nwrobel.mypycommons.file

class Logger_ModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        super(Logger_ModuleTest, self).setUpClass

        thisDirectory = mypycommons.file.getThisScriptCurrentDirectory()
        self.tempDir = mypycommons.file.joinPaths(thisDirectory, '~temp')

        if (not mypycommons.file.pathExists(self.tempDir)):
            mypycommons.file.createDirectory(self.tempDir)

    @classmethod
    def tearDownClass(self):  
        super(Logger_ModuleTest, self).tearDownClass      
        mypycommons.file.deletePath(self.tempDir)

    def test_logger(self):
        loggerWrapper = mypycommons.logger.CommonLogger("mainlogger", logDir=self.tempDir, logFilename=__name__)
        loggerWrapper.setConsoleOutputLogLevel(mypycommons.logger.LogLevel.DEBUG)
        loggerWrapper.setFileOutputLogLevel(mypycommons.logger.LogLevel.DEBUG)
        logger = loggerWrapper.getLogger()

        logger.info("test logging message")
        logger.error("test logging error")

        self.assertTrue(mypycommons.file.pathExists(loggerWrapper.logFilepath))

if __name__ == '__main__':
    unittest.main()
