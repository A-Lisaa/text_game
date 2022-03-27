from __future__ import annotations

import attr


@attr.define(order=True)
class Position:
    x: int = 0
    y: int = 0
