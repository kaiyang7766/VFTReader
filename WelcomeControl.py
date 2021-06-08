
from PytesseractReader import PytesseractReader
from CSVWriter import CSVWriter
from views.WelcomeView import WelcomeView

class WelcomeControl:
    def __init__(self, root):
        self.root = root
        self.writer = CSVWriter()
        self.filereader = PytesseractReader()

    def startActivity(self):
        self.views = WelcomeView(self.root, self)
        
    def extract(self, filepath):
        reportList = self.filereader.read(filepath)
        self.writer.write(reportList, filepath)
        outputPath = self.views.onFinishExtraction()
        self.writer.write(reportList, outputPath)
    def onNextActivity():
        pass
    

    
        