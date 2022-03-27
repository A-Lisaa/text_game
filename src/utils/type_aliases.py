from collections.abc import Callable
from typing import Any, TypeAlias

Func: TypeAlias = Callable[[], Any | None]
FuncArgs: TypeAlias = tuple[Any | None, ...] | list[Any | None]
FuncKwargs: TypeAlias = dict[str, Any]
FuncTuple: TypeAlias = tuple[Func, FuncArgs, FuncKwargs]
