from collections.abc import Callable, Mapping, Sequence
from typing import Any

Func = Callable[..., Any]
FuncArgs = Sequence[Any]
FuncKwargs = Mapping[str, Any]
FuncTuple = tuple[Func, FuncArgs, FuncKwargs]
