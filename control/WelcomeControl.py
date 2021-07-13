
from typing import List
from control.ReportEditControl import ReportEditControl
import tkinter
from control.ExtractionControl import ExtractionControl
from reader.PytesseractReader import PytesseractReader
from writer.CSVWriter import CSVWriter
from views.WelcomeView import WelcomeView
from models.VFTReport import VFTReport
import queue
class WelcomeControl(ExtractionControl):
    """The control class for the welcome activity. 
    
    The current welcome activity also contains the extraction feature.

    Attributes:
        root: The main tk window.
        writer: A .csv writer to write extracted VFT reports.
        views: The UI elements of the activity
        messageQueue: A queue to store messages to be printed to the log window.
        errorQueue: A queue to store errors to be printed to the log window.
        reportList: A list of extracted VFT reports, in VFTReport objects.
        reportReader: The reader for extracting the information out of VFT reports.
    """
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.writer = CSVWriter()
        self.messageQueue = queue.Queue()
        self.errorQueue = queue.Queue()
        self.reportList = None
    def startActivity(self):
        """Initializes the UI elements.
        """
        self.views = WelcomeView(self.root, self)
        
    def extract(self, filepath: str):
        """Extracts the VFT reports in the selected path.

        Args:
            filepath (str): The path to the file/folder containing the VFT reports.
        """
        self.views.disableExtraction()
        self.logMessage("Extracting data at: " + filepath)
        self.reportReader = PytesseractReader(filepath, self)
        self.reportReader.start()
        self.root.after(100, self.checkQueue)
        
    def onFinishExtraction(self, reportList: List[VFTReport]):
        """Method to be called upon finishing extraction.

        Args:
            reportList (List[VFTReport]): The list of extracted report.
        """
        self.reportList = reportList

    def saveReports(self):
        """Save the reports at selected location.
        """
        try:
            outputPath = self.views.onFinishExtraction()
            self.logMessage("Saving data at: "+ outputPath)
            self.writer.write(self.reportList, outputPath)
            self.onFinishSave()
        except PermissionError:
            self.logError("Selected location is not accessible, please select another location")
            self.saveReports()
        except FileNotFoundError:
            self.logError("Directory not found. Please try again.")
        finally:
            self.views.enableExtraction()
        

    def onFinishSave(self):
        """Method to be called upon finishing saving the extracted reports.
        """
        self.logMessage("Data saved successfully")
        self.views.enableExtraction()

    def queueMessage(self, message: str):
        """Queues a normal log message to be printed to the log window.

        Args:
            message (str): The message to be printed
        """
        self.messageQueue.put(message)
    def queueError(self, error: str):
        """Queues an error message to be printed to the log window.
        
        Args:
            error (str): The message to be printed
        """
        self.errorQueue.put(error)
    
    def checkQueue(self):
        """Checks both log message queues for messages to be printed.

        Due to tkinter's limitation, processes from other threads other than the main thread cannot access tkinter's widgets. Therefore, this
        function was created as a workaround to print log messages during the extraction of the VFT reports.
        """
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

    def onNextActivity(self):
        """Moves to the report viewing and editing activity.
        """
        new = ReportEditControl(self.root)
        new.startActivity()
    

    
        