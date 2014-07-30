import xlrd
workbook = xlrd.open_workbook('C:/Users/James/Desktop/testCase_01.xls')
worksheet = workbook.sheet_by_name('Text')
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
def readExcel(region):
	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = -1
	regionalValue = processRegions(region)
	regionData = {'Comp':[],'Original':[], 'Text':[]}
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
							regionData['Comp'].append(composition)
							regionData['Original'].append(original_cell_value)
							regionData['Text'].append(cell_value)
							#print 'Comp ->', composition, '    ', 'Language ->', worksheet.cell_value(0, curr_cell), '    ', 'text ->', cell_value
	print regionData
					#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
					#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
listToProcess = ['uk', 'na', 'it', 'sp', 'ger', 'ru', 'jap', 'fr']
for i in listToProcess:
	readExcel(i)
#readExcel('IT')