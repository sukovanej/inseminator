from typing import Any, Callable, Dict, Type, TypeVar, Union

from .dependency import Dependency, StaticDependency
from .exceptions import ContainerRegisterError
from .injector import DependencyResolver

T = TypeVar("T")
Dependable = Union[Callable[..., T], Type[T]]


class Container:
    def __init__(self) -> None:
        self._container: Dict[Dependable, Dependency] = {}
        self._resolver = DependencyResolver(self._container)

    def register(
        self, dependency: Type[T], value: T = None, factory: Callable[..., T] = None
    ) -> None:
        resolved_dependency: Dependency[T]

        if value is not None and factory is not None:
            raise ContainerRegisterError(
                "Can't decide whether to use factory or value for dependency instantiation"
            )

        if value is not None:
            resolved_dependency = StaticDependency(value)
        elif factory is not None:
            resolved_dependency = self._resolver.resolve(factory)
        else:
            resolved_dependency = self._resolver.resolve(dependency)

        self._container[dependency] = resolved_dependency

    def resolve(self, dependency: Type[T]) -> T:
        if dependency not in self._container:
            self.register(dependency)

        return self._container[dependency].get_instance()
