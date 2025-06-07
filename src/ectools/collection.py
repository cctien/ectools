import logging
import operator
from collections.abc import Collection, Mapping, Sequence
from functools import reduce

from omegaconf import DictConfig, OmegaConf

logger = logging.getLogger(__name__)


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
