from collections.abc import Iterable, Sequence
from typing import Any

import polars as pl


def read_parquet(filepath: str) -> pl.DataFrame:
    return pl.read_parquet(filepath)
