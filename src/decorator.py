import inspect
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast, get_type_hints

from .metrics import Metrics
from .resolver import DependencyResolver


class DecoratorResolver:
    def __init__(
        self, resolver: DependencyResolver, metrics: Optional[Metrics] = None, cache_enabled: bool = True
    ) -> None:
        self.__resolver = resolver
        self.__metrics = metrics
        self.__cache_enabled = cache_enabled

    def inject_function(self, fn: Callable) -> Callable:
        signature_parameters = inspect.signature(fn).parameters
        cache = {}

        @wraps(fn)
        def wrapper(*args, **kwargs):
            t1 = time.perf_counter()
            injected_args: Dict[str, Any] = {}

            for parameter_name, parameter in signature_parameters.items():
                default = parameter.default

                if (
                    parameter_name == "return"
                    or default == inspect.Signature.empty
                    or not isinstance(default, ParameterDependence)
                ):
                    continue

                if self.__cache_enabled:
                    if default.parameter_dependency not in cache:
                        dependency = self.__resolver.resolve(default.parameter_dependency).get_instance()
                        cache[default.parameter_dependency] = dependency
                    else:
                        dependency = cache[default.parameter_dependency]
                else:
                    dependency = self.__resolver.resolve(default.parameter_dependency).get_instance()

                injected_args[parameter_name] = dependency

            dt = time.perf_counter() - t1

            if self.__metrics is not None:
                self.__metrics.save_metric(fn.__name__, dt)

            return fn(*args, **{**injected_args, **kwargs})

        return wrapper


class ParameterDependence:
    def __init__(self, parameter_dependency: Type) -> None:
        self.parameter_dependency = parameter_dependency


T = TypeVar("T")


def Depends(parameter_type: Type[T]) -> T:
    return cast(T, ParameterDependence(parameter_type))
