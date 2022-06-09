from .. import globs


def convert_temperature(temperature: float, in_celsius: bool = True):
    if in_celsius and not globs.config["temperature_in_celsius"]:
        # Перевод в фаренгейт из цельсия
        temperature = 1.8*temperature + 32
    elif not in_celsius and globs.config["temperature_in_celsius"]:
        # Перевод в цельсий из фаренгейта
        # 0.56 = 5/9
        temperature = 0.56*(temperature - 32)
    return temperature
