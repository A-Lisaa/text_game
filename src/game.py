import inspect
import logging
from typing import Any

from character import Character
from event import Event
from plan import Plan
from text import yes_no_prompt
from time_tracker import Time
from utils import get_settings, get_text
from utils.type_aliases import Func, FuncArgs

settings = get_settings()
text = get_text()


class Game:
    ############################################################################
    #                          Not In-Game Methods                             #
    ############################################################################

    def undo_update(self):
        self.undo_queue.append(self.saved_variables)

        if len(self.undo_queue) > settings["undo_depth"]:
            self.undo_queue.pop(0)

    def events_update(self):
        for event in self.event_queue:
            if event.trigger():
                event.action()

    def update(self):
        self.undo_update()
        self.events_update()

    def main_cycle(self):
        while self.active:
            self.update()
            self.command_execution(*self.get_input())

    ############################################################################
    #                       In-Game Methods (Commands)                         #
    ############################################################################

    def info(self, func: str | None = None):
        if func is not None:
            if func in self.command_pool:
                print(inspect.getdoc(self.command_pool[func]))
            else:
                print(text_pool["wrong_func_info"], func)
        else:
            print(text_pool["game_info"])

    def undo(self):
        for name, value in self.undo_queue[-1].items():
            setattr(self, name, value)

    ## System

    def quit(self):
        def yes():
            self.active = False
        yes_no_prompt(text_pool["quit_message"], (yes, (), {}))

    def new_game(self):
        self.update_map()
        self.main_cycle()

    ############################################################################
    #                             Base Game Methods                            #
    ############################################################################

    def __init__(self):

        ## In-Game vars
        self.active: bool = True

        ## Saved variables
        self.time: Time = Time()
        self.event_queue: list[Event] = []
        self.player: Character = Character("Alice", "al")
        self.plans: list[Plan] = []

        self.saved_variables = {
            "time": self.time,
            "event_queue": self.event_queue,
            "player": self.player
        }
        if settings["rogue_like"]:
            self.saved_variables["map"] = self.map
        self.undo_queue: list[dict[str, Any]] = []

        system_commands = {
            "save": self.save,
            "load": self.load,
            "exit": self.quit,
        }
        debug_commands = {
            "gll": self.get_logging_level,
            "sll": self.set_logging_level,
            "mv": self.map.movement,
            "movement": self.map.movement,
            "rmv": self.map.rotation_movement,
            "rotation_movement": self.map.rotation_movement,
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
        self.command_pool: dict[str, Func] = dict(
            **system_commands,
            **movement_commands,
            **interaction_commands,
            **info_commands
        )
        if settings["debug_enabled"]:
            self.command_pool.update(
                debug_commands
            )


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
            user_input[0].lower(),  # ! lower() используется. если команды регистрочувствительны - это проблема
            self.type_casting(user_input[1].split()) if len(user_input) > 1 else []
        )

    def command_execution(self, command: str, args: FuncArgs):
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
    text_pool = read_json_file("./translations/ru_RU.json")
    settings = read_json_file("./settings.json")
    game = Game()
    game.main()
