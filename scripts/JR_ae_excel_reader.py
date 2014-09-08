# -*- coding: utf-8 -*-
import xlrd
import sys
from JR_system_class import System
import codecs
########################################################################################################
class ProcessExcelDoc(System):
	def __init__(self):
		System.__init__(self)
		self.finalList = []
		self.final_list = []
	def processRegions(self, region):
		regionCellValue = 0
		if region.upper() == 'UK':
			regionCellValue = 2
		elif region.upper() == 'REPLACE WITH':
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
		elif region.upper() == 'NA':
			regionCellValue = 11
		elif region.upper() == 'WW':
			regionCellValue = 12
		return regionCellValue
	########################################################################################################
	def readExcel(self, region, excelDoc, worksheet_name):
		regionalValue = self.processRegions(region)
		regionData = {'ID':'', 'Comp':[],'Original':[], 'Text':[]}
		workbook = xlrd.open_workbook(excelDoc)
		#worksheet = workbook.sheet_by_name('Text')
		worksheet = workbook.sheet_by_name(worksheet_name)
		num_rows = worksheet.nrows - 1
		num_cells = worksheet.ncols - 1
		curr_row = -1
		while curr_row < num_rows:
			curr_row += 1
			curr_cell = -1
			if curr_row == 0:
				pass
			else:
				while curr_cell < num_cells:
					curr_cell += 1
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
								cell_value_encoded = cell_value.encode("utf-8")
								original_cell_value_encoded = original_cell_value.encode("utf-8")
								regionData['ID'] = region
								if region.upper() == 'REPLACE WITH': # this removes the region for the replace function to work
									regionData['Comp'].append([composition, original_cell_value_encoded, cell_value_encoded ])
								else:
									regionData['Comp'].append([region+'_'+composition, original_cell_value_encoded, cell_value_encoded ])
		for x in range(len(regionData['Comp'])):
			a = regionData['Comp'][x]
			for i in range(len(a)):
				regionData['Comp'][x][i] = a[i].decode("utf-8")
			self.final_list.append(regionData['Comp'][x])
		print self.finalList
		self.writeOut(self.final_list)
	########################################################################################################
	def writeOut(self, item):
		print item
		self.textFile = self.userName + '/Desktop/data.txt'
		self.output_file = codecs.open(self.textFile, 'w', encoding = "utf-8")
		for i in item:
			p = 0
			for x in range(len(i)):
				p +=1
				if p == len(i):
					self.output_file.write("'"+i[x]+"'"+u'\r\n')
				else:
					self.output_file.write("'"+i[x]+"'"+':,:,:')
			self.output_file.write('\n')
		self.output_file.close()
########################################################################################################
if __name__ == '__main__':
	Kk = ProcessExcelDoc()
	theList = []
	variable = sys.argv[1]
	#variable = ',Replace With'
	regList = Kk.regFind(variable, ',')
	regList.insert(0, (0,0)) # adding 0 to the beginning to we can flow through it properly. 
	for i in range(len(regList)):
		if i == len(regList)-1:
			x = variable[regList[i][1]:]
			theList.append(x)
		else:
			x = variable[regList[i][1]:regList[i+1][0]]
			theList.append(x)
	excel = theList[0]
	#excel = 'C:/Users/jricker/Desktop/original_text.xls'
	listToProcess = theList[1:]
	if listToProcess[0] == 'Replace With':
		worksheet_name = 'Replace'
	else:
		worksheet_name = 'Text'
	for i in listToProcess:
		Kk.readExcel(str(i), excel, worksheet_name)
##################################
### DOUBLE CHECK THE ORIGINAL DATA FIRST TO SEE IF ANYTHING HAS CHANGED IN THE EXCEL DOCUMENT, IF IT HAS CHANGE IT IN THE AE PROJECT
##################################