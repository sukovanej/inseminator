from threading import Thread
from time import sleep
from unittest.mock import MagicMock, call

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


def test_inject_cache():
    test_fn = MagicMock()

    class Dependency:
        def __init__(self):
            test_fn()

    container = Container()

    @container.inject
    def function(d=Depends(Dependency)):
        ...

    test_fn.assert_not_called()

    function()
    test_fn.assert_called_once()
    function()
    test_fn.assert_called_once()

    container.clear()

    function()
    test_fn.assert_has_calls([call(), call()])


def test_inject_scoped():
    test_fn = MagicMock()

    class Dependency:
        def __init__(self):
            test_fn()

    container = Container()

    @container.inject_scoped
    def function(d: Dependency = Depends(Dependency)):
        ...

    test_fn.assert_not_called()
    function()
    test_fn.assert_called_once()
    function()
    test_fn.assert_has_calls([call(), call()])


def test_cache_thread_safety():
    test_fn = MagicMock()

    class Dependency:
        def __init__(self):
            sleep(0.1)
            test_fn()

    container = Container()

    @container.inject
    def function(d: Dependency = Depends(Dependency)):
        ...

    threads = []

    for _ in range(10):
        thread = Thread(target=function)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    test_fn.assert_called_once()
