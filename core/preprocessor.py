from abc import ABC, abstractmethod


class Preprocessor(ABC):

    @abstractmethod
    def __call__(self, cluster):
        pass
