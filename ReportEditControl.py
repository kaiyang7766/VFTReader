
from ExtractionControl import ExtractionControl
from models.VFTReport import VFTReport
from reader.CSVReader import CSVReader
from views.ReportEditView import ReportEditView
import numpy as np
import pandas as pd
from CSVWriter import CSVWriter


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
            from WelcomeControl import WelcomeControl
            newActivity = WelcomeControl(self.root)
            newActivity.startActivity()

    def readCsv(self, filename):
        
        self.curFile = filename
        self.filelist = self.reader.read(filename)
        #TODO: Create proper VFTReport objects
        namelist = [i.getFileName() for i in self.filelist]
        self.views.displayReportList(namelist)
    
    def displayReport(self, index):
        self.curReport = self.filelist[index]
        self.views.GHT.set(self.curReport.results.getGHT())
        self.views.VFI.set(self.curReport.results.getVFI())
        self.views.MD.set(self.curReport.results.getMD())
        self.views.MDp.set(self.curReport.results.getMDp())
        self.views.PSD.set(self.curReport.results.getPSD())
        self.views.PSDp.set(self.curReport.results.getPSDp())
        self.views.patientName.set(self.curReport.getFileName())
        self.views.patientEye.set(self.curReport.patientData.getEyeSide())
        self.views.patientTestDate.set(self.curReport.patientData.getDatetime())
        self.views.duration.set(self.curReport.reliability.getTestDuration())
        self.views.FIXLOS.set(self.curReport.reliability.getFIXLOS())
        self.views.FPR.set(self.curReport.reliability.getFPR())
        self.views.FNR.set(self.curReport.reliability.getFNR())
        self.views.pattern.set(self.curReport.params.getPattern())
        self.views.background.set(self.curReport.params.getBackground())
        self.views.stimulus.set(self.curReport.params.getStimulus())
        self.views.strategy.set(self.curReport.params.getStrategy())
        self.views.sensitivityGraph.setVariables(self.curReport.sensitivityGraph.getValues(), self.curReport.patientData.getEyeSide())
        self.views.totalDeviationGraph.setVariables(self.curReport.MDGraph.getValues(), self.curReport.patientData.getEyeSide())
        self.views.patternDeviationGraph.setVariables(self.curReport.PSDGraph.getValues(), self.curReport.patientData.getEyeSide())
        
    def update(self):
        pass
    
    def saveReport(self):
        try:
            newReport = VFTReport(
                self.curReport.getFileName(),
                self.views.patientEye.get(),
                self.views.patientTestDate.get(),
                self.curReport.getPatientData().getAge(),
                self.curReport.getPatientData().getID(),
                self.views.FIXLOS.get(),
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
                True
            )
            self.writer.update(newReport, self.curFile)
            return True
        except:
            return False


