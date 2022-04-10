import attr

from .utils.__init_paths__ import data_path
from .utils.files_IO import read_json_file
from .utils.logger import get_logger

_logger = get_logger(__file__)

@attr.define
class Time:
    """
    Хранит время, при изменении времени мелкое переходит в большее
    """
    _year: int = 0
    _month: int = 1
    _day: int = 1
    _hour: int = 0
    _minute: int = 0
    _second: int = 0
    months_duration: dict[str, int] = read_json_file(f"{data_path}/months_duration.json")

    def is_leap_year(self, year: int | None = None) -> bool:
        """Проверка года на високосность, если year = None, проверяется текущий год класса

        Args:
            year (int | None, optional): Год для проверки. Defaults to None.

        Returns:
            bool: True - високосный, False - нет
        """
        if year is None:
            year = self.year
        if year % 4 == 0 and year % 100 != 0 and year % 400 == 0:
            return True
        return False

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, y: int):
        self._year = y
        _logger.debug("Set year to %i", self.year)

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, m: int):
        self.year += m // 12
        if m % 12 == 0:
            m += 1
        self._month = m % 12
        _logger.debug("Set month to %i", self.month)

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, d: int):
        while d >= 28:
            if self.month == 2:
                # костыли говна из-за високосности
                current_month_duration = self.months_duration["2.25" if self.is_leap_year() else "2.75"]
            else:
                current_month_duration = self.months_duration[str(self.month)]
            if d >= current_month_duration - self._day - 1:
                self.month += 1
                d -= current_month_duration
                self._day = 1
        self._day = d
        _logger.debug("Set day to %i", self.day)

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, h: int):
        self.day += h // 24
        self._hour = h % 24
        _logger.debug("Set hour to %i", self.hour)

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, m: int):
        self.hour += m // 60
        self._minute = m % 60
        _logger.debug("Set minute to %i", self.minute)

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, s: int):
        self.minute += s // 60
        self._second = s % 60
        _logger.debug("Set second to %i", self.second)
