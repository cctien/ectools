# TODO : improve and use it
import logging
import os.path as osp
import subprocess
import warnings
from collections.abc import Sequence

from .os import read_file
from .string import join

logger = logging.getLogger(__name__)


def subprocess_run_stdout_logged(
    command: Sequence[str], working_dir: str = ".", log_file_stem: str = "log"
) -> subprocess.CompletedProcess:

    log_file_path = osp.join(working_dir, f"{log_file_stem}.log")
    with open(log_file_path, "w") as log_stdout_file:
        subproc_out = subprocess.run(
            command,
            cwd=working_dir,
            stdout=log_stdout_file,
            stderr=subprocess.STDOUT,
            shell=False,
            check=False,
            text=True,
        )

    if subproc_out.returncode != 0:
        logger.info(join(read_file(log_file_path).splitlines(keepends=True)[-16:]))
        message = f"Error in running {" ".join(command)}:\n{subproc_out.stderr}"
        logger.error(message)
        warnings.warn(message)

    return subproc_out
