
from models.ReliabilityMetrics import ReliabilityMetrics
from models.NumDbGraph import NumDbGraph
from models.VFTParams import VFTParams
from models.PatientData import PatientData
from models.VFTResults import VFTResults

class VFTReport:
    def __init__(self, fileName, eyeSide, datetime, age, ID, FIXLOS, FIXTST, FNR, FPR, testDuration, GHT, VFI, MD, MDp, PSD, PSDp,  pattern, strategy, stimulus, background, foveaRefdB ,SGraphvalues, MDGraphValues, PSDGraphValues, checked):
        self.fileName = fileName
        self.patientData = PatientData(eyeSide, datetime, age, ID)
        self.params = VFTParams(pattern, strategy, stimulus, background)
        self.results = VFTResults(GHT, VFI, MD, MDp, PSD, PSDp)
        self.reliability = ReliabilityMetrics(FIXLOS, FIXTST, FNR, FPR, testDuration)
        self.checked = checked
        self.fovea = foveaRefdB

        self.sensitivityGraph = NumDbGraph(SGraphvalues)
        self.MDGraph = NumDbGraph(MDGraphValues)
        self.PSDGraph = NumDbGraph(PSDGraphValues)
    def isChecked(self):
        return self.checked
    def checked(self):
        self.checked = 1
    def getFileName(self):
        return self.fileName

    def getPatientData(self):
        return self.patientData
    
    def getReliabilityMetrics(self):
        return self.reliability

    def getTestParams(self):
        return self.params

    def getResults(self):
        return self.results

    def getFoveaRefdB(self):
        return self.fovea    
    
    def toDict(self):
        result =   {
                    "ID": self.getPatientData().getID(),
                    "Name": self.getFileName(),
                    "Visit": self.getPatientData().getDatetime(),
                    "Eye": self.getPatientData().getEyeSide(),
                    "Pattern": self.getTestParams().getPattern(),
                    "Strategy": self.getTestParams().getStrategy(),
                    "Stimulus": self.getTestParams().getStimulus(),
                    "Background": self.getTestParams().getBackground(),
                    "Duration": self.getReliabilityMetrics().getTestDuration(),
                    "FixLos": self.getReliabilityMetrics().getFIXLOS(),
                    "FixTst": self.getReliabilityMetrics().getFIXTST(),
                    "FNRate": self.getReliabilityMetrics().getFNR(),
                    "FPRate": self.getReliabilityMetrics().getFPR(),
                    "MD": self.getResults().getMD(),
                    "MDp": self.getResults().getMDp(),
                    "PSD": self.getResults().getPSD(),
                    "PSDp": self.getResults().getPSDp(),
                    "VFI": self.getResults().getVFI(),
                    "GHT": self.getResults().getGHT(),
                    "FoveaRefdB": self.getFoveaRefdB()
                }
        if result["Eye"].lower() == "right":
            index = 1
            for i in range(10):
                for j in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        pass
                    else:
                        if self.sensitivityGraph.getValues()[i][j] == "" or self.sensitivityGraph.getValues()[i][j] == "NA" or self.sensitivityGraph.getValues()[i][j] == None:
                            result["T" + str(index)] = "NA"
                        else:
                            result["T" + str(index)] = self.sensitivityGraph.getValues()[i][j]
                        index +=1
            index = 1
            for i in range(10):
                for j in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        pass
                    else:
                        if self.MDGraph.getValues()[i][j] == "" or self.MDGraph.getValues()[i][j] == "NA" or self.MDGraph.getValues()[i][j] == None:
                            result["MD" + str(index)] = "NA"
                        else:
                            result["MD" + str(index)] = self.MDGraph.getValues()[i][j]
                        index +=1
            index = 1
            for i in range(10):
                for j in range(10):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        pass
                    else:
                        if self.PSDGraph.getValues()[i][j] == "" or self.PSDGraph.getValues()[i][j] == "NA" or self.PSDGraph.getValues()[i][j] == None:
                            result["PSD" + str(index)] = "NA"
                        else:
                            result["PSD" + str(index)] = self.PSDGraph.getValues()[i][j]
                        index +=1
        else:
            index = 1
            for i in range(10):
                for j in range(9, -1, -1):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        pass
                    else:
                        if self.sensitivityGraph.getValues()[i][j] == "" or self.sensitivityGraph.getValues()[i][j] == "NA" or self.sensitivityGraph.getValues()[i][j] == None:
                            result["T" + str(index)] = "NA"
                        else:
                            result["T" + str(index)] = self.sensitivityGraph.getValues()[i][j]
                        index +=1
            index = 1
            for i in range(10):
                for j in range(9, -1, -1):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        pass
                    else:
                        if self.MDGraph.getValues()[i][j] == "" or self.MDGraph.getValues()[i][j] == "NA" or self.MDGraph.getValues()[i][j] == None:
                            result["MD" + str(index)] = "NA"
                        else:
                            result["MD" + str(index)] = self.MDGraph.getValues()[i][j]
                        index +=1
            index = 1
            for i in range(10):
                for j in range(9, -1, -1):
                    if i + j <=2 or i+j >=16 or i - j >= 7 or j - i >=7:
                        pass
                    else:
                        if self.PSDGraph.getValues()[i][j] == "" or self.PSDGraph.getValues()[i][j] == "NA" or self.PSDGraph.getValues()[i][j] == None:
                            result["PSD" + str(index)] = "NA"
                        else:
                            result["PSD" + str(index)] = self.PSDGraph.getValues()[i][j]
                        index +=1

        result["checked"] = self.isChecked()
        return result
