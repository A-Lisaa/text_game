import random

import attr

from position import Position
from room import Room
from utils.cfg import Config
from utils.container import Container
from utils.logger import get_logger

_config = Config()
_logger = get_logger(__file__)

@attr.define
class Plan:
    _plan: dict[Position, Room] = {}

    @classmethod
    def from_scratch(cls):
        _logger.debug("Made a Plan from scratch")
        return cls()

    @classmethod
    def from_json(cls, filepath: str):
        _logger.debug("Made a Plan from JSON file %s", filepath)

    def position_exists(self, position: Position) -> bool:
        return position in self._plan

    def update(
        self,
        position: Position,
        loot_amount: int = 2,
        events_amount: int = 1
        ):
        """
        Создание карты, если режим рогалика включен

        Args:
            loot_amount (int, optional): Кол-во лута на каждой создаваемой локации. Defaults to 2.
        """
        if _settings["rogue_like"] and not self.position_exists(position):
            chosen_location = random.choices(
                tuple(locations_pool.keys()),
                tuple(location["generation"][0] for location in locations_pool.values())
            )[0]
            chosen_location_properties = locations_pool[chosen_location]

            i = 0
            chosen_loot = Container()
            while i < loot_amount:
                chosen_loot_item = random.choices(
                    tuple(chosen_location_properties["loot"].keys()),
                    tuple(loot_item[0] for loot_item in chosen_location_properties["loot"].keys()),
                )[0]
                if chosen_loot_item not in chosen_loot:
                    chosen_loot[chosen_loot_item] = 0
                    chosen_location.possible_loot[chosen_loot_item].amount -= 1
                    i += 1

            i = 0
            chosen_events = []
            while i < events_amount:
                chosen_events = random.choices(
                    tuple(chosen_location.possible_events.keys()),
                    tuple(amount_chance.chance for amount_chance in chosen_location.possible_events.values()),
                    )
                chosen_event = random.choice(chosen_location.possible_events)
                if chosen_event not in chosen_events:
                    chosen_events.append(chosen_event)
                    i += 1

            self._plan[self.position] = chosen_location(loot=chosen_loot, events=chosen_events)
            locations_pool[chosen_location].amount -= 1
            if locations_pool[chosen_location].amount == 0:
                locations_pool.pop(chosen_location)

            _logger.debug("Created location: %s", locations_pool[chosen_location])

        self.curloc.times_visited += 1

    def examine_location(self):
        print(self.curloc)

    def show_map(self):
        self._plan = dict(zip(sorted(self._plan), self._plan.values()))
        for position, location in self._plan.items():
            print(position, location)
