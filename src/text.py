from utils.cfg import Config

_config = Config()


def temperature(degrees: float, celsius: bool = True):
    if celsius and not _config["temperature_in_celsius"]:
        # Перевод в фаренгейт из цельсия
        degrees = 1.8*degrees + 32
    elif not celsius and _config["temperature_in_celsius"]:
        # Перевод в цельсий из фаренгейта
        # 0.56 = 5/9
        degrees = 0.56*(degrees - 32)
    return degrees
