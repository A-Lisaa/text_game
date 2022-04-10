import inspect
from typing import Any

from .character import Character
from .engine import Engine
from .event import Event
from .plan import Plan
from .time_tracker import Time
from .ui.base_ui import UI
from .ui.cli import CLI
from .utils.cfg import Config
from .utils.lines import Lines
from .utils.type_aliases import Func

_config = Config()
_lines = Lines()


class Game:
    ############################################################################
    #                          Not In-Game Methods                             #
    ############################################################################

    def undo_update(self):
        self.undo_queue.append(self.saved_variables)

        if len(self.undo_queue) > _config["undo_depth"]:
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
            self.engine.execute_command(*self.engine.get_command_and_args())

    ############################################################################
    #                       In-Game Methods (Commands)                         #
    ############################################################################

    def info(self, func: str | None = None):
        if func is not None:
            if func in self.command_pool:
                self.ui.print(inspect.getdoc(self.command_pool[func]))
            else:
                self.ui.print(_lines["wrong_func_info"], func)
        else:
            self.ui.print(_lines["game_info"])

    def undo(self):
        for name, value in self.undo_queue[-1].items():
            setattr(self, name, value)

    ## System

    def quit(self):
        def yes():
            self.active = False
        self.ui.yes_no_prompt(_lines["quit_message"], (yes, (), {}))

    def new_game(self):
        self.update_map()
        self.main_cycle()

    ############################################################################
    #                             Base Game Methods                            #
    ############################################################################

    def __init__(self, ui: UI, lines: Lines):

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
        if _config["rogue_like"]:
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
        if _config["debug_enabled"]:
            self.command_pool.update(
                debug_commands
            )

        ## In-Game vars
        self.ui = ui
        self.lines = lines
        self.engine = Engine(ui, self.command_pool, lines)
        self.active: bool = True

    def main(self):
        self.ui.print(_lines["hello"])
        self.ui.menu({_lines["new_game_choose"]: (self.new_game, (), {})})


def main():
    lines = Lines()
    ui = CLI(lines)
    game = Game(ui, lines)
    game.main()
