import sys
import os, shutil
import numpy as np
import filecmp

current_directory = os.getcwd()
print(current_directory)
sys.path.append(os.path.join(current_directory, 'src'))

import WorkDir as wd

dir1 = wd.WorkDir(r'C:\Users\maxwu\Documents\Python Projects\FolderUnion\Test\Fold1')
dir2 = wd.WorkDir(r'C:\Users\maxwu\Documents\Python Projects\FolderUnion\Test\Fold2')
outDir = os.path.join(current_directory, 'Test', 'Fold3')

## Get the indices of all files to remove
dir1IndicesToRemove = [] # Cumulative list of indices to remove from dir1
dir2IndicesToRemove = [] # Cumulative list of indices to remove from dir2

# Loop over all files in dir1
for i in range(len(dir1.fileSizes)):
    if i not in dir1IndicesToRemove: # Only check the current file if it hasn't already been marked for removal
        # Get the indices of all files with the same size as the current file
        sameSizeDir1Indices = np.where(dir1.fileSizes == dir1.fileSizes[i])[0]
        sameSizeDir2Indices = np.where(dir2.fileSizes == dir1.fileSizes[i])[0]

        # Only compare against files that haven't already been checked (and are not the current file)
        sameSizeDir1Indices = sameSizeDir1Indices[sameSizeDir1Indices > i]

        # Loop over all unchecked files with the same size as the current file
        for j in sameSizeDir1Indices:
            if filecmp.cmp(dir1.filePaths[i], dir1.filePaths[j], shallow=False):
                dir1IndicesToRemove.append(j)
        for j in sameSizeDir2Indices:
            if filecmp.cmp(dir1.filePaths[i], dir2.filePaths[j], shallow=False):
                dir2IndicesToRemove.append(j)

# Loop over all files in dir2
for i in range(len(dir2.fileSizes)):
    if i not in dir2IndicesToRemove: # Only check the current file if it hasn't already been marked for removal
        # Get the indices of all files with the same size as the current file. No need to check files in dir1 again
        sameSizeDir2Indices = np.where(dir2.fileSizes == dir2.fileSizes[i])[0]

        # Only compare against files that haven't already been checked (and are not the current file)
        sameSizeDir2Indices = sameSizeDir2Indices[sameSizeDir2Indices > i]

        # Loop over all unchecked files with the same size as the current file
        for j in sameSizeDir2Indices:
            if filecmp.cmp(dir2.filePaths[i], dir2.filePaths[j], shallow=False):
                dir2IndicesToRemove.append(j)        

## Copy files to the output directory
if os.path.isdir(outDir):
    shutil.rmtree(outDir)
os.mkdir(outDir)
# First files from dir1
for i in range(len(dir1.filePaths)):
    if i not in dir1IndicesToRemove:
        filePath = dir1.filePaths[i]
        fileName = os.path.basename(filePath)
        outFilePath = os.path.join(outDir, fileName)
        print(f'Copying {filePath} to {outFilePath}')
        os.system(f'copy "{filePath}" "{outFilePath}"')

outDirFileNames = [f for f in os.listdir(outDir) if os.path.isfile(os.path.join(outDir, f))]
# Then files from dir2
for i in range(len(dir2.filePaths)):
    if i not in dir2IndicesToRemove:
        filePath = dir2.filePaths[i]
        fileName = os.path.basename(filePath)
        if fileName in outDirFileNames: # Skip files that already exist in the output directory
            fileName = fileName.split('.')[0] + '_alt.' + fileName.split('.')[1]
        outFilePath = os.path.join(outDir, fileName)
        print(f'Copying {filePath} to {outFilePath}')
        os.system(f'copy "{filePath}" "{outFilePath}"')
print(dir1.filesInfo[0]['filePath'])