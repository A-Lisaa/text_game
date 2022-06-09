import inspect
from typing import Any

from . import globs
from .utils.type_aliases import Func, FuncArgs


class Engine:
    def __init__(self, command_pool: dict[str, Func]):
        self._command_pool = command_pool

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

    def split_user_input(self, user_input: str) -> tuple[str, list[Any]]:
        if user_input.find(" ") > 1:
            command, args_string = user_input.split(maxsplit=1)
            args = args_string.split()
        else:
            command, args = user_input, []

        return (command, args)

    def process_user_input(self, user_input: str) -> tuple[str, list[Any]]:
        user_input = user_input.strip()
        command, args = self.split_user_input(user_input)

        # ! lower() используется. если команды регистрочувствительны - это проблема
        return (command.lower(), self.cast_types(args))

    def check_for_command_existence(self, command: str) -> bool:
        if command in self._command_pool:
            return True

        globs.ui.print(globs.lines["wrong_command"])
        return False

    def check_for_args_amount(self, sig: inspect.Signature, args: FuncArgs) -> bool:
        args_amount = len(args)
        expected_args_minimum_amount = len(sig.parameters) - len(tuple(k for k, v in sig.parameters.items() if v.default is not inspect.Parameter.empty))
        expected_args_maximum_amount = len(sig.parameters)

        if expected_args_minimum_amount <= args_amount <= expected_args_maximum_amount:
            return True

        globs.ui.print(
            globs.lines["wrong_arguments_amount1"], expected_args_minimum_amount,
            globs.lines["wrong_arguments_amount2"], expected_args_maximum_amount
        )
        return False

    def check_for_args_type(self, sig: inspect.Signature, args: FuncArgs) -> bool:
        for arg, expected_arg in zip(args, sig.parameters):
            expected_type = sig.parameters[expected_arg].annotation
            if not isinstance(arg, expected_type):
                globs.ui.print(
                    globs.lines["wrong_argument_type1"], arg, ". ",
                    globs.lines["wrong_argument_type2"], expected_type, sep=""
                )
                return False
        return True

    def execute_command(self, command: str, args: FuncArgs):
        if self.check_for_command_existence(command):
            sig = inspect.signature(self._command_pool[command])
            if self.check_for_args_amount(sig, args):
                if self.check_for_args_type(sig, args):
                    self._command_pool[command](*args)
                    globs.logger.debug(
                        "Executed %s with arguments: %s",
                        self._command_pool[command], args
                    )
