'''
com.nwrobel.file 

This module contains functionality related to performing file/directory operations, such as reading,  
writing, renaming, deleting, and moving.
'''

import os
import subprocess
from pathlib import Path
import gzip
import shutil
import tarfile
import inspect
import csv
import json

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.system

def isPossibleFilepath(filepath):
    '''
    Checks whether or not the given string is a legal, absolute, valid possible/potential filepath.
    This does not check for the existence of the path.  

    @params
    filepath: the string to check for a possible filepath
    '''
    return os.path.isabs(filepath)

def getThisScriptCurrentDirectory():
    '''
    Returns the current directory that this current script (the one being executed) is located in.
    '''
    callerModuleName = _getCallerModuleName()
    return (os.path.dirname(os.path.realpath(callerModuleName)))

def applyPermissionToPath(filepath, owner, group, mask, applyToPathType='', recursive=False):
    '''
    Applies the given Unix file permissions (owner, group, permission mask) to the given path using
    the chown and chmod commands. 

    @params
    path: the full path to the file or directory
    owner: the system username to apply as the owner
    group: the system groupname to apply as the group
    applyToPathType: optional, "file" or "dir" to apply permission to only files or only directories
    recursive: if true, sets the permissions to a directory recursively

    @notes
    This only works on Linux machines. 
    This requires root (sudo) permissions to work - the python script using this function must
    be run like "sudo python3 script.py".
    '''
    # Set ownership and permissions using by calling the linux chown and chmod commands
    ownerGroup = "{}:{}".format(owner, group)

    if (recursive):    
        if (applyToPathType == 'dir'):
            subprocess.call(['sudo', 'find', path, '-type', 'd', '-exec', 'chown', ownerGroup, '{}', '+'])
            subprocess.call(['sudo', 'find', path, '-type', 'd', '-exec', 'chmod', mask, '{}', '+'])
        
        elif (applyToPathType == 'file'):
            subprocess.call(['sudo', 'find', path, '-type', 'f', '-exec', 'chown', ownerGroup, '{}', '+'])
            subprocess.call(['sudo', 'find', path, '-type', 'f', '-exec', 'chmod', mask, '{}', '+'])

        else:
            subprocess.call(['sudo', 'chown', ownerGroup, '-R', path])
            subprocess.call(['sudo', 'chmod', mask, '-R', path])

    else:
        subprocess.call(['sudo', 'chown', ownerGroup, path])
        subprocess.call(['sudo', 'chmod', mask, path])

def getChildPathsRecursive(rootFilepath, pathType='', useWindowsExtendedPaths=False):
    '''
    Gets the child paths of the root filepath, recursively.

    @params
    rootFilepath: the parent filepath (directory) to search for paths within
    pathType: (optional) "file" or "dir" to return only files or only directories
    useWindowsExtendedPaths: (optional) makes all paths returned use the Windows extended path 
        syntax, to avoid problems with long filepaths 
    '''
    pathObj = Path(rootPath)
    childrenObjs = pathObj.glob('**/*')
    
    fileObjs = [childObj for childObj in childrenObjs if _isFile(childObj)]
    dirObjs = [childObj for childObj in childrenObjs if _isDir(childObj)]

    if (useWindowsExtendedPaths):
        filePaths = [('\\\\?\\' + str(fileObj)) for fileObj in fileObjs]
        dirPaths = [('\\\\?\\' + str(dirObj)) for dirObj in dirObjs]
    else:
        filePaths = [str(fileObj) for fileObj in fileObjs]
        dirPaths = [str(dirObj) for dirObj in dirObjs]

    if (pathType == 'file'):
        return filePaths

    elif (pathType == 'dir'):
        return dirPaths
    
    else:
        return (dirPaths + filePaths)

def getFilesByExtension(rootFilepath, fileExt, useWindowsExtendedPaths=False):
    '''
    Gets the filepaths of all files contained within the given root directory that have the given 
    file extension(s). Searches for files recursively. Either a single file extension or a list of 
    file extensions may be specified. If more than 1 extension is given, files matching any of those
    extensions are returned (searches using OR). Give file extension(s) with the dot.

    All filepaths will use the extended path syntax, to avoid problems with long filepaths, if this parameter 
    is set.

    ex) 
    GetAllFilesByExtension("C:\temp", ".mp3")
    GetAllFilesByExtension("C:\temp", [".mp3", ".flac"])
    '''
    if (not isinstance(fileExt, list)):
        fileExt = [fileExt]
    
    allFiles = getChildPathsRecursive(rootFilepath, pathType='file', useWindowsExtendedPaths=useWindowsExtendedPaths)
    matchingFilepaths = []

    for filepath in allFiles:
        currentFileExt = GetFileExtension(filepath)
        if (currentFileExt in fileExt):
            matchingFilepaths.append(filepath)

    return matchingFilepaths

def createDirectory(folderPath):
    '''
    Creates the directory specified by the given directory path.

    @params
    folderPath: path of the new directory to create
    '''
    folderPathObject = Path(folderPath)
    folderPathObject.mkdir(parents=True)

def moveFilesToDirectory(filepaths, destDir):
    '''
    Moves the given files to the destination directory. 
    Metadata and permissions are preserved.

    @params
    filepaths: list of filepaths to move to the dir
    destDir: path of the target directory to move the files to
    '''
    for filepath in filepaths:
        shutil.move(filepath, destDir) 

def copyFilesToDirectory(filepaths, destDir):
    '''
    Copies the given files to the destination directory. 
    Metadata and permissions are preserved.

    @params
    filepaths: list of filepaths to copy to the dir
    destDir: path of the target directory to copy the file to
    '''
    for filepath in filepaths:
        shutil.copy2(filepath, destDir)

def deletePath(filepath):
    '''
    Deletes a single file or directory

    @params
    filepath: the path of the file or directory to delete
    '''
    pathObj = Path(filepath)

    if (_isFile(pathObj)):
        os.remove(filePath)
    elif (_isDir(pathObj)):
        shutil.rmtree(directoryPath)

def getParentDirectory(filepath, useWindowsExtendedPaths=False):
    '''
    Given a path, returns the parent directory. 

    @params
    path: file or directory path
    useWindowsExtendedPaths: (optional) makes path returned use the Windows extended path 
        syntax, to avoid problems with long filepaths 
    '''
    filePathObject = Path(filepath)

    if (useWindowsExtendedPaths):
        parentDir = '\\\\?\\' + str(filePathObject.parent)
    else:
        parentDir = str(filePathObject.parent)

    return parentDir

def getFilename(filepath):
    '''
    Given a filepath, returns only the filename part, without the parent folders and containing its 
    file extension.
    '''
    filePathObject = Path(filepath)
    return filePathObject.name

def getFileExtension(filepath):
    '''
    Returns the file extension of a file, given its filepath. Specifically, this returns the final 
    ".something" in the given file's name. File extension is returned including the dot.
    Returns an empty string if no file extension exists.
    '''
    filePathObject = Path(filepath)
    return filePathObject.suffix

def getFileBaseName(filepath):
    '''
    Returns the "base" name of the file, given the filepath. The base name is the filename minus the
    file's extension. 

    ex) C:\data\playlist.m3u.tar --> playlist.m3u
    ex) C:\prog\connect.log --> connect
    '''
    filePathObject = Path(filepath)
    return filePathObject.stem

def joinPaths(path1, path2):
    '''
    Given a root absolute filepath and a child relative filepath, returns the effective combination
    of these two paths to make a 3rd filepath.

    ex) joinPaths("C:\prog\temp", "..\test.txt") --> "C:\prog\test.txt" 
    '''
    joined = os.path.join(path1, path2)
    return os.path.abspath(joined)

def fileExists(filePath):
    '''
    Returns bool for whether or not the given filepath represents a valid, existing file. Directories
    will return false.

    Params:
        filePath: the path to test
    '''
    pathObj = Path(filePath)
    return (_isFile(pathObj))

def directoryExists(filePath):
    '''
    Returns bool for whether or not the given filepath represents a valid, existing directory. Files
    will return false.

    Params:
        filePath: the path to test
    '''
    pathObj = Path(filePath)
    return (_isDir(pathObj))

def DecompressSingleGZFile(gzippedFilePath, decompFilePath):
    '''
    Given the filepath of an input .GZ file and the filepath of the output file, this
    decompresses that single .gz file and creates the decompressed output file.

    This only works for .gz archives that contain single files (a single file is compressed), not 
    for multi-file archives.
    '''
    with gzip.open(gzippedFilePath, 'rb') as inputFile:
        with open(decompFilePath, 'wb') as outputFile:
            shutil.copyfileobj(inputFile, outputFile)

def create7zArchive(inputFilePath, archiveOutFilePath):
    '''
    Creates a 7zip archive from the given path(s). 7zip must be installed on the system and 7z 
    must be in the path for this command to work.
    '''
    if (not isinstance(inputFilePath, list)):
        inputFilePath = [inputFilePath]

    if (mypycommons.system.thisMachineIsWindowsOS()):
        sevenZipCommand = 'C:\\Program Files\\7-Zip\\7z.exe'
    else:
        sevenZipCommand = '7z'

    sevenZipArgs = [sevenZipCommand] + ['a', '-t7z', '-mx=9', '-mfb=64', '-md=64m', archiveOutFilePath]
    for inFilePath in inputFilePath:
        sevenZipArgs.append(inFilePath)
        
    subprocess.call(sevenZipArgs)

def clearFileContents(filepath):
    '''
    Removes all the data from the target file by deleting the file and re-creating it as an empty
    file with 0 bytes of data.
    '''
    DeleteFile(filepath)
    open(filepath, 'wb').close()

def writeToFile(filepath, content):
    '''
    Writes the given data/content to the given file.

    Params:
        filePath: path to the output file
        content: data to be written to the file - must be either a string or a list of strings. Lists
            are written to the file with one string list item per line
    '''
    if (isinstance(content, str)):
        content = [content]

    with open(filepath, 'w', encoding='utf-8') as outputFile:
        for item in content:
            outputFile.write("{}\n".format(item))

def readFile(filepath):
    '''
    Reads the data line by line from the given file and returns a list of strings representing each
    line of the file. Newlines in the file will show up as newline characters for each string.
    '''
    with open(filepath, 'r', encoding='utf-8') as infile:
        fileLines = infile.readlines()
        
    return fileLines

def readJsonFile(filepath):
    '''
    Reads the given Json file and returns a dict or a Json array representing the data.
    '''
    with open(filepath) as f:
        data = json.load(f)

    return data

def readCSVFile(csvFilePath):
    csvLines = []
    with open(csvFilePath, mode='r') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for line in csvReader:
            csvLines.append(line)

    return csvLines

def getTextFileLineCount(filepath):
    with open(filepath) as f:
        lineCount = 0
        for line in f:
            lineCount += 1

    return lineCount

def removeFirstNLinesFromTextFile(filepath, numLines):
    with open(filepath) as f:
        originalLines = f.readlines()

    clearFileContents(filepath)

    with open(filepath, 'w') as f:
        linesToKeep = originalLines[numLines:]
        f.writelines(linesToKeep)

# -------------------------------- Private module helper functions ---------------------------------
#
def _isFile(pathObj):
    '''
    Returns bool for whether or not the given Path object represents a valid, existing file.
    '''
    if (pathObj.is_file()):
        return True
    else:
        extendedFilepath = "\\\\?\\" + str(pathObj)
        extendedPathObj = Path(extendedFilepath)

        if (extendedPathObj.is_file()):
            return True
        else:
            return False

def _isDir(pathObj):
    '''
    Returns bool for whether or not the given Path object represents a valid, existing directory.
    '''
    if (pathObj.is_dir()):
        return True
    else:
        extendedFilepath = "\\\\?\\" + str(pathObj)
        extendedPathObj = Path(extendedFilepath)

        if (extendedPathObj.is_dir()):
            return True
        else:
            return False

def _getCallerModuleName():
    '''
    Returns the name of the caller (of the caller) module. Used by the getThisScriptCurrentDirectory
    function.
    '''
    frm = inspect.stack()[2]
    module = inspect.getmodule(frm[0])
    return module.__file__


