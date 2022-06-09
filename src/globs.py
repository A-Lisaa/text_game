version: str = "0.0.1"

base_path: str = "."
appdata_path: str = f"{base_path}/__appdata__"
data_path: str = f"{base_path}/data"
translations_path: str = f"{data_path}/translations"
logs_path: str = f"{appdata_path}/log"
settings_path: str = f"{appdata_path}/settings.json"

from logging import Logger as _Logger

logger: _Logger = _Logger("log")

from .utils.cfg import Config as _Config

config: _Config = _Config()

from .utils.lines import Lines as _Lines

lines: _Lines = _Lines()

from .ui.base import UI as _UI
from .ui.cli.cli import CLI as _CLI

ui: _UI = _CLI()

from .game import Game as _Game

game: _Game = _Game()
