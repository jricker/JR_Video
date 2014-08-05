import sys
import re
from JR_system_class import System
import xlwt
import xlrd
class Directory(System):
	def __init__(self):
		System.__init__(self)
	def regFind(self, itemToSearch, searchForThis):
		d = itemToSearch
		s = re.compile(r'/*'+searchForThis) # this finds the backslashes in the to be created directory
		f = s.finditer(d)
		g = [ x.span() for x in f ]
		return g
	def readExcelDocument(self):
		workbook = xlrd.open_workbook(self.userName + '/Desktop/original_text.xls')
		worksheet = workbook.sheet_by_name('Text')
		num_rows = worksheet.nrows - 1
		num_cells = worksheet.ncols - 1
		curr_row = -1
		tempList = []
		while curr_row < num_rows:
			curr_row += 1
			#print 'Row:', curr_row
			curr_cell = -1
			if curr_row == 0:
				pass
			else:
				while curr_cell < num_cells:
					curr_cell += 1
					# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
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
		#
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
		wb.save(self.userName+'/Desktop/original_text.xls')
	def Run(self, variables):
		g = self.regFind(variables, '--B--')
		g.insert(0, (0,0)) # adding 0 to the beginning to we can flow through it properly. 
		##
		textDictionary = {}
		for i in range(len(g)):
			#print variables[0:16]
			if i == len(g)-1:
				x = variables[g[i][1]:]
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
		self.createExcelDocument(textDictionary)
if __name__ == '__main__':
	K = Directory()
	variables = sys.argv[1]
	K.Run(variables)