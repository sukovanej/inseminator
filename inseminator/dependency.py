from typing import Any, Protocol


class Dependency(Protocol):
    """Protocol specifying `Dependency` interface."""

    def get_instance(self) -> Any:
        """Returns the resolved dependency."""
        raise NotImplementedError


class StaticDependency:
    """Implementes the `Dependency` interface for static dependencies."""

    def __init__(self, instance: Any) -> None:
        """StaticDependency constructor.

        :param instance: The constructed dependency.

        :return: The constructed dependency.
        """
        self.__instance = instance

    def get_instance(self) -> Any:
        """Returns the resolved dependency.

        :return: The constructed dependency.
        """
        return self.__instance
