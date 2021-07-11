from control.ReportEditControl import ReportEditControl
from tkinter import *
from tkinter.font import families
import Constants
from tkinter import filedialog


class WelcomeView:
    def __init__(self, root, control):
        self.root = root
        self.control = control
        self.main = Frame(root)
        self.main.pack(fill = "both", expand= True)
        self.welcomeMessage = Label(self.main, text= "WELCOME", font= ("Arial", 44), padx= 20, pady = 20)
        self.welcomeMessage.pack(fill = "x")
        self.welcomeMessage.place(anchor = "n",relx = 0.5, rely=0.12)
        
        self.inputFrame = Frame(self.main)
        self.inputFrame.pack(fill = "x")
        self.inputFrame.place(relx= 0.1, rely = 0.4, relwidth= 0.80, relheight = 0.2)

        self.inputLabel = Label(self.inputFrame, text="Input directory: ", padx = 30)
        self.inputLabel.place(relx = 0)
        
        self.inputPath = StringVar()
        self.inputPath.set("")
        self.inputPathEntry = Entry(self.inputFrame, textvariable= self.inputPath)
        self.inputPathEntry.place(relx = 0.2, relwidth = 0.6)

        self.browseInputDir = Button(self.inputFrame, text= "Browse", command = self.onBrowseDirectory)
        self.browseInputDir.place(relx = 0.85)
        
        self.extractButton = Button(self.main, text = "Extract", command = self.onExtractRequest)
        self.extractButton.pack(side = "bottom", expand = True)
        self.extractButton.place(anchor = "n",relx = 0.5, rely = 0.6)
        
        self.reviewButton = Button(self.main, text = "Review", command = self.onNextActivity)
        self.reviewButton.pack(side = "bottom", expand = True)
        self.reviewButton.place(anchor = "n", relx = 0.5, rely = 0.7)
        self.start()
        
    def onNextActivity(self):
        self.main.destroy()
        new = ReportEditControl(self.root)
        new.startActivity()
        
    def onBrowseDirectory(self)->None:
        path = filedialog.askdirectory()
        self.inputPath.set(path)
    def onExtractRequest(self):
        self.control.extract(self.inputPath.get())
    def onFinishExtraction(self):
        file = filedialog.asksaveasfilename(filetypes = (("CSV Files","*.csv"),), defaultextension = ".csv")
        return file
    def disableExtraction(self):
        self.extractButton.config(state= DISABLED)
    def enableExtraction(self):
        self.extractButton.config(state= NORMAL)
    def start(self)-> None:
        pass


        

    

        
        
    
        

        
        

        
    
        
        