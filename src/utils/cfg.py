import json
import os
from typing import Any

from .. import globs
from .cfg_default import CFG_DEFAULT
from .files_IO import read_json_file, write_json_file


class Config:
    def __init__(self, settings_filepath: str | None = None):
        """Класс конфига, получайте и ставьте значения через кв. скобки или методами

        Args:
            settings_filepath (str, optional): Путь к файлу настроек. Defaults to settings_path.
        """

        self.settings_filepath = settings_filepath if settings_filepath is not None else globs.settings_path
        self._defaults = json.loads(CFG_DEFAULT)
        self._settings = self._get_settings()

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
            globs.logger.error("Setting %s not found", name)
            return name

    def set_setting(self, name: str, value: Any):
        self._settings[name] = value
        self._set_settings()
        globs.logger.debug("Set %s with value: %s", name, value)

    def get_default(self, name: str) -> Any:
        try:
            return self._defaults[name]
        except KeyError:
            globs.logger.error("Default setting %s not found", name)
            return name

    def set_default(self, name: str):
        self.set_setting(name, self.get_default(name))
        globs.logger.debug("Setting %s set to default", name)

    def set_all_defaults(self):
        self._settings = self._defaults
        globs.logger.debug("All settings set to default")

    def update_settings(self, settings_filepath: str | None = None):
        if settings_filepath is not None:
            settings_filepath = self.settings_filepath
        self._settings = self._get_settings()
