from collections.abc import Iterable, Iterator, Mapping, MutableMapping

from frozendict import frozendict


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
