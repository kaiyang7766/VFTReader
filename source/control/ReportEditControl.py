
from tkinter import Tk
from Log import Log
from models.VFTReport import VFTReport
from reader.CSVReader import CSVReader
from views.ReportEditView import ReportEditView
from CSVWriter import CSVWriter
import traceback

class ReportEditControl:
    """Control class for viewing and verifying extracted VFT reports.

    Attributes:
        root: The main Tk window.
        writer: A writer to write the extracted VFT reports. Currently, only .csv writer is implemented. 
        reader: A reader to read the extracted VFT reports. Currently only .csv reader is implemented.
        views: The UI elements of the activity.
        curFile: The file path to the file being viewed by the user. Currently, this should point to a .csv file.
        filelist: The VFT reports read from the selected file.

    """
    def __init__(self, root: Tk):
        """Initializes the control class.

        Args:
            root (Tk): The main Tk window.
        """
        self.root = root
        self.writer = CSVWriter()
        self.reader = CSVReader()
        
    def startActivity(self):
        """Initializes the activity. This should be called right after initializing the control class.
        """
        self.views = ReportEditView(self, self.root)

    def back(self):
        """Return to the previous activity, which is the welcome activity.
        """
        try:
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()
        except:
            from control.WelcomeControl import WelcomeControl
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()

    def readCsv(self, filename: str):
        """Loads the VFT reports into the program from a .csv file. The reports are then represented in VFTReport objects and stored in filelist.

        Args:
            filename (str): The path to the file
        """
        try:
            self.curFile = filename
            self.filelist = self.reader.read(filename)
            namelist = [i.getFileName() for i in self.filelist]
            checklist = [i.isChecked() for i in self.filelist]
            Log.n("Loading reports from " + self.curFile)
            #Display the names of the reports in the list widget
            self.views.displayReportList(namelist, checklist)
        except: #The program may throws an error if the file is currently being opened
            traceback.print_exc()
            Log.e("Error opening file. Ensure that the file is accessible")
    def displayReport(self, index:int):
        """Displays the information of a selected VFT report on the user interface

        Args:
            index (int): The index of the report selected in the list
        """
        self.curReport = self.filelist[index]   #Find the report inside filelist
        Log.n("Displaying report: "+ self.curReport.getFileName())
        #Sets the values inside entry boxes to the values of the selected report
        self.views.GHT.set(self.curReport.results.getGHT())
        self.views.VFI.set(self.curReport.results.getVFI())
        self.views.MD.set(self.curReport.results.getMD())
        self.views.MDp.set(self.curReport.results.getMDp())
        self.views.PSD.set(self.curReport.results.getPSD())
        self.views.PSDp.set(self.curReport.results.getPSDp())
        self.views.patientName.set(self.curReport.getPatientData().getName())
        self.views.patientEye.set(self.curReport.patientData.getEyeSide())
        self.views.patientTestDate.set(self.curReport.patientData.getDatetime())
        self.views.patientAge.set(self.curReport.patientData.getAge())
        self.views.patientBirthDate.set(self.curReport.patientData.getDOB())
        self.views.duration.set(self.curReport.reliability.getTestDuration())
        self.views.FIXLOS.set("/".join((self.curReport.reliability.getFIXLOS(), self.curReport.reliability.getFIXTST())))
        self.views.FPR.set(self.curReport.reliability.getFPR())
        self.views.FNR.set(self.curReport.reliability.getFNR())
        self.views.pattern.set(self.curReport.params.getPattern())
        self.views.background.set(self.curReport.params.getBackground())
        self.views.stimulus.set(self.curReport.params.getStimulus())
        self.views.strategy.set(self.curReport.params.getStrategy())
        self.views.sensitivityGraph.setVariables(self.curReport.sensitivityGraph.getValues())
        self.views.totalDeviationGraph.setVariables(self.curReport.MDGraph.getValues())
        self.views.patternDeviationGraph.setVariables(self.curReport.PSDGraph.getValues())
        if self.views.showWarning():    #Checks for potential errors in displayed values
            self.logFieldWarnings()
        
    def update(self, newReport:VFTReport):
        """Updates the UI after committing the file.

        Args:
            newReport (VFTReport): The new values of the report.
        """
        for i in range(len(self.filelist)):
            if self.filelist[i].getFileName() == newReport.getFileName():
                self.filelist[i] = newReport
                self.displayReport(i)
                break

    def logFieldWarnings(self):
        """Writes a warning about missing fields in the selected report.
        """
        Log.e("There are potentially wrong values in selected report. Please manually check.")

    def saveReport(self):
        """Save the changes to the selected report.

        Returns:
            bool: True if the changes were saved successfully.
        """
        try:
            FIXLOS, FIXTST = self.views.FIXLOS.get().split("/")
            newReport = VFTReport(
                self.curReport.getFileName(),
                self.views.patientName.get(),
                self.views.patientEye.get(),
                self.views.patientTestDate.get(),
                self.views.patientAge.get(),
                self.views.patientBirthDate.get(),
                self.curReport.getPatientData().getID(),
                FIXLOS,
                FIXTST,
                self.views.FNR.get(),
                self.views.FPR.get(),
                self.views.duration.get(),
                self.views.GHT.get(),
                self.views.VFI.get(),
                self.views.MD.get(),
                self.views.MDp.get(),
                self.views.PSD.get(),
                self.views.PSDp.get(),
                self.views.pattern.get(),
                self.views.strategy.get(),
                self.views.stimulus.get(),
                self.views.background.get(),
                self.curReport.getFoveaRefdB(),
                self.views.sensitivityGraph.getVariables(),
                self.views.totalDeviationGraph.getVariables(),
                self.views.patternDeviationGraph.getVariables(),
                1
            )
            self.writer.update(newReport, self.curFile)
            Log.n("Successfully saved changes")
            self.update(newReport)
            
            return True
        except:
            traceback.print_exc()
            Log.e("Error saving changes, make sure that all fields are in correct format")
            return False


