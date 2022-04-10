import attr

from .character import Character
from .event import Event
from .utils.container import Container


@attr.define
class Room:
    """
    Базовый класс локации
    """
    name: str
    characters: list[Character] = attr.Factory(list)
    events: list[Event] = attr.Factory(list)
    loot: Container = Container()
    times_visited: int = 0
    loot_chance: float = 0.5


@attr.define
class RoomCity(Room):
    name = "City"


@attr.define
class RoomForest(Room):
    name = "Forest"
