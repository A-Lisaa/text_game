from ... import globs
from ..base import UI


class CLI(UI):
    def start(self):
        globs.game.start()
        self.execute_command()

    def read_user_input(self) -> str:
        while True:
            user_input = input(globs.lines["command_enter"]).strip()
            if user_input:
                return user_input

    def execute_command(self):
        while globs.game.active:
            user_input = self.read_user_input()
            globs.game.engine.execute_command(*globs.game.engine.process_user_input(user_input))
            globs.game.update()

    def print(self, *values, sep = " ", end = "\n"):
        print(*values, sep=sep, end=end)

    def input(self, prompt):
        return input(prompt)

    def menu(self, actions, *, prompt = None, start_number = 1):
        actions = {
            str(position): (name, func)
            for position, (name, func)
            in enumerate(actions.items(), start=start_number)
        }
        while True:
            if prompt is not None:
                self.print(prompt)
            for position, (action, _) in enumerate(actions.values(), start=start_number):
                self.print(f"{position}) {action}")
            answer = self.input(globs.lines["choose_menu_answer"])
            if answer in actions:
                break
            self.print(globs.lines["wrong_menu_answer"])

        actions[answer][1]()

    def yes_no_prompt(self, prompt, yes_func, no_func = lambda: None):
        choices = {
            globs.lines["yes_choice"]: yes_func,
            globs.lines["no_choice"]: no_func
        }
        self.menu(choices, prompt=prompt)
