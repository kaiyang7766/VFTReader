
class VFTParams:
    def __init__(self, pattern, strategy, stimulus, background):
        self.pattern = pattern
        self.stimulus =stimulus
        self.background = background
        self.strategy = strategy
    def getPattern(self):
        return self.pattern
    def setPattern(self, pattern):
        self.pattern = pattern
    def getStrategy(self):
        return self.strategy
    def setStrategy(self, strategy):
        self.strategy = strategy
    def getBackground(self):
        return self.background
    def setBackground(self, background):
        self.background = background
    def getStimulus(self):
        return self.stimulus
    def setStimulus(self, stimulus):
        self.stimulus =stimulus