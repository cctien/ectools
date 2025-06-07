import functools
import logging
from collections.abc import Callable, Sized
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


def identity[t](x: t) -> t:
    return x


def ngt(f: Callable[P, bool], /) -> Callable[P, bool]:
    @functools.wraps(f)
    def ngt_x(*args, **kwargs):
        return not f(*args, **kwargs)

    return ngt_x


def est(y: object, x: object, /) -> bool:
    return x is y


def is_empty(x: Sized, /) -> bool:
    return len(x) == 0
