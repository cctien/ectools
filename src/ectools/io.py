import json
import os
import os.path as osp
from collections.abc import Mapping, Sequence

import orjson
import yaml


def read_file(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()


def write_file_(filepath: str, content: str) -> None:
    with open(filepath, "w") as file:
        file.write(content)


def orjson_load(filepath: str) -> Sequence | Mapping:
    with open(filepath, "rb") as f:
        return orjson.loads(f.read())


def orjson_save_(
    filepath: str,
    data: Sequence | Mapping,
    option: int | None = orjson.OPT_APPEND_NEWLINE | orjson.OPT_INDENT_2,
) -> None:
    # TODO : expose options as parameters to this function
    os.makedirs(osp.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(orjson.dumps(data, option=option))


def json_load(filepath: str, **kwargs) -> Sequence | Mapping:
    with open(filepath, "r") as f:
        return json.load(f, **kwargs)


def json_save_(
    filepath: str,
    data: Sequence | Mapping,
    indent: int | None = None,
    sort_keys: bool = False,
    **kwargs,
) -> None:
    os.makedirs(osp.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=indent, sort_keys=sort_keys, **kwargs)


def yaml_load(filepath: str) -> Sequence | Mapping:
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def yaml_save_(filepath: str, data: Sequence | Mapping, **kwargs) -> None:
    os.makedirs(osp.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        yaml.safe_dump(data, f, **kwargs)
