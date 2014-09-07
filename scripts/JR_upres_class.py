import os
import shutil
import re
import tkFileDialog
from JR_convert_class import Convert
from JR_ui_class import UI
########################################################################################
class HighRes(UI, Convert):
	def __init__(self):
		UI.__init__(self)
	def set_variables(self, input_data = 'NA'):
		self.tk.withdraw()
		if input_data == 'NA':
			self.project_file = tkFileDialog.askopenfilename(title = 'Select Project to Convert')
		else:
			self.project_file = input_data
		if self.project_file:
			self.original_folder = tkFileDialog.askdirectory(title = 'Select Folder containing Raw/Original Media')
			if self.original_folder:
				self.HQ_folder = tkFileDialog.askdirectory(title = 'Select New Locaton') # load directory selection window
				find_placement = [m.start() for m in re.finditer('/', self.HQ_folder)]
				self.new_relative_path = "../../" + self.HQ_folder[find_placement[1]+1:]+'/'
			else:
				print 'Canceled operation'
		else:
			print 'Canceled operation'
		if (self.project_file and self.original_folder and self.HQ_folder and self.new_relative_path):
			print 'all here'
		else:
			print 'one missing'
	def Create_HighRes(self):
		project = open(self.project_file, 'r')
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
		for dirpath,dirnames,filenames in os.walk(self.original_folder):
			if filenames != []:
				for x in filenames:
					dot = x.rfind(".")
					if x[:dot] in fileList:
						original_list.append(dirpath+'\\'+x)
						HQ_list.append(self.HQ_folder +'\\'+x)
		########################################################################################
		## HERE IS WHERE YOU COPY THE FILES FROM RAID TO LOCAL
		########################################################################################
		for i in range(len(original_list)):
			if os.path.exists(HQ_list[i]):
				pass
			else:
				#>>if original_list[i].endswith('.MXF'):
				#>>	if os.path.exists(HQ_list[i][:-4]+'.mov'): # have to do this because Adobe can't use MXF file types
				#>>		pass
				#>>	else:
				#>>		self.mov2prores(original_list[i], HQ_list[i][:-4]+'.mov')
				#>>else:
				shutil.copy(original_list[i], self.HQ_folder)
		input_file = open(self.project_file, 'r',)
		output_file = open(self.project_file[:-7]+"01.prproj", 'w')
		########################################################################################
		# iterate through all of the lines once more to replace and write out anything that has H264 associated with it.
		########################################################################################
		for lines in input_file:
			if "H264" in lines:
				data = lines
				if "<Title>" in lines or "<Name>" in lines:
					MP4 = lines.rfind("_H264.mp4")
					beginning = lines.find(">")
					middle = lines[beginning+1:MP4]
					end = lines.rfind("</")
					for i in HQ_list:
						# ACTIVE AGAIN IF MXF CONVERSION IS NEEDED
						#>>if i.endswith(".MXF"):
						#>>	#i = i[:-4]+'.mov'
						#>>	i = i[:-4]+'.MXF'
						if middle in i:
							#'----------------TITLE OR NAME ------------------------------'
							data = lines[:beginning+1] + i[i.rfind('/')+1:] + lines[end:]
				elif "<FilePath>" in lines or '<ActualMediaFilePath>' in lines:
					backspace = lines.rfind("\\")
					MP4 = lines.rfind("_H264.mp4")
					beginning = lines.find(">")
					middle = lines[backspace+1:MP4]
					end = lines.rfind("</")
					for i in HQ_list:
						# ACTIVE AGAIN IF MXF CONVERSION IS NEEDED
						#>>if i.endswith(".MXF"):
						#>>	#i = i[:-4]+'.mov'
						#>>	i = i[:-4]+'.MXF'
						if str(middle) in str(i):
							#'---------------- FILE PATH OR ACTUAL MEDIA PATH ------------------------------'
							data = lines[:beginning+1] + i + lines[end:]
				elif 'RelativePath':
					backspace = lines.rfind("\\")
					MP4 = lines.rfind("_H264.mp4")
					beginning = lines.find(">")
					middle = lines[backspace+1:MP4]
					end = lines.rfind("</")
					for i in HQ_list:
						# ACTIVE AGAIN IF MXF CONVERSION IS NEEDED
						#>>if i.endswith(".MXF"):
						#>>	#i = i[:-4]+'.MXF'
						#>>	i = i[:-4]+'.mov'
						if str(middle) in str(i):
							#'---------------- FILE PATH OR ACTUAL MEDIA PATH ------------------------------'
							data = lines[:beginning+1] + self.new_relative_path +i[i.rfind('/')+1:] + lines[end:]
				output_file.write(data)
			else:
				output_file.write(lines)
if __name__ == '__main__':
    Main = HighRes()
    Main.set_variables()