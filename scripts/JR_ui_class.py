import Tkinter as TK
from functools import partial
from JR_system_class import System
class UI(System):
    def __init__(self):
        System.__init__(self)
        self.tk = TK.Tk()
        self.tk.iconbitmap(default= self.images + "\UI\icon.ico") 
    def CreateButtons(self, input_data, color = '#136ec7', title = '', ):
        self.tk = TK.Tk()
        self.BRC = '' # reset button cash on button build call
        self.tk.title(title)
        self.tk.overrideredirect(1)
        text_width = ''
        pointer_x = self.tk.winfo_pointerx()
        pointer_y = self.tk.winfo_pointery()
        i = 0
        for name in input_data.keys():
            text_width += name
            lb = TK.Button(self.tk, text=name, bg = color, fg = 'white', command = partial(self.exec_action, input_data.get(name)) )
            lb.grid(row=1, column=i)
            i += 1
        row_width = len(text_width) * 7.5/2
        middle_width = pointer_x - row_width
        self.tk.geometry('+'+str(int(middle_width))+'+'+str(pointer_y-20) )
        self.tk.bind('<Escape>', quit) # BIND TO ESC KEY
        self.tk.bind("<FocusOut>", self.killWindow)
        #self.tk.withdraw()
        self.tk.mainloop()
    def killWindow(self, event):
        self.tk.destroy()
    def exec_action(self,value):
        exec value
        self.tk.destroy()
    def print_test(self, text):
        print text
#if __name__ == '__main__':
#    K = UI()
#    #names = {'422_Proxy':'Proxy', '422_LT':'Light', '422_Normal':'Normal', '422_HQ':'highquality'}
#    K.CreateButtons(
#        input_data={
#        '422_Proxy':'self.print_test("light")', 
#        '422_LT':'self.print_test("light")', 
#        '422_Normal':'self.print_test("normal")', 
#        '422_HQ':'self.print_test("highquality")'
#        } 
#        )