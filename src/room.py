import attr

from .event import Event
from .utils.container import Container


@attr.define
class Room:
    """
    Базовый класс локации
    """
    name: str
    characters = attr.Factory(list)
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
