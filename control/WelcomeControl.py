
import tkinter
from control.ExtractionControl import ExtractionControl
from reader.PytesseractReader import PytesseractReader
from CSVWriter import CSVWriter
from views.WelcomeView import WelcomeView
import queue
import Log
class WelcomeControl(ExtractionControl):
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.writer = CSVWriter()
        self.messageQueue = queue.Queue()
        self.errorQueue = queue.Queue()
        self.reportList = None
    def startActivity(self):
        self.views = WelcomeView(self.root, self)
        
    def extract(self, filepath):
        self.views.disableExtraction()
        self.logMessage("Extracting data at: " + filepath)
        self.reportReader = PytesseractReader(filepath, self)
        self.reportReader.start()
        self.root.after(100, self.checkQueue)
        
    def onFinishExtraction(self, reportList):
        self.reportList = reportList

    def saveReports(self):
        try:
            outputPath = self.views.onFinishExtraction()
            self.logMessage("Saving data at: "+ outputPath)
            self.writer.write(self.reportList, outputPath)
            self.onFinishSave()
        except PermissionError:
            self.logError("Selected location is not accessible, please select another location")
            self.saveReports()
    def onFinishSave(self):
        self.logMessage("Data saved successfully")
        self.views.enableExtraction()

    def queueMessage(self, message):
        self.messageQueue.put(message)
    def queueError(self, error):
        self.errorQueue.put(error)
    
    def checkQueue(self):
        try: 
            message = self.messageQueue.get(False)
            if message == 0:
                self.saveReports()
            else:
                self.logMessage(message)
                self.logError(self.errorQueue.get(False))
                self.root.after(100, self.checkQueue)   
        except queue.Empty:
            self.root.after(50, self.checkQueue)

    def onNextActivity():
        pass
    

    
        