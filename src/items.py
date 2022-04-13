import copy
import os
from typing import Any

import attr

from .exceptions import ItemError
from .item_types import ITEM_TYPES
from .utils.files_IO import read_json_file
from .utils.logger import get_logger

_logger = get_logger(__file__)

class Items:
    def __init__(self, items: dict[str, Any]):
        self._items = items

    @classmethod
    def from_json_file(cls, path: str):
        json_items = read_json_file(path)
        items = cls._construct_items_dict(json_items)
        return cls(items)

    @classmethod
    def from_json_folder(cls, folder: str):
        json_items = {}
        for file in (file for _, _, files in os.walk(folder) for file in files):
            json_items.update(read_json_file(file))
        items = cls._construct_items_dict(json_items)
        return cls(items)

    @staticmethod
    def _construct_item_class(name: str, properties: dict[str, Any]) -> Any:
        types = tuple(ITEM_TYPES[type_] for type_ in properties.pop("type")[::-1])
        inherited_class = type("inherited_class", types, {})
        cls = attr.define(type(properties["name"].replace(" ", ""), (inherited_class,), {}))
        if len(properties) != len(cls.__init__.__defaults__):
            _logger.critical(
                "Wrong amount of properties for %s, should be %i",
                name, len(cls.__init__.__defaults__)
            )
            raise ItemError(
                f"Wrong amount of properties for {name}, should be {len(cls.__init__.__defaults__)}"
            )
        return cls(**properties)

    @staticmethod
    def _construct_items_dict(json_items: dict[str, Any]) -> dict[str, Any]:
        items = {}
        for name, properties in json_items.items():
            items[name] = Items._construct_item_class(name, properties)
        return items

    def __getitem__(self, name: str) -> Any:
        return self.get_item(name)

    def get_item(self, name: str) -> Any:
        if name not in self._items:
            _logger.critical("Item %s not found", name)
            raise ItemError(f"Item {name} not found")
        return copy.deepcopy(self._items[name])
