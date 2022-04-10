from typing import Final

from .__init_paths__ import appdata_path, translations_path

# Конфиг по умолчанию
CFG_DEFAULT: Final[str] = f"""
{{
    "debug_enabled": true,

    "lines_path": "{translations_path}/ru_RU.json",
    "saves_path": "{appdata_path}/saves",

    "rogue_like": true,
    "undo_depth": 10,
    "temperature_in_celsius": true
}}
"""
