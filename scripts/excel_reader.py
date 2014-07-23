import xlrd
workbook = xlrd.open_workbook('C:/Users/jricker/Desktop/testCase.xls')
worksheet = workbook.sheet_by_name('Text')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = -1
while curr_row < num_rows:
	curr_row += 1
	row = worksheet.row(curr_row)
	print 'Row:', curr_row
	curr_cell = -1
	while curr_cell < num_cells:
		curr_cell += 1
		# Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
		cell_type = worksheet.cell_type(curr_row, curr_cell)
		cell_value = worksheet.cell_value(curr_row, curr_cell)
		if cell_value == '':
			pass
		else:
			print '	', cell_type, ':', cell_value, worksheet.cell_value(0, curr_cell)