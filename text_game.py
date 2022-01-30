from __future__ import annotations
import inspect
import json
import logging
import math
import random
from typing import Any, Callable, Type

import attr

# Constants
PI_HALF = 1.5707963267948966
MONTHS_DURATION = {
    1: 31,
    2: (28, 29),
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def get_text_pool(path: str) -> dict[str, str]:
    with open(path, encoding="utf-8") as json_file:
        return json.load(json_file)


@attr.define
class Position:
    x: int = 0
    y: int = 0


@attr.define
class Time:
    _year: int = 0
    _month: int = 1
    _day: int = 1
    _hour: int = 0
    _minute: int = 0
    _second: int = 0

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, y: int):
        self._year = y

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, m: int):
        self.year += m // 12
        if m % 12 == 0:
            m += 1
        self._month = m % 12

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, d: int):
        while d >= 28:
            if self.month == 2:
                current_month_duration = MONTHS_DURATION[2][1 if self.year % 4 != 0 and self.year % 100 == 0 and self.year % 400 != 0 else 0]
            else:
                current_month_duration = MONTHS_DURATION[self.month]
            if d >= current_month_duration - self._day - 1:
                self.month += 1
                d -= current_month_duration
                self._day = 1
        self._day = d

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, h: int):
        self.day += h // 24
        self._hour = h % 24

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, m: int):
        self.hour += m // 60
        self._minute = m % 60

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, s: int):
        self.minute += s // 60
        self._second = s % 60


@attr.define(hash=True)
class Item:
    name: str


@attr.define
class Character:
    name: str
    inventory: dict[Item, int] = {}
    stats: dict = {}

    def add_item(self, item: Item, amount: int):
        if item in self.inventory:
            self.inventory[item] += amount
        else:
            self.inventory[item] = amount

    def remove_item(self, item: Item, amount: int):
        if item in self.inventory:
            self.inventory[item] -= amount
        if self.inventory[item] == 0:
            self.inventory.pop(item)


@attr.define
class Location:
    name: str
    characters: list[Character] = []
    loot: dict[Item, list] = {} # Item: list(amount, chance)
    loot_chance: float = 0.5

    def remove_loot(self, item: Item, amount: int):
        if item in self.loot:
            self.loot[item][0] -= amount
        if self.loot[item][0] == 0:
            self.loot.pop(item)


@attr.define(hash=True)
class LocationCity(Location):
    name: str = "City"


@attr.define(hash=True)
class LocationForest(Location):
    name: str = "Forest"


class Game:
    ### General methods

    def yes_no_prompt(self, message: str,
                      yes_func: Callable, no_func: Callable | None = None,
                      yes_args: tuple | list = (), no_args: tuple | list = ()):
        answer = str()
        while answer not in ("y", "n"):
            answer = input(f"{message} (Y/N)? ").lower()
            if answer == "y":
                yes_func(*yes_args)
            elif answer == "n":
                if no_func is not None:
                    no_func(*no_args)
                else:
                    return
            else:
                print(text_pool["yes_no_invalid_input"])

    def movement(self, x: int = 0, y: int = 0):
        if self.rogue_like or f"{self.position.x + x}; {self.position.y + y}" in self.map:
            self.position.x += x
            self.position.y += y
            self.update_map()

    def rotation_movement(self, distance: float, angle: float, angle_in_degrees: bool = True):
        if angle_in_degrees:
            angle = math.radians(angle)
        self.movement(round(math.cos(angle - PI_HALF)*distance),
                      round(math.sin(angle + PI_HALF)*distance))

    @property
    def map_coords(self):
        return (self.position.x, self.position.y)

    @property
    def cur_location(self):
        return self.map[self.map_coords]

    def update_map(self, loot_amount: int = 2):
        if self.rogue_like and self.map_coords not in self.map:
            chosen_location = random.choices(
                tuple(self.location_pool.keys()),
                tuple(zip(*self.location_pool.values()))[1]
            )[0]

            i = 0
            chosen_loot = {}
            while i < loot_amount:
                chosen_loot_item = random.choice(tuple(self.location_loot_pool[chosen_location].keys()))
                if chosen_loot_item not in chosen_loot:
                    chosen_loot[chosen_loot_item] = self.location_loot_pool[chosen_location][chosen_loot_item]
                    i += 1

            self.map[self.map_coords] = chosen_location(loot=chosen_loot)
            self.location_pool[chosen_location][0] -= 1
            if self.location_pool[chosen_location][0] == 0:
                self.location_pool.pop(chosen_location)

    ### Commands

    ## Movement
    # Для "обычных" углов можно использовать movement() напрямую, может увеличить скорость
    # 90 degrees
    def north(self):
        self.rotation_movement(1, 0)

    def south(self):
        self.rotation_movement(1, 180)

    def east(self):
        self.rotation_movement(1, 90)

    def west(self):
        self.rotation_movement(1, 270)

    # 45 degrees
    def north_east(self):
        self.rotation_movement(2, 45)

    def south_east(self):
        self.rotation_movement(2, 135)

    def south_west(self):
        self.rotation_movement(2, 225)

    def north_west(self):
        self.rotation_movement(2, 315)

    ## Interaction
    def search(self, search_time: int = 1):
        if len(self.cur_location.loot) != 0:
            for _ in range(search_time):
                if random.random() < self.cur_location.loot_chance:
                    found_item = random.choices(
                        tuple(self.cur_location.loot.keys()),
                        tuple(zip(*self.cur_location.loot.values()))[1]
                    )

                    self.player.add_item(found_item[0], 1)
                    self.cur_location.remove_loot(found_item[0], 1)
                    print(text_pool["found_something"], found_item[0])
                else:
                    print(text_pool["nothing_found"])
        else:
            print(text_pool["nothing_to_find"])

    ## Info
    def get_position(self):
        print(f"x: {self.position.x}\ny: {self.position.y}")

    def examine_location(self):
        print(self.cur_location)

    def show_map(self):
        self.map = dict(zip(sorted(self.map), self.map.values()))
        for (x, y), value in self.map.items():
            print((x, y), value)

    def show_inventory(self):
        for item, amount in self.player.inventory.items():
            print(item, amount)

    ## System

    # Exit
    def exit_yes(self):
        self.game_active = False

    def exit(self):
        logging.info("Initiated exit")
        self.yes_no_prompt(text_pool["exit_message"], self.exit_yes)

    # Logging
    def get_logging_level(self):
        print(logging.root.level)

    def set_logging_level(self, logging_level: int):
        logging.basicConfig(level=logging_level, force=True)

    def antigravity(self):
        import antigravity
        antigravity.geohash(58.00, 56.19, b"2022-01-30-34725.47")

    ### Game methods

    def __init__(self):
        system_commands = {
            "exit": self.exit,
            "gll": self.get_logging_level,
            "sll": self.set_logging_level,
            "ag": self.antigravity,
            "antigrav": self.antigravity,
            "antigravity": self.antigravity,
        }
        debug_commands = {
            "mv": self.movement,
            "movement": self.movement,
            "rmv": self.rotation_movement,
            "rotation_movement": self.rotation_movement,
        }
        movement_commands = {
            # 90 degrees
            "n": self.north,
            "north": self.north,
            "s": self.south,
            "south": self.south,
            "w": self.west,
            "west": self.west,
            "e": self.east,
            "east": self.east,
            # 45 degrees
            "ne": self.north_east,
            "north_east": self.north_east,
            "se": self.south_east,
            "south_east": self.south_east,
            "sw": self.south_west,
            "south_west": self.south_west,
            "nw": self.north_west,
            "north_west": self.north_west,
        }
        interaction_commands = {
            "srch": self.search,
            "search": self.search
        }
        info_commands = {
            "gp": self.get_position,
            "getpos": self.get_position,
            "get_position": self.get_position,
            "el": self.examine_location,
            "examloc": self.examine_location,
            "examine_location": self.examine_location,
            "sm": self.show_map,
            "show_map": self.show_map,
            "si": self.show_inventory,
            "showinv": self.show_inventory,
            "show_inv": self.show_inventory,
            "show_inventory": self.show_inventory
        }
        self.command_pool = dict(
            **system_commands,
            **debug_commands,
            **movement_commands,
            **interaction_commands,
            **info_commands
        )

        self.rogue_like = True

        self.game_active = True
        self.time = Time()

        self.player = Character("Alice")

        self.location_pool = {
            LocationCity: [5, 0.5],
            LocationForest: [-1, 0.5]
        }

        self.location_loot_pool = {
            LocationCity: {
                Item("Bread"): [2, 0.35],
                Item("Water"): [2, 0.1],
                Item("Knife"): [1, 0.05]
            },
            LocationForest: {
                Item("Bread"): [2, 0.1],
                Item("Water"): [2, 0.25],
                Item("Stick"): [5, 0.4]
            }
        }

        self.position = Position()
        self.map = {}

    def type_casting(self, args: list[Any]):
        for i, arg in enumerate(args):
            if arg.isdigit():
                args[i] = int(arg)
            elif "." in arg and arg.replace(".", "", 1).isdigit():
                args[i] = float(arg)
            elif arg.lower() in ("true", "false"):
                args[i] = bool(arg)

        return args

    def get_input(self):
        user_input = str()
        while user_input in ("", []):
            user_input = input(text_pool["command_enter"]).split(maxsplit=1)
        command = user_input[0].lower() # ! lower() is used, maybe it will have consequences
        args = self.type_casting(user_input[1].split()) if len(user_input) > 1 else []

        return (command, args)

    def command_execution(self, command: str, args: list[Any]):
        if command in self.command_pool:
            expected_args = inspect.get_annotations(self.command_pool[command])
            if len(args) == len(expected_args):
                for arg, expected_arg in zip(args, expected_args.values()):
                    if not isinstance(arg, expected_arg):
                        print(text_pool["wrong_argument_type1"], arg, ". ",
                              text_pool["wrong_argument_type2"], type(expected_arg), sep="")
                        break
                else:
                    self.command_pool[command](*args)
                    logging.debug("Executed %s with arguments: %s",
                                  self.command_pool[command], *args)
            else:
                print(text_pool["wrong_arguments_amount"], len(expected_args))
        else:
            print(text_pool["wrong_command"])

    def main(self):
        print(text_pool["hello"])
        self.update_map()
        while self.game_active:
            self.command_execution(*self.get_input())


if __name__ == "__main__":
    text_pool = get_text_pool("./translations/ru_RU.json")
    game = Game()
    game.main()
