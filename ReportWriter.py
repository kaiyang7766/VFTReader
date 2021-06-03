
from abc import abstractmethod
class ReportWriter:
    @abstractmethod
    def write(self, reportList, filepath):
        pass

    @abstractmethod
    def update(self, newReport, originalReportPath):
        pass
        