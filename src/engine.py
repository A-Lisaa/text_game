import inspect
from typing import Any

from .ui.base_ui import UI
from .utils.lines import Lines
from .utils.logger import get_logger
from .utils.type_aliases import Func, FuncArgs

_logger = get_logger(__file__)

class Engine:
    def __init__(self, ui: UI, command_pool: dict[str, Func], lines: Lines):
        """Движок для обработки команды

        Args:
            ui (UI): экземпляр пользовательского интерфейса
            command_pool (dict[str, Func]): словарь команд
            lines (Lines): экземпляр текста
        """
        self.ui = ui
        self.command_pool = command_pool
        self.lines = lines
        _logger.debug(
            "Initialized engine with ui: %s, command_pool: %s, lines: %s",
            ui, command_pool, lines
        )

    def cast_types(self, args: list[Any]) -> list[Any]:
        for i, arg in enumerate(args):
            arg = str(arg).lower()
            if arg in ("true", "false"):
                args[i] = bool(arg)
            elif arg == "none":
                args[i] = None
            else:
                try:
                    if arg.find(".") == 1 or arg.find(",") == 1:
                        args[i] = float(arg)
                except ValueError:
                    try:
                        args[i] = int(arg)
                    except ValueError:
                        pass

        return args

    def read_user_input(self) -> str:
        while True:
            user_input = self.ui.input(self.lines["command_enter"]).strip()
            if user_input:
                return user_input

    def split_user_input(self, user_input: str) -> tuple[str, list[Any]]:
        if user_input.find(" ") > 1:
            command, args_string = user_input.split(maxsplit=1)
            args = args_string.split()
        else:
            command, args = user_input, []

        return (command, args)

    def get_command_and_args(self) -> tuple[str, list[Any]]:
        user_input = self.read_user_input()

        command, args = self.split_user_input(user_input)

        # ! lower() используется. если команды регистрочувствительны - это проблема
        return (command.lower(), self.cast_types(args))

    def check_for_command_existence(self, command: str) -> bool:
        if command in self.command_pool:
            return True

        self.ui.print(self.lines["wrong_command"])
        return False

    def check_for_args_amount(self, sig: inspect.Signature, args: FuncArgs) -> bool:
        args_amount = len(args)
        expected_args_minimum_amount = len(sig.parameters) - len(tuple(k for k, v in sig.parameters.items() if v.default is not inspect.Parameter.empty))
        expected_args_maximum_amount = len(sig.parameters)

        if expected_args_minimum_amount <= args_amount <= expected_args_maximum_amount:
            return True

        self.ui.print(
            self.lines["wrong_arguments_amount1"], expected_args_minimum_amount,
            self.lines["wrong_arguments_amount2"], expected_args_maximum_amount
        )
        return False

    def check_for_args_type(self, sig: inspect.Signature, args: FuncArgs) -> bool:
        for arg, expected_arg in zip(args, sig.parameters):
            expected_type = sig.parameters[expected_arg].annotation
            if not isinstance(arg, expected_type):
                self.ui.print(
                    self.lines["wrong_argument_type1"], arg, ". ",
                    self.lines["wrong_argument_type2"], expected_type, sep=""
                )
                return False
        return True

    def execute_command(self, command: str, args: FuncArgs):
        if self.check_for_command_existence(command):
            sig = inspect.signature(self.command_pool[command])
            if self.check_for_args_amount(sig, args):
                if self.check_for_args_type(sig, args):
                    self.command_pool[command](*args)
                    _logger.debug(
                        "Executed %s with arguments: %s",
                        self.command_pool[command], *args
                    )
