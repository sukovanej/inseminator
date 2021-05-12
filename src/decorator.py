import inspect
from functools import wraps
from typing import Any, Callable, Dict, Type, TypeVar, cast, get_type_hints

from .resolver import DependencyResolver


class DecoratorResolver:
    def __init__(self, resolver: DependencyResolver) -> None:
        self.__resolver = resolver

    def inject_function(self, fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            type_hints = get_type_hints(fn)
            injected_args: Dict[str, Any] = {}

            signature_parameters = inspect.signature(fn).parameters
            for parameter_name, parameter in signature_parameters.items():
                default = parameter.default

                if (
                    parameter_name == "return"
                    or default == inspect.Signature.empty
                    or not isinstance(default, ParameterDependence)
                ):
                    continue

                dependency = self.__resolver.resolve(default.parameter_dependency)
                injected_args[parameter_name] = dependency.get_instance()

            return fn(*args, **{**injected_args, **kwargs})

        return wrapper


class ParameterDependence:
    def __init__(self, parameter_dependency: Type) -> None:
        self.parameter_dependency = parameter_dependency


T = TypeVar("T")


def Depends(parameter_type: Type[T]) -> T:
    return cast(T, ParameterDependence(parameter_type))
