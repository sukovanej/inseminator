from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from .decorator import DecoratorResolver
from .dependency import Dependency, StaticDependency
from .exceptions import ContainerRegisterError
from .metrics import Metrics
from .resolver import DependencyResolver
from .scoped_dict import ScopedDict

T = TypeVar("T")
Dependable = Union[Callable[..., T], Type[T]]


class Container:
    def __init__(
        self, parent_scoped_dict: Optional[ScopedDict[Dependable, Dependency]] = None, metrics: Optional[Metrics] = None
    ) -> None:
        self._container: ScopedDict[Dependable, Dependency] = ScopedDict(parent_scoped_dict)
        self._resolver = DependencyResolver(self._container)
        self._metrics = metrics
        self._decorator_resolvers: List[DecoratorResolver] = []

    def set_metrics(self, metrics: Metrics) -> None:
        self._metrics = metrics

    def register(
        self,
        dependency: Type[T],
        *,
        value: Optional[T] = None,
        factory: Optional[Callable[..., T]] = None,
        parameters: Optional[Dict[str, Dependable]] = None,
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
        decorator_resolver = DecoratorResolver(resolver=self._resolver, metrics=self._metrics)
        self._decorator_resolvers.append(decorator_resolver)
        return decorator_resolver.inject_function(fn)

    def inject_scoped(self, fn: Callable[..., T]) -> Callable[..., T]:
        decorator_resolver = DecoratorResolver(resolver=self._resolver, metrics=self._metrics, cache_enabled=False)
        self._decorator_resolvers.append(decorator_resolver)
        return decorator_resolver.inject_function(fn)

    def clear(self) -> None:
        self._container.clear()

        for decorator_resolve in self._decorator_resolvers:
            decorator_resolve.clear_cache()

    def preload_injected(self) -> None:
        for decorator_resolve in self._decorator_resolvers:
            decorator_resolve.preload()
