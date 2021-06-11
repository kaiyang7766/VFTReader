
from ExtractionControl import ExtractionControl
from reader.PytesseractReader import PytesseractReader
from CSVWriter import CSVWriter
from views.WelcomeView import WelcomeView
import Log
class WelcomeControl(ExtractionControl):
    def __init__(self, root):
        self.root = root
        self.writer = CSVWriter()
        self.filereader = PytesseractReader()

    def startActivity(self):
        self.views = WelcomeView(self.root, self)
        
    def extract(self, filepath):
        self.logSelectedDirectory(filepath)
        reportList = self.filereader.read(filepath, self)
        outputPath = self.views.onFinishExtraction()
        self.logOutputFile(outputPath)
        self.writer.write(reportList, outputPath)
        

    def onNextActivity():
        pass
    

    
        