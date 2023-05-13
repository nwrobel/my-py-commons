from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.file

class TestHelper:
    def __init__(self):
        self._thisDir = mypycommons.file.getThisScriptCurrentDirectory()
        self.testDataDir = self._getTestDataDir()
        self.testTempDir = self._getTestTempDir()

        self.cleanup()
        mypycommons.file.createDirectory(self.testTempDir)

    def _getTestDataDir(self):
        testDataDir = mypycommons.file.joinPaths(self._thisDir, 'data')
        return testDataDir

    def _getTestTempDir(self):
        thisDirectory = mypycommons.file.getThisScriptCurrentDirectory()
        tempDir = mypycommons.file.joinPaths(thisDirectory, '~temp')

        if (mypycommons.file.pathExists(tempDir)):
            mypycommons.file.deletePath(tempDir)

        mypycommons.file.createDirectory(tempDir) 
        return tempDir

    def cleanup(self):
        if (mypycommons.file.pathExists(self.testTempDir)):
            mypycommons.file.deletePath(self.testTempDir)

    def copyDataToTestTempDir(self, partialPath):
        sourcePath = mypycommons.file.joinPaths(self.testDataDir, partialPath)
        mypycommons.file.copyToDirectory(sourcePath, self.testTempDir)