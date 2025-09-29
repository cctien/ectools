from collections.abc import Callable, Collection, Iterable, Mapping, Sized
from functools import partial as prt
from itertools import filterfalse
from operator import contains, is_
from typing import Any

from frozendict import frozendict

from ..collection import len_0


def sorted_keys[K, V](
    x: Mapping[K, V],
    key: Callable | None = None,
    factory: Callable[[Iterable[tuple]], Mapping] | None = None,
) -> Mapping[K, V]:
    _factory = factory if factory is not None else type(x)
    return _factory(sorted(items(x), key=key))


filter_not_none: Callable[[Iterable[Any]], Iterable[Any]] = prt(filterfalse, prt(is_, None))
filter_nonempty: Callable[[Iterable[Sized]], Iterable[Sized]] = prt(filterfalse, len_0)
filter_not_space: Callable[[Iterable[str]], Iterable[str]] = prt(filterfalse, str.isspace)


def filter_in[T](c: Collection[T], iterable: Iterable[T]) -> Iterable[T]:
    return filter(prt(contains, c), iterable)


def filter_not_in[T](c: Collection[T], iterable: Iterable[T]) -> Iterable[T]:
    return filterfalse(prt(contains, c), iterable)
