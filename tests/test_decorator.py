from src.container import Container
from src.decorator import Depends


def test_decorator_dependency():
    class Dependency:
        def __init__(self):
            self.x = 1

    container = Container()

    @container.inject
    def my_function(dependency: Depends(Dependency), value: int) -> int:
        return value + dependency.x

    assert my_function(value=1) == 2
