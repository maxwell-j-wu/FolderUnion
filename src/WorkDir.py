from os import listdir
from os.path import isfile, join, getsize
import numpy as np 

class WorkDir:
    def __init__(self, path):
        self.path = path
        self.filePaths, self.fileSizes, self.filesInfo = self.getFilesInfo()

    def getFilePaths(self):
        fileNames = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        filePaths = np.array([])

        for fileName in fileNames:
            filePaths = np.append(filePaths,join(self.path, fileName))
        return filePaths
    
    def getFileSizes(self):
        filePaths = self.getFilePaths()
        fileSizes = np.array([])
        for filePath in filePaths:
            fileSizes = np.append(fileSizes,getsize(filePath))
        return filePaths, fileSizes
    
    def getFilesInfo(self):
        # Reorganize files by file size
        filePaths, fileSizes = self.getFileSizes()
        filesInfo  = [dict() for x in range(len(filePaths))]
        a = {}

        indices = np.argsort(fileSizes)
        fileSizes = fileSizes[indices]
        filePaths = filePaths[indices]
        
        for i in range(len(filePaths)):
            filesInfo[i]['fileSize'] = fileSizes[i]
            filesInfo[i]['filePath'] = filePaths[i]
        return filePaths, fileSizes, filesInfo