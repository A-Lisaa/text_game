from __init_paths__ import lines_path
from files_IO import read_json_file, write_json_file
from logger import get_logger

_logger = get_logger(__name__)

class Lines:
    def __init__(self, lines_filepath: str = lines_path):
        self.lines_filepath = lines_filepath
        self._lines = self._get_lines()

    def __getitem__(self, name: str) -> str:
        return self.get_line(name)

    def __setitem__(self, name: str, value: str):
        self._lines[name] = value

    def _get_lines(self, line_filepath: str | None = None) -> dict[str, str]:
        if line_filepath is None:
            line_filepath = self.lines_filepath
        return read_json_file(line_filepath)

    def _set_lines(self, line_filepath: str | None = None):
        if line_filepath is None:
            line_filepath = self.lines_filepath
        write_json_file(self._lines, line_filepath)

    def get_line(self, name: str) -> str:
        self._lines = self._get_lines()
        try:
            return self._lines[name]
        except KeyError:
            _logger.error("Line %s not found", name)
            return name

    def set_line(self, name: str, value: str):
        self._lines[name] = value
        self._set_lines()
        _logger.info("Line %s set with value: %s", name, value)
