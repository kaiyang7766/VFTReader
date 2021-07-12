
from abc import abstractmethod
class ReportWriter:
    """Interface for all writer classes.
    """
    @abstractmethod
    def write(self, reportList, filepath):
        """Writes a list of VFT reports to a file.

        Args:
            reportList (List[VFTReport]): The list of reports to be saved to a file.
            filepath (str): The path to the .csv file.
        """
        pass

    @abstractmethod
    def update(self, newReport, originalReportPath):
        """Commits all changes to a report from the user.

        Args:
            newReport (VFTReport): The new values for the report.
            originalReportPath (str): The path to the original file.
        """
        pass
        