from __future__ import annotations

from typing import Dict, Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class ScopedDict(Generic[K, V], Dict[K, V]):
    """Dictionary with ability to specify the parent dictionary.

    It tries to resolved `__getitem__` call using the underlying dictionary and
    if it can't find the key and tries to search in its parent dictionaries.
    """

    def __init__(self, parent_dict: Optional[ScopedDict[K, V]] = None) -> None:
        """ScopedDict constructor.

        :parameter parent_dict: The parent dictionary
        :type parent_dict: Optional[ScopedDict[K, V]]

        :rtype: None
        """

        self.__parent_dict = parent_dict

    def __getitem__(self, key: K) -> V:
        """``__getitem__`` implementation.

        :parameter key: Incomming key.
        :type key: K

        :return: Stored value.
        :rtype: V.
        """

        if not super().__contains__(key) and self.__parent_dict is not None:
            return self.__parent_dict[key]

        return super().__getitem__(key)

    def __contains__(self, key: object) -> bool:
        """``__contains__`` implementation.

        :parameter key: Incomming key.
        :type key: K

        :return: True if the value exist in the dictionary or its parents. Otherwise False.
        :rtype: bool.
        """

        if not super().__contains__(key):
            if self.__parent_dict is not None:
                return key in self.__parent_dict

            return False

        return True
