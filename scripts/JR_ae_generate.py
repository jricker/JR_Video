import sys
import os
import re
from functools import partial
from JR_system_class import System
import xlwt
import xlrd
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
	def regFind(self, itemToSearch, searchForThis):
		d = itemToSearch
		s = re.compile(r'/*'+searchForThis) # this finds the backslashes in the to be created directory
		f = s.finditer(d)
		g = [ x.span() for x in f ]
		return g
	def readExcelDocument(self):
		workbook = xlrd.open_workbook('C:/Users/jricker/Desktop/testCase.xls')
		worksheet = workbook.sheet_by_name('Text')
		num_rows = worksheet.nrows - 1
		num_cells = worksheet.ncols - 1
		curr_row = -1
		tempList = []
		while curr_row < num_rows:
			curr_row += 1
			row = worksheet.row(curr_row)
			#print 'Row:', curr_row
			curr_cell = -1
			if curr_row == 0:
				pass
			else:
				while curr_cell < num_cells:
					curr_cell += 1
					# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
					cell_type = worksheet.cell_type(curr_row, curr_cell)
					cell_value = worksheet.cell_value(curr_row, curr_cell)
					if curr_cell == 0:
						compositionQuery = cell_value = worksheet.cell_value(curr_row, curr_cell)
						if compositionQuery == '':
							pass
						else:
							composition = compositionQuery
					if cell_value == '':
						pass
					else:
						if worksheet.cell_value(0, curr_cell) == 'COMP':
							pass
						else:
							tempList.append('Comp ->', composition, '    ', 'Language ->', worksheet.cell_value(0, curr_cell), '    ', 'text ->', cell_value)
						#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
						#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
		return tempList
	def createExcelDocument(self, information):
		#print information, ' THIS IS INFOREMATION'
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Text')
		#
		### GET THE STYLE GOING ###
		font0 = xlwt.Font()
		font0.name = 'Arial'
		font0.colour_index = 87
		font0.bold = True
		#style0 = xlwt.XFStyle()
		#style0.font = font0
		st = xlwt.easyxf('pattern: pattern solid;')
		st.pattern.pattern_fore_colour = 44
		st.font = font0
		#BOARDERS
		borders = xlwt.Borders()
		borders.left = 1
		borders.right = 1
		borders.top = 1
		borders.bottom = 1
		#style for data
		st2 = xlwt.easyxf('pattern: pattern solid; borders: bottom dashed, left dashed')
		st2.pattern.pattern_fore_colour = 22
		st2.font = font0
		st2.borders = borders
		#style for comps
		st3 = xlwt.easyxf('pattern: pattern solid; borders: bottom dashed, left dashed')
		st3.pattern.pattern_fore_colour = 26
		st3.font = font0
		st3.borders = borders
		##ex = {'MASTER':['julian', 'Mark'], 'TEXT_01':['JAMES', 'text_01_v02'], 'TEXT_02':['text_02_v01', 'text_02_v01']}
		tt = 0
		for i in information:
			tt+=1
			a = information.get(i)
			aLen = len(a)
			ws.write(tt, 0, i, st3)
			for x in range(aLen):
				#print tt
				print i + '=' + a[x]
				ws.write(tt, 1, a[x], st2)
				tt +=1
		### CREATE THE FIELDS FOR THIS ###
		ws.write(0, 0, 'COMP', st)
		ws.write(0, 1, 'ORIGINAL', st)
		ws.write(0, 2, 'UK', st)
		ws.write(0, 3, 'ITALY', st)
		ws.write(0, 4, 'FRANCE', st)
		ws.write(0, 5, 'SPAIN', st)
		ws.write(0, 6, 'GERMANY', st)
		ws.write(0, 7, 'RUSSIA', st)
		ws.write(0, 8, 'JAPAN', st)
		ws.write(0, 9, 'POLAND', st)
		ws.write(0, 10, 'AUSTRALIA', st)
		ws.write(0, 11, 'NORTH AMERICA', st)
		ws.write(0, 12, 'WORLD WIDE (GENERAL)', st)
		for i in range(13):
			ws.col(i).width = 5000# + i
		wb.save(self.userName+'/Desktop/testCase.xls')
	def Run(self, variables):
		self.tk.geometry('200x400+600+300')
		self.tk.iconbitmap(default= self.images + "\UI\icon.ico")	 
		#self.tk.iconbitmap(default= self.userName + self.systemLocation + "images\UI\icon.ico")
		#TITLE
		self.tk.title('')
		# COLOURS
		bgColour = '#2f2f2f'
		self.btnColour1 = '#136ec7'
		self.btnColour2 = '#098400'
		# VARIABLE BREAKDOWN
		#d = variables
		#s = re.compile(r'/*--B--') # this finds the backslashes in the to be created directory
		#f = s.finditer(d)
		#g = [ x.span() for x in f ]
		g = self.regFind(variables, '--B--')
		g.insert(0, (0,0)) # adding 0 to the beginning to we can flow through it properly. 
		#print g
		#testx = variables.find('--B--')
		#print variables[:testx], ' THIS IS THE --B--'
		# BUTTONS
		#print variables
		textDictionary = {}
		for i in range(len(g)):
			#print variables[0:16]
			if i == len(g)-1:
				x = variables[g[i][1]:]
				#print x.find(":_:")
				#a = re.compile(r'/*:_:') # this finds the backslashes in the to be created directory
				#b = a.finditer(x)
				#gg = [ h.span() for h in b ]
				bb = self.regFind(x, ':_:')
				key = x[:bb[0][0]]
				value = x[bb[0][1]:]
				if key in textDictionary:
					textDictionary[key].append(value)
				else:
					textDictionary[key] = []
					textDictionary[key].append(value)
				#print variables[g[i][1]:]
			else:
				x = variables[g[i][1]:g[i+1][0]]
				bb = self.regFind(x, ':_:')
				key = x[:bb[0][0]]
				value = x[bb[0][1]:]
				if key in textDictionary:
					textDictionary[key].append(value)
				else:
					textDictionary[key] = []
					textDictionary[key].append(value)
				#
				#print variables[g[i][1]:g[i+1][0]]
		#print textDictionary
		self.createExcelDocument(textDictionary)
		#names = ''
		#for i in variables:
		#	names+=i
		#print names
		self.XMLBtn = Button(text = variables, bg = self.btnColour1, fg = 'white', width = 200, height = 03, command = partial(self.assignValues, 'XML') )
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
	def __call__(self):
		pass
if __name__ == '__main__':
	K = Directory()
	variables = sys.argv[1]
	K.Run(variables)
	#self.Run()
#main(['scriptName', r'D:\Mountfield_Benzin\SHOTS\MF_BE_M4\PLATE\MF_BE_M4_00.tif', '-p']) # for testing purposes only
#main(['scriptName', r'D:\Mountfield_Benzin\SHOTS\MF_BE_PV\RENDERS\2D_OUT\MF_BE_PV_KROVINOREZ_0001.jpg', '-p'])
	
	#main(sys.argv)
#K = Directory()
#K.Run()