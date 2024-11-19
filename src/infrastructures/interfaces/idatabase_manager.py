from abc import ABC, abstractmethod


class IDatabaseManager(ABC):
    @abstractmethod
    def connect(self):
        pass

    @property
    def db(self):
        pass