from collections.abc import Callable, Iterable, Mapping
from operator import not_
from typing import Any

from cytoolz import compose as cmp
from cytoolz import keyfilter


def sorted_keys[K, V](
    x: Mapping[K, V],
    key: Callable | None = None,
    factory: Callable[[Iterable[tuple]], Mapping] | None = None,
) -> Mapping[K, V]:
    _factory = factory if factory is not None else type(x)
    return _factory(sorted(items(x), key=key))


def keyfilterfalse[T](
    predicate: Callable[[T], bool],
    mapping: Mapping[T, Any],
    factory: Callable[[Iterable[tuple]], Mapping] = dict,
) -> Mapping[T, Any]:
    return keyfilter(cmp(not_, predicate), mapping, factory=factory)
