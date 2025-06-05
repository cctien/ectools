from collections.abc import Collection, Mapping
import logging

from omegaconf import OmegaConf, DictConfig

logger = logging.getLogger(__name__)


def identity[t](x: t) -> t:
    return x
