from abc import ABC, abstractmethod


class Metrics(ABC):
    """Abstract class declaring interface for collecting metrics from decorator resolver."""

    @abstractmethod
    def save_metric(self, name: str, time_spent: float) -> None:
        """This method is triggered whenever there is something to measure.

        :param name: Name of the metric.
        :type name: str

        :param time_spent: The measured time
        :type time_spent: float

        :rtype: None
        """
        ...
