import sys
import os
from functools import partial
from JR_system_class import *
from Tkinter import *
from PIL import Image, ImageTk
from tkFileDialog import askopenfilename, askdirectory
class Directory(System):
	def __init__(self):
		System.__init__(self)
		self.tk = Tk()
		self.directoryValue = ''
		self.xmlValue = ''
		self.projectValue = ''
		self.sceneValue = ''
		self.shotValue = ''
		self.userName = os.path.expanduser("~")
	def Run(self):
		self.tk.geometry('200x400+600+300')
		self.tk.iconbitmap(default= self.images + "\UI\icon.ico")	 
		#self.tk.iconbitmap(default= self.userName + self.systemLocation + "images\UI\icon.ico")
		#TITLE
		self.tk.title('')
		# COLOURS
		bgColour = '#2f2f2f'
		self.btnColour1 = '#136ec7'
		self.btnColour2 = '#098400'
		input_bgColour = '#cecece'
		input_fgColour = 'black'
		# TEXT
		btnFont = 'Arial'
		# BUTTONS
		self.XMLBtn = Button(text = 'XML > DIR', bg = self.btnColour1, fg = 'white', width = 200, height = 03, command = partial(self.assignValues, 'XML') )
		self.IMGBtn = Button(text = 'MOV', bg = self.btnColour1, fg = 'white', width = 200, height = 03, command = partial(self.assignValues, 'IMG') )
		self.AVIBtn = Button(text = 'PRORES', bg = self.btnColour1, fg = 'white', width = 200, height = 03, command = partial(self.assignValues, 'AVI') )
		self.RENAMEBtn = Button(text = 'RENAME', bg = self.btnColour1, fg = 'white', width = 200, height = 03, command = partial(self.assignValues, 'RENAME') )
		# BUTTON POSITION
		self.RENAMEBtn.pack(side = 'bottom' )
		self.AVIBtn.pack(side = 'bottom' )
		self.IMGBtn.pack(side = 'bottom' )
		self.XMLBtn.pack(side = 'bottom' )
		# FILE OPTIONS
		self.file_opt = options = {}
		options['filetypes'] = [ ('XML Files', '.xml')] # add options to the dictionary
		#print self.file_opt
		# HEAD IMAGE
		imageFile = self.images + "\UI\UI_header.jpg"
		#imageFile = self.userName + self.systemLocation + "images\UI\UI_header.jpg"
		image1 = ImageTk.PhotoImage(Image.open(imageFile))
		panel1 = Label(image=image1)
		#panel1.pack()
		panel1.pack(side = 'top', expand = 'yes')
		# FINAL CONFIGURATIONS
		self.tk.resizable(width=FALSE, height=FALSE)
		self.tk.configure(background= bgColour)
		self.tk.bind('<Escape>', quit) # BIND TO ESC KEY
		self.tk.mainloop()
	def assignValues(self, value):
		if value == 'XML':
			self.tk.destroy()
			A = XML_win.Directorys()
			A.Run()
			#self.XMLBtn.configure(bg = self.btnColour2 )
		elif value == 'DIR':
			directory = askdirectory()
			self.directoryValue = directory
			if self.directoryValue == '':
				pass
			else:
				self.directoryBtn.configure(bg = self.btnColour2 )
	def warningMessage(self, comment):
		w=Toplevel()
		w.iconify()
		var = StringVar()
		note = Message( w, textvariable=var, relief=RAISED )
		var.set(comment)
		note.pack()
	def buildDirectory(self, directory):
		self.projectValue = self.project_field.get()
		self.sceneValue = self.scene_field.get()
		self.shotValue = self.shot_field.get()
		if self.projectValue == '':
			print 'Please type in project name'
		elif self.directoryValue == 'None':
			print 'Please select Directory'
		elif self.xmlValue == 'None':
			print 'Please select XML location'
		elif self.sceneValue == '' or self.sceneValue == '0':
			print 'Please enter a scene amount'
		elif self.shotValue == '' or self.shotValue == '0':
			print 'Please enter a shot amount'
		else:
			print ' starting '
		if not os.path.exists(directory):
			os.makedirs(directory)
		else:
			print 'already exists'
	def __call__(self):
		pass
if __name__ == '__main__':
	K = Directory()
	K.Run()
	#self.Run()
#main(['scriptName', r'D:\Mountfield_Benzin\SHOTS\MF_BE_M4\PLATE\MF_BE_M4_00.tif', '-p']) # for testing purposes only
#main(['scriptName', r'D:\Mountfield_Benzin\SHOTS\MF_BE_PV\RENDERS\2D_OUT\MF_BE_PV_KROVINOREZ_0001.jpg', '-p'])
	
	#main(sys.argv)
#K = Directory()
#K.Run()