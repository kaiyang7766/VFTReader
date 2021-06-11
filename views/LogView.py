
from tkinter import *
from datetime import datetime
class LogView(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.text = Text(self, wrap=None, highlightbackground="#d6d6d6")
        self.vsb = Scrollbar(self, command=self.text.yview, orient="vertical")
        self.text.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_configure("n", background="#AAAAAA")
        self.text.tag_configure("e", background="#FFFFFF")
        self.pack()
        
            
    def print(self, text, tag = "n"):
        text =  ">>[" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] " + text
        self.text.insert("end", text, tag)