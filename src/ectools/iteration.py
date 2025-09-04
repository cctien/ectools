from collections.abc import Callable, ItemsView, Iterable, Mapping, Sequence
from functools import partial as prt
from itertools import filterfalse
from operator import is_

from .collection import len_0


def items[K, V](x: Mapping[K, V]) -> Iterable[tuple[K, V]]:
    return x.items()


def sorted_keys[K, V](
    x: Mapping[K, V],
    key: Callable | None = None,
    factory: Callable[[Iterable[tuple]], Mapping] | None = None,
) -> Mapping[K, V]:
    _factory = factory if factory is not None else type(x)
    return _factory(sorted(items(x), key=key))


filter_not_none: Callable[[Iterable], Iterable] = prt(filterfalse, prt(is_, None))
filter_nonempty: Callable[[Iterable], Iterable] = prt(filterfalse, len_0)

# ================================================================


def tplmap[S, T](func: Callable[[S], T], *iterables: Iterable[S]) -> Sequence[T]:
    return tuple(map(func, *iterables))
