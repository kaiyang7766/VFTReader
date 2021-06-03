
from models.VFTReport import VFTReport
from CSVReader import CSVReader
from views.ReportEditView import ReportEditView
import numpy as np
import pandas as pd

class ReportEditControl:
    def __init__(self, root):
        self.root = root
        
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
        reader = CSVReader()
        self.filelist = reader.read(filename)
        #TODO: Create proper VFTReport objects
        namelist = [i.getFileName() for i in self.filelist]
        self.views.displayReportList(namelist)
    
    def displayReport(self, index):
        report = self.filelist[index]
        self.views.GHT.set(report.results.getGHT())
        self.views.VFI.set(report.results.getVFI())
        self.views.MD.set(report.results.getMD())
        self.views.MDp.set(report.results.getMDp())
        self.views.PSD.set(report.results.getPSD())
        self.views.PSDp.set(report.results.getPSDp())   
        self.views.patientName.set(report.getFileName())
        self.views.patientEye.set(report.patientData.getEyeSide())
        self.views.patientTestDate.set(report.patientData.getDatetime())
        self.views.duration.set(report.reliability.getTestDuration())
        self.views.FIXLOS.set(report.reliability.getFIXLOS())
        self.views.FPR.set(report.reliability.getFPR())
        self.views.FNR.set(report.reliability.getFNR())
        self.views.pattern.set(report.params.getPattern())
        self.views.background.set(report.params.getBackground())
        self.views.stimulus.set(report.params.getStimulus())
        self.views.strategy.set(report.params.getStrategy())
        self.views.sensitivityGraph.setVariables(report.sensitivityGraph.getValues(), report.patientData.getEyeSide())
        self.views.totalDeviationGraph.setVariables(report.MDGraph.getValues(), report.patientData.getEyeSide())
        self.views.patternDeviationGraph.setVariables(report.PSDGraph.getValues(), report.patientData.getEyeSide())

        
        


