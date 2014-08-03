import xlrd
import os
import sys
###################################################
###################################################
variables = sys.argv[1]
excelDocument = variables[0]
listToProcess = variables[1:]
userName = os.path.expanduser("~")
#workbook = xlrd.open_workbook('C:/Users/James/Desktop/testCase_01.xls')
workbook = xlrd.open_workbook(excelDocument)
worksheet = workbook.sheet_by_name('Text')
textFile = 'C:/Users/James/Desktop/data.txt'
finalList = []
def processRegions(region):
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
output_file = open(textFile, 'w',)
def readExcel(region):
	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = -1
	regionalValue = processRegions(region)
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
	final_list = []
	for x in range(len(regionData['Comp'])):
		print regionData['Comp'][x]
		final_list.append(regionData['Comp'][x])
	writeOut(final_list)
		#print regionData['Comp'][x]
		#output_file.write(str(regionData['Comp'][x])+'\n')
		#output_file.write(x)
	#print regionData['Comp'][0]
	#print regionData['Comp'][1]
	#print regionData['Comp'][2]
					#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
					#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
def writeOut(item):
	for i in item:
		output_file.write(str(i)+'\n')
	#output_file.close()
#listToProcess = ['it', 'fr']
for i in listToProcess:
	readExcel(i)
#readExcel('IT')
##################################
### DOUBLE CHECK THE ORIGINAL DATA FIRST TO SEE IF ANYTHING HAS CHANGED IN THE EXCEL DOCUMENT, IF IT HAS CHANGE IT IN THE AE PROJECT
##################################