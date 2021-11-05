from abc import ABC, abstractmethod


class Metrics(ABC):
    @abstractmethod
    def save_metric(self, name: str, time_spent: float) -> None:
        ...
