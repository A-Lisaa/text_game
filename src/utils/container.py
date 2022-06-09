from collections import UserDict
from typing import Any

from .. import globs


class Container(UserDict):
    def __init__(self, no_value: Any = 0):
        """Словарь, который вернет no_value, если элемента нет и уберет элемент, если значение равно no_value

        Args:
            no_value (Any, optional): Значение, которое эквивалентно отсутствию. Defaults to 0.
        """
        super().__init__()
        self.no_value = no_value

    def __missing__(self, key: Any):
        self.data[key] = self.no_value
        globs.logger.debug("Container key %s is missing, set to value %s", key, self.no_value)
        return self.data[key]

    def __setitem__(self, key: Any, value: Any):
        if value == self.no_value:
            self.data.pop(key)
        else:
            self.data[key] = value
