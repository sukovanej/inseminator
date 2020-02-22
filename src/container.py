from __future__ import annotations

from typing import Any, Callable, Dict, Type, TypeVar, Union

from .decorator import DecoratorResolver
from .dependency import Dependency, StaticDependency
from .exceptions import ContainerRegisterError
from .resolver import DependencyResolver
from .scoped_dict import ScopedDict

T = TypeVar("T")
Dependable = Union[Callable[..., T], Type[T]]


class Container:
    def __init__(self, parent_scoped_dict: ScopedDict[Dependable, Dependency] = None) -> None:
        self._container: ScopedDict[Dependable, Dependency] = ScopedDict(parent_scoped_dict)
        self._resolver = DependencyResolver(self._container)

    def register(
        self,
        dependency: Type[T],
        *,
        value: T = None,
        factory: Callable[..., T] = None,
        parameters: Dict[str, Dependable] = None,
    ) -> None:
        resolved_dependency: Dependency[T]

        if value is not None and factory is not None:
            raise ContainerRegisterError("Can't decide whether to use factory or value for dependency instantiation")

        if value is not None:
            resolved_dependency = StaticDependency(value)
        elif factory is not None:
            resolved_dependency = self._resolver.resolve(factory, parameters)
        else:
            resolved_dependency = self._resolver.resolve(dependency, parameters)

        self._container[dependency] = resolved_dependency

    def resolve(self, dependency: Type[T], **parameters: Dependable) -> T:
        if dependency not in self._container:
            self.register(dependency, parameters=parameters)

        return self._container[dependency].get_instance()

    def sub_container(self) -> Container:
        return Container(parent_scoped_dict=self._container)

    def inject(self, fn: Callable[..., T]) -> Callable[..., T]:
        decorator_resolver = DecoratorResolver(resolver=self._resolver)
        return decorator_resolver.inject_function(fn)
