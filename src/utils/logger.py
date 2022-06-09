import logging
import os

from .. import globs


def getLogger(
    filename: str = "log",
    level: int = logging.DEBUG,
    mode: str = "w",
    formatter_string: str = "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)d]: %(message)s"
    ) -> logging.Logger:
    """
    Creates a proper logging.Logger object with options from args

    Args:
        level (str, optional): level of messages to log (ascending order: DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to "DEBUG".
        mode (str, optional): writing mode of log file. Defaults to "w".
        formatter_string (str, optional): how to format logging string. Defaults to "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)d]: %(message)s".

    Returns:
        logging.Logger: logging.Logger object
    """
    if not os.path.exists(globs.logs_path):
        os.makedirs(globs.logs_path)
    if not os.path.exists(f"{globs.logs_path}\\{filename}.log"):
        with open(f"{globs.logs_path}\\{filename}.log", "w", encoding="utf-8"):
            pass

    logger = logging.getLogger(filename)
    logger.setLevel(level)

    ch = logging.FileHandler(f"{globs.logs_path}\\{filename}.log", mode, encoding = "utf-8")
    ch.setLevel(level)

    formatter = logging.Formatter(formatter_string)
    ch.setFormatter(formatter)

    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)
    logger.addHandler(ch)

    return logger
