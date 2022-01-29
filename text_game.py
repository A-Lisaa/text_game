import inspect
import json
import logging
import random
from typing import Any, Callable


class Game:
    class Position:
        def __init__(self):
            self.x = 0
            self.y = 0

    class Location:
        class LocationType:
            def __init__(self, name: str):
                self.name = name

        def __init__(self, name: str, type_: LocationType):
            self.name = name
            self.type = type_

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

    @property
    def map_coords(self):
        return f"{self.position.x}; {self.position.y}"

    def update_map(self):
        if self.map_coords not in self.map:
            self.map[self.map_coords] = random.choice(self.location_pool)

    ### Commands

    ## Movement
    def north(self):
        self.position.x += 1
        self.update_map()

    def south(self):
        self.position.x -= 1
        self.update_map()

    def east(self):
        self.position.y += 1
        self.update_map()

    def west(self):
        self.position.y -= 1
        self.update_map()

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

    ### Game methods

    def __init__(self):
        self.command_pool = {
                             # System
                             "exit": self.exit,
                             "gll": self.get_logging_level,
                             "sll": self.set_logging_level,
                             # Movement
                             "n": self.north,
                             "north": self.north,
                             "s": self.south,
                             "south": self.south,
                             "w": self.west,
                             "west": self.west,
                             "e": self.east,
                             "east": self.east,
                             # Info
                             "gp": self.get_position,
                             "getpos": self.get_position,
                             "get_position": self.get_position,
                             "gl": self.get_location,
                             "getloc": self.get_location,
                             "get_location": self.get_location,
                             "sm": self.show_map,
                             "show_map": self.show_map
                            }

        with open("./translations/ru_RU.json", encoding="utf-8") as f:
            self.text_pool = json.load(f)

        self.location_pool = (
            self.Location("City", self.Location.LocationType("city")),
            self.Location("Forest", self.Location.LocationType("forest"))
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
                    logging.debug("Executed %s with arguments: %s", self.command_pool[command], *args)
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
