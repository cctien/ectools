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
from typing import Any, Protocol, Unpack, overload

from cytoolz import compose as cmp
from frozendict import frozendict

from .collection import len_0

# ================================================================


@overload
def tuplecmap[S, T](f: Callable[[S], T]) -> Callable[[Iterable[S]], Sequence[T]]: ...


@overload
def tuplecmap[S1, S2, T](
    f: Callable[[S1, S2], T],
) -> Callable[[Iterable[S1], Iterable[S2]], Sequence[T]]: ...
@overload
def tuplecmap[S1, S2, S3, T](
    f: Callable[[S1, S2, S3], T],
) -> Callable[[Iterable[S1], Iterable[S2], Iterable[S3]], Sequence[T]]: ...


@overload
def tuplecmap[S1, S2, S3, S4, T](
    f: Callable[[S1, S2, S3, S4], T],
) -> Callable[[Iterable[S1], Iterable[S2], Iterable[S3], Iterable[S4]], Sequence[T]]: ...


@overload
def tuplecmap[S1, S2, S3, S4, S5, T](
    f: Callable[[S1, S2, S3, S4, S5], T],
) -> Callable[
    [Iterable[S1], Iterable[S2], Iterable[S3], Iterable[S4], Iterable[S5]], Sequence[T]
]: ...


def tuplecmap[T](f: Callable[..., T]) -> Callable[..., Sequence[T]]:
    return cmp(tuple, prt(map, f))


# ================================================================


def tplmap[T](f: Callable[..., T], *iterables: Iterable) -> Sequence[T]:
    return tuple(map(f, *iterables))


def zps(*iterables: Iterable) -> zip:
    return zip(*iterables, strict=True)


def zip_mappings[T](**kwargs: Iterable[T]) -> Iterator[Mapping[str, T]]:
    """Zip keyword arguments into frozendicts."""
    keys = tuple(kwargs.keys())
    for values in zip(*kwargs.values()):
        yield frozendict(zip(keys, values))


def zps_mappings[T](**kwargs: Iterable[T]) -> Iterator[Mapping[str, T]]:
    """Zip keyword arguments into frozendicts with strict=True."""
    keys = tuple(kwargs.keys())
    for values in zip(*kwargs.values(), strict=True):
        yield frozendict(zip(keys, values))


def zip_dicts[T](**kwargs: Iterable[T]) -> Iterator[MutableMapping[str, T]]:
    """Zip keyword arguments into dictionaries."""
    keys = tuple(kwargs.keys())
    for values in zip(*kwargs.values()):
        yield dict(zip(keys, values))


def zps_dicts[T](**kwargs: Iterable[T]) -> Iterator[MutableMapping[str, T]]:
    """Zip keyword arguments into dictionaries with strict=True."""
    keys = tuple(kwargs.keys())
    for values in zip(*kwargs.values(), strict=True):
        yield dict(zip(keys, values))


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


# ================================================================

# from operator import methodcaller

# items = methodcaller("items")

# def items[K, V](x: Mapping[K, V]) -> Iterable[tuple[K, V]]:
#     return x.items()
#     return x.items()
# ================================================================

# from operator import methodcaller

# items = methodcaller("items")

# def items[K, V](x: Mapping[K, V]) -> Iterable[tuple[K, V]]:
#     return x.items()
#     return x.items()
