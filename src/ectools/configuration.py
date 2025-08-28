import argparse
import copy
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import is_dataclass

from class_registry import ClassRegistry
from omegaconf import DictConfig, OmegaConf


def commandline_args() -> tuple[str | None, Sequence[str]]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--cnfgr",
        "--cnfgr_file",
        "--configuration_file",
        dest="cnfgr",
        help="Path to the YAML/JSON configuration file",
        type=str,
        default=None,
    )
    args, unknown = parser.parse_known_args()
    if any(arg.startswith("-") for arg in unknown):
        raise ValueError("Additional command line arguments ought not to start with `-`")
    return args.cnfgr, unknown


def dictconfig_x_programme(default: Mapping | object | None) -> DictConfig:
    if default is None:
        return OmegaConf.create()
    if is_dataclass(default):
        return OmegaConf.structured(default)
    return OmegaConf.create(default)


def dictconfig_x_file(filepath: str | None) -> DictConfig:
    if filepath is None:
        return OmegaConf.create()
    return OmegaConf.load(filepath)


def dictconfig_x_cli(setting: Sequence[str] | None) -> DictConfig:
    if setting is None or len(setting) == 0:
        return OmegaConf.create()
    return OmegaConf.from_dotlist(setting)


def get_configuration(default: Mapping | object | None = None, strict_level: int = 0) -> DictConfig:
    cnfgr_x_programme = dictconfig_x_programme(default)
    config_filepath, arg_list = commandline_args()
    cnfgr_x_file = dictconfig_x_file(config_filepath)
    cnfgr_x_cli = dictconfig_x_cli(arg_list)
    merged_config: DictConfig = OmegaConf.merge(cnfgr_x_programme, cnfgr_x_file, cnfgr_x_cli)

    if strict_level == 0:
        return merged_config
    if strict_level == 1:  # check
        for key in cnfgr_x_cli.keys():
            if key not in cnfgr_x_file.keys() | cnfgr_x_programme.keys():
                message = f"Key {key} in command line arguments not found in file or programme. "
                warnings.warn(message)
                breakpoint()
                raise KeyError(message)
        return merged_config
    raise ValueError(f"Unknown strict level {strict_level}")


def instance(registry: ClassRegistry, configuration: Mapping | str, **kwargs):
    if isinstance(configuration, str):
        configuration = {"cls": configuration}
    _configuration = copy.deepcopy(dict(configuration))
    return registry.get(key=_configuration.pop("cls"), **_configuration, **kwargs)


# from .functional_tools import identity

# try:
#     import typer

#     typer.main.get_command_name = identity
# except ImportError:
#     pass
