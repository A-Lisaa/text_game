from abc import ABC, abstractmethod

import attr

from character import Character
from event import Event
from utils.container import Container


@attr.define
class Location(ABC):
    """
    Базовый класс локации
    """
    name: str
    characters: list[Character] = attr.Factory(list)
    events: list[Event] = attr.Factory(list)
    loot: Container = Container()
    times_visited: int = 0
    loot_chance: float = 0.5

    @abstractmethod
    def __hash__(self):
        pass


@attr.define(hash=True)
class LocationCity(Location):
    name = "City"


@attr.define(hash=True)
class LocationForest(Location):
    name = "Forest"
