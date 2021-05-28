
from tkinter import *

class LogView(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.text = Text(self, wrap=None, highlightbackground="#d6d6d6")
        self.vsb = Scrollbar(self, command=self.text.yview, orient="vertical")
        self.text.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_configure("even", background="#AAAAAA")
        self.text.tag_configure("odd", background="#FFFFFF")
        self.pack()
        with open(__file__, "r") as f:
            tag = "odd"
            for line in f.readlines():
                self.text.insert("end", line, tag)
                tag = "even" if tag == "odd" else "odd"
        