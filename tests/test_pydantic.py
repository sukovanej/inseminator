import os

import pytest

from inseminator.base_settings import BaseSettingsV1, BaseSettingsV1FromV2, BaseSettingsV2
from inseminator.container import Container


@pytest.mark.skipif(not BaseSettingsV1, reason="Missing pydantic v1")
def test_basesettings_v1():
    os.environ["test"] = "test"

    class MySettings(BaseSettingsV1):
        test: str

    class Client:
        def __init__(self, settings: MySettings) -> None:
            self.settings_test = settings.test

    container = Container()
    client = container.resolve(Client)

    assert client.settings_test == "test"


@pytest.mark.skipif(not BaseSettingsV2, reason="Missing pydantic-settings")
def test_basesettings_v2():
    os.environ["test"] = "test"

    class MySettings(BaseSettingsV2):
        test: str

    class Client:
        def __init__(self, settings: MySettings) -> None:
            self.settings_test = settings.test

    container = Container()
    client = container.resolve(Client)

    assert client.settings_test == "test"


@pytest.mark.skipif(not BaseSettingsV1FromV2, reason="Missing pydantic v2")
def test_basesettings_v1_from_v2():
    os.environ["test"] = "test"

    class MySettings(BaseSettingsV1FromV2):
        test: str

    class Client:
        def __init__(self, settings: MySettings) -> None:
            self.settings_test = settings.test

    container = Container()
    client = container.resolve(Client)

    assert client.settings_test == "test"
