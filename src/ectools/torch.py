import random

import torch
from torch import Tensor

from .math import number_like


def seed_torch_(seed: int | None) -> None:
    if seed is None:
        return
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    return


def fill_diagonal(
    x: Tensor, value: number_like, *, offset: int = 0, dim1: int = 0, dim2: int = 1
) -> Tensor:
    dshape = x.diagonal(offset=offset, dim1=dim1, dim2=dim2).shape
    src = torch.full(dshape, value, dtype=x.dtype, device=x.device)
    return torch.diagonal_scatter(x, src, offset=offset, dim1=dim1, dim2=dim2)
