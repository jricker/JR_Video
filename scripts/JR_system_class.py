import os
from JR_rename_class import Rename
class System(Rename):
    def __init__(self):
        Rename.__init__(self)
        ## MASTER PATHS 
        self.userName = os.path.expanduser("~")
        self.systemLocation = self.userName + '\\Copy\\GHOST\\CINEMATIC_SCRIPTS\\'
        ## PROGRAMS
        self.vlc = '"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"'
        self.djv = '"C:\\Program Files (x86)\\djv 0.8.3\\bin\\djv_convert"'
        self.ffmpeg = self.systemLocation + "programs\\FFMPEG\\ffmpeg"
        self.ffprobe = self.systemLocation + "programs\\FFMPEG\\ffprobe"
        self.redline = '"C:\\Program Files\\REDCINE-X PRO 64-bit\\redline"'
        self.vdub = self.systemLocation + "programs\\vDub\\vdub64.exe"
        self.mencoder = self.systemLocation + "programs\\MPlayer\\mencoder"
        ## FOLDER LOCATIONS
        self.libraries = self.systemLocation + "libraries"
        self.images = self.systemLocation + "images"
        self.files = self.systemLocation + "libraries\\files"
        self.scripts = self.userName +"\\Documents\\GitHub\\JR_Video\\scripts"
        self.settings = self.userName +"\\Documents\\GitHub\\JR_Video\\settings"
        self.sequences = self.systemLocation + "test\\sequences"
        ## SETTINGS
        self.compression = self.settings + '\\vDub_compression\\vDub_avi_compression.vcf', self.settings + '\\vDub_compression\\vDub_avi_compression_custom_01.vcf', self.settings + '\\vDub_compression\\vDub_avi_compression_23976.vcf'
        self.prores = {'ProRes422_Proxy': 0, 'ProRes422_LT':1, 'ProRes422_Normal':2, 'ProRes422_HQ':3 }
    def systemStart(self, app):
        os.system('"''start '+app+'"')
    def findFolder(self, input_data, folderName):
        if folderName in input_data:
            ii = input_data.find(folderName)
            pp = [i for i, letter in enumerate(input_data) if letter == '\\']
            high = [x for x in pp if x > ii]
            low = [x for x in pp if x < ii]
            return input_data[:high[0]], input_data[low[-1]+1:high[0]]
    def rename(self, input_data):
        input_data = [input_data]
        self.selection = input_data
        file_path = input_data[0][:[i for i, letter in enumerate(input_data[0]) if letter == '\\'][-1]+1]
        file_name = input_data[0][[i for i, letter in enumerate(input_data[0]) if letter == '\\'][-1]+1:]
        iter_placement = file_name.find(self.getIteratorValue(0))
        iter_length = len(self.getIteratorValue(0))
        file_extension = file_name[iter_placement + iter_length:]
        original_name = file_name[:iter_placement]
        new_name = file_name[:iter_placement]
        try:
            if self.findFolder(file_path, '_sh')[1] != None:
                new_name = self.findFolder(file_path, '_sh')[1]
        except TypeError:
            pass
        fileList = []
        os.chdir(file_path)
        for files in os.listdir("."):
            if original_name in files:
                fileList.append(files)
        iterator = -1
        new_return = [] # this is for the return so the mov converters know what it is now
        for x in sorted(fileList):
            iterator +=1
            if len(str(iterator)) == 1:
                padding = '000'
            elif len(str(iterator)) == 2:
                padding = '00'
            elif len(str(iterator)) == 3:
                padding = '0'
            else:
                padding = ''
            y = new_name + '_' + padding + str(iterator) + file_extension
            old = file_path + x
            new = file_path + y
            #print new
            #print x, 'to .. ', y
            new_return.append(new)
            os.rename(old, new)
        return new_return[0] # this is to return any item after it is renamed, for use in other functions
        #print new_return[0], 'asdfsa'
"""
if __name__ == '__main__':
    K = System()
    K.selection = 'C:\\Users\\jricker\\Desktop\\GC\\03_RENDER\\GC_sc01\\GC_sc01_sh010\\EXR\\4K\\test-001.exr'
    #K.selection.append('C:\\Users\\jricker\\Desktop\\test\\test-0001.exr')
    #K.selection.append('C:\\Users\\jricker\\Desktop\\GC\\03_RENDER\\GC_sc01\\GC_sc01_sh010\\EXR\\4K\\test-0001.exr')
    K.rename(K.selection)
"""