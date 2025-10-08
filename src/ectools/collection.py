from collections.abc import Callable, Collection, Iterable, Mapping, Sequence, Sized
from functools import partial as prt
from operator import eq
from typing import Any

from class_registry import ClassRegistry

try:
    from cytoolz import compose as cmp
except ImportError:
    from toolz import compose as cmp

from .iteration.mapping_tools import to_frozendict

len_0: Callable[[Sized], bool] = cmp(prt(eq, 0), len)
is_empty: Callable[[Sized], bool] = cmp(prt(eq, 0), len)


def ordered_unique(seq: Iterable) -> Sequence:
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)


def sole_item[T](x: Collection[T]) -> T:
    assert len(x) == 1
    return next(iter(x))


def unique_item[T](x: Iterable[T]) -> T:
    set_x = set(x)
    assert len(set_x) == 1
    return next(iter(set_x))


def instantiate[T](registry: ClassRegistry[T], configuration: Mapping[str, Any], **kwargs) -> T:
    cnfgr = to_frozendict(configuration)
    return registry.get(cnfgr["cls"], **cnfgr.delete("cls"), **kwargs)


# ================================================================

# from collections.abc import Collection, Hashable, Iterable, Mapping, Sequence, ValuesView

# from omegaconf import DictConfig, OmegaConf
# from plum import dispatch


# def tplchain[t](*iterables: Iterable[t]) -> Sequence[t]:
#     return tuple(ctn(*iterables))


# @dispatch
# def getitem(tbl: Sequence, key: int | slice) -> object:
#     return tbl.__getitem__(key)


# @dispatch
# def getitem(key: int | slice, tbl: Sequence) -> object:
#     return tbl.__getitem__(key)


# @dispatch
# def getitem(tbl: Mapping, key: Hashable) -> object:
#     return tbl.__getitem__(key)


# @dispatch
# def getitem(key: Hashable, tbl: Mapping) -> object:
#     return tbl.__getitem__(key)


# @dispatch
# def get(tbl: dict, key: Hashable, default: object = None) -> object:
#     return tbl.get(key, default)


# @dispatch
# def get(key: Hashable, tbl: dict, default: object = None) -> object:
#     return tbl.get(key, default)


# def to_dict_from_collection_rcrs[t](x: Collection | t) -> Collection | t:
#     if isinstance(x, DictConfig):
#         return OmegaConf.to_container(x, resolve=True)
#     if isinstance(x, dict):
#         return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
#     if isinstance(x, Mapping):
#         return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
#     if isinstance(x, list):
#         return [to_dict_from_collection_rcrs(item) for item in x]
#     if isinstance(x, tuple):
#         return tuple(to_dict_from_collection_rcrs(item) for item in x)
#     return x


# def mapping_to_dict_rcrs[t](x: Mapping) -> dict:
#     if isinstance(x, DictConfig):
#         return OmegaConf.to_container(x, resolve=True)
#     if isinstance(x, dict):
#         return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
#     if isinstance(x, Mapping):
#         return {k: to_dict_from_collection_rcrs(v) for k, v in x.items()}
#     raise TypeError(f"Unsupported type for mapping_to_dict_rcrs: {type(x)}. Expected Mapping.")

#     raise TypeError(f"Unsupported type for to_container: {type(x)}.")


# def mappings_values(tbl: Mapping) -> ValuesView:
#     return tbl.values()


# # python -m src.ectools.collection
# if __name__ == "__main__":
#     from functools import partial as prt

#     from rich.pretty import pprint
#     from wadler_lindig import pformat

#     tbl = {"a": 1, "b": 2, "c": 3}
#     assert getitem("b", tbl) == 2
#     assert getitem(tbl, "b") == 2
#     pprint(pformat("tests passed"))

#     assert prt(getitem, "b")(tbl) == 2
#     assert prt(getitem, tbl)("b") == 2
#     pprint(pformat("tests passed"))

#     assert get(tbl, "r") is None
#     assert get("r", tbl) is None
#     pprint(pformat("tests passed"))

#     assert prt(get, tbl)("r") is None
#     assert prt(get, "r")(tbl) is None
#     pprint(pformat("tests passed"))
