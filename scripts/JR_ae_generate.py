# -*- coding: utf-8 -*-
import sys
import re
from JR_system_class import System
import xlwt
class Directory(System):
	def __init__(self):
		System.__init__(self)
	def regFind(self, itemToSearch, searchForThis):
		d = itemToSearch
		s = re.compile(r'/*'+searchForThis) # this finds the backslashes in the to be created directory
		f = s.finditer(d)
		g = [ x.span() for x in f ]
		return g
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
		# style for Top Row
		st = xlwt.easyxf('pattern: pattern solid')
		st.pattern.pattern_fore_colour = 44
		st.font = font0
		#BOARDERS
		borders = xlwt.Borders()
		borders.left = 1
		borders.right = 1
		borders.top = 1
		borders.bottom = 1
		# style for original data
		st2 = xlwt.easyxf('pattern: pattern solid; borders: bottom dashed, left dashed; align: wrap 1')
		st2.pattern.pattern_fore_colour = 22
		st2.font = font0
		st2.borders = borders
		# style for comps
		st3 = xlwt.easyxf('pattern: pattern solid; borders: bottom dashed, left dashed')
		st3.pattern.pattern_fore_colour = 26
		st3.font = font0
		st3.borders = borders
		#
		st4 = xlwt.easyxf('protection: cell_locked false; align: wrap 1')
		tt = 0
		pp = 1
		for i in information:
			tt+=1
			a = information.get(i)
			aLen = len(a)
			ws.write(tt, 0, i, st3)
			for x in range(aLen):
				#print tt
				for ii in range(11):
					pp+=1
					ws.write(tt, pp, '', st4)
				pp = 1 # reset for next round
				ws.write(tt, 1, a[x].decode('utf-8'), st2)
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
		#############################
		#ws.protect = True
		#ws.password = "password1"
		for i in range(13):
			ws.col(i).width = 5000# + i
		ws.col(1).width = 9000# + i
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
	def test(self, items):
		print items
if __name__ == '__main__':
	K = Directory()
	variables = sys.argv[1].decode('cp1252').encode('utf-8')
	"""
	#LIST OF JAVA ESCAPE KEYS - just for reference
	and_sym = '%26' 		#&
	colon_sym= "%" + '3A' 	#:
	smiCol_sym= "%" + '3B' 	#;
	apost_sym = "%"+'u2018' #'
	comma_sym = '%'+'2C' 	#,
	ex_sym = '%21' 			#!
	dbQuote_sym = 'u201C' 	#"
	sterling_sym = '%'+'A3' #£
	money_sym = '%24' 		#$
	perc_sym = '%25' 		#%
	upArow_sym = '%'+'5E' 	#^
	column_L_sym = '%28' 	#(
	column_R_sym = '%29' 	#)
	equals_sym = '%'+'3D' 	#=
	dic_L_sym = '%'+'7B' 	#{
	dic_R_sym = '%'+'7D' 	#}
	lst_L_sym = '%'+'5B' 	#[
	lst_R_sym = '%'+'5D' 	#[
	lst_R_sym = '%'+'5D' 	#[
	pound_sym = '%23'		##
	squiggle_sum = '%'+'7E'	#~
	question_sym = '%'+'3F' #?
	great_sym = '%'+'3E'	#>
	less_sym = '%'+'3C'		#<
	backsl_sym = '%'+'5C'	#
	vertLn_sym = '%'+'7C'	#|
	hiApos_sym = '%60'		#`
	ind_sym = '%'+'AC'		#¬
	brkLn_sym = '%'+'A6'	#¦
	euro_sym = '%'+'u20AC'	#€
	copWrt_sym = '%'+'A9'	#©
	tm_sym = '%'+'u2122'	#™
	reg_sym = '%'+'AE'		#®
	"""	
	#################################################################
	and_sym = '%26'			#&
	great_sym = '%'+'3E'	#>
	less_sym = '%'+'3C'		#<
	vertLn_sym = '%'+'7C'	#|
	backsl_sym = '%'+'5C'	#\
	#################################################################
	and_count = [m.start() for m in re.finditer(and_sym, variables)]
	great_count = [m.start() for m in re.finditer(great_sym, variables)]
	less_count = [m.start() for m in re.finditer(less_sym, variables)]
	vertLn_count = [m.start() for m in re.finditer(vertLn_sym, variables)]
	backsl_count = [m.start() for m in re.finditer(backsl_sym, variables)]
	#################################################################
	for i in range(len(and_count)):
		variables = variables.replace(and_sym, '&', i+1)
	for i in range(len(great_count)):
		variables = variables.replace(great_sym, '>', i+1)
	for i in range(len(less_count)):
		variables = variables.replace(less_sym, '<', i+1)
	for i in range(len(vertLn_count)):
		variables = variables.replace(vertLn_sym, '|', i+1)
	for i in range(len(backsl_count)):
		variables = variables.replace(backsl_sym, '\\', i+1)
	#################################################################
	K.Run(variables)