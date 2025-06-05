from collections.abc import Mapping
import logging

from omegaconf import OmegaConf, DictConfig

logger = logging.getLogger(__name__)


def identity[t](x: t) -> t:
    return x


def mapping_to_dict_rcrs[t](x: Mapping | t) -> dict | t:
    if isinstance(x, DictConfig):
        return OmegaConf.to_container(x, resolve=True)
    if isinstance(x, dict):
        return {k: mapping_to_dict_rcrs(v) for k, v in x.items()}
    if isinstance(x, Mapping):
        return {k: mapping_to_dict_rcrs(v) for k, v in x.items()}
    if isinstance(x, list):
        return [mapping_to_dict_rcrs(item) for item in x]
    if isinstance(x, tuple):
        return tuple(mapping_to_dict_rcrs(item) for item in x)
    return x
