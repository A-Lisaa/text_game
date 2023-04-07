from abc import abstractmethod

from .utils.data_structures import Container, WeightedList


class Room:
    """
    Базовый класс рогалик-локации
    """
    def __init__(self, loot: Container):
        self.loot = loot
        self.times_visited = 0

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        ...

    @staticmethod
    @abstractmethod
    def get_possible_loot() -> WeightedList:
        ...

    @staticmethod
    @abstractmethod
    def get_loot_chance() -> WeightedList:
        ...

    @classmethod
    def create_with_loot(cls, loot: WeightedList | None = None):
        if loot is None:
            loot = cls.get_possible_loot()
        return cls(Container(loot))

class RoomCity(Room):
    @staticmethod
    def get_name():
        return "City"

    @staticmethod
    def get_possible_loot():
        return {}

    @staticmethod
    def get_loot_chance():
        return 0.5


class RoomForest(Room):
    @staticmethod
    def get_name():
        return "Forest"

    @staticmethod
    def get_possible_loot():
        return {}

    @staticmethod
    def get_loot_chance():
        return 0.5


rooms = (RoomCity, RoomForest)
