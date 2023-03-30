from abc import ABC, abstractmethod


class Driver(ABC):
    @abstractmethod
    def restart(self):
        pass
