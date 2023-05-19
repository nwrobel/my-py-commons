import os
import sys
import unittest

# Add project root to PYTHONPATH so MLU modules can be imported
scriptPath = os.path.dirname(os.path.realpath(__file__))
projectRoot = os.path.abspath(os.path.join(scriptPath ,".."))
sys.path.insert(0, projectRoot)

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.archive
import com.nwrobel.mypycommons.file

import common

class File_ModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #super(File_ModuleTest, self).setUpClass
        self.helper = common.TestHelper()

    def setUp(self):
        '''
        '''
        testFileName = 'test-file.txt'
        testDirName = 'test-dir'

        # Copy files from test data dir to test temp dir
        self.helper.copyDataToTestTempDir(testDirName)

        self.testDirectory = mypycommons.file.joinPaths(self.helper.testTempDir, testDirName)
        self.testFilePath = mypycommons.file.joinPaths(self.testDirectory, testFileName)

    def tearDown(self):  
        super(File_ModuleTest, self).tearDownClass      
        self.helper.cleanup()

    def test_renamePath_File(self):
        '''
        '''
        testFileExt = mypycommons.file.getFileExtension(self.testFilePath)
        testFileNewName = "new-name{}".format(testFileExt)
        mypycommons.file.renamePath(self.testFilePath, testFileNewName)
        
        newFilepath = mypycommons.file.joinPaths(self.testDirectory, testFileNewName)
        self.assertTrue(mypycommons.file.pathExists(newFilepath))
    
    def test_renamePath_Dir(self):
        '''
        '''
        newName = "new-dir-name"
        mypycommons.file.renamePath(self.testDirectory, newName)
        
        newPath = mypycommons.file.joinPaths(self.helper.testTempDir, newName)
        self.assertTrue(mypycommons.file.pathExists(newPath))

    def test_removeTrailingSlashFromPath(self):
        '''
        '''
        testPathsInput = [
            '/a/sample/linux/path/', 
            '/a/sample/linux/path',
            '/data/',
            '/data',
            '/',
            'D:\\a\\sample\\windows\\path\\',
            'D:\\a\\sample\\windows\\path',
            'D:\\', 
            'Z:\\\\network\\\\file\\',
            'Z:\\\\network\\\\file'
        ]
        testPathsExpectedOutput = [
            '/a/sample/linux/path', 
            '/a/sample/linux/path',
            '/data',
            '/data',
            '/',
            'D:\\a\\sample\\windows\\path',
            'D:\\a\\sample\\windows\\path',
            'D:', 
            'Z:\\\\network\\\\file',
            'Z:\\\\network\\\\file'
        ]

        for i in range(0, len(testPathsInput)):
            result = mypycommons.file.removeTrailingSlashFromPath(testPathsInput[i])
            self.assertEqual(testPathsExpectedOutput[i], result)

    def test_getParentDirectory(self):
        '''
        '''
        testPath = 'C:\\local\\data\\new\\file.txt'
        parentPath = mypycommons.file.getParentDirectoryPath(testPath)

        self.assertEqual(parentPath, 'C:\\local\\data\\new')

    def test_getChildPathsRecursive(self):
        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory)
        self.assertEqual(len(result), 13)
        
        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, pathType='file')
        self.assertEqual(len(result), 11)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, pathType='dir')
        self.assertEqual(len(result), 2)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, containsStr='txt')
        self.assertEqual(len(result), 6)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, containsStr='test')
        self.assertEqual(len(result), 8)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, containsStr='bar')
        self.assertEqual(len(result), 2)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, pathType='dir', containsStr='bar')
        self.assertEqual(len(result), 1)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, containsStr='foo')
        self.assertEqual(len(result), 6)

        result = mypycommons.file.getChildPathsRecursive(rootDir=self.testDirectory, pathType='file', containsStr='test')
        self.assertEqual(len(result), 8)

    def test_writeJsonFile(self):
        '''
        '''
        testOutputPath = mypycommons.file.joinPaths(self.helper.testTempDir, 'output.json')
        testContents = [{ 'a': 'b', 'c': 'd' }, { 'a': 'b', 'c': 'd' }]

        mypycommons.file.writeJsonFile(testOutputPath, testContents)
        self.assertTrue(mypycommons.file.pathExists(testOutputPath))

        actualJsonFileData = mypycommons.file.readJsonFile(testOutputPath)
        self.assertEqual(testContents, actualJsonFileData)

if __name__ == '__main__':
    unittest.main()
