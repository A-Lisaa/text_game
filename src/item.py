from abc import ABC, abstractmethod

import attr


@attr.define
class Item(ABC):
    """
    Базовый класс предметов
    """
    name: str = NotImplemented
    stack_size: int = NotImplemented
    weight: float = NotImplemented
    volume: float = NotImplemented

    @abstractmethod
    def __str__(self):
        ...


@attr.define
class ItemEquipment(Item):
    ...
