import argparse
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import is_dataclass
from functools import partial as prt
from itertools import filterfalse, takewhile
from operator import contains, eq, methodcaller
from typing import Any, Protocol

from class_registry import ClassRegistry
from frozendict import deepfreeze
from omegaconf import DictConfig, OmegaConf

from .dataclasses import DataclassLike
from .iteration.mapping_tools import filterfalse_keys_mapping


class DictConfigMerger(Protocol):
    def __call__(self, *x: DictConfig) -> DictConfig: ...


merged: DictConfigMerger = OmegaConf.merge  # type: ignore


def dictconfig_created(default: Mapping | DataclassLike | None) -> DictConfig:
    if default is None:
        return OmegaConf.create()
    if is_dataclass(default):
        return OmegaConf.structured(default)
    return OmegaConf.create(default)  # type: ignore


def dictconfig_ex_file(filepath: str) -> DictConfig:
    if not filepath:
        return OmegaConf.create()
    return OmegaConf.load(filepath)  # type: ignore


def dictconfig_ex_dotlist(dotlist: Sequence[str]) -> DictConfig:
    return OmegaConf.from_dotlist(dotlist)  # type: ignore


def dictconfig_with_cnfgr_file(default: Mapping | DataclassLike | None) -> DictConfig:
    cnfgr = dictconfig_created(default)
    cnfgr_file = cnfgr.pop("cnfgr_file", "")
    return merged(cnfgr, dictconfig_ex_file(cnfgr_file))


def parser_augmented_with_cnfgr_file(
    parser: argparse.ArgumentParser | None,
) -> argparse.ArgumentParser:
    parser = parser if parser is not None else argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--cnfgr",
        "--cnfgr_file",
        "--configuration_file",
        dest="cnfgr_file",
        help="Path to the YAML/JSON configuration file",
        type=str,
        default=None,
    )
    return parser


startswith_dash = methodcaller("startswith", "-")


def parsed_arguments(parser: argparse.ArgumentParser | None) -> tuple[DictConfig, DictConfig]:
    import sys

    all_args = tuple(sys.argv[1:])
    fst_idx_without_dash = len(list(takewhile(startswith_dash, all_args)))
    if any(map(startswith_dash, all_args[fst_idx_without_dash:])):
        raise ValueError("Additional command line arguments ought not to start with `-`")
    if not fst_idx_without_dash == len(list(filter(startswith_dash, all_args))):
        raise ValueError("Additional command line arguments ought not to start with `-`")

    parser = parser_augmented_with_cnfgr_file(parser)
    known_args, unknown_args_dotlist = parser.parse_known_args()
    cnfgr = dictconfig_with_cnfgr_file(vars(known_args))
    cnfgr_unknown = dictconfig_ex_dotlist(unknown_args_dotlist)
    return cnfgr, cnfgr_unknown


def merged_with_unknown(
    cnfgr_known: DictConfig, cnfgr_unknown: DictConfig, strict_level: int
) -> DictConfig:
    match strict_level:
        case 0:
            return merged(cnfgr_known, cnfgr_unknown)
        case 1:
            unavailable = tuple(filterfalse(prt(contains, cnfgr_known), cnfgr_unknown.keys()))
            if unavailable:
                message = f"Keys {unavailable} in command line arguments unavailable"
                warnings.warn(message)
                breakpoint()
                raise KeyError(message)
            return merged(cnfgr_known, cnfgr_unknown)
        case _:
            raise NotImplementedError(f"unimplemented strict level {strict_level}")


def parsed_command_line_arguments(
    default: Mapping | DataclassLike | None = None,
    parser: argparse.ArgumentParser | None = None,
    strict_level: int = 0,
) -> DictConfig:
    cnfgr_x_program = dictconfig_created(default)
    cnfgr_x_cli, cnfgr_x_cli_unknown = parsed_arguments(parser)
    cnfgr_known = merged(cnfgr_x_program, cnfgr_x_cli)
    cnfgr = merged_with_unknown(cnfgr_known, cnfgr_x_cli_unknown, strict_level)
    OmegaConf.resolve(cnfgr)
    return cnfgr


def instantiate(registry: ClassRegistry, configuration: Mapping, **kwargs) -> Any:
    configuration_: Mapping = deepfreeze(configuration)
    cnfgr_cls = configuration_["cls"]
    cnfgr = filterfalse_keys_mapping(prt(eq, "cls"), configuration_)
    return registry.get(cnfgr_cls, **cnfgr, **kwargs)


# ================================================================================================================================


# def commandline_args() -> tuple[str | None, Sequence[str]]:
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-c",
#         "--cnfgr",
#         "--cnfgr_file",
#         "--configuration_file",
#         dest="cnfgr",
#         help="Path to the YAML/JSON configuration file",
#         type=str,
#         default=None,
#     )
#     args, unknown = parser.parse_known_args()
#     if any(arg.startswith("-") for arg in unknown):
#         raise ValueError("Additional command line arguments ought not to start with `-`")
#     return args.cnfgr, unknown


# def get_configuration(default: Mapping | object | None = None, strict_level: int = 0) -> DictConfig:
#     """old"""
#     cnfgr_x_programme = dictconfig_created(default)
#     config_filepath, arg_list = commandline_args()
#     cnfgr_x_file = dictconfig_ex_file(config_filepath)
#     cnfgr_x_cli = dictconfig_ex_dotlist(arg_list)
#     merged_config: DictConfig = merged(cnfgr_x_programme, cnfgr_x_file, cnfgr_x_cli)

#     if strict_level == 0:
#         return merged_config
#     if strict_level == 1:  # check
#         for key in cnfgr_x_cli.keys():
#             if key not in cnfgr_x_file.keys() | cnfgr_x_programme.keys():
#                 message = f"Key {key} in command line arguments not found in file or programme. "
#                 warnings.warn(message)
#                 breakpoint()
#                 raise KeyError(message)
#         return merged_config
#     raise ValueError(f"Unknown strict level {strict_level}")
