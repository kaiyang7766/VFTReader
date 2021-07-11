
from abc import abstractmethod
from tkinter import Tk
import Log
class ExtractionControl:
    """An interface for activities that implements VFT report extraction features

        Args:
            root (Tk): Root window to contain widgets for the activity
        """
    def __init__(self, root: Tk):
        self.root = root

    def logMessage(self, message: str):
        """Prints a normal log message to the log window

        Args:
            message (str): 
        """
        Log.n(message)
    def logError(self, error: str):
        Log.e(error)
    @abstractmethod
    def extract(self):
        pass
    @abstractmethod
    def onFinishExtraction(self, reportList):
        pass
