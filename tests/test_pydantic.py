import os
from typing import Protocol

import pytest
from pydantic import BaseSettings

from src.container import Container
from src.exceptions import ResolverError


def test_sub_container():
    os.environ["test"] = "test"

    class MySettings(BaseSettings):
        test: str

    class Client:
        def __init__(self, settings: MySettings) -> None:
            self.settings_test = settings.test

    container = Container()
    client = container.resolve(Client)

    assert client.settings_test == "test"
