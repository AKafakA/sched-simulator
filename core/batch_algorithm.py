from abc import ABC, abstractmethod


class BatchAlgorithm(ABC):

    def __init__(self, batch):
        self.batch = batch

    @abstractmethod
    def __call__(self, cluster, clock):
        pass