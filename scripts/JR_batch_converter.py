import os
import JR_convert_class
import shutil
convert = JR_convert_class.Convert()
directory = "D:/FOOTAGE"
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
## CONVERT ALL MOVIES IN DIRECTORY
findMovies(directory)
for i in movList:
	H264version = i[:-4]+'_H264.mp4'
	if os.path.exists(H264version):
		pass
	else:
		print 'release command if you want to run this'
		#convert.mov2H264(i)
##
def createMOV():
	for i in finalSet[0]:
		firstImage = ''
		for dirpath,dirnames,filename in os.walk(i):
			for file in filename:
				if 'Screenshot' in file:
					firstImage = file
					break
       		item = i+'\\'+firstImage
def moveMovies():
	for i in range(len(movList)):
		shutil.move(movList[i], newMovDir[i])
#moveMovies()