from control.ReportEditControl import ReportEditControl
from tkinter import *
from tkinter.font import families
import Constants
from tkinter import filedialog


class WelcomeView:
    """UI components for the welcome activity.
    """
    def __init__(self, root, control):
        """Initializes the UI elements

        Args:
            root (Tk): The main application window.
            control (WelcomeControl): The control of the activity. 
        """
        self.root = root
        self.control = control
        self.mainFrame = Frame(root)
        self.mainFrame.pack(fill = "both", expand= True)
        self.welcomeMessage = Label(self.mainFrame, text= "WELCOME\nVisual Field Test report reader", font= ("Arial", 36), padx= 20, pady = 20)
        self.welcomeMessage.pack(fill = "x")
        self.welcomeMessage.place(anchor = "n",relx = 0.5, rely=0.12)
        
        self.inputFrame = Frame(self.mainFrame)
        self.inputFrame.pack(fill = "x")
        self.inputFrame.place(relx= 0.1, rely = 0.4, relwidth= 0.80, relheight = 0.2)

        self.inputLabel = Label(self.inputFrame, text="Input directory: ", padx = 30)
        self.inputLabel.place(relx = 0)
        
        self.inputPath = StringVar()
        self.inputPath.set("")
        self.inputPathEntry = Entry(self.inputFrame, textvariable= self.inputPath)
        self.inputPathEntry.place(relx = 0.2, relwidth = 0.6)

        self.browseInputDirButton = Button(self.inputFrame, text= "Browse", command = self.onBrowseDirectory)
        self.browseInputDirButton.place(relx = 0.85)
        
        self.extractButton = Button(self.mainFrame, text = "Extract", command = self.onExtractRequest)
        self.extractButton.pack(side = "bottom", expand = True)
        self.extractButton.place(anchor = "n",relx = 0.5, rely = 0.6)
        
        self.reviewButton = Button(self.mainFrame, text = "Review", command = self.onNextActivity)
        self.reviewButton.pack(side = "bottom", expand = True)
        self.reviewButton.place(anchor = "n", relx = 0.5, rely = 0.7)
        self.start()
        
    def onNextActivity(self):
        """Method to call upon selecting to move to next activity
        """
        self.mainFrame.destroy()
        self.control.onNextActivity()
        
    def onBrowseDirectory(self)->None:
        """Method to be called upon clicking the "Browse" button.
        """
        path = filedialog.askdirectory()
        self.inputPath.set(path)
    def onExtractRequest(self):
        """Method to be called upon clicking the "Extract" button.
        """
        self.control.extract(self.inputPath.get())
    def onFinishExtraction(self):
        """Method to be called after activity's control finished extracting selected reports.

        Asks the user for a location to save the extracted reports.

        Returns:
            str: The path specified by the user
        """
        file = filedialog.asksaveasfilename(filetypes = (("CSV Files","*.csv"),), defaultextension = ".csv")
        return file
    def disableExtraction(self):
        """Disables the extract button. Used during the extraction process.
        """
        self.extractButton.config(state= DISABLED)
    def enableExtraction(self):
        """Enables the extract button. Used after the extraction process.
        """
        self.extractButton.config(state= NORMAL)
    def start(self)-> None:
        pass


        

    

        
        
    
        

        
        

        
    
        
        