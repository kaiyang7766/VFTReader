
from abc import abstractmethod
import Log
class ExtractionControl:
    def __init__(self, root):
        self.root = root

    def logMessage(self, message):
        Log.n(message)
    def logError(self, error):
        Log.e(error)
    @abstractmethod
    def extract(self):
        pass
    @abstractmethod
    def onFinishExtraction(self, reportList):
        pass
