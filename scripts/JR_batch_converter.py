import os
import JR_convert_class
import shutil
convert = JR_convert_class.Convert()
directory = "H:/JAPAN/FOOTAGE"
newDirectory = "D:/JAPAN/02_FOOTAGE/02_LIVE_ACTION"
screenshotDirectory = []
movList = []
newMovDir = []
finalSet = []
def getFileExtList (dirPath,uniq=True,sorted=True):
    for dirpath,dirnames,filenames in os.walk(dirPath):
        for file in filenames:
            #fileExt=os.path.splitext(file)[-1]
            if 'Screenshot' in file:
            	screenshotDirectory.append(dirpath)
def findScreenshots():
	getFileExtList(directory)
	a = set(screenshotDirectory)
	finalSet.append( sorted(a) )
def findMovies (dirPath,uniq=True,sorted=True):
    for dirpath,dirnames,filenames in os.walk(dirPath):
        for file in filenames:
            if file.endswith('.mov') or file.endswith('.R3D') or file.endswith('.MXF'):
            	movList.append(dirpath + '\\' + file)
            	newMovDir.append(directory + '\\' + file)
def findH264 (dirPath,uniq=True,sorted=True):
    for dirpath,dirnames,filenames in os.walk(dirPath):
        for file in filenames:
            if file.endswith('.mp4'):
            	if 'H264' in file:
            		####
            		currentFile = dirpath + '\\' + file
            		newFile = newDirectory + dirpath[len(directory):] + '\\' + file
            		####
            		movList.append(currentFile)
            		newMovDir.append(newFile)
            	else:
            		pass
def batchConvert():
	findMovies(directory)
	for i in movList:
		H264version = i[:-4]+'_H264.mp4'
		if os.path.exists(H264version):
			pass
		else:
			convert.mov2H264(i)
def createMOV():
	for i in finalSet[0]:
		firstImage = ''
		for dirpath,dirnames,filename in os.walk(i):
			for file in filename:
				if 'Screenshot' in file:
					firstImage = file
					break
       		item = i+'\\'+firstImage
       		print item
def moveH264():
	findH264(directory)
	for i in range(len(newMovDir)):
		parentPath = newMovDir[i] [: [x for x, letter in enumerate(newMovDir[i]) if letter == '\\'][-1] ]
		if not os.path.exists(parentPath):
			os.makedirs(parentPath)
		shutil.copy(movList[i], newMovDir[i])
#moveMovies()
#moveH264()