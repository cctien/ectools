import logging
import operator
from collections.abc import Collection, Hashable, Iterable, Mapping, Sequence
from functools import reduce

from omegaconf import DictConfig, OmegaConf
from plum import dispatch

logger = logging.getLogger(__name__)


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
def sole_item(x: Collection) -> object:
    assert len(x) == 1
    return next(iter(x))


@dispatch
def unique_item(x: Iterable) -> object:
    return sole_item(set(x))


@dispatch
def get(key: Hashable, tbl: dict, default: object = None) -> object:
    return tbl.get(key, default)


def cnct(*args: Sequence) -> Sequence:
    return reduce(operator.concat, args)


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
