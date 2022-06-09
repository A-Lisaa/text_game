from . import globs
from .utils.type_aliases import CommandsDict


class Debug:
    def commands(self) -> CommandsDict:
        return {
            "undo_test": self.undo_test
        }

    def undo_test(self):
        setattr(globs.game, 'undo_test', [])
        globs.ui.print(self.undo_test)
        globs.game.saved_variables["undo_test"] = self.undo_test
        globs.game.undo_update()
        globs.game.undo_test.append(1488) # type: ignore
        globs.game.undo_test.append(666) # type: ignore
        globs.game.undo_test.append(2154) # type: ignore
        globs.ui.print(self.undo_test)
        globs.game.system.undo()
        globs.ui.print(self.undo_test)
        delattr(globs.game, 'undo_test')
