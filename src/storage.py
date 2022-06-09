import attr

from . import globs
from .exceptions import StorageError
from .item import Item


@attr.define
class Storage:
    _weight_threshold: float = -1
    _items: dict[str, list[Item]] = attr.Factory(dict)

    def __attrs_post_init__(self):
        self._items = {}

    def add_item(self, item: Item):
        if item.__class__.__name__ not in self._items:
            self._items[item.__class__.__name__] = []
        self._items[item.__class__.__name__].append(item)

    def get_item(self, item: Item, index: int):
        if item.__class__.__name__ not in self._items:
            globs.logger.critical("Item %s not found", item.__class__.__name__)
            raise StorageError(f"Item {item.__class__.__name__} not found")
        return self._items[item.__class__.__name__][index]

    def remove_item(self, item: Item, index: int):
        if item.__class__.__name__ not in self._items:
            globs.logger.critical("Item %s not found", item.__class__.__name__)
            raise StorageError(f"Item {item.__class__.__name__} not found")
        stored_item = self._items[item.__class__.__name__].pop(index)
        if len(self._items[item.__class__.__name__]) == 0:
            self._items.pop(item.__class__.__name__)
        return stored_item
