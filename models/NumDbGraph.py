
class NumDbGraph:
    def __init__(self, values) -> None:
        self.values = values

    def setValue(self, index, new):
        self.values[index] = new

    def getValues(self):
        return self.values

