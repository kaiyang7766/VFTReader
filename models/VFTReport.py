
from models.ReliabilityMetrics import ReliabilityMetrics
from models.NumDbGraph import NumDbGraph
from models.VFTParams import VFTParams
from models.PatientData import PatientData
from models.VFTResults import VFTResults

class VFTReport:
    def __init__(self, fileName, eyeSide, datetime, age, FIXLOS, FNR, FPR, testDuration, GHT, VFI, MD, MDp, PSD, PSDp,  pattern, strategy, stimulus, background, SGraphvalues, MDGraphValues, PSDGraphValues, checked):
        self.fileName = fileName
        self.patientData = PatientData(eyeSide, datetime, age)
        self.params = VFTParams(pattern, strategy, stimulus, background)
        self.results = VFTResults(GHT, VFI, MD, MDp, PSD, PSDp)
        self.reliability = ReliabilityMetrics(FIXLOS, FNR, FPR, testDuration)
        self.checked = checked

        self.sensitivityGraph = NumDbGraph(SGraphvalues)
        self.MDGraph = NumDbGraph(MDGraphValues)
        self.PSDGraph = NumDbGraph(PSDGraphValues)
    def isChecked(self):
        return self.checked

    def getFileName(self):
        return self.fileName
    
    
