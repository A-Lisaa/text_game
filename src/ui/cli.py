from ..utils.lines import Lines
from ..utils.type_aliases import FuncTuple
from .base_ui import UI


class CLI(UI):
    def __init__(self, lines: Lines):
        self.lines = lines

    def print(self, *values: object, sep: str = " ", end: str = "\n"):
        print(*values, sep=sep, end=end)

    def input(self, prompt: str) -> str:
        return input(prompt)

    def menu(self, actions: dict[str, FuncTuple], *, prompt: str | None = None, start_number: int = 1):
        actions = {str(k): v for k, v in enumerate(actions.values(), start=start_number)}
        while True:
            if prompt is not None:
                print(prompt)
            print(self.lines["choose_menu_answer"], end="")
            for position, action in enumerate(actions, start=start_number):
                print(f"{position}) {action}")
            answer = input()
            if answer in actions:
                break
            print(self.lines["wrong_menu_answer"])

        actions[answer][0](*actions[answer][1], **actions[answer][2])

    def yes_no_prompt(self, prompt: str, yes_tuple: FuncTuple, no_tuple: FuncTuple = (lambda: None, [], {})):
        choices = {
            self.lines["yes_choice"]: yes_tuple,
            self.lines["no_choice"]: no_tuple
        }
        self.menu(choices, prompt=prompt)
