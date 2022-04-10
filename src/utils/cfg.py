import json
import os
from typing import Any

from .__init_paths__ import settings_path
from .cfg_default import CFG_DEFAULT
from .files_IO import read_json_file, write_json_file
from .logger import get_logger

_logger = get_logger(__file__)

class Config:
    def __init__(self, settings_filepath: str = settings_path):
        """Класс конфига, получайте и ставьте значения через кв. скобки или методами

        Args:
            settings_filepath (str, optional): Путь к файлу настроек. Defaults to settings_path.
        """
        self.settings_filepath = settings_filepath
        self._settings = self._get_settings()
        self._defaults = json.loads(CFG_DEFAULT)

    def __getitem__(self, name: str) -> Any:
        return self.get_setting(name)

    def __setitem__(self, name: str, value: Any):
        self.set_setting(name, value)

    def _get_settings(self, settings_filepath: str | None = None) -> dict[str, Any]:
        if settings_filepath is None:
            settings_filepath = self.settings_filepath
        if not os.path.exists(settings_filepath):
            self._settings = self._defaults
            self._set_settings()
        return read_json_file(settings_filepath)

    def _set_settings(self, settings_filepath: str | None = None):
        if settings_filepath is None:
            settings_filepath = self.settings_filepath
        write_json_file(self._settings, settings_filepath)

    def get_setting(self, name: str) -> Any:
        self._settings = self._get_settings()
        try:
            return self._settings[name]
        except KeyError:
            _logger.error("Setting %s not found", name)
            return name

    def set_setting(self, name: str, value: Any):
        self._settings[name] = value
        self._set_settings()
        _logger.debug("Set %s with value: %s", name, value)

    def get_default(self, name: str) -> Any:
        try:
            return self._defaults[name]
        except KeyError:
            _logger.error("Default setting %s not found", name)
            return name

    def set_default(self, name: str):
        self.set_setting(name, self.get_default(name))
        _logger.debug("Setting %s set to default", name)

    def set_all_defaults(self):
        self._settings = self._defaults
        _logger.debug("All settings set to default")

    def update_settings(self, settings_filepath: str | None = None):
        if settings_filepath is not None:
            settings_filepath = self.settings_filepath
        self._settings = self._get_settings()
