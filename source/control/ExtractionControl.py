
from abc import abstractmethod
from tkinter import Tk
from Log import Log
from typing import *
from models.VFTReport import VFTReport
class ExtractionControl:
    """An interface for activities that implements VFT report extraction features.

        Args:
            root (Tk): Root window to contain widgets for the activity.
        """
    def __init__(self, root: Tk):
        self.root = root

    def logMessage(self, message: str):
        """Prints a normal log message to the log window.

        Args:
            message (str): The message to be printed.
        """
        Log.n(message)
    def logError(self, error: str):
        """Prints an error message to the log window.

        Args:
            error (str): The error message.
        """
        Log.e(error)
    @abstractmethod
    def extract(self):
        """Extract the VFT reports specified.
        """
        pass
    @abstractmethod
    def onFinishExtraction(self, reportList: List[VFTReport]):
        """Called on finish extracting all requested VFT reports.

        Args:
            reportList (List[VFTReport]): The list of reports that was extracted.
        """
        pass
