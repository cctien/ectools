from collections.abc import Callable, Generator, Iterable, Mapping, Sequence, Sized
from functools import partial as prt
from itertools import filterfalse
from operator import is_
from typing import Any, Protocol, overload

from cytoolz import compose as cmp
from frozendict import frozendict

from .collection import len_0


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


def tplmap[T](f: Callable[..., T], *iterables: Iterable) -> Sequence[T]:
    return tuple(map(f, *iterables))


def zps(*iterables: Iterable) -> zip:
    return zip(*iterables, strict=True)


def zps_dicts[T](**kwargs: Iterable[T]) -> Generator[Mapping[str, T], None, None]:
    """Zip keyword arguments into dictionaries."""
    if not kwargs:
        return
    keys = tuple(kwargs.keys())
    for values in zps(*kwargs.values()):
        yield dict(zip(keys, values))


def zip_frozendicts[T](**kwargs: Iterable[T]) -> Generator[Mapping[str, T], None, None]:
    """Zip keyword arguments into dictionaries."""
    if not kwargs:
        return
    keys = tuple(kwargs.keys())
    for values in zip(*kwargs.values()):
        yield frozendict(zip(keys, values))


def zps_frozendicts[T](**kwargs: Iterable[T]) -> Generator[Mapping[str, T], None, None]:
    """Zip keyword arguments into dictionaries."""
    if not kwargs:
        return
    keys = tuple(kwargs.keys())
    for values in zps(*kwargs.values()):
        yield frozendict(zip(keys, values))


def zip_dicts[T](**kwargs: Iterable[T]) -> Generator[dict[str, T], None, None]:
    """Zip keyword arguments into dictionaries."""
    if not kwargs:
        return
    keys = tuple(kwargs.keys())
    for values in zip(*kwargs.values()):
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

# ================================================================

# from operator import methodcaller

# items = methodcaller("items")

# def items[K, V](x: Mapping[K, V]) -> Iterable[tuple[K, V]]:
#     return x.items()
