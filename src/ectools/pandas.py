from collections.abc import Iterable, Sequence
from typing import Any

import pandas as pd


def read_parquet(filepath: str) -> pd.DataFrame:
    return pd.read_parquet(filepath).convert_dtypes()


def to_parquet(filepath: str, df: pd.DataFrame) -> None:
    df.to_parquet(filepath)


def isna_all(x: Any) -> bool:
    y = pd.isna(x)
    if isinstance(y, bool):
        return y
    return y.all().item()


def none_if_all_na[t](x: t) -> t | None:
    if isna_all(x):
        return None
    return x
