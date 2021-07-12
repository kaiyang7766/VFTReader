
from typing import List


class NumDbGraph:
    """The numerical dB graph component of a VFT report.

    Inside the application, numerical dB graphs are to be represented as a 10 x 10 2D list.

    Attributes:
        values: The values of the numerical dB graph.
    """
    def __init__(self, values: List[List[str]]) -> None:
        self.values = values

    def setValues(self, new):
        self.values = new

    def getValues(self):
        return self.values

