# pylint: disable=no-name-in-module
from PyQt6.QtWidgets import (QButtonGroup, QDialog, QGridLayout, QLabel,
                             QMainWindow, QPushButton)

from ... import globs
from ..base import UI
from .main_window import Ui_MainWindow


class PyQt6(Ui_MainWindow, UI, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.executeButton.clicked.connect(self.execute_command)
        self.inputField.returnPressed.connect(self.execute_command)

    def start(self):
        self.show()
        globs.game.start()
        if not globs.game.active:
            self.close()

    def execute_command(self):
        inp = self.inputField.text()
        globs.game.engine.execute_command(*globs.game.engine.process_user_input(inp))
        globs.game.update()
        if not globs.game.active:
            self.close()

    def print(self, *values, sep = " ", end = "\n"):
        message = sep.join(str(value) for value in values) + end
        self.outputField.append(message)

    def input(self, prompt):
        ...

    def menu(self, actions, *, prompt = None):
        icon = self.windowIcon()
        font = self.font()

        class Dialog(QDialog):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Menu")
                self.setWindowIcon(icon)
                self.setFont(font)
                #self.setBaseSize(400, 300)
                layout = QGridLayout(self)

                if prompt is not None:
                    self.prompt = QLabel()
                    self.prompt.setText(prompt)
                    layout.addWidget(self.prompt)

                self.buttons_group = QButtonGroup()
                self.buttons_group.buttonClicked.connect(self.close)

                for i, (name, action) in enumerate(actions.items()):
                    button = QPushButton(name)
                    button.clicked.connect(action)
                    setattr(self, f"button{i}", button)
                    self.buttons_group.addButton(getattr(self, f"button{i}"))
                    layout.addWidget(getattr(self, f"button{i}"))

        dialog = Dialog()
        dialog.exec()
        dialog.deleteLater()

    def yes_no_prompt(self, prompt, yes_func, no_func = lambda: None):
        choices = {
            globs.lines["yes_choice"]: yes_func,
            globs.lines["no_choice"]: no_func
        }
        self.menu(choices, prompt=prompt)
