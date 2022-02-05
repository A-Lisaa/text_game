import collections
import inspect
import json
import logging
import math
import random
from typing import Any, Callable, Optional

import attr

############################################################################
#                               Constants                                  #
############################################################################
PI_HALF = 1.5707963267948966192313216916398
FIVE_OVER_NINE = 0.55555555555555555555555555555556
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

_F = Callable[[], Optional[Any]]
_FARGS = tuple[Optional[Any], ...] | list[Optional[Any]]

############################################################################
#                            Global functions                              #
############################################################################
def get_json_file(path: str) -> dict[str, str]:
    with open(path, encoding="utf-8") as json_file:
        return json.load(json_file)

############################################################################
#                             Global Classes                               #
############################################################################
class text:
    @staticmethod
    def temperature(temperature: float, celsius: bool = True):
        if celsius and not settings["temperature_in_celsius"]:
            temperature = 1.8*temperature + 32
        elif not celsius and settings["temperature_in_celsius"]:
            temperature = FIVE_OVER_NINE*(temperature - 32)
        return temperature


@attr.define
class Position:
    """
    Хранит положение для возможности доступа через Position.x или Position.y
    """
    x: int = 0
    y: int = 0


@attr.define
class Time:
    """
    Хранит время, при изменении времени мелкое переходит в большее
    """
    _year: int = 0
    _month: int = 1
    _day: int = 1
    _hour: int = 0
    _minute: int = 0
    _second: int = 0
    months_duration: dict = MONTHS_DURATION

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
                current_month_duration = self.months_duration[2][1 if self.year % 4 != 0 and self.year % 100 == 0 and self.year % 400 != 0 else 0]
            else:
                current_month_duration = self.months_duration[self.month]
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
    """
    Базовый класс предметов
    """
    name: str


@attr.define
class ItemEquipment(Item):
    pass


class Container(collections.UserDict):
    def __init__(self, default_value = 0):
        super().__init__()
        self.data = {}
        self.default_value = default_value

    def __getitem__(self, key: Any):
        if key not in self.data:
            self.data[key] = self.default_value
        return super().__getitem__(key)

    def __setitem__(self, key: Any, value: Any):
        if value == self.default_value:
            self.data.pop(key)
        else:
            super().__setitem__(key, value)


@attr.define
class Character:
    """
    Класс персонажа
    """
    name: str
    id: str
    inventory: Container = Container()
    equipment: dict[str, ItemEquipment | None] = {}
    stats: dict = {}


@attr.define
class Event:
    name: str
    trigger: Callable
    action: Callable


@attr.define
class Location:
    """
    Базовый класс локации
    """
    name: str
    characters: list[Character] = []
    events: list[Event] = []
    loot: Container = Container()
    loot_chance: float = 0.5


@attr.define(hash=True)
class LocationCity(Location):
    name: str = "City"


@attr.define(hash=True)
class LocationForest(Location):
    name: str = "Forest"


############################################################################
#                                Main Class                                #
############################################################################
class Game:
    """
    Главный класс игры, все взаимодействия здесь, почти все функции здесь
    """
    ############################################################################
    #                          Not In-Game Methods                             #
    ############################################################################
    def yes_no_prompt(self, message: str,
                      yes_func: _F, no_func: Optional[_F] = None,
                      yes_args: _FARGS = (), no_args: _FARGS = ()):
        """
        Выбор да или нет

        Args:
            message (str): Сообщение для вывода
            yes_func (Callable): Функция для вызова при подтверждении
            no_func (Callable, optional): Функция для вызова при отказе, может быть None, тогда ничего не произойдет. Defaults to None.
            yes_args (tuple, optional): Аргументы для функции подтверждения. Defaults to ().
            no_args (tuple, optional): Аргументы для функции отказа. Defaults to ().
        """
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

    def menu(self, actions: dict[str, tuple[_F, _FARGS]]):
        for position, action in enumerate(actions, start=1):
            print(f"{position}) {action}")

        functions = {str(k): v for k, v in enumerate(actions.values(), start=1)}
        while True:
            print(text_pool["choose_menu_answer"], end="")
            answer = input()
            if answer in functions:
                break
            print(text_pool["wrong_menu_answer"])

        functions[answer][0](*functions[answer][1])

    def movement(self, x: int = 0, y: int = 0):
        """
        Перемещение на x вправо и y вверх, возможны отриц. значения

        Args:
            x (int, optional): Расстояние вправо. Defaults to 0.
            y (int, optional): Расстояние вверх. Defaults to 0.
        """
        if self.rogue_like or f"{self.position.x + x}; {self.position.y + y}" in self.map:
            self.position.x += x
            self.position.y += y
            self.update_map()

    def rotation_movement(self, distance: float, angle: float, angle_in_degrees: bool = True):
        """
        Перемещение на distance с углом angle, считая угол от 0 градусов по часовой стрелке

        Args:
            distance (float): расстояние для перемещения, будет округлено после рассчетов
            angle (float): угол под которым перемещаться, градусы или радианы
            angle_in_degrees (bool, optional): угол в градусах или в радианах, True - градусы. Defaults to True.
        """
        if angle_in_degrees:
            angle = math.radians(angle)
        self.movement(round(math.cos(angle - PI_HALF)*distance),
                      round(math.sin(angle + PI_HALF)*distance))

    @property
    def map_coords(self):
        """
        Получение текущей позиции по формату self.map

        Returns:
            tuple[int, int]: кортеж с координатами как в self.map
        """
        return (self.position.x, self.position.y)

    @property
    def cur_location(self):
        """
        Получение текущей локации из карты

        Returns:
            Location: локация с текущими координатами
        """
        return self.map[self.map_coords]

    def update_map(self, loot_amount: int = 2):
        """
        Создание карты, если режим рогалика включен

        Args:
            loot_amount (int, optional): Кол-во лута на каждой создаваемой локации. Defaults to 2.
        """
        if self.rogue_like and self.map_coords not in self.map:
            chosen_location = random.choices(
                tuple(self.location_pool.keys()),
                tuple(zip(*self.location_pool.values()))[1]
            )[0]

            i = 0
            chosen_loot = Container()
            while i < loot_amount:
                chosen_loot_item = random.choice(tuple(self.location_loot_pool[chosen_location].keys()))
                if chosen_loot_item not in chosen_loot:
                    chosen_loot[chosen_loot_item] = self.location_loot_pool[chosen_location][chosen_loot_item]
                    i += 1

            self.map[self.map_coords] = chosen_location(loot=chosen_loot)
            self.location_pool[chosen_location][0] -= 1
            if self.location_pool[chosen_location][0] == 0:
                self.location_pool.pop(chosen_location)

    def update(self):
        pass

    def main_cycle(self):
        while self.game_active:
            self.update()
            self.command_execution(*self.get_input())

    ############################################################################
    #                       In-Game Methods (Commands)                         #
    ############################################################################

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
        if len(self.cur_location.loot) > 0:
            for _ in range(search_time):
                if random.random() < self.cur_location.loot_chance:
                    found_item = random.choices(
                        tuple(self.cur_location.loot.keys()),
                        tuple(zip(*self.cur_location.loot.values()))[1]
                    )[0]

                    self.player.inventory[found_item] += 1
                    self.cur_location.loot[found_item][0] -= 1
                    print(text_pool["found_something"], found_item)
                else:
                    print(text_pool["nothing_found"])
        else:
            print(text_pool["nothing_to_find"])

    ## Info
    def info(self, func: Optional[str] = None):
        if func is not None:
            if func in self.command_pool:
                print(inspect.getdoc(self.command_pool[func]))
            else:
                print(text_pool["wrong_func_info"], func)
        else:
            print(text_pool["game_info"])

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

    def new_game(self):
        self.update_map()
        self.main_cycle()

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

    ############################################################################
    #                             Base Game Methods                            #
    ############################################################################

    def __init__(self):
        # Pools
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
            "info": self.info,
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
        self.command_pool: dict[str, _F] = dict(
            **system_commands,
            **debug_commands,
            **movement_commands,
            **interaction_commands,
            **info_commands
        )
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

        # Settings
        self.rogue_like: bool = True

        # In-Game vars
        self.game_active: bool = True
        self.time: Time = Time()
        self.event_queue: list[Event] = []
        self.player: Character = Character("Alice", "al")
        self.position: Position = Position()
        self.map: dict[tuple[int, int], Location] = {}

    def type_casting(self, args: list[Any]):
        for i, arg in enumerate(args):
            if arg.isdigit():
                args[i] = int(arg)
            elif "." in arg and arg.replace(".", "", 1).isdigit():
                args[i] = float(arg)
            elif arg.lower() in ("true", "false"):
                args[i] = bool(arg)
            elif arg.lower() == "none":
                args[i] = None

        return args

    def get_input(self):
        user_input = str()
        while not user_input:
            user_input = input(text_pool["command_enter"]).split(maxsplit=1)

        return (
            user_input[0].lower(),  # ! lower() используется, если команды регистрочувствительны, это проблема
            self.type_casting(user_input[1].split()) if len(user_input) > 1 else []
        )

    def command_execution(self, command: str, args: _FARGS):
        if command in self.command_pool:
            sig = inspect.signature(self.command_pool[command])
            args_amount = len(args)
            expected_args_minimum_amount = len(sig.parameters) - len(tuple(k for k, v in sig.parameters.items() if v.default is not inspect.Parameter.empty))
            expected_args_maximum_amount = len(sig.parameters)

            if expected_args_minimum_amount <= args_amount <= expected_args_maximum_amount:
                for arg, expected_arg in zip(args, sig.parameters):
                    expected_type = sig.parameters[expected_arg].annotation
                    if not isinstance(arg, expected_type):
                        print(text_pool["wrong_argument_type1"], arg, ". ",
                              text_pool["wrong_argument_type2"], expected_type, sep="")
                        break
                else:
                    self.command_pool[command](*args)
                    logging.debug("Executed %s with arguments: %s",
                                  self.command_pool[command], *args)
            else:
                print(text_pool["wrong_arguments_amount1"], expected_args_minimum_amount,
                      text_pool["wrong_arguments_amount2"], expected_args_maximum_amount)
        else:
            print(text_pool["wrong_command"])

    def main(self):
        print(text_pool["hello"])
        self.menu({text_pool["new_game_choose"]: (self.new_game, ())})


if __name__ == "__main__":
    text_pool = get_json_file("./translations/ru_RU.json")
    settings = get_json_file("./settings.json")
    game = Game()
    game.main()
