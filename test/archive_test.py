
import os
import sys

# Add project root to PYTHONPATH so MLU modules can be imported
scriptPath = os.path.dirname(os.path.realpath(__file__))
projectRoot = os.path.abspath(os.path.join(scriptPath ,".."))
sys.path.insert(0, projectRoot)

import unittest
from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.archive
import com.nwrobel.mypycommons.file

class Archive_ModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''
        '''
        super(Archive_ModuleTest, self).setUpClass

        thisDirectory = mypycommons.file.getThisScriptCurrentDirectory()
        testDataDir = mypycommons.file.joinPaths(thisDirectory, 'data')

        self.tempDir = testDataDir = mypycommons.file.joinPaths(thisDirectory, '~temp')
        mypycommons.file.createDirectory(self.tempDir)

        self.archiveInputDirPath = mypycommons.file.joinPaths(testDataDir, 'test-archive-input-dir')
        self.archiveInputFilepath = mypycommons.file.joinPaths(self.archiveInputDirPath, 'test-archive-input-file-1.txt')


    @classmethod
    def tearDownClass(self):  
        super(Archive_ModuleTest, self).tearDownClass      
        mypycommons.file.deletePath(self.tempDir)

    def test_createTarArchive(self):
        '''
        '''
        testArchiveOutFilename = 'test-out-1.tar'
        testArchiveOutFilepath = mypycommons.file.joinPaths(self.tempDir, testArchiveOutFilename)
        mypycommons.archive.createTarArchive(self.archiveInputFilepath, testArchiveOutFilepath)

        self.assertTrue(mypycommons.file.pathExists(testArchiveOutFilepath))

        testArchiveOutFilename = 'test-out-2.tar'
        testArchiveOutFilepath = mypycommons.file.joinPaths(self.tempDir, testArchiveOutFilename)
        mypycommons.archive.createTarArchive(self.archiveInputDirPath, testArchiveOutFilepath)

        self.assertTrue(mypycommons.file.pathExists(testArchiveOutFilepath))
        print("Place breakpoint here and check archives manually")

if __name__ == '__main__':
    unittest.main()
