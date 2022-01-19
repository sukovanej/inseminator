from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

from .decorator import DecoratorResolver
from .dependency import Dependency, StaticDependency
from .exceptions import ContainerRegisterError
from .metrics import Metrics
from .resolver import DependencyResolver
from .scoped_dict import ScopedDict

T = TypeVar("T")

#: Functions returning an instance implemeting T or a class that implements T
Dependable = Union[Callable[..., Any], Any]


class Container:
    """`Container` provides functionality to register and resolve class instances."""

    def __init__(
        self,
        parent_scoped_dict: Optional[ScopedDict[Dependable, Dependency]] = None,
        metrics: Optional[Metrics] = None,
    ) -> None:
        """Container constructor.

        :param parent_scoped_dict: ScopedDict object representing the parent scope of the container.
        :type parent_scoped_dict: ScopedDict[Dependable, Dependency] | None

        :param metrics: Metrics instance to be used in the DecoratorResolver.
        :type metrics: Metrics | None
        """
        self._container: ScopedDict[Dependable, Dependency] = ScopedDict(parent_scoped_dict)
        self._resolver = DependencyResolver(self._container)
        self._metrics = metrics
        self._decorator_resolvers: List[DecoratorResolver] = []

    def set_metrics(self, metrics: Metrics) -> None:
        """Set `Metrics` objects to be used to report metrics.

        :param metrics: ScopedDict object representing the parent scope of the container.
        :type metrics: Metrics

        :rtype: None
        """
        self._metrics = metrics

    def register(
        self,
        dependency: Type[T],
        *,
        value: Optional[T] = None,
        factory: Optional[Callable[..., T]] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register value of factory function / class to be used when dependency of type T is needed.

        Example abstract class with it's implementation::

            from abc import ABC

            class MyInterface(ABC):
                def method(self) -> None:
                    raise NotImplemented

            class MyManager:
                def do_stuff(self) -> None:
                    print("hello")

            class MyImplementation(MyInterface):
                def __init__(self, manager: MyManager) -> None:
                    self._manager = manager

                def method(self) -> None:
                    self._manager.do_stuff()
                    print("world")

        Implementation can be registered using the object instance.::

            container = Container()
            container.register(MyInterface, value=MyImplementation(MyManager()))

        Implementation can be registered using the implementing class. In this case, `MyImplementation` is itself
        resolved in the container.::

            container = Container()
            container.register(MyInterface, factory=MyImplementation)

        Also, implementation can be registered using a callable returning the instance.::

            def create_implementation() -> MyInterface:
                return MyImplementation(MyManager())

            container = Container()
            container.register(MyInterface, factory=create_implementation)


        :param dependency: Type to be registered.
        :type dependency: Type[T]

        :param value: Instance of type T to be provided when Type[T] is required.
        :type value: T

        :param factory: A function that returns instance of T or class that implements T.
        :type factory: Callable[..., T] | Type[T]

        :param parameters: Mapping specifying parameters to be forcefully used when resolving T.
        :type parameters: Dict[str, Any]

        :rtype: None
        """
        resolved_dependency: Dependency

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
        """
        :param dependency: Type to be registered.
        :type dependency: Type[T]

        :keyword parameters: Keyword arguments specifying parameters to be forcefully used when resolving T.

        :return: Instance of type T.
        :rtype: T
        """
        if dependency not in self._container:
            self.register(dependency, parameters=parameters)

        return cast(T, self._container[dependency].get_instance())

    def sub_container(self) -> Container:
        """Creates a new child container. The inner container is passed as a `parent_scoped_dict` constructor parameter.

        :return: New container.
        :rtype: Container
        """
        return Container(parent_scoped_dict=self._container)

    def inject(self, fn: Callable[..., T]) -> Callable[..., T]:
        """Lazily injects parameters into a function. Injected objects **are cached**.

        :param fn: Function to be injected.
        :type fn: Callable[..., T]

        :return: Functions that have injected parameters when invoked.
        :rtype: Callable[..., T]
        """
        decorator_resolver = DecoratorResolver(resolver=self._resolver, metrics=self._metrics)
        self._decorator_resolvers.append(decorator_resolver)
        return decorator_resolver.inject_function(fn)

    def inject_scoped(self, fn: Callable[..., T]) -> Callable[..., T]:
        """Lazily injects parameters into a function. Injected objects **are not cached** and are recreated
        during every invocation of the function.

        :param fn: Function to be injected.
        :type fn: Callable[..., T]

        :return: Functions that have injected parameters when invoked.
        :rtype: Callable[..., T]
        """
        decorator_resolver = DecoratorResolver(resolver=self._resolver, metrics=self._metrics, cache_enabled=False)
        self._decorator_resolvers.append(decorator_resolver)
        return decorator_resolver.inject_function(fn)

    def clear(self) -> None:
        """Clear all cached objects. Also clear all resolved objects for injected functions.

        :rtype: None
        """
        self._container.clear()

        for decorator_resolve in self._decorator_resolvers:
            decorator_resolve.clear_cache()

    def preload_injected(self) -> None:
        """Resolve all objects for injected functions.

        :rtype: None
        """
        for decorator_resolve in self._decorator_resolvers:
            decorator_resolve.preload()
