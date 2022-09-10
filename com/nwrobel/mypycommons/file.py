'''
com.nwrobel.file 

This module contains functionality related to performing file/directory operations, such as reading,  
writing, renaming, deleting, and moving.
'''

import os
from pathlib import Path
import shutil
import inspect
import csv
import json
import subprocess

def getThisScriptCurrentDirectory():
    '''
    Returns the current directory that this current script (the one being executed) is located in.
    '''
    callerModuleName = _getCallerModuleName()
    return (os.path.dirname(os.path.realpath(callerModuleName)))

def isFile(path):
    '''
    Checks if the given path represents a valid, existing file.

    @params
    path: (str) the path to check
    '''
    pathObj = Path(path)
    return _isFile(pathObj)

def isDirectory(path):
    '''
    Checks if the given path represents a valid, existing directory.

    @params
    path: (str) the path  to check
    '''
    pathObj = Path(path)
    return _isDir(pathObj)

def pathExists(path):
    '''
    Returns bool for whether or not the given path represents a valid, existing path (file or directory). 
    
    @params
    path: (str) the path to check
    '''
    pathObj = Path(path)
    return (_isFile(pathObj) or _isDir(pathObj))

def isPossiblePath(path):
    '''
    Checks whether or not the given string is a legal, absolute, valid possible/potential path to
    a file or directory.
    This does not check for the existence of the path.  

    @params
    path: (str) the path to check    
    '''
    return os.path.isabs(path)

def joinPaths(path1, path2):
    '''
    Given a root absolute filepath and a child relative filepath, returns the effective combination
    of these two paths to make a 3rd filepath.

    @params
    path1: (str) the first part of the path, an absolute path
    path2: (str) the second part of the path, a relative/child path

    @example
    joinPaths("C:\prog\temp", "..\test.txt") --> "C:\prog\test.txt" 
    '''
    joined = os.path.join(path1, path2)
    return os.path.abspath(joined)

def getChildPathsRecursive(rootDirPath, pathType='', useWindowsExtendedPaths=False):
    '''
    Gets the child paths of the root filepath, recursively.

    @params
    rootDirPath: the parent directory to search for paths within
    pathType: (optional) "file" or "dir" to return only files or only directories
    useWindowsExtendedPaths: (optional) makes all paths returned use the Windows extended path 
        syntax, to avoid problems with long filepaths 
    '''
    pathObj = Path(rootDirPath)
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

def getFilesByExtension(rootDirPath, fileExt, useWindowsExtendedPaths=False):
    '''
    Gets the filepaths of all files contained within the given root directory that have the given 
    file extension(s). Searches for files recursively. Either a single file extension or a list of 
    file extensions may be specified. If more than 1 extension is given, files matching any of those
    extensions are returned (searches using OR, of course). Give file extension(s) with the dot.

    @params
    rootDirPath: the parent directory to search for files within
    fileExt: (str or list) file extension(s) to search for files by
    useWindowsExtendedPaths: (optional) makes all paths returned use the Windows extended path 
        syntax, to avoid problems with long filepaths 

    @example
    GetAllFilesByExtension("C:\temp", ".mp3")
    GetAllFilesByExtension("C:\temp", [".mp3", ".flac"])
    '''
    if (not isinstance(fileExt, list)):
        fileExt = [fileExt]
    
    allFiles = getChildPathsRecursive(rootDirPath, pathType='file', useWindowsExtendedPaths=useWindowsExtendedPaths)
    matchingFilepaths = []

    for filepath in allFiles:
        currentFileExt = getFileExtension(filepath)
        if (currentFileExt in fileExt):
            matchingFilepaths.append(filepath)

    return matchingFilepaths

def createDirectory(path):
    '''
    Creates a new directory.

    @params
    path: (str) path of the new directory to create
    '''
    folderPathObject = Path(path)
    folderPathObject.mkdir(parents=True)

def moveToDirectory(path, destDir):
    '''
    Moves the given path (file or folder) to the destination directory. 
    Metadata and permissions are preserved.

    @params
    path: (str) the path (file or folder) to move to the dir
    destDir: path of the target directory to move to
    '''
    shutil.move(path, destDir) 

def copyToDirectory(path, destDir):
    '''
    Copies the given path (file or folder) to the destination directory. 
    Metadata and permissions are preserved.

    @params
    path: (str) the path (file or folder) to copy to the dir
    destDir: (str) path of the target directory to copy to
    '''
    if (isFile(path)):
        shutil.copy2(path, destDir)
    elif (isDirectory(path)):
        sourceDirName = getFilename(path)
        newDirFilepath = joinPaths(destDir, sourceDirName)
        shutil.copytree(path, newDirFilepath)
    else:
        raise Exception("The given path is invalid")

def deletePath(path):
    '''
    Deletes a single file or directory

    @params
    path: (str) the path (file or folder) to delete
    '''
    pathObj = Path(path)

    if (_isFile(pathObj)):
        os.remove(path)
    elif (_isDir(pathObj)):
        shutil.rmtree(path)

def renamePath(path, newName):
    '''
    Renames a single file or directory. Note: If given a file, this function will rename the entire
    name (base name and file extension) to the given name. So, if you want the file to have an 
    extension, you need to provide it in the new name given.

    @params
    path: (str) the path (file or folder) to rename
    newName: (str) the new name to give to the file or folder
    '''
    pathObj = Path(path)
    pathObj.rename(Path(pathObj.parent, newName))


def getParentDirectory(path, useWindowsExtendedPaths=False):
    '''
    Given a path, returns the parent directory. 

    @params
    path: (str) the path (file or folder) to find the parent of
    useWindowsExtendedPaths: (optional) makes path returned use the Windows extended path 
        syntax, to avoid problems with long filepaths 
    '''
    filePathObject = Path(path)

    if (useWindowsExtendedPaths):
        parentDir = '\\\\?\\' + str(filePathObject.parent)
    else:
        parentDir = str(filePathObject.parent)

    return parentDir

def getFilename(filepath):
    '''
    Given a filepath, returns only the filename part, without the parent folders and containing its 
    file extension.

    @params:
    filepath: path to the file 
    '''
    filePathObject = Path(filepath)
    return filePathObject.name

def getFileExtension(filepath):
    '''
    Returns the file extension of a file, given its filepath. Specifically, this returns the final 
    ".something" in the given file's name. File extension is returned including the dot.
    Returns an empty string if no file extension exists.

    @params:
    filepath: path to the file 
    '''
    filePathObject = Path(filepath)
    return filePathObject.suffix

def getFileBaseName(filepath):
    '''
    Returns the "base" name of the file, given the filepath. The base name is the filename minus the
    file's extension. 

    @params:
    filepath: path to the file 

    @example
    C:\data\playlist.m3u.tar --> playlist.m3u
    C:\prog\connect.log --> connect
    '''
    filePathObject = Path(filepath)
    return filePathObject.stem

def applyPermissionToPath(path, owner, group, mask, recursive=False):
    '''
    Applies the given Unix file permissions (owner, group, permission mask) to the given path using
    the chown and chmod commands. 

    @params
    path: the full path to the file or directory
    owner: the system username to apply as the owner
    group: the system groupname to apply as the group
    mask: the octal mask to apply to the path
    recursive: if true, sets the permissions to a directory recursively

    @notes
    This only works on Linux machines. 
    This requires root (sudo) permissions to work - the python script using this function must
    be run like "sudo python3 script.py".
    '''
    # Set ownership and permissions using by calling the linux chown and chmod commands
    ownerGroup = "{}:{}".format(owner, group)

    if (recursive):    
        subprocess.call(['sudo', 'chown', ownerGroup, '-R', path])
        subprocess.call(['sudo', 'chmod', mask, '-R', path])

    else:
        subprocess.call(['sudo', 'chown', ownerGroup, path])
        subprocess.call(['sudo', 'chmod', mask, path])

def clearFileContents(filepath):
    '''
    Removes all the data from the target file by deleting the file and re-creating it as an empty
    file with 0 bytes of data.

    @params
    filepath: (str) the path of the file to clear
    '''
    deletePath(filepath)
    open(filepath, 'wb').close()

def writeToFile(filepath, content, append=False):
    '''
    Writes the given data/content to the given file.

    @params:
    filepath: path to the output file
    content: data to be written to the file - must be either a string or a list of strings. Lists
        are written to the file with one string list item per line
    append: add the content to the end of the existing file, instead of replacing file contents on
        write if data exists
    '''
    if (isinstance(content, str)):
        content = [content]

    writeMode = "w"
    if (append):
        writeMode = "a"

    with open(filepath, writeMode, encoding='utf-8') as outputFile:
        for item in content:
            outputFile.write("{}\n".format(item))

def readFile(filepath, encoding='utf-8'):
    '''
    Reads the data line by line from the given file and returns a list of strings representing each
    line of the file. Newlines in the file will show up as newline characters in each string in the list.

    @params:
    filepath: path to the file  
    encoding: (optional) the encoding to use to read the text of the file as, default is utf-8 
    '''
    with open(filepath, 'r', encoding=encoding) as infile:
        fileLines = infile.readlines()
        
    return fileLines

def readJsonFile(filepath):
    '''
    Reads the given Json file and returns a dict or a Json array representing the data.

    @params:
    filepath: path to the file  
    '''
    with open(filepath) as f:
        data = json.load(f)

    return data

def readCSVFile(filepath):
    '''
    Reads the given CSV file and returns a list of arrays, each of which represent a row in the
    CSV file with the line split by the comma delimiter to get the data in each column.

    @params:
    filepath: path to the file  
    '''
    csvLines = []
    with open(filepath, mode='r') as csvFile:
        iterCleanLines = _filterCSVLinesForIterator(csvFile)
        csvReader = csv.DictReader(iterCleanLines)

        for line in csvReader:
            csvLines.append(line)

    return csvLines

def getFileLineCount(filepath):
    '''
    Returns the line count of the given file. Useful for text (non-binary) files.

    @params:
    filepath: path to the file 
    '''
    with open(filepath) as f:
        lineCount = 0
        for line in f:
            lineCount += 1

    return lineCount

def removeFirstNLinesFromTextFile(filepath, numLines):
    '''
    Edits the file to remove the first N lines of text data. 

    @params:
    filepath: path to the file 
    numLines: number of lines "N" to remove
    '''
    with open(filepath) as f:
        originalLines = f.readlines()

    clearFileContents(filepath)

    with open(filepath, 'w') as f:
        linesToKeep = originalLines[numLines:]
        f.writelines(linesToKeep)

def getFileSizeBytes(filepath):
    '''
    Returns the size of the given file in bytes.

    @params:
    filepath: path to the file
    '''
    return Path(filepath).stat().st_size

def getFileDateModifiedTimestamp(filepath):
    '''
    Returns the date modified timestamp of the given file.

    @params:
    filepath: path to the file
    '''
    return Path(filepath).stat().st_mtime

def removeTrailingSlashFromPath(path):
    '''
    Returns the given path without a '/' or '\' at the end. If the path does not end with these,
    the path is simply returned, making this function safe to call on all paths in order to normalize
    them to an expected format (without trailing slash).

    @params:
    path: a path string
    '''
    if (path[-1] == '/' or path[-1] == '\\'):
        path = path[:-1] # remove last char. from string
        
    return path

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

def _CSVLineIsComment(line):
    return line.startswith('#')

def _CSVLineIsEmpty(line):
    line = line.strip()
    if (not line or line.isspace()):
        return True
    else:
        return False

def _filterCSVLinesForIterator(inFileIterator):
    for line in inFileIterator:
        if (not _CSVLineIsComment(line) and not _CSVLineIsEmpty(line)):
            yield line

