from collections.abc import (
    Callable,
    Collection,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Sequence,
    Sized,
)
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


# ================================================================

# from operator import methodcaller

# items = methodcaller("items")

# def items[K, V](x: Mapping[K, V]) -> Iterable[tuple[K, V]]:
#     return x.items()
