import math
import random

import attr

from .plan import Plan
from .position import Position
from .room import Room
from .utils.cfg import Config
from .utils.container import Container
from .utils.logger import get_logger

_logger = get_logger(__file__)
_config = Config()


@attr.define
class Character:
    name: str
    id: str
    inventory: Container = Container()
    equipment: Container = Container()
    position: Position = Position(0, 0)
    stats: dict = {}
    schedule: dict = {}

    def search(self, location: Room, search_time: int = 1):
        if len(location.loot) > 0:
            for _ in range(search_time):
                if random.random() < location.loot_chance:
                    found_item = random.choices(
                        tuple(location.loot.keys()),
                        tuple(zip(*location.loot.values()))[1]
                    )[0]

                    self.inventory[found_item] += 1
                    location.loot[found_item] -= 1
                    print(_lines["found_something"], found_item)
                else:
                    print(_lines["nothing_found"])
        else:
            print(_lines["nothing_to_find"])

    def movement(self, plan: Plan, x: int = 0, y: int = 0):
        """
        Перемещение на x вправо и y вверх, возможны отриц. значения

        Args:
            x (int, optional): Расстояние вправо. Defaults to 0.
            y (int, optional): Расстояние вверх. Defaults to 0.
        """
        for _ in range(x):
            self.position.x += 1
            if _config["rogue_like"] or plan.position_exists():
                plan.update(self.position)
        for _ in range(y):
            self.position.y += 1
            if _config["rogue_like"] or plan.position_exists():
                plan.update(self.position)

    def rotation_movement(self, distance: float, angle: float, angle_in_degrees: bool = True):
        """
        Перемещение на distance с углом angle, считая угол от 0 градусов по часовой стрелке

        Args:
            distance (float): расстояние для перемещения, будет округлено после рассчетов
            angle (float): угол под которым перемещаться, градусы или радианы
            angle_in_degrees (bool, optional): угол в градусах или в радианах, True - градусы. Defaults to True.
        """
        # 1.57 = pi/2
        if angle_in_degrees:
            angle = math.radians(angle)
        self.movement(
            round(math.cos(angle - 1.57)*distance),
            round(math.sin(angle + 1.57)*distance)
        )

    # 90 degrees
    def north(self, distance: int = 1):
        self.movement(0, -distance)

    def south(self, distance: int = 1):
        self.movement(0, distance)

    def west(self, distance: int = 1):
        self.movement(-distance, 0)

    def east(self, distance: int = 1):
        self.movement(distance, 0)

    def show_position(self):
        print(self.position)

    def show_inventory(self):
        for item, amount in self.inventory.items():
            print(item, amount)
