from abc import abstractmethod


class IDatabaseManager:
    @abstractmethod
    def connect(self):
        pass

    @property
    def db(self):
        pass