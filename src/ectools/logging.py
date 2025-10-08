import logging
import os
import os.path as osp
from collections.abc import Iterable, Mapping

from rich.logging import RichHandler
from wadler_lindig import pformat

from .iteration.mapping_tools import to_frozendict
from .time import time_now_filing

noisy_loggers_to_be_suppressed = ("requests", "urlib3")
default_log_file_dirname = "results/logs"
default_log_file_name = "log.txt"
default_fmt: str = "%(asctime)s-%(name)s-%(levelname)s\t%(message)s"
default_datefmt: str = "%Y%m%d-%H:%M:%S"


class RichPrettyHandler(RichHandler):
    def emit(self, record):
        record.msg = pformat(record.msg)
        super().emit(record)


class PrettyHandler(logging.StreamHandler):
    def emit(self, record):
        record.msg = pformat(record.msg)
        super().emit(record)


def add_handler_root_logger_(handler: logging.Handler) -> None:
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)


def set_logger_level_handlers_lowest_(logger: logging.Logger):
    """
    Adjust the logger's level to match the most verbose (lowest) level among its handlers.
    This ensures the logger won't filter out messages that any handler would want to process.

    Args:
        logger: A logging.Logger instance with handlers attached
    """
    logger.setLevel(min(handler.level for handler in (*logger.handlers, logger)))


def get_full_log_file_path(dirname: str | None, time_subdir: bool, filename: str | None) -> str:
    dirname = dirname or default_log_file_dirname
    log_subdir = time_now_filing() if time_subdir else ""
    filename = filename or default_log_file_name
    result = osp.join(dirname, log_subdir, filename)

    full_dirname = osp.dirname(result)
    if time_subdir:
        assert not osp.exists(full_dirname), f"Log directory {full_dirname} already exists."
    os.makedirs(full_dirname, exist_ok=True)
    return result


def get_file_handler(
    level: int | str = logging.INFO,
    dirname: str | None = None,
    time_subdir: bool = False,
    filename: str | None = None,
    fmt: str = default_fmt,
    datefmt: str = default_datefmt,
) -> logging.Handler:
    if dirname is not None:
        os.makedirs(dirname, exist_ok=True)
    full_log_file_path = get_full_log_file_path(dirname, time_subdir, filename)
    file_handler = logging.FileHandler(full_log_file_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return file_handler


def get_stream_handler(
    level: int | str = logging.INFO,
    use_rich_handler: bool = True,
    use_wadler_lindig: bool = True,
    fmt: str = default_fmt,
    datefmt: str = default_datefmt,
) -> logging.Handler:
    console_handler: logging.Handler
    match (use_rich_handler, use_wadler_lindig):
        case (False, False):
            console_handler = logging.StreamHandler()
        case (False, True):
            console_handler = PrettyHandler()
        case (True, False):
            console_handler = RichHandler()
        case (True, True):
            console_handler = RichPrettyHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    return console_handler


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
        stream = to_frozendict(stream)
        stream = stream.setdefault("level", level)
        console_handler = get_stream_handler(**stream)
        logger.addHandler(console_handler)

    if file is not None:
        file = to_frozendict(file)
        file = file.setdefault("level", level)
        file_handler = get_file_handler(**file)
        logger.addHandler(file_handler)

    if wandb is not None:
        from .logging_wandb_tools import get_wandb_handler

        wandb = to_frozendict(wandb)
        wandb = wandb.setdefault("level", level)
        wandb_handler = get_wandb_handler(**wandb)
        logger.addHandler(wandb_handler)

    set_logger_level_handlers_lowest_(logger)
    return logger
