from abc import abstractmethod

from ..utils.type_aliases import Func


class UI:
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def execute_command(self):
        ...

    @abstractmethod
    def print(self, *values: object, sep: str = " ", end: str = "\n"):
        ...

    @abstractmethod
    def input(self, prompt: str) -> str:
        ...

    @abstractmethod
    def menu(self, actions: dict[str, Func],  *, prompt: str | None = None):
        ...

    @abstractmethod
    def yes_no_prompt(self, prompt: str, yes_func: Func, no_func: Func = lambda: None):
        ...
