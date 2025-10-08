from collections.abc import Callable, Iterable, Mapping, MutableMapping
from itertools import filterfalse
from operator import itemgetter
from typing import Any

try:
    from cytoolz import compose as cmp
    from cytoolz import identity
except ImportError:
    from toolz import compose as cmp
    from toolz import identity
from frozendict import deepfreeze, frozendict
from omegaconf import DictConfig, OmegaConf


def sorted_keys(x: Mapping, key: Callable = identity, reverse: bool = False) -> Iterable[tuple]:
    return sorted(x.items(), key=cmp(key, itemgetter(0)), reverse=reverse)


sorted_keys_mapping: Callable[[Mapping, Callable, bool], Mapping] = cmp(frozendict, sorted_keys)
sorted_keys_dict: Callable[[Mapping, Callable, bool], MutableMapping] = cmp(dict, sorted_keys)


def filter_keys[T](predicate: Callable[[T], bool], tbl: Mapping[T, Any]) -> Iterable[tuple[T, Any]]:
    return filter(cmp(predicate, itemgetter(0)), tbl.items())


filter_keys_mapping: Callable[[Mapping, Callable | None, bool], Mapping] = cmp(
    frozendict, filter_keys
)
filter_keys_dict: Callable[[Mapping, Callable | None, bool], MutableMapping] = cmp(
    dict, filter_keys
)


def filterfalse_keys[T](
    predicate: Callable[[T], bool], tbl: Mapping[T, Any]
) -> Iterable[tuple[T, Any]]:
    return filterfalse(cmp(predicate, itemgetter(0)), tbl.items())


filterfalse_keys_mapping: Callable[[Mapping, Callable | None, bool], Mapping] = cmp(
    frozendict, filterfalse_keys
)
filterfalse_keys_dict: Callable[[Mapping, Callable | None, bool], MutableMapping] = cmp(
    dict, filterfalse_keys
)


def to_mapping(x: Mapping) -> Mapping:
    if isinstance(x, DictConfig):
        return deepfreeze(OmegaConf.to_container(x, resolve=True))
    return deepfreeze(x)


to_dict: Callable[[Mapping], MutableMapping] = cmp(dict, to_mapping)
