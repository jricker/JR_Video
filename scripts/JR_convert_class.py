# -*- coding: utf-8 -*-
from JR_project_class import Project
from JR_system_class import System
from JR_ui_class import UI
from JR_rename_class import Rename
import codecs
import shutil
import sys
import os
class Convert(System, Project, UI, Rename): # CREATE A MASTER BAT FILE WHICH HOLDS ALL OF THE CONVERSION SCRIPTS
	def __init__(self):
		# System is already initialized in the Projects class
		UI.__init__(self)
		Rename.__init__(self)
		System.__init__(self)
		#Project.__init__(self)
	def regWriter(self):
		template_reg = self.settings + '\\registry\\default_reg.reg'
		user_reg = self.settings + '\\registry\\custom_reg.reg'
		user_reg_data = codecs.open(template_reg, encoding = "utf-16") # type of data it needs "C:\\Users\\James\\Desktop\\test.reg"
		user_reg_lines = user_reg_data.readlines()
		#print user_reg_lines
		new_list = []
		for i in user_reg_lines:
			x = i.strip()
			if 'USERNAME' in x:
				new_line = x.replace('USERNAME', self.userName[9:])
			else:
				new_line = x
			if '@=hex(2):' in new_line:
				new_line = new_line[:9] + self.text2regHex(new_line[9:])
			new_list.append(new_line)
		with open(user_reg,'w') as file:
		    for i in new_list:
		    	print>>file, (i)
		os.system('"''start '+user_reg+'"')
		# find a way to delete the created custom_reg file after it's used?
	def text2regHex(self, input_data):
		text_as_hex = input_data.encode('hex')
		digit_counter = 0
		hex_list = []
		for i in range(len(text_as_hex)/2 ): # JUMPING TWO SPOTS, ADDING 00 AND , TO EACH
			if digit_counter > len(text_as_hex)-2 or digit_counter == len(text_as_hex):
				pass
			else:
				o = text_as_hex[digit_counter] + text_as_hex[digit_counter+1] +','+'00' + ','
			hex_list.append(o)
			digit_counter +=2
		regHexJoin = [''.join(x for x in hex_list)]
		REGHEX_from_txt = regHexJoin[0][:-1]
		return REGHEX_from_txt
	def regHex2text(self, input_data):
		if input_data.endswith('.reg'):
			reg_data = codecs.open(input_data, encoding="utf_16") # type of data it needs "C:\\Users\\James\\Desktop\\test.reg"
			reg_lines = reg_data.readlines()
			reg_list = []
			for i in range(len(reg_lines)):
				if ':' in reg_lines[i]:
					reg_list.append(i)
			reghex_read = reg_lines[reg_list[0]:]
			reghex_join = [''.join(x for x in reghex_read)]
			reghex = reghex_join[0] # the end just removes the @=hex(2) which needs to be put pack in later when writing to a .reg file
		else:
			reghex = input_data
		remove_comma = reghex.replace(',', '')
		remove_backspace = remove_comma.replace('\\', '')#.decode('hex')
		reghex_decoded = remove_backspace.replace('  ', '').decode('hex')
		regList = []
		for i in reghex_decoded:
			if i == '\x00':
				pass
			else:
				regList.append(i)
		reghex_clean = [''.join(x for x in regList)]
		text_from_hex = reghex_clean[0]
		return text_from_hex	
	def processMetadata(self, input_data):
		metadata = {'FPS':0, 'Width':0, 'Height':0}
		if input_data.endswith('.R3D'):
			batch_cmd = "metadataRED"
			processed = self.processInput(input_data)
			output_metadata = processed[2]+processed[3]+'_metadata.txt'
			action = (self.scripts + "\\JR_convert.bat "+ batch_cmd+ ' ' +self.redline+ ' ' +input_data+ ' ' +output_metadata)
			os.system(action) # output the metadata to a file
			meta_file = open(output_metadata)
			meta_lines = meta_file.readlines()
			for i in meta_lines:
				c = " ".join(i.split())
				if c.startswith('Frame Width'):
					print 'caught width', c
					temp_width = ''.join([x for x in c if x.isdigit()])
					metadata['Width'] = temp_width
				if c.startswith('Frame Height'):
					print 'caught height', c
					temp_height = ''.join([x for x in c if x.isdigit()])
					metadata['Height'] = temp_height
				if c.startswith('FPS'):
					print 'caught FPS', c
					temp_fps = ''.join([x for x in c if x.isdigit()])
					metadata['FPS'] = temp_fps
		meta_file.close() # close the file now so we can remove it
		os.remove(output_metadata)
		return metadata
	def img2mov(self, input_data = 'NA', metadata = 'NA', format = 'ProRes', size = '1920x1080', compression = 'ProRes422_HQ'):
		##############################################################################################################################################
		compression_01 = self.compression[1] # use the original compression file which is 01 for it's data
		compression_02 = self.compression[1][:-6]+'02.vcf' # then write out to compression file 02 each line but with the updated FPS
		compression_file = open(compression_01)
		compression_file_amend = open(compression_02, 'w')
		compression_lines = compression_file.readlines()
		firstLine = 'VirtualDub.video.SetFrameRate2' # this is the line we're searching for in the .vcf file for vdub - amend FPS on it
		if metadata != 'NA':
			##############################################################################################################################################
			if len(metadata['FPS']) == 2:
				percent = '1'
			elif len(metadata['FPS']) == 3:
				percent = '10'
			elif len(metadata['FPS']) == 4:
				percent = '100'
			elif len(metadata['FPS']) == 5:
				percent = '1000'
			for line in compression_lines:
				if line.startswith(firstLine):
					line = firstLine + '('+str(metadata['FPS'])+','+percent+',1);\n'
				compression_file_amend.write(line) # now write the line out with the proper FPS for the shot.
			compression_file.close()
			compression_file_amend.close()
			##############################################################################################################################################
			## Get width x height ########################################################################################################################
			WxH = str(metadata['Width'])+'x'+str(metadata['Height'])
			if WxH == '0x0': # this is here in case there wasn't any metadata to extract, default back to 1920x1080
				WxH = '1920x1080'
			resizeWxH = '"'+'640 360'+'"' # we resize the width and hight for the initial TIF export so it isn't so massive. Start off with 640x360 as a base
			if 1919 < metadata['Width'] < 2048:
				resizeWxH = '"'+ str(int(metadata['Width'])/2)+' '+str(int(metadata['Height'])/2) + '"'
			if 2047 < metadata['Width'] < 4096:
				resizeWxH = '"'+ str(int(metadata['Width'])/2)+' '+str(int(metadata['Height'])/2) + '"'
			if 4096 < metadata['Width']:
				resizeWxH = '"'+ str(int(metadata['Width'])/2)+' '+str(int(metadata['Height'])/2) + '"'
		else:
			WxH = size
			resizeWxH = '"'+'1920 1080'+'"'
		##############################################################################################################################################
		#QT_final_name = self.processFinalName(input_data)+output_ext #for renaming the QT without the iterations or seperators
		processed = self.processInput(input_data) #grab the name ouputs from the rename class
		output_data = processed[2]+processed[3]
		parent_name = processed[2]+self.processFinalName(input_data)
		#!!parent_name = processed[2]+processed[3]
		iteration_length = processed[1]
		print iteration_length
		##############################################################################################################################################
		## See if the RENDER folder is there, if not, then take the folder the data is coming from ###################################################
		try:
			if self.findFolder(input_data, "RENDER")[0] != None:
				parent_folder = self.findFolder(input_data, "RENDER")[0]
		except TypeError:
			parent_folder = processed[2]
		##############################################################################################################################################
		JPG_folder = processed[2] + '\\JPG_temp\\' # find the last . in the string to create the name of the file for avi and mov output.		
		if parent_folder.endswith("RENDER"): # Find the render folder, should be -5 up as the parent_folder VAR dictates?
			parent_name = parent_folder + '\\01_MOV' + parent_name[[i for i, letter in enumerate(parent_name) if letter == '\\'][-1]: ]
		##############################################################################################################################################
		if processed[0] == '.exr' or processed[0] == '.tif':
			batch_cmd = "EXR2IMG2MOV"
			iteration = '-9' # this is at the beginning of the iteration so it's alwatys the highest it can be. ie: 100-900, 100000-900000
			for i in range(len(iteration_length[1:])):
				iteration += '0' # the maxIteration needs to be the same length as the one in the file. 
			JPG_output = JPG_folder + processed[3]
			if not os.path.exists(JPG_folder):
				os.makedirs(JPG_folder)
			print ' got here 01'
			setup = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +  '"'+JPG_output+'_temp_0000.jpg'+'"' + ' ' + self.djv + ' ' + '"'+output_data+iteration+processed[0]+'"' + ' ' + resizeWxH )
			os.system(setup)
			##############################################################################################################################################
			## ONCE COMPLETED THEN CREATE MOV FROM IMGS ##################################################################################################
			batch_cmd = "IMG2MOV"
			#!!action = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +  '"'+JPG_output+'_temp_0000.jpg'+'"' + ' ' + compression_02 + ' ' + self.vdub + ' ' + self.ffmpeg + ' ' + '"'+parent_name+'"' + ' ' +  WxH + ' ' + self.djv + ' ' + '"'+output_data+iteration+processed[0]+'"' + ' ' + JPG_output )
			action = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +  '"'+JPG_output+'_temp_0000.jpg'+'"' + ' ' + self.compression[0] + ' ' + self.vdub + ' ' + self.ffmpeg + ' ' + '"'+parent_name+'"' + ' ' +  WxH+ ' ' + format + ' ' + str(self.prores[compression]))
			os.system(action)
			#os.rename(parent_name+output_ext, QT_final_name)
		else:
			WxH = size
			batch_cmd = "IMG2MOV"
			if format == 'ProRes':
				setup = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +  '"'+input_data+'"' + ' ' + self.compression[0] + ' ' + self.vdub + ' ' + self.ffmpeg + ' ' + '"'+parent_name+'"' + ' ' +  WxH+ ' ' + format + ' ' + str(self.prores[compression]))
				os.system(setup)
			elif format == 'H264':
				setup = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +  '"'+input_data+'"' + ' ' + self.compression[0] + ' ' + self.vdub + ' ' + self.ffmpeg + ' ' + '"'+parent_name+'"' + ' ' +  WxH+ ' ' + format + ' ' + str(self.prores[compression]))
				os.system(setup)
			os.remove(parent_name+'.avi')
			#setup = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +  '"'+input_data+'"' + ' ' + compression_02 + ' ' + self.vdub + ' ' + self.ffmpeg + ' ' + '"'+parent_name+'"' + ' ' + self.vlc)
		# \/ reinstate this at the end to rename once everything is working properly again
		#os.rename(parent_name+output_ext, parent_folder+QT_final_name) # rename the file after all is set and done. 
			#os.rename(parent_name+output_ext, QT_final_name) # rename the file after all is set and done. 
		##############################################################################################################################################
		##############################################################################################################################################
		if os.path.exists(JPG_folder):
			shutil.rmtree(JPG_folder) # remove temp JPG folder
		##############################################################################################################################################
		##############################################################################################################################################
		if os.path.exists( parent_folder+'\\01_MOV' ):
			batch_cmd = "OPENFOLDER"
			movFolder = parent_folder+'\\01_MOV'
			setup2 = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' + '"'+movFolder+'"') # This opens the MOV folder after creation, but have to control if batch converting multiple shots
			os.system(setup2)
			#os.system('"''start '+parent_folder+'\\01_MOV'+'"') # have to make a fix for this if it doesn't export to an MOV folder and just does it to the recent directory
	def mov2prores(self, input_data = '', output_data = '', output_format = 'ProRes422_HQ'):
		batch_cmd = 'PRORES'
		if output_data == '':
			output_data = input_data[:[i for i, letter in enumerate(input_data) if letter == '.'][-1] ]+'_prores.mov'
		if self.processInput(input_data)[0] == '.R3D': # Need a special process for .R3D files because FFMPEG can't process them. Have to use redline initially.
			self.red2mov(input_data, 'PRORES')
		else:
			action = (self.scripts + "\\JR_convert.bat "+ batch_cmd+ ' ' +self.ffmpeg+ ' ' +'"'+input_data+'"'+ ' ' +output_data + ' ' + str(self.prores[output_format]) )
			os.system(action)
	def mov2H264(self, input_data):
		batch_cmd = 'H264'
		if self.processInput(input_data)[0] == '.R3D': # Need a special process for .R3D files because FFMPEG can't process them. Have to use redline initially.
			self.red2mov(input_data, 'H264')
		else:
			processed = self.processInput(input_data)
			output_file = '"' + processed[2]+processed[3] +'_H264.mp4'+ '"' # THE [1:] is to get rid of the \\ that exists on the filename, this may cause issues on the end
			input_file = '"' + processed[2]+processed[3] +processed[0]+ '"' # THE [1:] is to get rid of the \\ that exists on the filename, this may cause issues on the end
			action = (self.scripts + "\\JR_convert.bat "+ batch_cmd+ ' ' +self.ffmpeg+ ' ' +input_file+ ' ' + output_file )
			os.system(action)
	def red2mov(self, input_data ='', format = ''):
		batch_cmd = 'REDH264'
		## process metadata
		metadata = self.processMetadata(input_data)
		# finish metadata processing
		#output_folder = input_data[:[i for i, letter in enumerate(input_data) if letter == '.'][-1] ]
		processed = self.processInput(input_data)
		output_folder = processed[2]
		##############################################################################################################################################
		##############################################################################################################################################
		## Create temp TIFF folder
		TIFF_folder = processed[2]+ 'TIFF_temp/'
		if not os.path.exists(TIFF_folder):
			os.makedirs(TIFF_folder)
		##############################################################################################################################################
		##############################################################################################################################################
		output_name = processed[3]
		output_tiff = TIFF_folder+output_name+'.000000.tif' # THIS IS THE ouput REdCine creates. Thus we have to have 6 zeros at the end
		output_mov = TIFF_folder+output_name+'.mov'
		move_mov_to = output_folder+output_name+'.mov'
		##############################################################################################################################################
		##############################################################################################################################################
		action = (self.scripts + "\\JR_convert.bat "+ batch_cmd+ ' ' +self.redline+ ' ' +input_data+ ' ' + TIFF_folder + ' ' + output_name + ' ' + output_tiff )
		os.system(action) # convert R3D files to TIFF sequence
		##############################################################################################################################################
		##############################################################################################################################################
		if format == 'PRORES':
			self.img2mov(input_data= output_tiff, metadata= metadata, compression = self.BRC) # Send the new tiff files to be turned into a movie
		else:
			self.img2mov(output_tiff, metadata)
		shutil.move(output_mov, move_mov_to) # move the newly created MOV file out of the temp TIFF folder
		shutil.rmtree(TIFF_folder) #remove the temp tiff folder after it's done compressing into prores mov
		##############################################################################################################################################
		##############################################################################################################################################
		#NOW CONVERT TO H264
		if format == 'H264':
			self.mov2H264(move_mov_to)
			#NOW DELETE ORIGINAL PRORES FILE
			os.remove(move_mov_to)
		##############################################################################################################################################
		##############################################################################################################################################
	def edl2mov(self, input_data):
		batch_cmd = "MOV2CUTDOWN"
		EDL = []
		edit_folder = self.findFolder(input_data, 'EDIT')[0]
		project_folder = edit_folder[:[i for i, letter in enumerate(edit_folder) if letter == '\\'][-1] ]
		# find the MOV folder where all of the mov files are held
		for dirpath,dirnames,filenames in os.walk(project_folder):
			if dirpath.endswith('MOV'):
				if 'RENDER' in dirpath:
					mov_folder = dirpath
			if dirpath.endswith('CUTDOWNS'):
				if 'RENDER' in dirpath:
					cutdown_folder = dirpath
		MOV_file = []
		MOV_list = []
		MOV_in = []
		MOV_out = []
		MOV_newName = []
		counter = 0
		## CREATE NEW EDIT FOLDER IF IT DOESN'T EXIST ALREADY
		#if not os.path.exists(cutdown_folder):
		#	os.makedirs(cutdown_folder)
		## COLLECT FILES IN FOLDER
		for dirpath,dirnames,filenames in os.walk( mov_folder ):
			for i in filenames:
				MOV_file.append(i)
		## READ THE EDL LINE BY LINE
		with open(input_data) as fp:
		    for line in fp:
		        EDL.append(line.strip())
		## RUN THROUGH EDL AND FIND MATCHES WITH FILE LIST
		for i in range(len(EDL)):
			if [x for x in MOV_file if x in EDL[i] ]:
				counter += 1
				MOV_list.append( EDL[i][18:] )
				MOV_in.append( EDL[(i-1)][29:41] )
				MOV_out.append( EDL[(i-1)][41:53] )
				MOV_newName.append( str(counter) +'_'+ EDL[i][18:] ) 
		## RENAME ITEMS WITH DIRECTORY VALUES AND RE-CALCULATE THE FRAMES TO MILISECONDS
		for i in range( len(MOV_list) ):
			in_frames = int(MOV_in[i][9:])*33.3
			out_frames = int(MOV_out[i][9:])*33.3
			# ADD 0'S WHERE THERE ARE UNDER 3 VALUES FOR MILISECONDS
			if len(str(in_frames)[:-2]) == 2:
				in_frames = ''.join('0' + str(in_frames) )
			elif len(str(in_frames)[:-2]) == 1:
				in_frames = ''.join('00' + str(in_frames) )
			if len(str(out_frames)[:-2]) == 2:
				out_frames = ''.join('0' + str(out_frames) )
			##
			MOV_in[i] = '00' + MOV_in[i][2:-4] + '.' + str(in_frames)[:-2] # the added 00 at the start is to rule out hours added in by accident
			MOV_out[i] = '00' + MOV_out[i][2:-4] + '.' + str(out_frames)[:-2]
			MOV_newName[i] = ''.join(cutdown_folder + '\\' + MOV_newName[i])
			MOV_list[i] = ''.join(mov_folder + '\\' + MOV_list[i])
			## CALL THE ENCODING OF ALL EDIT FILES
			#Action = (self.userName + "\\Documents\\GitHub\\JR_Project\\videoProcessing\\EDL_to_MOV.bat "  +self.ffmpeg+ ' ' + MOV_list[i] + ' ' + MOV_newName[i] + ' ' + MOV_in[i] + ' ' +MOV_out[i] )
			Action = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' +self.ffmpeg+ ' ' + MOV_list[i] + ' ' + MOV_newName[i] + ' ' + MOV_in[i] + ' ' +MOV_out[i] )
			os.system(Action)
		batch_cmd = "EDL2MOV"
		a = [' '.join(x for x in MOV_newName)]	
		b = ''.join(( edit_folder + '\\' + 'PREVIEW_EDIT.mov ' ) + a[0] )
		Action2 = (self.scripts + "\\JR_convert.bat "+ batch_cmd + ' ' +self.mencoder+ ' ' + '"'+b+'"' )
		#Action2 = (self.userName + "\\Documents\\GitHub\\JR_Project\\videoProcessing\\CREATE_EDIT.bat "  +self.mencoder+ ' ' + '"'+b+'"' )
		os.system(Action2)
		####
		"""
		ONLY NEED TO ACTIVATE IF USING FFMPEG WITH CONCAT - ISSUE IS IT DOESN't ACCURETLY STITCH FRAME BY FRAME
		
		## WRITE NEW NAMES OUT TO TXT FILE
		with open(( cutdown_folder + '\\' + 'EDL.txt'),'w') as file:
		    for item in MOV_newName:
		        print>>file, ('file ' + "'" + item + "'")
		"""
	def gxml2dir(self, xml, dir):
		pass
	def exr2img(self, input_data = 'NA', format = '.tga', size = '1920 1080'):
		batch_cmd = "EXR2IMG"
		self.selection = input_data
		input_data = self.rename_auto(self.selection)
		#input_data = input_data[0] # must do this after the rename
		#input_data = self.rename(input_data) #renames the files in case they are incorrect
		iteration_length =  input_data[[i for i, letter in enumerate(input_data) if letter == '_'][-1] : ]
		iteration = '-9'
		for i in range(len(iteration_length[1:-5])):
			iteration+='0'
		output_data = input_data[:[i for i, letter in enumerate(input_data) if letter == '.'][-1] ]
		new_folder = input_data[:[i for i, letter in enumerate(input_data) if letter == '\\'][-1] ]+ '\\'+format[1:].upper()+'_version' # find the last . in the string to create the name of the file for avi and mov output.		
		if not os.path.exists(new_folder):
			os.makedirs(new_folder)
		new_output =  new_folder + output_data[[i for i, letter in enumerate(input_data) if letter == '\\'][-1] : ]+format
		setup = (self.scripts + "\\JR_convert.bat " + batch_cmd + ' ' + self.djv + ' ' +  '"'+output_data+iteration+'.exr'+'"' + ' ' + '"'+new_output+'"'+ ' '+ '"'+size+'"')
		os.system(setup)
	def folderScreenshots(self, input_data):
		folder_name = self.processFinalName(input_data)
		processed = self.processInput(input_data)
		folder_path = processed[2]
		directory = folder_path+folder_name
		X = self.findImageSequence(input_data)
		if not os.path.exists(directory):
			os.makedirs(directory)
		for i in X:
			original = folder_path+i
			new = directory+'/'+i
			shutil.move(original, new)
if __name__ == '__main__':
	conversion = Convert()
	if sys.argv[2] == 'IMG2MOV':
		conversion.CreateButtons(input_data={'ProRes':'self.returnItem("ProRes")', 'H264':'self.returnItem("H264")'} )
		if conversion.BRC != '':
			conversion.img2mov(sys.argv[1], format = conversion.BRC)
	elif sys.argv[2] == 'IMG2DIR':
		conversion.folderScreenshots(sys.argv[1])
	elif sys.argv[2] == 'RENAME CUSTOM':
		#print 'hello'
		#try:
		#	a = conversion.name.winfo_exists()
		#except:
		#	print ' didnt work'
		#print 'nope'
		#conversion.tk.destroy()
		conversion.RenameWindow(sys.argv[1])
		#conversion.file_list.append(sys.argv[1])
		#if conversion.windowOpen == 1:
		#	conversion.CreateButtons(input_data = {str(conversion.file_list):'hi'})
		#else:
		#	conversion.CreateButtons(input_data = {'went wrong':''})
		#a = conversion.name.winfo_exists()
		#if a == True:
		#	conversion.CreateButtons(input_data={str(conversion.file_list):'test'})
    	#else:
    	#	conversion.file_list.append(sys.argv[1])
    	#	conversion.CreateButtons(input_data={str(conversion.file_list):'test'})
	elif sys.argv[2] == 'RENAME AUTO':
		conversion.rename_auto( sys.argv[1])
	elif sys.argv[2] == 'PRORES':
		conversion.CreateButtons(
    		input_data={
    	    '422_Proxy':'self.returnItem("ProRes422_Proxy")', 
    	    '422_LT':'self.returnItem("ProRes422_LT")', 
    	    '422_Normal':'self.returnItem("ProRes422_Normal")', 
    	    '422_HQ':'self.returnItem("ProRes422_HQ")'
    	    } 
    	    )
		conversion.mov2prores(sys.argv[1], output_format=conversion.BRC)
	elif sys.argv[2] == 'EXR2IMG':
		conversion.exr2img(input_data = sys.argv[1])
	elif sys.argv[2] == 'MOV2CUTDOWN':
		pass
	elif sys.argv[2] == 'MOV2H264':
		conversion.mov2H264(input_data = sys.argv[1])
	elif sys.argv[2] == 'EDL2MOV':
		conversion.edl2mov(sys.argv[1])
	else:
		pass