from abc import ABC, abstractmethod

class Uuid(ABC):
    @abstractmethod
    def uuid4(self):
        pass