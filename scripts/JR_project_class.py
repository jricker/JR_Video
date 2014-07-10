from JR_system_class import *
class Project(System):
	def __init__(self):
		System.__init__(self)
		self.projectName = ''
		self.projectLocation = ''
	def switchProject(self):
		pass
	def buildReg(self):
		pass
	def build(self):
		pass
if __name__ == '__main__':
	K = Project()
	print dir(K)