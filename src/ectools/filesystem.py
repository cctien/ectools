import fnmatch
import os
from collections.abc import Sequence
from functools import partial as prt
from functools import reduce
from operator import add

from plum import dispatch


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


def files_matched_patterns(dirname: str, patterns: Sequence[str]) -> list[str]:
    """Return all files in a directory that match any of the given patterns."""
    if not os.path.isdir(dirname):
        raise NotADirectoryError(f"{dirname} is not a directory")

    matched_files = []
    for pattern in patterns:
        matched_files.extend(files_matched(dirname, pattern))

    return matched_files
