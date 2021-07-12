
from abc import abstractmethod
from threading import Thread
from typing import List
from models.VFTReport import VFTReport
class ReportReader(Thread):
    """An interface for VFT report readers.

    """
    @abstractmethod
    def read(self, dir) -> List[VFTReport]:
        """[summary]

        Args:
            dir (str): The directory containing all VFT reports to be extracted.

        Returns:
            List[VFTReport]: The extracted reports.
        """
        pass
