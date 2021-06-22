
import Log
from models.VFTReport import VFTReport
from reader.CSVReader import CSVReader
from views.ReportEditView import ReportEditView
from CSVWriter import CSVWriter
import traceback

class ReportEditControl():
    def __init__(self, root):
        self.root = root
        self.writer = CSVWriter()
        self.reader = CSVReader()
        
    def startActivity(self):
        self.views = ReportEditView(self, self.root)

    def back(self):
        try:
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()
        except:
            from control.WelcomeControl import WelcomeControl
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()

    def readCsv(self, filename):
        try:
            self.curFile = filename
            self.filelist = self.reader.read(filename)
            #TODO: Create proper VFTReport objects
            namelist = [i.getFileName() for i in self.filelist]
            checklist = [i.isChecked() for i in self.filelist]
            Log.n("Loading reports from " + self.curFile)
            self.views.displayReportList(namelist, checklist)
        except:
            traceback.print_exc()
            Log.e("Error opening file. Ensure that the file is accessible")
    def displayReport(self, index):
        self.curReport = self.filelist[index]
        Log.n("Displaying report: "+ self.curReport.getFileName())
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
        if self.views.showWarning():
            self.logFieldWarnings()
        
    def update(self, newReport):
        for i in range(len(self.filelist)):
            if self.filelist[i].getFileName() == newReport.getFileName():
                self.filelist[i] = newReport
                self.displayReport(i)
                break

    def logFieldWarnings(self):
        Log.e("There are potentially wrong values in selected report. Please manually check.")

    def saveReport(self):
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


