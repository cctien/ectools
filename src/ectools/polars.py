from collections.abc import Iterable, Sequence
from operator import methodcaller
from typing import Any

import polars as pl
from polars.expr.expr import IntoExpr

read_parquet = methodcaller("read_parquet")


def stable_sort(
    df: pl.DataFrame,
    by: Iterable[IntoExpr],
    descending: Sequence[bool] = (False,),
    nulls_last: Sequence[bool] = (False,),
    multithreaded: bool = True,
) -> pl.DataFrame:
    """extra safe stable sort by adding a row index as the last sorting key"""
    df = df.with_row_index(name="__row_index_temporary_for_extra_cautionary_stable_sorting__")
    df = df.sort(
        (*by, "__row_index_temporary_for_extra_cautionary_stable_sorting__"),
        descending=(*descending, False),
        nulls_last=(*nulls_last, False),
        multithreaded=multithreaded,
        maintain_order=True,
    )
    df = df.drop("__row_index_temporary_for_extra_cautionary_stable_sorting__")
    return df
