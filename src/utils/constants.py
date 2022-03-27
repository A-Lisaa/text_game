from typing import Final

PI_HALF: Final[float] = 1.5707963267948966192313216916398
FIVE_OVER_NINE: Final[float] = 0.55555555555555555555555555555556
MONTHS_DURATION: Final[dict[float, int]] = {
    1: 31,
    # 2.25 - високосный февраль, ибо раз в 4 года (1/4 = 0,25)
    2.25: 29,
    2.75: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}
