
from abc import abstractmethod
import Log
class ExtractionControl:
    def __init__(self, root):
        self.root = root

    def logNumFiles(self, num):
        Log.n("Found " + str(num) + " files with supported format at directory. Beginning extraction")

    def logCurFile(self, filepath, index, length):
        Log.n("("+ str(index + 1) + "/" + str(length) + ") Extracting report at: " + filepath)

    def logSelectedDirectory(self, dir):
        Log.n("Extracting files at" + dir)

    def logOutputFile(self, outputPath):
        Log.n("Extraction finished. Saving data at " + outputPath)
    def logConfirmation(self,text = "Data saved successfully"):
        Log.n(text)
    def logError(self):
        Log.e("Error: Unable to read data. Skipping file")
    def refresh(self):
        self.root.update()
    @abstractmethod
    def extract(self):
        pass
