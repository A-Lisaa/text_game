import random

import attr

from . import globs
from .plan import Plan
from .room import Room
from .utils.data_structures import Container


@attr.define
class Character:
    name: str
    location: Room
    inventory: Container = Container()
    equipment: Container = Container()
    stats: dict = {}
    schedule: dict = {}

    def search(self) -> str:
        if len(self.location.loot) <= 0:
            return globs.lines["nothing_to_find"]

        if random.random() >= self.location.loot_chance:
            return globs.lines["nothing_found"]

        found_item, = random.choices(
            tuple(self.location.loot.keys()),
            tuple(self.location.loot.values())
        )

        self.inventory[found_item] += 1
        self.location.loot[found_item] -= 1
        return f"{globs.lines['found_something']} {found_item}"
