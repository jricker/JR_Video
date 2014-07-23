import xlrd
workbook = xlrd.open_workbook('C:/Users/jricker/Desktop/testCase.xls')
worksheet = workbook.sheet_by_name('Text')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1
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
					print 'Comp ->', composition, '    ', 'Language ->', worksheet.cell_value(0, curr_cell), '    ', 'text ->', cell_value
				#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition
				#print '	', 'text ->', cell_value, 'Language ->', worksheet.cell_value(0, curr_cell), 'Comp ->', composition