from ReportEditControl import ReportEditControl
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
        self.inputFrame.place(relx= 0, rely = 0.4, relwidth= 1)

        self.inputHint = Label(self.inputFrame, text="Input directory: ", padx = 30)
        self.inputHint.pack(side = "left")
        
        #TODO: Create logic for default path 
        self.inputPath = StringVar()
        self.inputPath.set("This is a default path")
        self.inputPathEntry = Entry(self.inputFrame, textvariable= self.inputPath, width= 70)
        self.inputPathEntry.pack(fill = "y", side = "left", expand= False)

        self.browseInputDir = Button(self.inputFrame, text= "Browse", command = self.onBrowseDirectory)
        self.browseInputDir.pack(fill = "y", side = "left", expand= False, padx= 10)
        
        self.extractButton = Button(self.main, text = "Extract", command = self.onExtractRequest)
        self.extractButton.pack(side = "bottom", expand = True)
        self.extractButton.place(anchor = "n",relx = 0.5, rely = 0.6)
        
        self.continueButton = Button(self.main, text = "Continue", command = self.onNextActivity)
        self.continueButton.pack(side = "bottom", expand = True)
        self.continueButton.place(anchor = "n", relx = 0.5, rely = 0.7)
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
        file = filedialog.asksaveasfile(filetypes = ("CSV Document", "*.csv"), defaultextension = ("CSV Document", "*.csv"))
        return file
        
    def start(self)-> None:
        pass


        

    

        
        
    
        

        
        

        
    
        
        