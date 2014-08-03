import xlrd
import os
import sys
from JR_system_class import System
###################################################
###################################################
class ProcessExcelDoc(System):
	def __init__(self):
		System.__init__(self)
		self.finalList = []
		self.final_list = []
	def processRegions(self, region):
		regionCellValue = 0
		if region.upper() == 'UK':
			regionCellValue = 2
		elif region.upper() == 'IT':
			regionCellValue = 3
		elif region.upper() == 'FR':
			regionCellValue = 4
		elif region.upper() == 'SP':
			regionCellValue = 5
		elif region.upper() == 'GER':
			regionCellValue = 6
		elif region.upper() == 'RU':
			regionCellValue = 7
		elif region.upper() == 'JAP':
			regionCellValue = 8
		elif region.upper() == 'POL':
			regionCellValue = 9
		elif region.upper() == 'AU':
			regionCellValue = 10
		elif region.upper() == 'WW':
			regionCellValue = 11
		return regionCellValue
	def readExcel(self, region, excelDoc):
		#################################################
		#################################################

		#################################################
		#################################################
		##
		self.textFile = 'C:/Users/James/Desktop/data.txt'
		self.output_file = open(self.textFile, 'w',)
		self.userName = os.path.expanduser("~")
		#workbook = xlrd.open_workbook('C:/Users/James/Desktop/testCase_01.xls')
		##
		workbook = xlrd.open_workbook(excelDoc)
		worksheet = workbook.sheet_by_name('Text')
		num_rows = worksheet.nrows - 1
		num_cells = worksheet.ncols - 1
		curr_row = -1
		regionalValue = self.processRegions(region)
		regionData = {'ID':'', 'Comp':[],'Original':[], 'Text':[]}
		while curr_row < num_rows:
			curr_row += 1
			#row = worksheet.row(curr_row)
			#print 'Row:', curr_row
			curr_cell = -1
			if curr_row == 0:
				pass
			else:
				while curr_cell < num_cells:
					curr_cell += 1
					# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
					#cell_type = worksheet.cell_type(curr_row, curr_cell)
					cell_value = worksheet.cell_value(curr_row, curr_cell)
					original_cell_value = worksheet.cell_value(curr_row, 1)
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
							if curr_cell == regionalValue:
								#print region
								#print region+'_'+composition, original_cell_value , cell_value
								regionData['ID'] = region
								regionData['Comp'].append([region+'_'+composition,[original_cell_value],[cell_value]])
								#regionData['Original'].append(original_cell_value)
								#regionData['Text'].append(cell_value)
								#print 'Comp ->', composition, '    ', 'Language ->', worksheet.cell_value(0, curr_cell), '    ', 'text ->', cell_value
		for x in range(len(regionData['Comp'])):
			#print regionData['Comp'][x]
			self.final_list.append(regionData['Comp'][x])
		self.writeOut(self.final_list)
			#print regionData['Comp'][x]
			#output_file.write(str(regionData['Comp'][x])+'\n')
			#output_file.write(x)
		#print regionData['Comp'][0]
		#print regionData['Comp'][1]
		#print regionData['Comp'][2]
						#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
						#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
	def writeOut(self, item):
		#print 'here'
		for i in item:
			#print i
			self.output_file.write(str(i)+'\n')
		#self.output_file.close()
	#listToProcess = ['it', 'fr']
if __name__ == '__main__':
	Kk = ProcessExcelDoc()
	theList = []
	variable = sys.argv[1]
	#variable = 'C:/Users/James/Desktop/testCase_01.xls,it,fr'
	regList = Kk.regFind(variable, ',')
	regList.insert(0, (0,0)) # adding 0 to the beginning to we can flow through it properly. 
	for i in range(len(regList)):
		#print variables[0:16]
		if i == len(regList)-1:
			x = variable[regList[i][1]:]
			theList.append(x)
			#print x.find(":_:")
			#a = re.compile(r'/*:_:') # this finds the backslashes in the to be created directory
			#b = a.finditer(x)
			#gg = [ h.span() for h in b ]
			#bb = self.regFind(x, ':_:')
			#key = x[:bb[0][0]]
			#value = x[bb[0][1]:]
			#if key in textDictionary:
			#	textDictionary[key].append(value)
			#else:
			#	textDictionary[key] = []
			#	textDictionary[key].append(value)
			#print variables[regList[i][1]:]
		else:
			x = variable[regList[i][1]:regList[i+1][0]]
			theList.append(x)
			#bb = self.regFind(x, ':_:')
			#key = x[:bb[0][0]]
			#value = x[bb[0][1]:]
			#if key in textDictionary:
			#	textDictionary[key].append(value)
			#else:
			#	textDictionary[key] = []
			#	textDictionary[key].append(value)
	#a = list(pp)
	#print a
	#t = sys.argv[1]
	#a = []
	#for i in t:
	#	a.append(i)
	#for i in variables:
	#variables = ['C:/Users/James/Desktop/testCase_01.xls', 'it', 'fr']
	#variables = sys.argv[1]
	print theList
	excel = theList[0]
	listToProcess = theList[1:]
	for i in listToProcess:
		Kk.readExcel(str(i), excel)
##	self.excelDocument = variables[0]
##	self.listToProcess = variables[1:]
##	######
##	K = Directory()
##	v = sys.argv[1]
##	K.Run(variables)
##for i in self.listToProcess:
##	readExcel(i)
#readExcel('IT')
##################################
### DOUBLE CHECK THE ORIGINAL DATA FIRST TO SEE IF ANYTHING HAS CHANGED IN THE EXCEL DOCUMENT, IF IT HAS CHANGE IT IN THE AE PROJECT
##################################