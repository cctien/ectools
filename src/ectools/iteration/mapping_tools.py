from collections.abc import Callable, Iterable, Mapping
from itertools import filterfalse
from operator import itemgetter
from typing import Any

from cytoolz import compose as cmp
from frozendict import frozendict


def sorted_keys(x: Mapping, key: Callable | None = None) -> Iterable[tuple]:
    if key is None:
        return sorted(x.items(), key=itemgetter(0))
    return sorted(x.items(), key=cmp(key, itemgetter(0)))


def sorted_keys_mapping[K, V](
    x: Mapping[K, V],
    key: Callable | None = None,
    factory: Callable[[Iterable[tuple]], Mapping] = frozendict,
) -> Mapping[K, V]:
    return factory(sorted_keys(x, key=key))


def filter_key[T](predicate: Callable[[T], bool], tbl: Mapping[T, Any]) -> Iterable[tuple[T, Any]]:
    return filter(cmp(predicate, itemgetter(0)), tbl.items())


def filterfalse_key[T](
    predicate: Callable[[T], bool], tbl: Mapping[T, Any]
) -> Iterable[tuple[T, Any]]:
    return filterfalse(cmp(predicate, itemgetter(0)), tbl.items())


def filter_key_mapping[T](
    predicate: Callable[[T], bool],
    tbl: Mapping[T, Any],
    factory: Callable[[Iterable[tuple]], Mapping] = frozendict,
) -> Mapping[T, Any]:
    return factory(filter_key(predicate, tbl))


def filterfalse_key_mapping[T](
    predicate: Callable[[T], bool],
    tbl: Mapping[T, Any],
    factory: Callable[[Iterable[tuple]], Mapping] = frozendict,
) -> Mapping[T, Any]:
    return factory(filterfalse_key(predicate, tbl))


filter_key_frozendict = cmp(frozendict, filter_key)
filterfalse_key_frozendict = cmp(frozendict, filterfalse_key)

filter_key_dict = cmp(dict, filter_key)
filterfalse_key_dict = cmp(dict, filterfalse_key)
