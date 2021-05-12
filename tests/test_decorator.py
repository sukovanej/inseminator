from src.container import Container
from src.decorator import Depends


def test_decorator_dependency():
    class Dependency:
        def __init__(self):
            self.x = 1

    container = Container()

    @container.inject
    def my_function(value: int, dependency: Dependency = Depends(Dependency)) -> int:
        return value + dependency.x

    assert my_function(value=1) == 2


def test_decorator_dependency_with_positional_arguments():
    class Dependency:
        def __init__(self):
            self.x = 1

    container = Container()

    @container.inject
    def my_function(value: int, dependency: Dependency = Depends(Dependency)) -> int:
        return value + dependency.x

    assert my_function(1) == 2


def test_decorator_dependency_with_mixed_arguments():
    class Dependency:
        def __init__(self):
            self.x = 1

    container = Container()

    @container.inject
    def my_function(p1: int, p2: int, p3: int, p4: int, dep: Dependency = Depends(Dependency)) -> int:
        return p1 + p2 + dep.x + p3 + p4

    assert my_function(1, 2, 3, p4=4) == 11
    assert my_function(1, p3=2, p2=3, p4=4) == 11
