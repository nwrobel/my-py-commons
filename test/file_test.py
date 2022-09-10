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

class File_ModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''
        '''
        super(File_ModuleTest, self).setUpClass

        thisDirectory = mypycommons.file.getThisScriptCurrentDirectory()
        testDataDir = mypycommons.file.joinPaths(thisDirectory, 'data')

        self.tempDir = mypycommons.file.joinPaths(thisDirectory, '~temp')
        mypycommons.file.createDirectory(self.tempDir)

        # Copy test file and test dir from test data dir to temp dir
        testFileName = 'test-file.txt'
        testDirName = 'test-dir'

        testDirFilepath = mypycommons.file.joinPaths(testDataDir, testDirName)
        mypycommons.file.copyToDirectory(testDirFilepath, self.tempDir)

        self.testDirFilepath = mypycommons.file.joinPaths(self.tempDir, testDirName)
        self.testFileFilepath = mypycommons.file.joinPaths(self.testDirFilepath, testFileName)

    @classmethod
    def tearDownClass(self):  
        super(File_ModuleTest, self).tearDownClass      
        mypycommons.file.deletePath(self.tempDir)

    def test_renamePath_File(self):
        '''
        '''
        testFileExt = mypycommons.file.getFileExtension(self.testFileFilepath)
        testFileNewName = "new-name{}".format(testFileExt)
        mypycommons.file.renamePath(self.testFileFilepath, testFileNewName)
        
        newTestFileFilepath = mypycommons.file.joinPaths(self.tempDir, testFileNewName)
        self.assertTrue(mypycommons.file.pathExists(newTestFileFilepath))
    
    def test_renamePath_Dir(self):
        '''
        '''
        testDirNewName = "new-dir-name"
        mypycommons.file.renamePath(self.testDirFilepath, testDirNewName)
        
        newTestDirFilepath = mypycommons.file.joinPaths(self.tempDir, testDirNewName)
        self.assertTrue(mypycommons.file.pathExists(newTestDirFilepath))

    def test_removeTrailingSlashFromPath(self):
        '''
        '''
        testPathsNoTrailingSlash = ['/a/sample/linux/path', 'D:\\a\\sample\\windows\\path']
        testPathsTrailingSlash = ['/a/sample/linux/path/', 'D:\\a\\sample\\windows\\path\\']

        for i in range(0, 2):
            newPath1 = mypycommons.file.removeTrailingSlashFromPath(testPathsNoTrailingSlash[i])
            newPath2 = mypycommons.file.removeTrailingSlashFromPath(testPathsTrailingSlash[i])

            self.assertEqual(newPath1, newPath2)
            self.assertTrue(newPath1[-1] != '/' and newPath1[-1] != '\\')
            self.assertTrue(newPath2[-1] != '/' and newPath2[-1] != '\\')

    def test_getParentDirectory(self):
        '''
        '''
        testPath = 'C:\\local\\data\\new\\file.txt'
        parentPath = mypycommons.file.getParentDirectoryPath(testPath)

        self.assertEqual(parentPath, 'C:\\local\\data\\new')

    def test_writeJsonFile(self):
        '''
        '''
        testOutputPath = mypycommons.file.joinPaths(self.tempDir, 'output.json')
        testContents = [{ 'a': 'b', 'c': 'd' }, { 'a': 'b', 'c': 'd' }]

        mypycommons.file.writeJsonFile(testOutputPath, testContents)
        self.assertTrue(mypycommons.file.pathExists(testOutputPath))

        actualJsonFileData = mypycommons.file.readJsonFile(testOutputPath)
        self.assertEqual(testContents, actualJsonFileData)
