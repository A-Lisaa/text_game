from collections import UserDict
from typing import Any

from logger import get_logger

_logger = get_logger(__name__)

class Container(UserDict):
    def __init__(self, default_value: Any = 0):
        super().__init__()
        self.default_value = default_value

    def __missing__(self, key: Any):
        self.data[key] = self.default_value
        _logger.debug("Container key %s is missing, set to default value %s", key, self.default_value)
        return self.data[key]

    def __setitem__(self, key: Any, value: Any):
        if value == self.default_value:
            self.data.pop(key)
        else:
            super().__setitem__(key, value)
