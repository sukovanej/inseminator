from typing import Any, Generic, Protocol, TypeVar

T = TypeVar("T", covariant=True)


class Dependency(Protocol, Generic[T]):
    def get_instance(self) -> T:
        raise NotImplementedError


class StaticDependency(Generic[T]):
    def __init__(self, instance: T) -> None:
        self.__instance = instance

    def get_instance(self) -> T:
        return self.__instance
