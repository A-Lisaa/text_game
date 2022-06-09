from .. import globs
from .files_IO import read_json_file, write_json_file


class Lines:
    def __init__(self, lines_filepath: str | None = None):
        """Держатель текста, работать через кв. скобки или через методы

        Args:
            lines_filepath (str, optional): Путь к файлу с текстом. Defaults to _config["lines_path"].
        """
        self.lines_filepath = lines_filepath if lines_filepath is not None else globs.config["lines_path"]
        self._lines = self._get_lines()

    def __getitem__(self, name: str) -> str:
        return self.get_line(name)

    def __setitem__(self, name: str, value: str):
        self._lines[name] = value

    def _get_lines(self, line_filepath: str | None = None) -> dict[str, str]:
        return read_json_file(line_filepath if line_filepath is not None else self.lines_filepath)

    def _set_lines(self, line_filepath: str | None = None):
        if line_filepath is None:
            line_filepath = self.lines_filepath
        write_json_file(self._lines, line_filepath if line_filepath is not None else self.lines_filepath)

    def get_line(self, name: str) -> str:
        try:
            return self._lines[name]
        except KeyError:
            globs.logger.error("Line %s not found", name)
            return name

    def set_line(self, name: str, value: str):
        self._lines[name] = value
        self._set_lines()
        globs.logger.info("Line %s set with value: %s", name, value)

    def update_lines(self, lines_filepath: str | None = None):
        if lines_filepath is None:
            lines_filepath = self.lines_filepath
        self._lines = self._get_lines(lines_filepath)
