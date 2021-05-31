
from abc import abstractmethod


class ReportReader:
    @abstractmethod
    def read(self, filepath):
        pass
