from collections.abc import Mapping, Sequence

from datasets import Dataset


def dataset_from_sequence(squ: Sequence[Mapping]) -> Dataset:
    return Dataset.from_list(squ)
