from abc import ABC, abstractmethod

from ...character import Character


class IConsumable(ABC):
    @abstractmethod
    def consume(self, character: Character):
        ...
