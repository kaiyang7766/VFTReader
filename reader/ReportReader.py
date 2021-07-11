
from abc import abstractmethod
from threading import Thread
from models.VFTReport import VFTReport
class ReportReader(Thread):
    @abstractmethod
    def read(self, dir):
        pass
    @abstractmethod
    def run(self) -> None:
        pass
