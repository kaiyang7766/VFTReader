
class ReliabilityMetrics:
    """The reliability metrics in a VFT report

    Attributes:
        FIXLOS: The fixation losses.
        FIXTST: The number of fixation tests.
        FNR: False negative rate.
        FPR: False positive rate.
        testDuration: The duration of the test.
    """
    def __init__(self, FIXLOS,FIXTST, FNR, FPR, testDuration):
        self.FIXLOS = FIXLOS
        self.FIXTST = FIXTST
        self.FNR = FNR
        self.FPR = FPR
        self.testDuration = testDuration

    def getFIXLOS(self):
        return self.FIXLOS

    def getFIXTST(self):
        return self.FIXTST
    def getFNR(self):
        return self.FNR

    def getFPR(self):
        return self.FPR
    def getTestDuration(self):
        return self.testDuration

    def setFIXLOS(self, FIXLOS):
        self.FIXLOS = FIXLOS

    def setFIXTST(self, FIXTST):
        self.FIXTST = FIXTST
    def setFNR(self, FNR):
        self.FNR = FNR

    def setFPR(self, FPR):
        self.FPR = FPR

    def setTestDuration(self, testDuration):
        self.testDuration = testDuration
        