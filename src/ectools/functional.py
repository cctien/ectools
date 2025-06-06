from collections.abc import Collection, Mapping
import logging

from omegaconf import OmegaConf, DictConfig

logger = logging.getLogger(__name__)


def identity[t](x: t) -> t:
    return x


def being(a: object, b: object) -> bool:
    return b is a


def not_being(a: object, b: object) -> bool:
    return b is not a
