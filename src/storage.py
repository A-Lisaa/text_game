import attr

from .item import Item
from .utils.logger import get_logger

_logger = get_logger(__file__)


@attr.define
class Storage:
    cells_threshold: int = -1
    volume_threshold: float = -1
    weight_threshold: float = -1
    _items: list[list[Item]] = attr.Factory(list)
    _cells_fullness: int = 0
    _volume_fullness: float = 0
    _weight_fullness: float = 0

    def __attrs_post_init__(self):
        self._items = [[] for _ in range(self.cells_threshold)]

    def __str__(self):
        return f"{self._items}"

    def _addition_update(self, item: Item):
        self._cells_fullness += 1
        self._weight_fullness += item.weight

    def _removal_update(self, item: Item):
        self._cells_fullness -= 1
        self._weight_fullness -= item.weight

    @property
    def _get_empty_cell(self) -> int:
        try:
            return self._items.index([])
        except ValueError:
            return -1

    def get_item_cell(self, item: Item, start: int = 0) -> int:
        for i, cell in enumerate(self._items, start):
            if cell and isinstance(item, type(cell[0])):
                return i
        return -1

    def _check_fittings(self, item: Item, item_cell_index: int) -> bool:
        return all((
            self.get_cell_size(item_cell_index) == item.stack_size,
            self._weight_fullness + item.weight <= self.weight_threshold,
        ))

    def _get_cell_for_item(self, item: Item, start: int = 0) -> int:
        item_cell_index = self.get_item_cell(item, start)
        if item_cell_index == -1:
            return self._get_empty_cell
        if not self._check_fittings(item, item_cell_index):
            self._get_cell_for_item(item, item_cell_index+1)
        return item_cell_index

    def get_cell_size(self, cell_index: int) -> int:
        return len(self._items[cell_index])

    def add_item(self, item: Item):
        cell_index = self._get_cell_for_item(item)
        if cell_index == -1:
            return
        self._items[cell_index].append(item)
        self._addition_update(item)
        _logger.debug("Added item %s to %i", item, cell_index)

    def remove_item_from_cell(self, cell_index: int):
        if cell_index >= self.cells_threshold or self.get_cell_size(cell_index) == 0:
            return
        self._removal_update(self._items[cell_index][0])
        self._items[cell_index].pop(0)
        _logger.debug("Removed item from %i", cell_index)
