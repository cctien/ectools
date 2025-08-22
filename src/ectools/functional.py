import functools
from collections.abc import Iterable, Sized


def len_0(x: Sized, /) -> bool:
    return len(x) == 0


def zps(*iterables: Iterable) -> zip:
    return zip(*iterables, strict=True)
