from abc import ABC, abstractmethod
from typing import Any

import attr

from . import globs


@attr.define(slots=False)
class Item(ABC):
    """
    Базовый класс предметов
    """
    name: str = NotImplemented
    weight: float = NotImplemented
    cost: float = NotImplemented

    @classmethod
    def __attrs_post_init__(cls):
        ...

    @classmethod
    def from_dict(cls, dic: dict[str, Any]):
        if cls.__name__ != "Item":
            return cls(**dic)
        globs.logger.error("Trying to instantiate abstract class Item with from_dict")

    # @abstractmethod
    # def __str__(self):
    #     ...


@attr.define(slots=False)
class ItemEquipment:
    durability: float = NotImplemented

    def do_damage(self, damage: float):
        self.durability -= damage


@attr.define(slots=False)
class ItemConsumable:
    consumption_time: float = NotImplemented
