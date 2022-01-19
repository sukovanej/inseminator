import inspect
import time
from functools import wraps
from threading import Lock
from typing import Any, Callable, Dict, Mapping, Optional, Type, TypeVar, cast

from .metrics import Metrics
from .resolver import DependencyResolver


class DecoratorResolver:
    """Class used internally to provide functionality for ``inject`` decorator."""

    def __init__(
        self, resolver: DependencyResolver, metrics: Optional[Metrics] = None, cache_enabled: bool = True
    ) -> None:
        """DecoratorResolver constructor.

        :param resolver: DependencyResolver to be used for resolving dependencies.
        :type resolver: DependencyResolver

        :param metrics: Metrics object for reporting.
        :type metrics: Optional[Metrics]

        :param cache_enabled: If set to ``True``, objects are constructed only onced and then reused.
        :type cache_enabled: bool

        :rtype: None
        """

        self.__resolver = resolver
        self.__metrics = metrics
        self.__cache_enabled = cache_enabled
        self.__cache: Dict[str, Any] = {}
        self.__lock = Lock()
        self.__parameters: Optional[Mapping[str, inspect.Parameter]] = None

    def preload(self) -> None:
        """Construct all dependencies and store it in the cache.

        :rtype: None
        """

        self.__cache = self.construct_dependencies()

    def clear_cache(self) -> None:
        """Remove all cached dependencies.

        :rtype: None
        """

        self.__cache.clear()

    def construct_dependencies(self) -> Dict[str, Any]:
        """Construct all dependencies.

        :rtype: None
        """
        injected_args: Dict[str, Any] = {}

        if self.__parameters is None:
            raise Exception("parameters not set")

        for parameter_name, parameter in self.__parameters.items():
            default = parameter.default

            if (
                parameter_name == "return"
                or default == inspect.Signature.empty
                or not isinstance(default, ParameterDependence)
            ):
                continue

            dependency: Any = self.__resolver.resolve(default.parameter_dependency).get_instance()
            injected_args[parameter_name] = dependency

        return injected_args

    def inject_function(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        """Convert the function into a new function that will received requested dependencies when invoked.

        :param fn: The function.
        :type fn: Callable[..., Any]

        :return: Function that will be assigned dependencies.
        :rtype: Callable[..., Any]
        """

        self.__parameters = inspect.signature(fn).parameters

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            t1 = time.perf_counter()
            injected_args: Dict[str, Any] = {}

            if self.__cache_enabled:
                self.__lock.acquire()

                if not self.__cache:
                    self.__cache = self.construct_dependencies()

                self.__lock.release()

                injected_args = self.__cache
            else:
                injected_args = self.construct_dependencies()

            if self.__metrics is not None:
                dt = time.perf_counter() - t1
                self.__metrics.save_metric(fn.__name__, dt)

            return fn(*args, **{**injected_args, **kwargs})

        return wrapper


class ParameterDependence:
    """Helper class to represent dependency request."""

    def __init__(self, parameter_dependency: Any) -> None:
        """ParameterDependence constructor.

        :param parameter_dependency: The dependency type.
        :type parameter_dependency: Any
        """
        self.parameter_dependency = parameter_dependency


T = TypeVar("T")


def Depends(parameter_type: Type[T]) -> T:
    """Helper function to mark a function parameter as a dependency.

    :param parameter_type: The dependency
    :type parameter_type: Type[T]

    :return: Value representing the dependency request.
    :rtype: T to satisfy type checker but it actually returns an instance of ``ParameterDependence``.
    """
    return cast(T, ParameterDependence(parameter_type))
