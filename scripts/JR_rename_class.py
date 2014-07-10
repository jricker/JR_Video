import os
import re
class Rename():
	def __init__(self):#, selection, name):
		self.name = ''
		self.selection = ''
		#self.name = name
		#self.selection = selection + name # append the name to the end of the selection list so we can process it's properties with a -1 call in the 'i'
	def processInput(self, input_data):
		self.selection = [input_data]
		extension = input_data[[i for i, letter in enumerate(input_data) if letter == '.'][-1]:]
		iteratorValue = input_data[self.getIteratorLocation(0)[-1][0]:self.getIteratorLocation(0)[-1][1]]
		filepath = input_data[:[i for i, letter in enumerate(input_data) if letter == '/'][-1]+1 ]
		filename = input_data[[i for i, letter in enumerate(input_data) if letter == '/'][-1]+1 : -len(extension) ]
		return extension, iteratorValue, filepath, filename
	def processFinalName(self, input_data):
		final_name_location = []
		processed = self.processInput(input_data)
		temp = processed[3].find(processed[1])
		for i in range(temp):
			temp-=1
			for x in processed[3][temp]:
				if x == '_' or x =='.' or x =='-' or x.isalpha():
					final_name_location.append(temp)
		final_name = processed[3][:final_name_location[0]]
		return final_name
	def processNamespace(self, i):
		if self.selection[-1][0] == ':': # if the input name starts with : then we want to return the root
			return ':'
		elif len( self.getNamespace(-1) ) >= 2: # if it is longer than 1, means it isn't the root and thus we want to return it's namespace
			return self.getNamespace(-1)
		else:
			return self.getNamespace(i) # if none of the above then there is no namespace in the input name and we want to return the selection namespace.
	def processRename(self, i):
		if self.selection[-1][0] == '_': # Suffix addition only
			return ( self.getAfterNamespace(i) + self.selection[-1] )
		elif self.selection[-1][-1] == '_': # Prefix addition only
			return ( self.selection[-1] + self.getAfterNamespace(i) )
		if self.selection[-1][-1] == ':': # Namespace replacement only
			if self.getIteratorValue(i) == 1: # value of 1 means no iterator present in original name
				return self.getPrefix(i) 
			else:
				return ( self.getPrefix(i) +  self.getIteratorValue(i) + self.getSuffix(i) )
		else:
			if self.getIteratorValue(-1) == 1: # value of 1 means no iterator present in original name
				if len(self.selection) > 2: # for more than one item selected
					return ( self.getPrefix(-1) + '_' + str((int( self.getIteratorValue(-1) ) + int(i)))  )
				else: #for only one item selected
					return self.getPrefix(-1) 
			else:
				if len(self.selection) > 2: # for more than one item selected
					return ( self.getPrefix(-1) + str( ( int( self.getIteratorValue(-1) ) + int(i) ) ) + self.getSuffix(-1) )
				else: #for only one item selected
					return self.getPrefix(-1)
	def reFunction(self, item, isolate):
		# This method finds the location of 
		# the provided isolate var in the 
		# provided item var and returns a list
		#
		s = re.compile( isolate ) # compile a string obj, ie: '\:' or '\d+'
		f = s.finditer(item)
		return [ x.span() for x in f ]
	def getIteratorLocation(self, i):
		# This method uses the reFunction to
		# find the location of a selections
		# iter if there is digits in the selection
		#
		digitList = [x for x in self.selection[i] if x.isdigit()]
		if digitList == []:
			return []
		else:
			return ( self.reFunction (self.selection[i] , '\d+') ) 
	def getIteratorValue(self, i):
		# This method process the list from
		# getIteratorLocation and returns the value of
		# last nuber group in the selected object
		#
		iterLocation = self.getIteratorLocation(i)
		if iterLocation == []:
			return 1
		else:
			return self.selection[i] [ iterLocation [-1][0] : iterLocation [-1][1] ]
	def getPrefix(self, i):
		# This method uses the getIterLocation (if there is one)
		# and the getNamespace value, if there is one, to identify
		# the value of the prefix which will be between both items
		#
		iterLocation = self.getIteratorLocation(i)
		if self.getNamespace(i) == ':':
			if iterLocation == []:
				return self.selection[i]
			else:
				prefix = self.selection[i] [ : iterLocation[-1][0] ]
				return prefix
		else:
			if iterLocation == []:
				return self.selection[i] [ len(self.getNamespace(i)) : ] # + 1 : ]
			else:
				prefix = self.selection[i] [ : iterLocation[-1][0] ]
				return prefix[len(self.getNamespace(i)) :] # + 1 :]
	def getSuffix(self, i):
		iterLocation = self.getIteratorLocation(i)
		if iterLocation == []:
			return ''
		else:
			suffix = self.selection[i] [ iterLocation[-1][1] : ]
			return suffix
	def getNamespace(self, i):
		if ':' in self.selection[i]:
			V = self.reFunction(self.selection[i], '\:+')
			return self.selection[i] [ : V[0][1] ]
		else: # no namespaces present
			return ':'
	def getAfterNamespace(self, i):
		if ':' in self.selection[i]:
			V = self.reFunction(self.selection[i], '\:+')
			return self.selection[i] [ V[0][1] : ]
		else: # no namespaces present
			return self.selection[i]
"""
if __name__ == '__main__':
	b = ['C:\\Desktop\\test_m03-0031.jpg']
	c = ['renamed']
	K = Rename()
	K.selection = ['C:\\Desktop\\test_m03-0031.jpg']
	K.name = ['renamed']
	print K.processRename(0)
	t = b[0].find(K.getIteratorValue(0))
	p = int(t) + len(K.getIteratorValue(0))
	print K.getIteratorValue(0)
	iterator = ''
	for i in range(len(K.getIteratorValue(0) )):
		iterator += '0'
	print b[0][:t]
	print b[0][p:]
	print iterator
	print b[0][:t] + iterator + b[0][p:]
"""