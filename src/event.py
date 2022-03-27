from abc import ABC, abstractmethod

import attr


@attr.define(hash=True)
class Event(ABC):
    max_triggers_number: int = -1
    trigger_chance: float = 0.5
    _triggers_number = 0

    @abstractmethod
    def action(self) -> None:
        ...

    @abstractmethod
    def trigger(self) -> bool:
        ...
