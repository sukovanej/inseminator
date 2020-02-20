import typing

import pytest

from src.container import Container
from src.exceptions import ContainerRegisterError


def test_basic_register_resolve():
    class TestDependency:
        def __init__(self):
            self.x = 1

    container = Container()
    container.register(TestDependency)

    assert container.resolve(TestDependency).x == 1


def test_multiple_basic_register_resolve():
    class TestDependency:
        def __init__(self):
            self.x = 1

    class AnotherTestDependency:
        def __init__(self):
            self.x = 2

    container = Container()
    container.register(TestDependency)
    container.register(AnotherTestDependency)

    assert container.resolve(TestDependency).x == 1
    assert container.resolve(AnotherTestDependency).x == 2


def test_dependency_without_registered_dependencies():
    class TestDependency:
        def __init__(self):
            self.x = 1

    container = Container()

    dependency_1 = container.resolve(TestDependency)
    dependency_2 = container.resolve(TestDependency)

    assert dependency_1.x == 1
    assert dependency_2.x == 1
    assert dependency_1 is dependency_2


def test_simple_hierarchy_depedency():
    class TestDependency:
        def __init__(self):
            self.x = 1

    class AnotherTestDependency:
        def __init__(self, dependency: TestDependency):
            self.x = dependency.x + 1

    container = Container()
    container.register(AnotherTestDependency)

    assert container.resolve(AnotherTestDependency).x == 2


def test_simple_hierarchy_depedency_without_registerd_dependency():
    class TestDependency:
        def __init__(self):
            self.x = 1

    class AnotherTestDependency:
        def __init__(self, dependency: TestDependency):
            self.x = dependency.x + 1

    container = Container()

    dependency_1 = container.resolve(AnotherTestDependency)
    dependency_2 = container.resolve(AnotherTestDependency)

    assert dependency_1 is dependency_2
    assert dependency_1.x == 2


def test_register_dependency_with_default_value():
    class TestDependency:
        def __init__(self, x):
            self.x = x

    class AnotherTestDependency:
        def __init__(self, dependency: TestDependency):
            self.x = dependency.x + 1

    container = Container()
    container.register(TestDependency, value=TestDependency(x=2))

    assert container.resolve(AnotherTestDependency).x == 3


def test_multiple_dependencies():
    class Dependency1:
        def __init__(self):
            self.x = 1

    class Dependency2:
        def __init__(self):
            self.x = 2

    class Dependency3:
        def __init__(self, dependency: Dependency1):
            self.x = dependency.x + 1

    class Dependency4:
        def __init__(self, dependency_3: Dependency3, dependency_2: Dependency2):
            self.x = dependency_3.x + dependency_2.x

    container = Container()

    assert container.resolve(Dependency4).x == 4


def test_register_dependency_by_factory():
    class Dependency:
        def __init__(self, x):
            self.x = x

    def dependency_factory() -> Dependency:
        return Dependency(1)

    class AnotherDependency:
        def __init__(self, dependency: Dependency):
            self.x = dependency.x

    container = Container()
    container.register(Dependency, factory=dependency_factory)

    assert container.resolve(AnotherDependency).x == 1


def test_value_and_factory_register_exception():
    class Dependency:
        def __init__(self, x):
            self.x = x

    def dependency_factory() -> Dependency:
        return Dependency(1)

    class AnotherDependency:
        def __init__(self, dependency: Dependency):
            self.x = dependency.x

    container = Container()

    with pytest.raises(ContainerRegisterError):
        container.register(Dependency, factory=dependency_factory, value=Dependency(2))
