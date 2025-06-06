from collections.abc import Sequence
import fnmatch
from functools import partial as prt, reduce
import os
from operator import add


def subdirectories(x: str, /) -> list[str]:
    """Return all subdirectories of a given directory."""
    if not os.path.isdir(x):
        raise NotADirectoryError(f"{x} is not a directory")

    subdirs = []
    for root, dirs, files in os.walk(x):
        for d in dirs:
            subdirs.append(os.path.join(root, d))

    return subdirs


def files_matched(dirname: str, pattern: str) -> list[str]:
    if not os.path.isdir(dirname):
        raise NotADirectoryError(f"{dirname} is not a directory")

    matched_files = []
    for root, dirs, files in os.walk(dirname):
        for filename in fnmatch.filter(files, pattern):
            matched_files.append(os.path.join(root, filename))

    return matched_files
