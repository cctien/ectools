import copy
import logging
from collections.abc import Mapping

import wandb
from rich.logging import RichHandler

from .collection import mapping_to_dict_rcrs

noisy_loggers_to_be_suppressed = ("requests", "urlib3")
default_log_file_name = "log.txt"
default_fmt: str = "%(asctime)s-%(name)s-%(levelname)s\t%(message)s"
default_datefmt: str = "%Y%m%d-%H:%M:%S"


def wandb_init(cnfgr: Mapping):
    cnfgr = mapping_to_dict_rcrs(copy.deepcopy(cnfgr))
    cnfgr_wandb = cnfgr.pop("wandb")
    return wandb.init(config=cnfgr, **cnfgr_wandb)


class WandbHandler(logging.Handler):
    def emit(self, record):
        wandb.log({"log": self.fmt(record)})


def get_wandb_handler(
    level: int | str = logging.INFO,
    fmt: str = default_fmt,
    datefmt: str = default_datefmt,
) -> WandbHandler:
    wandb_handler = WandbHandler()
    wandb_handler.setLevel(level)
    wandb_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return wandb_handler
