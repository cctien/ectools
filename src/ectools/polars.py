from collections.abc import Iterable, Sequence
from itertools import chain, repeat
from operator import methodcaller

import polars as pl
from polars._typing import IntoExpr

read_parquet = methodcaller("read_parquet")


def stable_sort(
    df: pl.DataFrame,
    by: Sequence[IntoExpr],
    descending: bool | Sequence[bool] = False,
    nulls_last: bool | Sequence[bool] = False,
    multithreaded: bool = True,
) -> pl.DataFrame:
    """extra safe stable sort by adding a row index as the last sorting key"""
    nm = len(by)
    df = df.with_row_index(name="__row_index_temporary_for_extra_cautionary_stable_sorting__")
    by = (*by, "__row_index_temporary_for_extra_cautionary_stable_sorting__")
    descending = tuple(
        chain((repeat(descending, nm) if isinstance(descending, bool) else descending), (False,))
    )
    nulls_last = tuple(
        chain((repeat(nulls_last, nm) if isinstance(nulls_last, bool) else nulls_last), (False,))
    )
    df = df.sort(
        by,
        descending=descending,
        nulls_last=nulls_last,
        multithreaded=multithreaded,
        maintain_order=True,
    )
    df = df.drop("__row_index_temporary_for_extra_cautionary_stable_sorting__")
    return df
