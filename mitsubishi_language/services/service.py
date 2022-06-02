from abc import ABC, abstractmethod

class Service(ABC):

    @property
    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        The name of the mitsubishi service.
        """

        pass

    @staticmethod
    @abstractmethod
    def insert(value):
        pass