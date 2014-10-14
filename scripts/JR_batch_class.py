import os
import sys
import shutil
from JR_system_class import System
from JR_rename_class import Rename
from JR_convert_class import Convert
from JR_ui_class import UI
class batchConvert(Convert, UI, Rename, System):
    def __init__ (self):
        Convert.__init__(self)
        ######################
        self.sourceDirectory = ""
        self.destDirectory = ""
        self.screenshotDirectory = []
        self.movList = []
        self.newMovDir = []
        self.finalSet = []
    def findScreenshots(self, directory = '', specific_name = ''):
        self.screenshotDirectory= self.getFileList(directory, specific_name)
    	X = set(self.screenshotDirectory)
        return sorted(X)
    def findMovies (self, dirPath,uniq=True,sorted=True):
        #self.movie_ext = ('.mov', '.R3D', '.MXF', '.mp4', '.MP4' , '.avi')
        movList = []
        for dirpath,dirnames,filenames in os.walk(dirPath):
            for file in filenames:
                if file.endswith(self.movie_ext): #self.movie_ext is located in the system section
                #if file.endswith('.mov') or file.endswith('.R3D') or file.endswith('.MXF') or file.endswith('.mp4') or file.endswith('.avi'):
                	movList.append(dirpath + '\\' + file)
        return movList
        #        	self.newMovDir.append(self.sourceDirectory + '\\' + file)
    def findH264 (self, dirPath, destPath, uniq=True,sorted=True):
        X = []
        Y = []
        for dirpath,dirnames,filenames in os.walk(dirPath):
            for file in filenames:
                if file.endswith('.mp4'):
                	if 'H264' in file:
                		currentFile = dirpath + '\\' + file
                        newFile = destPath + '\\' + file
                        X.append(currentFile)
                        Y.append(newFile)
                else:
                    pass
        return X, Y
    def batch_convert2H264(self, directory):
        parent_directory = directory[:[i for i, letter in enumerate(directory) if letter == '/' or letter == '\\'][-1]]
        movies = self.findMovies(directory)
    	for i in movies:
            processed = self.processInput(i)
            H264version = processed[1]+'_H264.mp4'# i[:-4]+'_H264.mp4'
            if os.path.exists(H264version):
    			pass
            else:
                self.mov2H264(i)
            original = directory+'/'+processed[3]+'_H264.mp4'
            move_to =  parent_directory+'/'+processed[3]+'_H264.mp4'
            shutil.move(original, move_to)
    def batch_SS2MOV(self, directory):
        output_format = self.BRC
        parent_directory = directory[:[i for i, letter in enumerate(directory) if letter == '/' or letter == '\\'][-1]]
        self.finalSet.append(self.findScreenshots(directory))
        for i in self.finalSet[0]:
            firstImage = ''
            for dirpath,dirnames,filename in os.walk(i):
                for file in filename:
                    #print file
                    #if 'screenshot' in file.lower():
                    #    firstImage = file
                    #    break
                    if file.endswith(self.image_ext):
                        firstImage = file
                        break
                item = i+'\\'+firstImage
                self.img2mov(input_data = item, format = output_format )
                #### MOVE VIDEOS AFTER THEY ARE CONVERTED TO THE PARENT FOLDER FOR EASY ACCESS
                if self.BRC == 'H264':
                    mov_ext = '.mp4'
                elif self.BRC == 'ProRes':
                    mov_ext = '.mov'
                final_movie = i+'/'+self.processFinalName(item)+mov_ext
                move_to = parent_directory+'/'+self.processFinalName(item)+mov_ext
                shutil.move(final_movie, move_to )
    def batch_moveH264(self, sourceDirectory):
        destinationDirectory = self.setDirectory('Select Folder to Move Content To:')
    	X = self.findH264(sourceDirectory, destinationDirectory)
        for i in range(len(X[1])):
            parentPath = X[1][i] [: [x for x, letter in enumerate(X[1][i]) if letter == '\\'][-1] ]
            if not os.path.exists(parentPath):
                os.makedirs(parentPath)
        #RELEASE THIS TO ENABLE COPYING OVER
        #shutil.copy(X[0][i], X[1][i])
####
if __name__ == '__main__':
    batch = batchConvert()
    #print os.getcwd()
    ############################
    #a = 'C:/Users/James/Desktop/test/A003_C018_1004UY.RDC'
    #batch.batch_convert2H264(a)
    if sys.argv[2] == 'SS2MOV':
        batch.CreateButtons(input_data={'ProRes':'self.returnItem("ProRes")', 'H264':'self.returnItem("H264")'} )
        if batch.BRC != '':
            batch.batch_SS2MOV(sys.argv[1])
    elif sys.argv[2] == 'MOV2H264':
        batch.batch_convert2H264(sys.argv[1])
    else:
        pass