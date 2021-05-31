
class ReliabilityMetrics:
    def __init__(self, FIXLOS, FNR, FPR, testDuration):
        self.FIXLOS = FIXLOS
        self.FNR = FNR
        self.FPR = FPR
        self.testDuration = testDuration

    def getFIXLOS(self):
        return self.FIXLOS

    def getFNR(self):
        return self.FNR

    def getFPR(self):
        return self.FPR
    def getTestDuration(self):
        return self.testDuration

    def setFIXLOS(self, FIXLOS):
        self.FIXLOS = FIXLOS

    def setFNR(self, FNR):
        self.FNR = FNR

    def setFPR(self, FPR):
        self.FPR = FPR

    def setTestDuration(self, testDuration):
        self.testDuration = testDuration
        