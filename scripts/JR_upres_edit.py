import os
import shutil
import JR_convert_class
########################################################################################
convert = JR_convert_class.Convert()
project_file = "D:\\GATEBIL\\03_EDITS\\02_PREMIER_PROJECT\\GATEBIL_EDIT_HIGHRES.prproj"
project = open(project_file, 'r')
original_folder = "H:\\Gatetbil 2014"
HQ_folder = "D:\\GATEBIL\\02_FOOTAGE\\03_MOV\\01_HQ"
new_relative_path = "..\\..\\02_FOOTAGE\\03_MOV\\00_HQ\\"
tempList = []
########################################################################################
for line in project:
	if "H264" in line:
		MP4 = line.rfind(".mp4")
		backspace = line.rfind("\\")
		a = line[backspace+1:MP4+4]
		if '>' in a:
			ff = line.rfind(">")
			bb = a[ff:]
		else:
			bb = a
		tempList.append(bb)
	else:
		pass
project.close() # close the project once you've read through all of the lines so it can be used later
tempList = set(tempList)
fileList = []
########################################################################################
for i in tempList:
	if i== '':
		pass
	else:
		fileList.append(i[:-9])
########################################################################################
original_list = []
HQ_list = []
for dirpath,dirnames,filenames in os.walk(original_folder):
	if filenames != []:
		for x in filenames:
			dot = x.rfind(".")
			if x[:dot] in fileList:
				original_list.append(dirpath+'\\'+x)
				HQ_list.append(HQ_folder +'\\'+x)
########################################################################################
## HERE IS WHERE YOU COPY THE FILES FROM RAID TO LOCAL
########################################################################################
for i in range(len(original_list)):
	if os.path.exists(HQ_list[i]):
		pass
	else:
		if original_list[i].endswith('.MXF'):
			if os.path.exists(HQ_list[i][:-4]+'.mov'): # have to do this because Adobe can't use MXF file types
				pass
			else:
				convert.mov2prores(original_list[i], HQ_list[i][:-4]+'.mov')
		else:
			shutil.copy(original_list[i], HQ_folder)
input_file = open(project_file, 'r',)
output_file = open(project_file[:-7]+"01.prproj", 'w')
########################################################################################
# iterate through all of the lines once more to replace and write out anything that has H264 associated with it.
########################################################################################
for lines in input_file:
	if "H264" in lines:
		aaa = lines
		if "<Title>" in lines or "<Name>" in lines:
			MP4 = lines.rfind("_H264.mp4")
			beginning = lines.find(">")
			middle = lines[beginning+1:MP4]
			end = lines.rfind("</")
			for i in HQ_list:
				if i.endswith(".MXF"):
					i = i[:-4]+'.mov'
				if middle in i:
					original_middle = lines[beginning+1:end]
					#print '----------------TITLE OR NAME ------------------------------'
					#print lines[:beginning+1] + original_middle + lines[end:]
					#print lines[:beginning+1] + i[i.rfind('/')+1:] + lines[end:]
					aaa = lines[:beginning+1] + i[i.rfind('/')+1:] + lines[end:]
		elif "<FilePath>" in lines or '<ActualMediaFilePath>' in lines:
			backspace = lines.rfind("\\")
			MP4 = lines.rfind("_H264.mp4")
			beginning = lines.find(">")
			middle = lines[backspace+1:MP4]
			end = lines.rfind("</")
			for i in HQ_list:
				if i.endswith(".MXF"):
					i = i[:-4]+'.mov'
				if str(middle) in str(i):
					original_middle = lines[beginning+1:end]
					#print '---------------- FILE PATH OR ACTUAL MEDIA PATH ------------------------------'
					#print lines[:beginning+1] + original_middle + lines[end:]
					#print lines[:beginning+1] + i + lines[end:]
					aaa = lines[:beginning+1] + i + lines[end:]
		elif 'RelativePath':
			backspace = lines.rfind("\\")
			MP4 = lines.rfind("_H264.mp4")
			beginning = lines.find(">")
			middle = lines[backspace+1:MP4]
			end = lines.rfind("</")
			for i in HQ_list:
				if i.endswith(".MXF"):
					i = i[:-4]+'.mov'
				if str(middle) in str(i):
					original_middle = lines[beginning+1:end]
					#print '---------------- FILE PATH OR ACTUAL MEDIA PATH ------------------------------'
					#print lines[:beginning+1] + original_middle + lines[end:]
					#print lines[:beginning+1] + new_relative_path +i[i.rfind('/')+1:] + lines[end:]
					aaa = lines[:beginning+1] + new_relative_path +i[i.rfind('/')+1:] + lines[end:]
		output_file.write(aaa)
	else:
		output_file.write(lines)