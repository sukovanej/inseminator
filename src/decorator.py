from functools import wraps
from typing import Any, Callable, Dict, Type, TypeVar, cast, get_type_hints

from .resolver import DependencyResolver


class DecoratorResolver:
    def __init__(self, resolver: DependencyResolver) -> None:
        self.__resolver = resolver

    def inject_function(self, fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            args = list(args).copy()
            type_hints = get_type_hints(fn)

            positional_arguments = []
            kw_arguments = {}

            for parameter_name, parameter_dependency in type_hints.items():
                if parameter_name == "return" or not isinstance(parameter_dependency, ParameterDependence):
                    if args:
                        positional_arguments.append(args.pop(0))
                    continue

                dependency = self.__resolver.resolve(parameter_dependency.parameter_dependency)

                if args:
                    positional_arguments.append(dependency.get_instance())
                else:
                    kw_arguments[parameter_name] = dependency.get_instance()

            kw_arguments.update(kwargs)

            return fn(*positional_arguments, **kw_arguments)

        return wrapper


class ParameterDependence:
    def __init__(self, parameter_dependency: Type) -> None:
        self.parameter_dependency = parameter_dependency


T = TypeVar("T")


def Depends(parameter_type: Type[T]) -> T:
    return cast(T, ParameterDependence(parameter_type))
