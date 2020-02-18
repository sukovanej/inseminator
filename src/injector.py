import inspect
from typing import Any, Callable, Dict, Type, TypeVar, Union, get_type_hints

from .dependency import Dependency, StaticDependency

T = TypeVar("T")

Dependable = Union[Callable[..., T], Type[T]]


class DependencyResolver:
    def __init__(self, container: Dict[Dependable, Dependency]) -> None:
        self._container = container

    def resolve(self, dependency: Dependable) -> Dependency[T]:
        if dependency in self._container:
            return self._container[dependency]

        if inspect.isclass(dependency):
            type_hints = get_type_hints(dependency.__init__)  # type: ignore
        elif inspect.isfunction(dependency):
            type_hints = get_type_hints(dependency)

        args: Dict[str, Any] = {}

        for parameter_name, parameter_dependency in type_hints.items():
            if parameter_name == "return":
                continue

            args[parameter_name] = self.resolve(parameter_dependency).get_instance()

        return StaticDependency(instance=dependency(**args))
