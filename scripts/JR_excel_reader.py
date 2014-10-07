# -*- coding: utf-8 -*-
import xlrd
from JR_system_class import System
########################################################################################################
class ProcessExcelDoc(System):
	def __init__(self):
		System.__init__(self)
		self.finalList = []
		self.final_list = []
	########################################################################################################
	def readExcel(self, excelDoc):
		workbook = xlrd.open_workbook(excelDoc)
		worksheet1 = workbook.sheet_by_index(0)
		worksheet2 = workbook.sheet_by_index(1)
		column_0_values2 = worksheet2.col_values(colx=0)
		column_0_values = worksheet1.col_values(colx=0)
		for i in column_0_values[1:]:
			for x in column_0_values2[1:]:
				if x in i:
					print i
########################################################################################################
if __name__ == '__main__':
	Kk = ProcessExcelDoc()
	excel = 'C:/Users/James/Desktop/Active Users - Shotgun as of Aug 2014.xlsx'
	Kk.readExcel( excel)