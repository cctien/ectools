from collections.abc import Iterable, Mapping
from copy import deepcopy
from datetime import datetime
import logging
import os

from rich.logging import RichHandler

from .collection import mapping_to_dict_rcrs

noisy_loggers_to_be_suppressed = ("requests", "urlib3")
default_log_file_name = "log.txt"
default_fmt: str = "%(asctime)s-%(name)s-%(levelname)s\t%(message)s"
default_datefmt: str = "%Y%m%d-%H:%M:%S"


def set_logger_level_handlers_lowest_(logger: logging.Logger):
    """
    Adjust the logger's level to match the most verbose (lowest) level among its handlers.
    This ensures the logger won't filter out messages that any handler would want to process.

    Args:
        logger: A logging.Logger instance with handlers attached
    """
    logger.setLevel(min(handler.level for handler in (*logger.handlers, logger)))


def get_full_log_file_path(log_dir: str | None, log_time_subdir: bool, log_file: str | None) -> str:

    log_dir = log_dir or ""
    if log_time_subdir:
        now = datetime.now()
        log_subdir = now.strftime("%Y%m%d_%H%M%S%f")
    else:
        log_subdir = ""

    log_file = default_log_file_name if log_file is None else log_file
    log_file_dirname, log_file_basename = os.path.split(log_file)

    full_log_dir = os.path.join(log_dir, log_subdir, log_file_dirname)
    if log_time_subdir:
        assert not os.path.exists(full_log_dir), f"Log directory {full_log_dir} already exists."
    os.makedirs(full_log_dir, exist_ok=True)

    return os.path.join(full_log_dir, log_file_basename)


def get_stream_handler(
    level: int | str = logging.INFO,
    use_rich_handler: bool = True,
    fmt: str = default_fmt,
    datefmt: str = default_datefmt,
) -> logging.Handler:
    if not use_rich_handler:
        console_handler = logging.StreamHandler()
    else:
        console_handler = RichHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return console_handler


def get_file_handler(
    level: int | str = logging.INFO,
    log_dir: str | None = "outputs/logs/",
    log_time_subdir: bool = False,
    log_file: str | None = None,
    fmt: str = default_fmt,
    datefmt: str = default_datefmt,
) -> logging.Handler:
    if log_dir is not None:
        os.makedirs(log_dir, exist_ok=True)
    full_log_file_path = get_full_log_file_path(log_dir, log_time_subdir, log_file)
    file_handler = logging.FileHandler(full_log_file_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return file_handler


def set_root_logger(
    level: int | str = logging.INFO,
    stream: Mapping | None = {},
    file: Mapping | None = None,
    wandb: Mapping | None = None,
    force_clear_handlers: bool = True,
    suppressed_loggers: Iterable[str] = noisy_loggers_to_be_suppressed,
) -> logging.Logger:

    logger = logging.getLogger()
    logger.setLevel(level)

    if force_clear_handlers and logger.hasHandlers():
        logger.handlers.clear()

    if stream is not None:
        stream = mapping_to_dict_rcrs(deepcopy(stream))
        stream["level"] = level if stream.get("level") is None else stream["level"]
        console_handler = get_stream_handler(**stream)
        logger.addHandler(console_handler)

    if file is not None:
        file = mapping_to_dict_rcrs(deepcopy(file))
        file["level"] = level if file.get("level") is None else file["level"]
        file_handler = get_file_handler(**file)
        logger.addHandler(file_handler)

    if wandb is not None:
        from .logging_wandb_tools import get_wandb_handler

        wandb = mapping_to_dict_rcrs(deepcopy(wandb))
        wandb["level"] = level if wandb.get("level") is None else wandb["level"]
        wandb_handler = get_wandb_handler(**wandb)
        logger.addHandler(wandb_handler)

    set_logger_level_handlers_lowest_(logger)
    return logger
