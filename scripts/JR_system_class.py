import os
import re
import Tkinter as TK
from Tkinter import *
from functools import partial
from JR_rename_class import Rename
import Tkinter, tkFileDialog
from Tkinter import Entry, Label, Button
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
        self.TKicon = self.images + "\UI\EA_ICON.ico"
        # CACHE ITEMS
        self.BRC = ''
        ## SETTINGS
        self.movie_ext = ('.mov', '.R3D', '.MXF', '.mp4', '.MP4' , '.avi')
        self.image_ext = ('.jpg','.tiff','.png', '.tga', '.exr')
        # VDUB COMPRESSION
        self.compression = (
            self.settings + '\\vDub_compression\\vDub_avi_compression.vcf', 
            self.settings + '\\vDub_compression\\vDub_avi_compression_custom_01.vcf',
            self.settings + '\\vDub_compression\\vDub_avi_compression_custom_02.vcf',  
            self.settings + '\\vDub_compression\\vDub_avi_compression_23976.vcf'
            )
        # PRORES
        self.prores = {
        'ProRes422_Proxy': 0, 
        'ProRes422_LT':1, 
        'ProRes422_Normal':2, 
        'ProRes422_HQ':3 
        }
    def systemStart(self, app):
        os.system('"''start '+app+'"')
    def findParentFolder(self, input_data):
        processed = self.processInput(input_data)
        file_path2 = processed[2]
        parent_dir = file_path2[1+[i for i, letter in enumerate(file_path2) if letter == '\\' or letter =='/'][-2]:-1]
        return parent_dir
    def findFolder(self, input_data, folderName):
        if folderName in input_data:
            ii = input_data.find(folderName)
            pp = [i for i, letter in enumerate(input_data) if letter == '\\']
            high = [x for x in pp if x > ii]
            low = [x for x in pp if x < ii]
            return input_data[:high[0]], input_data[low[-1]+1:high[0]]
    def findVersioning(self, input_data):
        processed = self.processInput(input_data)
        parent_dir = self.findParentFolder(input_data)
        if 'v' in parent_dir:
            X = parent_dir.lower().rfind('v')
            if parent_dir[X+1:X+2].isdigit():
                if 'v' in processed[3].lower():
                    X = input_data.lower().rfind('v')
                    if input_data[X+1:X+2].isdigit():
                        Y = input_data[X+1:]
                        break_list = []
                        for i in range(len(Y)):
                            if Y[i].isdigit():
                                pass
                            else:
                                break_list.append(i)
                                break
                        return input_data[X:X+break_list[0]+1]
                else:
                    return ''
        elif 'v' in input_data.lower():
            X = input_data.lower().rfind('v')
            if input_data[X+1:X+2].isdigit():
                Y = input_data[X+1:]
                break_list = []
                for i in range(len(Y)):
                    if Y[i].isdigit():
                        pass
                    else:
                        break_list.append(i)
                        break
                return input_data[X:X+break_list[0]+1]
        else:
            return ''
    def setDirectory(self, message = 'Please select a folder'):
        root = Tkinter.Tk()
        root.withdraw()
        X = tkFileDialog.askdirectory(parent=root,initialdir="/",title= message)
        return X
    def returnItem(self, item):
        self.BRC = item
        self.tk.destroy()
    def setProResFormat(self):
        pass
    def getFileList (self, dirPath, name, uniq=True,sorted=True):
        X = []
        for dirpath,dirnames,filenames in os.walk(dirPath):
            for file in filenames:
                if name == '':
                    if file.endswith(self.image_ext):
                        X.append(dirpath)
                elif name.lower() in file.lower():
                    X.append(dirpath)
        return X
        #Y = set(X)
        #return sorted(Y)
                    #self.screenshotDirectory.append(dirpath)
    def regFind(self, itemToSearch, searchForThis):
        d = itemToSearch
        s = re.compile(r'/*'+searchForThis) # this finds the backslashes in the to be created directory
        f = s.finditer(d)
        g = [ x.span() for x in f ]
        return g
    def RenameWindow(self, input_data):
        #print input_data
        try:
            self.tk
        except AttributeError:
            self.tk = TK.Tk()
            self.tk.iconbitmap(default= self.TKicon) 
        self.tk.geometry('200x120')
        #TITLE
        self.tk.title('Rename')
        # COLOURS
        bgColour = '#2f2f2f'
        self.btnColour2 = '#098400'
        input_bgColour = '#cecece'
        input_fgColour = 'black'
        # POSITION
        pointer_x = self.tk.winfo_pointerx()
        pointer_y = self.tk.winfo_pointery()
        self.tk.geometry('+'+str(int(pointer_x))+'+'+str(pointer_y) )
        self.tk.resizable(width=FALSE, height=FALSE)
        # LABELS
        labelOffset = 25
        Name = Label(text = 'Name :', bg = bgColour, fg = 'white').place(x=8, y=5)
        scene = Label(text = 'Replace :', bg = bgColour, fg = 'white').place(x=8, y=5+labelOffset)
        shots = Label(text = 'With :', bg = bgColour, fg = 'white').place(x=8, y=30+labelOffset)
        ## INPUT FIELDS
        self.name_field = Entry(bg = input_bgColour, fg=input_fgColour, bd = 0)
        self.replace_field = Entry(bg = input_bgColour, fg=input_fgColour, bd = 0)
        self.with_field = Entry(bg = input_bgColour, fg=input_fgColour, bd = 0)
        a= self.processFinalName(input_data)
        self.name_field.insert(0,a)
        #self.name_field.focus()
        # INPUT FIELD POSITION
        self.name_field.place(x=60, y= 8)
        self.replace_field.place(x=60, y= 8+labelOffset )
        self.with_field.place(x=60, y=33 + labelOffset )
        #
        # BUTTON OPTIONS
        renameBtn = Button(text = 'RENAME', bg = bgColour, fg = 'white', width = 200 , command = partial(self.rename_custom, input_data ) )  #partial(return self.name_field, self.replace_field, self.with_field) )
        # BUTTON POSITION
        renameBtn.pack(side = 'bottom' )
        #
        self.tk.configure(background= bgColour)
        self.tk.bind('<Escape>', quit) # BIND TO ESC KEY
        self.tk.bind('<Return>', partial(self.rename_custom, input_data ))
        #self.tk.bind("<FocusOut>", self.killWindow)
        self.tk.mainloop()
    def rename_custom(self, input_data, *args):
        #print input_data
        self.custom_list = [self.name_field.get(), self.replace_field.get(), self.with_field.get()]
        self.tk.destroy()
        self.manual_rename = 'yes'
        self.rename_auto(input_data)
        #self.RenameWindow(input_data)
    def processRename(self, old, new):
        #print old
        #print new
        #print '#####'
        os.rename(old, new)
    def findImageSequence(self, input_data):
        fileList = []
        processed = self.processInput(input_data)
        file_ext = processed[0]
        file_path = processed[2]
        original_name = self.processFinalName(input_data)
        os.chdir(file_path)
        for files in os.listdir("."):
            if original_name in files:
                X = file_path+files
                if len(self.processFinalName(X)) == len(original_name):
                    if files.endswith(file_ext):
                       fileList.append(files)
        return fileList
    def rename_auto(self, input_data):
        try:
            self.manual_rename
        except AttributeError:
            self.manual_rename = 'no'
        self.selection = [input_data]
        processed = self.processInput(input_data)
        file_path2 = processed[2]
        parent_dir = file_path2[1+[i for i, letter in enumerate(file_path2) if letter == '\\' or letter =='/'][-2]:-1] # find the parent folder name for automatically renaming
        file_extension2 = processed[0]
        original_name2 = self.processFinalName(input_data)
        ##################################################
        #fileList = []
        #os.chdir(file_path2)
        #for files in os.listdir("."):
        #    if original_name2 in files:
        #        test = file_path2+files
        #        if len(self.processFinalName(test)) == len(original_name2):
        #            if files.endswith(file_extension2):
        #               fileList.append(files)
        fileList = self.findImageSequence(input_data)
        iterator = -1
        new_return = [] # this is for the return so the mov converters know what it is now
        ver = self.findVersioning(input_data)
        for x in sorted(fileList):
            #self.findVersioning(x)
            iterator +=1
            if len(str(iterator)) == 1:
                padding = '000'
            elif len(str(iterator)) == 2:
                padding = '00'
            elif len(str(iterator)) == 3:
                padding = '0'
            else:
                padding = ''
            if self.manual_rename == 'yes':
                if self.custom_list[1] != '':
                    replace_name = original_name2.replace(self.custom_list[1], self.custom_list[2])
                    y = replace_name + '_' + padding + str(iterator) + file_extension2
                else:
                    #print 'top'
                    if self.custom_list[0][0] == '_':
                        #print 'suffix'
                        ### this is a suffix
                        y = original_name2 + self.custom_list[0] + '_' + padding + str(iterator) + file_extension2
                    elif self.custom_list[0][-1] == '_':
                        ### this is a prefix
                        y = self.custom_list[0] + original_name2 + '_' + padding + str(iterator) + file_extension2                        
                    else:
                        y = self.custom_list[0] + '_' + padding + str(iterator) + file_extension2
                #y = parent_dir + '_' + padding + str(iterator) + file_extension2
            else:
                if ver == '':
                    y = parent_dir + '_' + padding + str(iterator) + file_extension2
                else:
                    y = parent_dir + '_' + ver + '_' + padding + str(iterator) + file_extension2
            old = file_path2 + x
            new = file_path2 + y
            new_return.append(new)
            self.processRename(old, new)
            #os.rename(old, new)
            #os.rename(old, new)
        return new_return[0] # this is to return any item after it is renamed, for use in other functions
    """
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
    a = 'D:/EXAMPLE_PROJECT/Frostbite_Renders/OMAHA_TT_sc01_sh010_0000.tga'
    K.RenameWindow(a)
    #a = 'D:/EXAMPLE_PROJECT/Frostbite_Renders/OMAHA_TT_sc01_sh025/data_0000.tga'
    #a = 'D:/EXAMPLE_PROJECT/Frostbite_Renders/OMAHA_TT_sc01_sh025/OMAHA_TT_sc01_sh025_0000.tga'
    #a = 'D:/EXAMPLE_PROJECT/Frostbite_Renders/OMAHA_TT_sc01_sh025/OMAHA_TT_sc01_sh250_0006.tga'
    ##a = 'D:/EXAMPLE_PROJECT/Frostbite_Renders/shot_02_v01/OMAHA_TT_sc01_sh025_V02_00.tga'
    #a = 'D:/EXAMPLE_PROJECT/Frostbite_Renders/OMAHA_TT_sc01_sh011/OMAHA_TT_sc01_sh011_V01_0000.tga'
    #K.rename_auto(a)
    #K.RenameWindow(a)