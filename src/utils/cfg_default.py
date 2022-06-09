from typing import Final

from .. import globs

# Конфиг по умолчанию
CFG_DEFAULT: Final[str] = f"""
{{
    "debug_enabled": true,

    "lines_path": "{globs.translations_path}/ru_RU.json",
    "saves_path": "{globs.appdata_path}/saves",

    "rogue_like": true,
    "undo_depth": 10,
    "temperature_in_celsius": true
}}
"""
