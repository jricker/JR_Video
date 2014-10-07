import os
myintvariable = 1
strauss = os.environ.get('Path')
X = strauss.split(';')
for i in X:
	print i