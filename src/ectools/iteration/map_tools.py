from collections.abc import Callable, Iterable, Sequence
from functools import partial as prt
from typing import overload

from cytoolz import compose as cmp

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
