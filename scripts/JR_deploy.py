## start script for installation
from JR_convert_class import *
import os
def deployPrograms():
	launch = Convert()
	DJV_location = 'C:\\Program Files (x86)\\djv 0.8.3'
	PYTHON_location = 'C:\\Python26'
	# install libraries
	launch.systemStart( launch.libraries + "\\exe\\OpenEXR-1.2.0.win-amd64-py2.6.exe" )
	launch.systemStart( launch.libraries + "\\exe\\Pillow-2.2.1.win-amd64-py2.6.exe" )
	launch.systemStart( launch.libraries + "\\exe\\PyAlembic-1.5.2.win-amd64-py2.6.exe" )
	if not os.path.exists(DJV_location):
		launch.systemStart( launch.systemLocation + "programs\\djv-0.8.3-pre2_winxp-x64.exe" )
	if not os.path.exists(PYTHON_location):
		launch.systemStart( launch.systemLocation + "programs\\python-2.6.6.amd64" )
	## once applications are installed, launch the registry writer
	launch.regWriter()
if __name__ == '__main__':
	deployPrograms()