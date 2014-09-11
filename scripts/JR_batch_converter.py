import os
from JR_convert_class import Convert
import shutil
from JR_ui_class import UI
#import Tkinter, tkFileDialog
#from JR_system_class import System
class batchConvert(Convert, UI):
    def __init__ (self):
        Convert.__init__(self)
        #UI.__init__(self)
        #System.__init__(self)
        self.sourceDirectory = ""
        self.destDirectory = ""
        self.screenshotDirectory = []
        self.movList = []
        self.newMovDir = []
        self.finalSet = []
    #def setDirectory(self):
    #    root = Tkinter.Tk()
    #    root.withdraw()
    #    self.destDirectory = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Select destination ...')
    #def getFileList (self, dirPath,uniq=True,sorted=True):
    #    for dirpath,dirnames,filenames in os.walk(dirPath):
    #        for file in filenames:
    #            if 'Screenshot' in file:
    #            	self.screenshotDirectory.append(dirpath)
    def findScreenshots(self, directory):
        name_to_search = 'Screenshot'
        self.screenshotDirectory= self.getFileList(directory, name_to_search)
    	X = set(self.screenshotDirectory)
        return sorted(X)
    def findMovies (self, dirPath,uniq=True,sorted=True):
        for dirpath,dirnames,filenames in os.walk(dirPath):
            for file in filenames:
                if file.endswith('.mov') or file.endswith('.R3D') or file.endswith('.MXF'):
                	self.movList.append(dirpath + '\\' + file)
                	self.newMovDir.append(self.sourceDirectory + '\\' + file)
    def findH264 (self, dirPath, destPath, uniq=True,sorted=True):
        #self.destDirectory = self.setDirectory()
        #print self.destDirectory
        X = []
        Y = []
        for dirpath,dirnames,filenames in os.walk(dirPath):
            for file in filenames:
                if file.endswith('.mp4'):
                	if 'H264' in file:
                		####
                		currentFile = dirpath + '\\' + file
                        newFile = destPath + '\\' + file
                		#newFile = self.destDirectory + dirpath[len(self.sourceDirectory):] + '\\' + file
                		####
                        X.append(currentFile)
                        Y.append(newFile)
                else:
                    pass
        return X, Y
    def batch_convert2H264(self):
    	self.findMovies(self.sourceDirectory)
    	for i in self.movList:
    		H264version = i[:-4]+'_H264.mp4'
    		if os.path.exists(H264version):
    			pass
    		else:
    			self.mov2H264(i)
    def batch_SS2MOV(self, directory):
        # CREAT BUTTONS FOR OPTIONS
        self.CreateButtons(input_data={'ProRes':'self.returnItem("ProRes")', 'H264':'self.returnItem("H264")'} )
        ########################################################################################################
        if self.BRC != '':
            output_format = self.BRC
            self.finalSet.append(self.findScreenshots(directory))
            for i in self.finalSet[0]:
                firstImage = ''
                for dirpath,dirnames,filename in os.walk(i):
                    for file in filename:
                        if 'screenshot' in file.lower():
                            firstImage = file
                            break
                    item = i+'\\'+firstImage
                    self.img2mov(input_data = item, output_format = output_format )
    def batch_moveH264(self, sourceDirectory):
        destinationDirectory = self.setDirectory('Select Folder to Move Content To:')
    	X = self.findH264(sourceDirectory, destinationDirectory)
        #print X
        for i in range(len(X[1])):
            parentPath = X[1][i] [: [x for x, letter in enumerate(X[1][i]) if letter == '\\'][-1] ]
            if not os.path.exists(parentPath):
                os.makedirs(parentPath)
        #RELEASE THIS TO ENABLE COPYING OVER
        #shutil.copy(X[0][i], X[1][i])
####
####
####
if __name__ == '__main__':
    #H264  = 'C:\\Users\\James\\Desktop\\H264 Folder'
    SS = 'C:\\Users\\jricker\\Desktop\\test'
    batch = batchConvert()
    batch.batch_SS2MOV(SS)
    #batch.batch_SS2MOV(directory='C:\\Users\\James\\Desktop\\SHOTS')
    #batch.batch_moveH264(H264)
    #batch.findH264(batch.destDirectory)
    #batch.findScreenshots('C:\\Users\\James\\Desktop\\SHOTS')