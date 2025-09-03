from collections.abc import Callable, ItemsView, Iterable, Mapping, Sequence
from functools import partial as prt
from itertools import filterfalse
from operator import is_

from .collection import len_0


def items(x: Mapping) -> ItemsView:
    return x.items()


filter_not_none: Callable[[Iterable], Iterable] = prt(filterfalse, prt(is_, None))
filter_nonempty: Callable[[Iterable], Iterable] = prt(filterfalse, len_0)

# ================================================================


def tplmap[S, T](func: Callable[[S], T], *iterables: Iterable[S]) -> Sequence[T]:
    return tuple(map(func, *iterables))
