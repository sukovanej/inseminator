import inspect
import time
from functools import wraps
from threading import Lock
from typing import Any, Callable, Dict, Mapping, Optional, Type, TypeVar, cast, get_type_hints

from .metrics import Metrics
from .resolver import DependencyResolver


class DecoratorResolver:
    def __init__(
        self, resolver: DependencyResolver, metrics: Optional[Metrics] = None, cache_enabled: bool = True
    ) -> None:
        self.__resolver = resolver
        self.__metrics = metrics
        self.__cache_enabled = cache_enabled
        self.__cache: Dict[str, Any] = {}
        self.__lock = Lock()
        self.__parameters: Optional[Mapping[str, inspect.Parameter]] = None

    def preload(self) -> None:
        self.__cache = self.construct_dependencies()

    def clear_cache(self):
        self.__cache.clear()

    def construct_dependencies(self) -> Dict[str, Any]:
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

    def inject_function(self, fn: Callable) -> Callable:
        self.__parameters = inspect.signature(fn).parameters

        @wraps(fn)
        def wrapper(*args, **kwargs):
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
    def __init__(self, parameter_dependency: Type) -> None:
        self.parameter_dependency = parameter_dependency


T = TypeVar("T")


def Depends(parameter_type: Type[T]) -> T:
    return cast(T, ParameterDependence(parameter_type))
