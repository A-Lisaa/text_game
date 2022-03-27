import json
import os
from typing import Any

from logger import get_logger

_logger = get_logger(__name__)

def read_json_file(path: str) -> dict[str, str]:
    if not os.path.exists(path):
        _logger.error("Could not find file %s", path)
        return {}
    with open(path, encoding="utf-8") as json_file:
        return json.load(json_file)

def write_json_file(obj: Any, path: str):
    os.makedirs(path)
    with open(path, mode="w", encoding="utf-8") as json_file:
        json.dump(obj, json_file)
