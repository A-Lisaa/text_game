import copy
from typing import Any

from . import globs
from .character import Character
from .debug import Debug
from .engine import Engine
from .event import Event
from .plan import Plan
from .system import System
from .time_tracker import Time
from .utils.type_aliases import CommandsDict, Func


class Game:
    def undo_update(self):
        self.undo_queue.append(copy.deepcopy(self.saved_variables))

        if len(self.undo_queue) > globs.config["undo_depth"]:
            self.undo_queue.pop(0)

    def events_update(self):
        for event in self.event_queue:
            if event.trigger():
                event.action()

    def update(self):
        self.undo_update()
        self.events_update()

    def __init__(self):

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
        # if globs.config["rogue_like"]:
        #     self.saved_variables["map"] = self.map
        self.undo_queue: list[dict[str, Any]] = []

        ## In-Game vars
        self.active: bool = True
        self.system = System()
        self.debug = Debug()

        system_commands: CommandsDict = self.system.commands()
        movement_commands: CommandsDict = {
            # # 90 degrees
            # "n": self.north,
            # "north": self.north,
            # "s": self.south,
            # "south": self.south,
            # "w": self.west,
            # "west": self.west,
            # "e": self.east,
            # "east": self.east,
            # # 45 degrees
            # "ne": self.north_east,
            # "north_east": self.north_east,
            # "se": self.south_east,
            # "south_east": self.south_east,
            # "sw": self.south_west,
            # "south_west": self.south_west,
            # "nw": self.north_west,
            # "north_west": self.north_west,
        }
        interaction_commands: CommandsDict = {
            # "srch": self.search,
            # "search": self.search
        }
        info_commands: CommandsDict = {
            # "gp": self.get_position,
            # "getpos": self.get_position,
            # "get_position": self.get_position,
            # "el": self.examine_location,
            # "examloc": self.examine_location,
            # "examine_location": self.examine_location,
            # "sm": self.show_map,
            # "show_map": self.show_map,
            # "si": self.show_inventory,
            # "showinv": self.show_inventory,
            # "show_inv": self.show_inventory,
            # "show_inventory": self.show_inventory
        }
        self.command_pool: dict[str, Func] = dict(
            **system_commands,
            **movement_commands,
            **interaction_commands,
            **info_commands
        )
        if globs.config["debug_enabled"]:
            self.command_pool.update(**self.debug.commands())

        self.engine = Engine(self.command_pool)

    def new_game(self):
        return None

    def start(self):
        globs.ui.print(globs.lines["hello"])
        globs.ui.menu(
            {
                globs.lines["new_game_choose"]: self.new_game,
                "Выйти": self.system.quit
            }
        )
