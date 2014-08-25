import xml.etree.ElementTree as ET
import os
import re
import shutil # this module is used to copy files across to other directories
from JR_system_class import *
############################
JRsystem = System()
############################
############################################################################################################################################
############################################################################################################################################

#                                  THIS OBVIOUSLY NEEDS TOOOONS OF CLEANUP, CURRENTLY A MESS

############################################################################################################################################
############################################################################################################################################
############################################################################################################################################
fileList = []
edgeList = []
folderList = []
sharedFolderList = []
directoryList = []
userName = os.path.expanduser("~")
#mainDirectory = '\\eucr-fs1.eu.ad.ea.com\\Studio\\HawaiiMarketing\\CINEMATICS\\MERCURY NFS15'
mainDirectory = userName + '\\Desktop'
masterXML = 'project.xgml'
projectName = 'FRANK'
produceLOD = 0
produceSC = 1
sceneAmount = 5
shotAmount = 20
############################
tree = ET.parse(masterXML)
root = tree.getroot()
############################
for child in root:
	if child.tag == 'section':
		x = child.keys()
		for i in range(len(x)):
			pass
	for a in child:
		item = ''
		label = ''
		identity = ''
		node = ''
		if a.tag == 'section':
			x = a.keys()
			for i in range(len(x)):
				ii = a.get(a.keys()[i])
				if ii == 'node':
					identity =  a[0].text
					for b in a:
						if b.tag == 'section':
							x = b.keys()
							for i in range(len(x)):
								iii =  b.get(b.keys()[i])
								if iii == 'graphics':
									item = b[5].text
									if item == '#FFCC00':
										node = 'folder'
									elif item == '#00CC00':
										node = 'file'
									elif item == '#0099FF':
										node = 'directory'
									elif item == '#FF99CC':
										node = 'sharedFolder'
									else:
										node == 'NA'
								elif iii == 'LabelGraphics':
									label = b[0].text
								add = [identity, item, label] # collection of all of the nodes added to the scene
					if node == 'folder':
						folderList.append(add)
					elif node == 'file':
						fileList.append(add)
					elif node == 'directory':
						directoryList.append(add)
					elif node == 'sharedFolder':
						sharedFolderList.append(add)
				elif ii == 'edge':
					for b in a:
						if b.tag == 'section':
							x = b.keys()
							for i in range(len(x)):
								iii =  b.get(b.keys()[i])
								one = a[0].text
								two = a[1].text
								add = [one, two]
								edgeList.append(add)
def getFileExtList (dirPath,uniq=True,sorted=True):
    extList=list()
    for dirpath,dirnames,filenames in os.walk(dirPath):
        for file in filenames:
            fileExt=os.path.splitext(file)[-1]
            extList.append(fileExt)
 
    if uniq:
        extList=list(set(extList))
    if sorted:
        extList.sort()
    return extList
###
defaultFileLocation = JRsystem.files
fileLibrary = getFileExtList(defaultFileLocation)
###
total = []
def createTotal():
	for i in folderList:
		total.append(i)
	for i in fileList:
		total.append(i)
	for i in sharedFolderList:
		total.append(i)
createTotal()
###
dirTemp = []
dirFinal = []
def again(source):
	x = [i for i in total if source in i] # folder list actually needs to be the total list with files and shared folders
	if x == []: # means that you've hit zero on the list and it is the 
		pass # break out of the loop and go to the next 'i' in the edgeList loop
	else:
		dirTemp.append(x[0])
		a = [i for i in edgeList if x[0][0] in i]
		for i in a:
			if i[1] == x[0][0]:
				again(i[0])
for i in edgeList:
	lastItem = [x for x in total if i[1] in x]
	dirTemp.append(lastItem[0])
	again(i[0])
	dirTemp.append([mainDirectory])
	dirFinal.append(dirTemp)
	dirTemp = []
###
a = ''
counter = 0
shotCounter = 0
sceneCounter = 0
sceneList = []
shotList = []
for i in dirFinal:
	for x in reversed(i):
		if counter != 0:
			a += '\\' +x[-1]
		else:
			a += x[-1]
		counter += 1
	if a[:1] == '\\':
		d =  a[1:]
	else:
		d = a
	if '*NAME*' in d:
		d = d.replace('*NAME*', projectName)
	s = re.compile(r'/*\\') # this finds the backslashes in the to be created directory
	f = s.finditer(d)
	g = [ x.span() for x in f ]
	h= d[g[-1][0] : ][1:] # this is a long winded way, we already ahve this information when we parse the first item. Just get it from there?
	p = [x for x in fileLibrary if h.endswith((x))]
	if 'sc##' in d:
		sceneList.append(d)
	elif 'lod##' in d:
		sceneList.append(d)
	else:
		eee = d
	#print 'this is the scene LIST', sceneList
	if p != []:
		fileDirectory = eee[:(-1*(len(h)) )] # finds the directory from where to copy and past it
		if fileDirectory.endswith(("\\")):
			oldFile = defaultFileLocation + '\\' + [each for each in os.listdir(defaultFileLocation) if each.endswith(p[0])][0]
			newFile = fileDirectory + h
			if not os.path.exists(fileDirectory):
				os.makedirs(fileDirectory)
			if os.path.exists(newFile):
				pass
				#print 'file already exists'
			else:
				shutil.copyfile(oldFile, newFile)
			if '.sbs' in newFile: # replace section of substance which will rename the graph to the asset name
				# NEED TO TURN THIS INTO A CLASS INSTEAD OF INSIDE THIS CODE				
				ins = open(newFile).read()
				out = open(newFile, 'w')
				replacements = {'Master':projectName}
				for i in replacements.keys():
				    ind = ins.replace(i, replacements[i])
				out.write(ind)
				out.close
		else:
			pass
			#print fileDirectory, ' this is getting ignored'
	if p == []:
		if not os.path.exists(eee):
			os.makedirs(eee)
	a = ''
###
iterationList = []
while sceneAmount != sceneCounter:
	sceneCounter += 1
	if len(str(sceneCounter)) == 1:
		sceneCounterA = '0' + str(sceneCounter)
	for i in sceneList:
		if produceLOD == 1:
			temp = i.replace('lod##', ('lod_' + str(sceneCounter - 1 )) ) #minus 1 from the scene counter for LOD so it starts at  0 
		elif produceSC == 1:
			temp = i.replace('sc##', ('sc' + str(sceneCounterA)) )
		shotList.append(temp)
while shotAmount != shotCounter:
	shotCounter += 1
	if len(str(shotCounter)) == 1:
		shotCounterA = '0' + str(shotCounter*10)
	elif len(str(shotCounter)) == 2:
		shotCounterA = str(shotCounter*10)
	for i in shotList:
		temp2 = i.replace('sh##', ('sh' + str(shotCounterA)) )
		iterationList.append(temp2)
###
aaa = ''
counter2 = 0
for i in reversed(iterationList):
	if i[:1] == '\\':
		ddd =  i[1:]
	else:
		ddd = i
	s = re.compile(r'/*\\') # this finds the backslashes in the to be created directory
	f = s.finditer(ddd)
	g = [ x.span() for x in f ]
	h= ddd[g[-1][0] : ][1:] # this is a long winded way, we already ahve this information when we parse the first item. Just get it from there?
	p = [x for x in fileLibrary if h.endswith((x))]
	if p != []:
		fileDirectory = ddd[:(-1*(len(h)) )] # finds the directory from where to copy and past it
		if fileDirectory.endswith(("\\")):
			oldFile = defaultFileLocation + '\\' + [each for each in os.listdir(defaultFileLocation) if each.endswith(p[0])][0]
			newFile = fileDirectory + h
			if not os.path.exists(fileDirectory):
				os.makedirs(fileDirectory)
			if os.path.exists(newFile):
				pass
				#print 'file already exists'
			else:
				shutil.copyfile(oldFile, newFile)
			#print 'NEW FILE = ', oldFile
	if p == []:
		if not os.path.exists(ddd):
			os.makedirs(ddd)
	aaa = ''