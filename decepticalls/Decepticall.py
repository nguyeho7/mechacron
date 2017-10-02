from abc import ABC, abstractmethod

class Decepticall(ABC):
    
    @abstractmethod
    def weekly_report(self) -> str:
        pass

    @abstractmethod
    def daily_report(self) -> str:
        pass
