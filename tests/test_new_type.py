from typing import NewType

import pytest

from src.container import Container
from src.exceptions import ResolverError


def test_new_type_properly_set() -> None:
    container = Container()
    MyType = NewType("MyType", int)
    my_type_value = MyType(1)

    container.register(MyType, value=my_type_value)

    class MyService:
        def __init__(self, my_type: MyType) -> None:
            self.my_type = my_type

    instance = container.resolve(MyService)
    assert instance.my_type == my_type_value
