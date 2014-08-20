from Tkinter import *
from functools import partial
from JR_system_class import System
A = System()
root = Tk()

#names = {'422_Proxy':'Proxy', '422_LT':'Light', '422_Normal':'Normal', '422_HQ':'highquality'}
names = {'422_Normal':"test2()"}
color = '#136ec7'
entry = {}
button = {}
#
test = ''
x1 = root.winfo_pointerx()
y1 = root.winfo_pointery()
root.title('')
root.overrideredirect(1)

root.iconbitmap(default= A.images + "\UI\icon.ico") 

def test2():
    print 'value'
def print_all_entries(value):
	exec value
	root.destroy()
i = 0
for name in names.keys():
	test += name
	lb = Button(root, text=name, bg = color, fg = 'white', command = partial(print_all_entries, names.get(name)) )
	lb.grid(row=1, column=i)
	button[name] = lb
	i += 1
tt = len(test) * 7.5/2
ss = x1 - tt
#w=(root.winfo_screenwidth()*5)//6
#h=root.winfo_screenheight()//15
#root.minsize(w,h)
#root.maxsize(w,h)
root.geometry('+'+str(int(ss))+'+'+str(y1-5) )
mainloop()