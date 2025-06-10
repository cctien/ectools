import fnmatch
import logging
import os
import os.path as osp
import shutil
from collections.abc import Iterable, Sequence
from functools import partial as prt
from itertools import chain

logger = logging.getLogger(__name__)


def osp_stem(x: str, /) -> str:
    return osp.splitext(x)[0]


def osp_extension(x: str, /) -> str:
    return osp.splitext(x)[1]


def osp_basestem(x: str, /) -> str:
    return osp.splitext(osp.basename(x))[0]


def subdirnames(x: str, /) -> Sequence[str]:
    result = []
    for root, dirs, files in os.walk(x):
        result.extend(chain(*map(prt(osp.join, root), dirs)))
    return tuple(result)


def files_matched(dirname: str, pattern: str) -> Sequence[str]:
    result = []
    for root, dirs, files in os.walk(dirname):
        result.extend(chain(*map(prt(osp.join, root), fnmatch.filter(files, pattern))))
    return tuple(result)


def files_matched_patterns(dirname: str, patterns: Iterable[str]) -> Sequence[str]:
    return tuple(chain(*map(prt(files_matched, dirname), patterns)))


def copy_files_filtered_(
    src_dir: str,
    dst_dir: str,
    exclude_patterns: Sequence[str] | None = None,
    include_patterns: Sequence[str] | None = None,
) -> None:
    os.makedirs(dst_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        src_path = osp.join(src_dir, item)
        if osp.isdir(src_path):
            continue
        if include_patterns is not None and len(include_patterns) > 0:
            matches_include = any(fnmatch.fnmatch(item, pattern) for pattern in include_patterns)
            if not matches_include:
                continue
        if exclude_patterns is not None and len(exclude_patterns) > 0:
            matches_exclude = any(fnmatch.fnmatch(item, pattern) for pattern in exclude_patterns)
            if matches_exclude:
                continue
        shutil.copy2(src_path, osp.join(dst_dir, item))
