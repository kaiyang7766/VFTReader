
from abc import abstractmethod
from threading import Thread

class ReportReader(Thread):
    @abstractmethod
    def read(self, dir):
        pass
    @abstractmethod
    def run(self) -> None:
        pass
