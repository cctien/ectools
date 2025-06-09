import fnmatch
import logging
import os
import os.path as osp
import shutil
from collections.abc import Sequence

logger = logging.getLogger(__name__)


def osp_stem(filepath: str) -> str:
    return osp.splitext(filepath)[0]


def osp_extension(filepath: str) -> str:
    return osp.splitext(filepath)[1]


def osp_basestem(filepath: str) -> str:
    return osp.splitext(osp.basename(filepath))[0]


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


def copy_files_filtered_(
    src_dir: str,
    dst_dir: str,
    exclude_patterns: Sequence[str] | None = None,
    include_patterns: Sequence[str] | None = None,
) -> None:
    os.makedirs(dst_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)

        if os.path.isdir(src_path):
            continue
        if include_patterns is not None and len(include_patterns) > 0:
            matches_include = any(fnmatch.fnmatch(item, pattern) for pattern in include_patterns)
            if not matches_include:
                continue
        if exclude_patterns is not None and len(exclude_patterns) > 0:
            matches_exclude = any(fnmatch.fnmatch(item, pattern) for pattern in exclude_patterns)
            if matches_exclude:
                continue

        dst_path = os.path.join(dst_dir, item)
        shutil.copy2(src_path, dst_path)
