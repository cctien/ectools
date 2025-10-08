from collections.abc import Callable, Collection, Iterable, Sized
from functools import partial as prt
from itertools import filterfalse
from operator import contains, is_
from typing import Any

from ..collection import len_0

filter_not_none: Callable[[Iterable[Any]], Iterable[Any]] = prt(filterfalse, prt(is_, None))
filter_nonempty: Callable[[Iterable[Sized]], Iterable[Sized]] = prt(filterfalse, len_0)
filter_not_space: Callable[[Iterable[str]], Iterable[str]] = prt(filterfalse, str.isspace)


def filter_in[T](c: Collection[T], iterable: Iterable[T]) -> Iterable[T]:
    return filter(prt(contains, c), iterable)


def filter_not_in[T](c: Collection[T], iterable: Iterable[T]) -> Iterable[T]:
    return filterfalse(prt(contains, c), iterable)
