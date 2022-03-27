from utils.cfg import Config
from utils.constants import FIVE_OVER_NINE
from utils.lines import Lines
from utils.type_aliases import FuncTuple

_config = Config()
_lines = Lines()


def temperature(degrees: float, celsius: bool = True):
    if celsius and not _config["temperature_in_celsius"]:
        # Перевод в фаренгейт из цельсия
        degrees = 1.8*degrees + 32
    elif not celsius and _config["temperature_in_celsius"]:
        # Перевод в цельсий из фаренгейта
        degrees = FIVE_OVER_NINE*(degrees - 32)
    return degrees


def menu(prompt: str, actions: dict[str, FuncTuple], start_number: int = 1):
    actions = {str(k): v for k, v in enumerate(actions.values(), start=start_number)}
    while True:
        print(prompt)
        print(_lines["choose_menu_answer"], end="")
        for position, action in enumerate(actions, start=start_number):
            print(f"{position}) {action}")
        answer = input()
        if answer in actions:
            break
        print(_lines["wrong_menu_answer"])

    actions[answer][0](*actions[answer][1], **actions[answer][2])


def yes_no_prompt(prompt: str, yes_tuple: FuncTuple, no_tuple: FuncTuple = (lambda: None, [], {})):
    choices = {
        _lines["yes_choice"]: yes_tuple,
        _lines["no_choice"]: no_tuple
    }
    menu(prompt, choices)
