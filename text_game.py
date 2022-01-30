import inspect
import json
import logging
import attr
import math
import random
from abc import ABC, abstractmethod
from typing import Any, Callable


PI_HALF = 1.5707963267948966


class Game:
    @attr.define
    class Position:
        x: int = 0
        y: int = 0

    @attr.define
    class Location(ABC):
        name: str

    @attr.define
    class LocationCity(Location):
        pass

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
                print(self.text_pool["yes_no_invalid_input"])

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
        return f"{self.position.x}; {self.position.y}"

    def update_map(self):
        if self.rogue_like and self.map_coords not in self.map:
            self.map[self.map_coords] = random.choice(self.location_pool)

    ### Commands

    ## Movement
    # 90 degrees
    def north(self):
        self.rotation_movement(1, 0)
        #self.movement(0, 1)

    def south(self):
        self.rotation_movement(1, 180)
        #self.movement(0, -1)

    def east(self):
        self.rotation_movement(1, 90)
        #self.movement(1, 0)

    def west(self):
        self.rotation_movement(1, 270)
        #self.movement(-1, 0)

    # 45 degrees
    def north_east(self):
        self.rotation_movement(2, 45)

    def south_east(self):
        self.rotation_movement(2, 135)

    def south_west(self):
        self.rotation_movement(2, 225)

    def north_west(self):
        self.rotation_movement(2, 315)

    ## Info
    def get_position(self):
        print(f"x: {self.position.x}\ny: {self.position.y}")

    def get_location(self):
        print(self.map[self.map_coords])

    def show_map(self):
        print(self.map)

    ## System

    # Exit
    def exit_yes(self):
        self.game_active = False

    def exit(self):
        logging.info("Initiated exit")
        self.yes_no_prompt(self.text_pool["exit_message"], self.exit_yes)

    # Logging
    def get_logging_level(self):
        print(logging.root.level)

    def set_logging_level(self, logging_level: int):
        logging.basicConfig(level=logging_level, force=True)

    def antigravity(self):
        import antigravity

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
        info_commands = {
            "gp": self.get_position,
            "getpos": self.get_position,
            "get_position": self.get_position,
            "gl": self.get_location,
            "getloc": self.get_location,
            "get_location": self.get_location,
            "sm": self.show_map,
            "show_map": self.show_map
        }
        self.command_pool = dict(
            **system_commands,
            **debug_commands,
            **movement_commands,
            **info_commands
        )

        with open("./translations/ru_RU.json", encoding="utf-8") as json_file:
            self.text_pool = json.load(json_file)

        self.rogue_like = True

        self.location_pool = (
            self.Location("City"),
            self.Location("Forest")
        )

        self.game_active = True
        self.position = self.Position()
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
        user_input = input(self.text_pool["command_enter"]).split(maxsplit=1)
        command = user_input[0].lower() # ! lower() is used, maybe it will have consequences
        args = self.type_casting(user_input[1].split()) if len(user_input) > 1 else []

        return (command, args)

    def command_execution(self, command: str, args: list[Any]):
        if command in self.command_pool:
            expected_args = inspect.get_annotations(self.command_pool[command])
            if len(args) == len(expected_args):
                for arg, expected_arg in zip(args, expected_args.values()):
                    if not isinstance(arg, expected_arg):
                        print(self.text_pool["wrong_argument_type1"], arg, ". ",
                              self.text_pool["wrong_argument_type2"], type(expected_arg), sep="")
                        break
                else:
                    self.command_pool[command](*args)
                    logging.debug("Executed %s with arguments: %s",
                                  self.command_pool[command], *args)
            else:
                print(self.text_pool["wrong_arguments_amount"], len(expected_args))
        else:
            print(self.text_pool["wrong_command"])

    def main(self):
        print(self.text_pool["hello"])
        self.update_map()
        while self.game_active:
            self.command_execution(*self.get_input())


if __name__ == "__main__":
    game = Game()
    game.main()
