from __future__ import annotations

from typing import Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class ScopedDict(dict, Generic[K, V]):
    def __init__(self, parent_dict: Optional[ScopedDict[K, V]] = None) -> None:
        self.__parent_dict = parent_dict

    def __getitem__(self, key: K) -> V:
        if not super().__contains__(key) and self.__parent_dict is not None:
            return self.__parent_dict[key]

        return super().__getitem__(key)

    def __contains__(self, key: object) -> bool:
        if not super().__contains__(key):
            if self.__parent_dict is not None:
                return key in self.__parent_dict

            return False

        return True
