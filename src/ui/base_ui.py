from abc import ABC, abstractmethod

from utils.type_aliases import FuncTuple


class UI(ABC):
    @abstractmethod
    def print(self, *values: object, sep: str = " ", end: str = "\n"):
        ...

    @abstractmethod
    def input(self, message: str) -> str:
        ...

    @abstractmethod
    def menu(self, actions: dict[str, FuncTuple],  *, prompt: str | None = None):
        ...

    @abstractmethod
    def yes_no_prompt(self, prompt: str, yes_tuple: FuncTuple, no_tuple: FuncTuple = (lambda: None, [], {})):
        ...
