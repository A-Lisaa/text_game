from . import globs
from .utils.type_aliases import CommandsDict


class Debug:
    def commands(self) -> CommandsDict:
        return {
            "undo_test": self.undo_test,
            "show_commands": self.show_commands,
        }

    def undo_test(self):
        setattr(globs.game, 'undo_test', [])
        globs.ui.print(globs.game.undo_test)
        globs.game.saved_variables["undo_test"] = globs.game.undo_test
        globs.game.undo_update()
        globs.game.undo_test.append(1488)
        globs.game.undo_test.append(666)
        globs.game.undo_test.append(2154)
        globs.ui.print(globs.game.undo_test)
        globs.game.system.undo()
        globs.ui.print(globs.game.undo_test)
        delattr(globs.game, 'undo_test')

    def show_commands(self):
        for command, func in globs.game.command_pool.items():
            globs.ui.print(f"{command}: {func}", end="\n")
        globs.ui.print(end="\n")
