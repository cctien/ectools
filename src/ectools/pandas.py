from collections.abc import Iterable, Sequence

import pandas as pd


def isna_all(x: Iterable) -> bool:
    y = pd.isna(x)
    if isinstance(y, bool):
        return y
    return y.all().item()


def none_if_all_na(x: Iterable) -> None | Iterable:
    if isna_all(x):
        return None
    return x
