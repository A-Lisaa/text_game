import logging
import os

from .__init_paths__ import logs_path


def get_logger(
    name: str,
    level: int = logging.DEBUG,
    mode: str = "a",
    formatter_string: str = "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)d]: %(message)s"
    ) -> logging.Logger:
    """
    Creates a proper logging.Logger object with options from args

    Args:
        name (str): path and name of the file to log in. Use __file__ variable\n
        level (str, optional): level of messages to log (ascending order: DEBUG, INFO, WARNING, ERROR, CRITICAL). Defaults to "DEBUG".\n
        mode (str, optional): writing mode of log file. Defaults to "a".\n
        formatter_string (str, optional): how to format logging string. Defaults to "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)d]: %(message)s".\n

    Returns:
        logging.Logger: logging.Logger object
    """
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    if not os.path.exists(f"{logs_path}\\{os.path.splitext(os.path.split(name)[-1])[0]}.log"):
        with open(f"{logs_path}\\{os.path.splitext(os.path.split(name)[-1])[0]}.log", "w", encoding="utf-8"):
            pass

    logger = logging.getLogger()
    logger.setLevel(level)

    ch = logging.FileHandler(f"{logs_path}\\{os.path.splitext(os.path.split(name)[-1])[0]}.log", mode, encoding = "utf-8")
    ch.setLevel(level)

    formatter = logging.Formatter(formatter_string)
    ch.setFormatter(formatter)

    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)
    logger.addHandler(ch)

    return logger
