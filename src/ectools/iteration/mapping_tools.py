from collections.abc import Callable, Iterable, Mapping, MutableMapping
from itertools import filterfalse
from operator import itemgetter
from types import MappingProxyType
from typing import Any, TypeVar

try:
    from cytoolz import compose as cmp
    from cytoolz import identity
except ImportError:
    from toolz import compose as cmp
    from toolz import identity
from frozendict import deepfreeze, frozendict
from omegaconf import DictConfig, OmegaConf


def sorted_keys[C, V](
    x: Mapping[C, V], key: Callable[[C], Any] = identity, reverse: bool = False
) -> Iterable[tuple[C, V]]:
    return sorted(x.items(), key=cmp(key, itemgetter(0)), reverse=reverse)


def filter_keys[C, V](predicate: Callable[[C], bool], tbl: Mapping[C, V]) -> Iterable[tuple[C, V]]:
    return filter(cmp(predicate, itemgetter(0)), tbl.items())


def filterfalse_keys[C, V](
    predicate: Callable[[C], bool], tbl: Mapping[C, V]
) -> Iterable[tuple[C, V]]:
    return filterfalse(cmp(predicate, itemgetter(0)), tbl.items())


def to_dict[C, V](x: Mapping[C, V]) -> MutableMapping[C, V]:
    if isinstance(x, DictConfig):
        return OmegaConf.to_container(x, resolve=True)  # type: ignore
    return dict(x)


C = TypeVar("C")
V = TypeVar("V")
sorted_keys_dict: Callable[[Mapping[C, V], Callable[[C], Any], bool], MutableMapping[C, V]] = cmp(
    dict, sorted_keys
)
sorted_keys_mapping: Callable[[Mapping[C, V], Callable[[C], Any], bool], Mapping[C, V]] = cmp(
    MappingProxyType, sorted_keys_dict
)
filter_keys_dict: Callable[[Callable[[C], bool], Mapping[C, V]], MutableMapping[C, V]] = cmp(
    dict, filter_keys
)
filter_keys_mapping: Callable[[Callable[[C], bool], Mapping[C, V]], Mapping[C, V]] = cmp(
    MappingProxyType, filter_keys_dict
)
filterfalse_keys_dict: Callable[[Callable[[C], bool], Mapping[C, V]], MutableMapping[C, V]] = cmp(
    dict, filterfalse_keys
)
filterfalse_keys_mapping: Callable[[Callable[[C], bool], Mapping[C, V]], Mapping[C, V]] = cmp(
    MappingProxyType, filterfalse_keys_dict
)
to_mapping: Callable[[Mapping[C, V]], Mapping[C, V]] = cmp(MappingProxyType, to_dict)
to_frozendict: Callable[[Mapping[C, V]], frozendict[C, V]] = cmp(deepfreeze, to_mapping)
