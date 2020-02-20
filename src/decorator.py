from functools import wraps
from typing import Any, Callable, Dict, Type, TypeVar, cast, get_type_hints

from .resolver import DependencyResolver


class DecoratorResolver:
    def __init__(self, resolver: DependencyResolver) -> None:
        self.__resolver = resolver

    def inject_function(self, fn: Callable) -> Callable:
        type_hints = get_type_hints(fn)
        injected_args: Dict[str, Any] = {}

        for parameter_name, parameter_dependency in type_hints.items():
            if parameter_name == "return" or not isinstance(parameter_dependency, ParameterDependence):
                continue

            injected_args[parameter_name] = self.__resolver.resolve(
                parameter_dependency.parameter_dependency
            ).get_instance()

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **{**injected_args, **kwargs})

        return wrapper


class ParameterDependence:
    def __init__(self, parameter_dependency: Type) -> None:
        self.parameter_dependency = parameter_dependency


T = TypeVar("T")


def Depends(parameter_type: Type[T]) -> T:
    return cast(T, ParameterDependence(parameter_type))
