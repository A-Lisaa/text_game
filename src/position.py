import attr


@attr.define(frozen=True, order=True)
class Position:
    x: int
    y: int
