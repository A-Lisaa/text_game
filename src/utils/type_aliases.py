from collections.abc import Callable, Mapping, Sequence
from typing import Any

# Любая функция
Func = Callable[..., Any]
# Любые позиц. аргументы функции
FuncArgs = Sequence[Any]
# Любые ключевые аргументы функции
FuncKwargs = Mapping[str, Any]
# Кортеж из функции, позиц. аргументов и ключ. аргументов
FuncTuple = tuple[Func, FuncArgs, FuncKwargs]
