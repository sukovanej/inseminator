from typing import NewType, Protocol
from unittest.mock import MagicMock, call

import pytest

from src.container import Container
from src.exceptions import ResolverError


def test_sub_container():
    class Dependency(Protocol):
        x: int

    class Dependency1:
        x = 1

    class Dependency2:
        x = 2

    class Client:
        def __init__(self, dependency: Dependency) -> None:
            self.x = dependency.x

    container = Container()

    sub_container = container.sub_container()
    sub_container.register(Dependency, value=Dependency1())

    with pytest.raises(ResolverError) as e:
        container.resolve(Client)

    client1 = sub_container.resolve(Client)

    assert client1.x == 1

    container.register(Dependency, value=Dependency2())
    client2 = container.resolve(Client)

    assert client2.x == 2


def test_sub_container_2():
    class Dependency(Protocol):
        x: int

    class Dependency1:
        x = 1

    class Client:
        def __init__(self, dependency: Dependency) -> None:
            self.x = dependency.x

    container = Container()
    container.register(Dependency, value=Dependency1())

    sub_container = container.sub_container()
    client = sub_container.resolve(Client)

    assert client.x == 1


def test_resolving_with_parameters():
    class FirstDependency:
        x = 1

    class Dependency(Protocol):
        y: int

    class ConcreteDependency:
        y = 2

    class Client:
        def __init__(self, first_dependency: FirstDependency, second_dependency: Dependency) -> None:
            self.x = first_dependency.x
            self.y = second_dependency.y

        def add(self) -> int:
            return self.x + self.y

    container = Container()
    client = container.resolve(Client, second_dependency=ConcreteDependency)

    assert client.add() == 3


def test_resolving_with_wrong_parameters():
    class Dependency:
        x = 1

    class Client:
        def __init__(self, dependency: Dependency) -> None:
            self._dependency = dependency

    container = Container()

    with pytest.raises(ResolverError):
        client = container.resolve(Client, non_existing_parameter=Dependency())


def test_more_complex_example():
    class Dependency:
        x = 1

    def factory():
        return 1

    Dep = NewType("Dep", int)

    class Client:
        def __init__(self, dep1: Dependency, dep2: Dep) -> None:
            self.dep1 = dep1
            self.dep2 = dep2

    container = Container()
    container.register(Dep, factory=factory)
    container.register(Dependency, value=Dependency())

    client = container.resolve(Client)

    assert client.dep1.x == 1
    assert client.dep2 == 1


def test_container_clear() -> None:
    test_callable = MagicMock()

    class Dependency:
        def __init__(self):
            test_callable()

    class Client:
        def __init__(self, dep: Dependency):
            ...

    container = Container()

    container.resolve(Dependency)
    test_callable.assert_called_once()

    container.resolve(Dependency)
    test_callable.assert_called_once()

    container.clear()
    container.resolve(Dependency)
    test_callable.assert_has_calls([call(), call()])

    container.resolve(Dependency)
    test_callable.assert_has_calls([call(), call()])


def test_missing_dependencies() -> None:
    class Dependency:
        ...

    class Client:
        def __init__(self, dep: Dependency, unknown_dep):
            ...

    def function(dep: Client, unknown_param):
        ...

    container = Container()

    with pytest.raises(ResolverError, match="Can resolve dependencies for"):
        container.resolve(Client)

    with pytest.raises(ResolverError, match="Can resolve dependencies for"):
        container.resolve(function)
