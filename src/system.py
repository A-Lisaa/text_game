import os
import pickle
from typing import Any

from utils.cfg import Config
from utils.lines import Lines
from utils.logger import get_logger

_logger = get_logger(__file__)
_config = Config()
_text_pool = Lines()


def save(variables: Any, save_name: str = "save"):
    if not os.path.exists(_config["saves_path"]):
        os.makedirs(_config["saves_path"])

    with open(f"{_config['saves_path']}/{save_name}.sav", "wb", encoding="utf-8") as save_file:
        pickle.dump(variables, save_file)

    _logger.info("Saved a game with %s to %s", variables, save_name)

def load(final_object: object, save_name: str = "save"):
    if not os.path.exists(f"{_config['saves_path']}/{save_name}.sav"):
        print(_text_pool["save_not_found_error"])
        return

    variables = []
    with open(f"{_config['saves_path']}/{save_name}.sav", "rb") as save_file:
        while True:
            try:
                variables.append(pickle.load(save_file))
            except EOFError:
                break
    variables = variables[0]

    for name, value in variables.items():
        if name in final_object:
            setattr(final_object, name, value)
        else:
            _logger.error("No name %s in %s", name, dir(final_object))

    _logger.info("Loaded a game from %s to %s", save_name, final_object)
