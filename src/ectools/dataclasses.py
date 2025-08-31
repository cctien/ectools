import dataclasses
from collections.abc import Callable, Mapping
from typing import Any, Protocol, runtime_checkable


def packed[t](f: Callable[..., t], data: Any) -> t:
    return f(**dataclasses.asdict(data))


def unpacked[t](f: Callable[[t], Any]) -> Callable[[t], Mapping[str, Any]]:
    def _f(*args, **kwargs) -> Mapping[str, Any]:
        return dataclasses.asdict(f(*args, **kwargs))

    return _f


@runtime_checkable
class DataclassLike(Protocol):
    __dataclass_fields__: dict
