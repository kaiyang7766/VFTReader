
from models.ReliabilityMetrics import ReliabilityMetrics
from models.NumDbGraph import NumDbGraph
from models.VFTParams import VFTParams
from models.PatientData import PatientData
from models.VFTResults import VFTResults

class VFTReport:
    """The representation of a Visual Field Test report in the application

    Attributes:
        fileName: The name of the VFT report file.
        patientData: The patient's information.
        params: The parameters of the test.
        results: Information about the results of the test.
        reliability: The reliability metrics of the test.
        fovea: Information regarding the fovea.
        sensitivityGraph: The main numeric dB graph.
        MDGraph: The total deviation graph.
        PSDGraph: The pattern deviation graph.
        checked: 0 if the report has not been revised.
    """
    def __init__(self, fileName, name, eyeSide, datetime, age, dob, ID, FIXLOS, FIXTST, FNR, FPR, testDuration, GHT, VFI, MD, MDp, PSD, PSDp,  pattern, strategy, stimulus, background, foveaRefdB ,SGraphvalues, MDGraphValues, PSDGraphValues, checked):
        self.fileName = fileName
        self.patientData = PatientData(name, eyeSide, datetime, age, dob, ID)
        self.params = VFTParams(pattern, strategy, stimulus, background)
        self.results = VFTResults(GHT, VFI, MD, MDp, PSD, PSDp)
        self.reliability = ReliabilityMetrics(FIXLOS, FIXTST, FNR, FPR, testDuration)
        self.checked = checked
        self.fovea = foveaRefdB

        self.sensitivityGraph = NumDbGraph(SGraphvalues)
        self.MDGraph = NumDbGraph(MDGraphValues)
        self.PSDGraph = NumDbGraph(PSDGraphValues)
    def isChecked(self):
        """Returns the checked status of the report

        Returns:
            int: 0 if the report has not been checked, 1 if otherwise
        """
        return self.checked
    def checked(self):
        """Updates the checked status to '1' (have been checked)
        """
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
    def getSensitivityGraph(self):
        return self.getSensitivityGraph
    def getMDGraph(self):
        return self.MDGraph
    def getPSDGraph(self):
        return self.PSDGraph
    def toDict(self):
        """Creates a dictionary representation of the VFT report. The keys in the dict are the field names, same as those in the sample .csv files, and the values of the dict are the values in the report

        Returns:
            Dict: The dictionary containing the information of the report.
        """
        result =   {
                    "ID": self.getPatientData().getID(),
                    "File name": self.getFileName(),
                    "Name": self.getPatientData().getName(),
                    'Date of Birth':self.getPatientData().getDOB(),
                    'Age':self.getPatientData().getAge(),
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
        if result['Eye']:
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
