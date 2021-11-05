from typing import Any, Protocol


class Dependency(Protocol):
    def get_instance(self) -> Any:
        raise NotImplementedError


class StaticDependency:
    def __init__(self, instance: Any) -> None:
        self.__instance = instance

    def get_instance(self) -> Any:
        return self.__instance
