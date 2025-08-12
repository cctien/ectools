import logging
from collections.abc import Callable, Collection, Hashable, Iterable, Mapping, Sequence, ValuesView
from itertools import chain

from omegaconf import DictConfig, OmegaConf
from plum import dispatch

logger = logging.getLogger(__name__)


def sorted_keys(
    tbl: Mapping, /, *, key: Callable | None = None, reverse: bool = False, factory: Callable = dict
) -> Mapping:
    return factory((k, tbl[k]) for k in sorted(tbl.keys(), key=key, reverse=reverse))


def ordered_unique(seq: Iterable) -> Sequence:
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def sole_item[t](x: Collection[t]) -> t:
    assert len(x) == 1
    return next(iter(x))


def unique_item[t](x: Iterable[t]) -> t:
    set_x = set(x)
    assert len(set_x) == 1
    return next(iter(set_x))


def tplchain[t](*iterables: Iterable[t]) -> Sequence[t]:
    return tuple(chain(*iterables))


@dispatch
def getitem(tbl: Sequence, key: int | slice) -> object:
    return tbl.__getitem__(key)


@dispatch
def getitem(key: int | slice, tbl: Sequence) -> object:
    return tbl.__getitem__(key)


@dispatch
def getitem(tbl: Mapping, key: Hashable) -> object:
    return tbl.__getitem__(key)


@dispatch
def getitem(key: Hashable, tbl: Mapping) -> object:
    return tbl.__getitem__(key)


@dispatch
def get(tbl: dict, key: Hashable, default: object = None) -> object:
    return tbl.get(key, default)


@dispatch
def get(key: Hashable, tbl: dict, default: object = None) -> object:
    return tbl.get(key, default)


def to_dict_from_collection_rcrs[t](x: Collection | t) -> Collection | t:
    if isinstance(x, DictConfig):
        return OmegaConf.to_container(x, resolve=True)
    if isinstance(x, dict):
        return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
    if isinstance(x, Mapping):
        return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
    if isinstance(x, list):
        return [to_dict_from_collection_rcrs(item) for item in x]
    if isinstance(x, tuple):
        return tuple(to_dict_from_collection_rcrs(item) for item in x)
    return x


def mapping_to_dict_rcrs[t](x: Mapping) -> dict:
    if isinstance(x, DictConfig):
        return OmegaConf.to_container(x, resolve=True)
    if isinstance(x, dict):
        return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
    if isinstance(x, Mapping):
        return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
    raise TypeError(f"Unsupported type for mapping_to_dict_rcrs: {type(x)}. Expected Mapping.")


def mappings_values(tbl: Mapping) -> ValuesView:
    return tbl.values()


# python -m src.ectools.collection
if __name__ == "__main__":
    from functools import partial as prt

    from rich.pretty import pprint
    from toolz import curry as crr
    from wadler_lindig import pformat

    tbl = {"a": 1, "b": 2, "c": 3}
    assert getitem("b", tbl) == 2
    assert getitem(tbl, "b") == 2
    pprint(pformat(f"tests passed"))

    assert prt(getitem, "b")(tbl) == 2
    assert prt(getitem, tbl)("b") == 2
    pprint(pformat(f"tests passed"))

    assert get(tbl, "r") is None
    assert get("r", tbl) is None
    pprint(pformat(f"tests passed"))

    assert prt(get, tbl)("r") is None
    assert prt(get, "r")(tbl) is None
    pprint(pformat(f"tests passed"))
