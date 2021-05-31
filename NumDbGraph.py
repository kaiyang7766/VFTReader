
class NumDbGraph:
    def __init__(self, tag) -> None:
        self.tag = tag
        self.values = []

    def setValue(self, index, new):
        self.values[index] = new

    def getValues(self):
        return self.values

