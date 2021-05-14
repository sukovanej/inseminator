from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import timedelta
from typing import Dict, Iterator, List, Mapping, NewType, Protocol, Tuple
from unittest.mock import MagicMock

from src.container import Container
from src.decorator import Depends

CustomType = object

OneCustomType = NewType("DefaultCustomType", CustomType)
TwoCustomType = NewType("TwoCustomType", CustomType)
ThreeCustomType = NewType("ThreeCustomType", CustomType)
FourCustomType = NewType("FourCustomType", CustomType)
FiveCustomType = NewType("FiveCustomType", CustomType)


class ServiceOne:
    def __init__(self, d1: ServiceTwo, d2: ServiceThree, d3: MyStorage) -> None:
        ...


class MyStorage:
    def __init__(self, d1: AnotherRepository, d2: MyClient) -> None:
        ...


class ServiceTwo:
    def __init__(self, d1: AnotherRepository, d2: MyClient) -> None:
        ...


class MyMainClass:
    def __init__(
        self, d1: MyBuilderClass, d2: RepositoryOne, d3: KioskTwo, d4: MyClient, d5: Toolbox, d6: ServiceOne
    ) -> None:
        ...


class MyAnotherService:
    def __init__(self, url: str) -> None:
        ...


class KioskTwo:
    def __init__(self, settings: Settings, another_dep: TwoCustomType, dep: MyAnotherService) -> None:
        ...


class MyBuilderClass:
    def __init__(self, client: MyClient, toolbox: Toolbox, service: ServiceOne):
        ...


class Database:
    def __init__(self, connection: DatabaseConnection) -> None:
        ...


class RepositoryOne(Database):
    ...


class AnotherRepository(Database):
    ...


class MyClient:
    def __init__(self, settings: Settings) -> None:
        ...


class ServiceThree:
    def __init__(self, d1: MyFactory, d2: MyClient, d3: Toolbox, d4: ServiceTwo) -> None:
        ...


class MyFactory:
    def __init__(self, toolbox: Toolbox, booking_backend_client: MyClient) -> None:
        ...


class Toolbox:
    def __init__(self, d1: AnotherMagicClass, d2: Settings, d3: MyCacheOne, d4: MyCacheTwo) -> None:
        ...


class MyCacheOne:
    def __init__(self, locations_client: LocationsClient, redis_client: ThreeCustomType) -> None:
        ...


class LocationsClient:
    def __init__(self, settings: Settings) -> None:
        ...


class MyCacheTwo:
    def __init__(self, d1: MyAnotherClientClass, d2: ThreeCustomType) -> None:
        ...


class MyAnotherClientClass:
    def __init__(self, settings: Settings):
        ...


class AnotherMagicClass:
    def __init__(self, cache: ToolboxCache) -> None:
        ...


class ToolboxCache:
    def __init__(self, settings: Settings, d2: ThreeCustomType, repository: RepositoryFour, parser: Parser) -> None:
        ...


class RepositoryFour(Database):
    ...


class Parser:
    def __init__(self) -> None:
        ...


class DatabaseConnection:
    def __init__(self, settings: Settings, pool_size: int = 5, pool_max_overflow: int = 10) -> None:
        ...


class Settings:
    def __init__(self) -> None:
        ...


class AnotherMainClass:
    def __init__(self, d1: TaskRepository, d2: KioskTwo, d3: ImplementationService) -> None:
        ...


class TaskRepository(Database):
    ...


class AbstractService(ABC):
    @abstractmethod
    @contextmanager
    def with_active_lock(
        self, resources: Mapping[str, str], acquire_timeout: timedelta, ttl_max: timedelta
    ) -> Iterator[None]:
        ...


class ImplementationService(AbstractService):
    def __init__(self, redis: TwoCustomType):
        ...

    @contextmanager
    def with_active_lock(
        self, resources: Mapping[str, str], acquire_timeout: timedelta, ttl_max: timedelta
    ) -> Iterator[None]:
        yield


def test_big_dependency_tree():
    metrics = MagicMock()
    container = Container()
    container.set_metrics(metrics)
    container.register(Settings, value=object())
    container.register(OneCustomType, value=OneCustomType(object))
    container.register(TwoCustomType, value=TwoCustomType(object))
    container.register(ThreeCustomType, value=ThreeCustomType(object))
    container.register(FourCustomType, value=FourCustomType(object))
    container.register(FiveCustomType, value=FiveCustomType(object))
    container.register(AbstractService, factory=ImplementationService)

    @container.inject
    def set_values(
        param1: int,
        d1: ServiceOne = Depends(ServiceOne),
        d2: MyMainClass = Depends(MyMainClass),
        d3: AnotherMainClass = Depends(AnotherMainClass),
    ) -> None:
        ...

    for _ in range(10):
        set_values(1)

    calls = metrics.save_metric.mock_calls
    assert calls
