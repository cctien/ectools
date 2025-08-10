import datetime
import json
import logging
import os
import os.path as osp
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

import orjson

logger = logging.getLogger(__name__)


def current_time(strf: str = "%Y%m%d-%H:%M:%S", /) -> str:
    return datetime.datetime.now().strftime(strf)


def get_directory_tree(directory_path: str) -> str:
    """Run the tree command and capture its output."""
    try:
        result = subprocess.run(
            ["tree", directory_path], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except FileNotFoundError:
        return "Error: 'tree' command not found. Install it for the shell or the system"


def get_tree_string(directory, prefix="", is_last=True):
    """Return directory tree structure as a string"""
    path = Path(directory)

    if not path.exists():
        return f"Directory '{directory}' does not exist\n"

    if not path.is_dir():
        return f"'{directory}' is not a directory\n"

    result = ""

    # Add current directory
    connector = "└── " if is_last else "├── "
    result += f"{prefix}{connector}{path.name}/\n"

    # Get all items in directory
    try:
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

        # Process each item
        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            new_prefix = prefix + ("    " if is_last else "│   ")

            if item.is_dir():
                result += get_tree_string(item, new_prefix, is_last_item)
            else:
                connector = "└── " if is_last_item else "├── "
                result += f"{new_prefix}{connector}{item.name}\n"

    except PermissionError:
        new_prefix = prefix + ("    " if is_last else "│   ")
        result += f"{new_prefix}[Permission Denied]\n"

    return result


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
    filepath: str, data: Sequence | Mapping, option: int | None = orjson.OPT_INDENT_2
) -> None:
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
