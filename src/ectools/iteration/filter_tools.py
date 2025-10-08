from collections.abc import Callable, Collection, Iterable, Sized
from functools import partial as prt
from itertools import filterfalse
from operator import contains, eq, is_
from typing import Any, TypeVar

try:
    from cytoolz import compose as cmp
except ImportError:
    from toolz import compose as cmp


def filter_in[T](c: Collection[T], iterable: Iterable[T]) -> Iterable[T]:
    return filter(prt(contains, c), iterable)


def filter_not_in[T](c: Collection[T], iterable: Iterable[T]) -> Iterable[T]:
    return filterfalse(prt(contains, c), iterable)


T = TypeVar("T")
is_none: Callable[[Any], bool] = prt(is_, None)
is_empty: Callable[[Sized], bool] = cmp(prt(eq, 0), len)
filter_not_none: Callable[[Iterable[T]], Iterable[T]] = prt(filterfalse, is_none)
filter_nonempty: Callable[[Iterable[Sized]], Iterable[Sized]] = prt(filterfalse, is_empty)
filter_not_space: Callable[[Iterable[str]], Iterable[str]] = prt(filterfalse, str.isspace)
