from typing import Union

try:
    # try to get BaseSettings from pydantic@v2
    from pydantic_settings import BaseSettings as BaseSettingsV2
except ImportError:
    BaseSettingsV2 = None

try:
    # try to get BaseSettings from pydantic@V2 in backward compatibility module
    from pydantic.v1 import BaseSettings as BaseSettingsV1FromV2
except ImportError:
    BaseSettingsV1FromV2 = None

try:
    # try to get BaseSettings for pydantic@v1
    from pydantic import BaseSettings as BaseSettingsV1
except ImportError:
    BaseSettingsV1 = None


BaseSettings = Union[BaseSettingsV2, BaseSettingsV1FromV2, BaseSettingsV1]
