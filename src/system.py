import inspect
import os
import pickle
from typing import Any

from . import globs
from .utils.type_aliases import CommandsDict


class System:
    def commands(self) -> CommandsDict:
        return {
            "undo": self.undo,
            "info": self.info,
            "help": self.info,
            "save": self.save,
            "load": self.load,
            "quit": self.quit,
            "exit": self.quit,
        }

    def undo(self):
        for name, value in globs.game.undo_queue[-1].items():
            setattr(globs.game, name, value)

    def info(self, func: str | None = None):
        """
        Информация о информации? Серьезно?
        """
        if func is not None:
            if func in globs.game.command_pool:
                globs.ui.print(inspect.getdoc(globs.game.command_pool[func]))
            else:
                globs.ui.print(globs.lines["wrong_func_info"], func)
        else:
            globs.ui.print(globs.lines["game_info"])

    def quit(self):
        def yes():
            globs.game.active = False
        globs.ui.yes_no_prompt(globs.lines["quit_message"], yes)

    def save(self, variables: Any, save_name: str = "save"):
        if not os.path.exists(globs.config["saves_path"]):
            os.makedirs(globs.config["saves_path"])

        with open(f"{globs.config['saves_path']}/{save_name}.sav", "wb", encoding="utf-8") as save_file:
            pickle.dump(variables, save_file)

        globs.logger.info("Saved a game with %s to %s", variables, save_name)

    def load(self, save_name: str = "save"):
        if not os.path.exists(f"{globs.config['saves_path']}/{save_name}.sav"):
            globs.ui.print(globs.lines["save_not_found_error"])
            return

        variables = []
        with open(f"{globs.config['saves_path']}/{save_name}.sav", "rb") as save_file:
            while True:
                try:
                    variables.append(pickle.load(save_file))
                except EOFError:
                    break
        variables = variables[0]

        if len(variables) != len(globs.game.saved_variables):
            globs.ui.print(globs.lines["incompatible_save"])
            return

        for name, value in variables.items():
            if name in globs.game.saved_variables:
                setattr(globs.game, name, value)
            else:
                globs.ui.print(globs.lines["incompatible_save"])
                return

        globs.logger.info("Loaded a game from %s to %s", save_name, globs.game)
