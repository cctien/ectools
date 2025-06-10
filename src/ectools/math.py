import math

import numpy as np
from jaxtyping import Float, Int
from numpy.typing import ArrayLike
from scipy import special


def isclose_to_int(x: float, /, **kwargs) -> bool:
    return math.isclose(x, round(x), **kwargs)


def logsumexp(
    a: ArrayLike,
    axis: int | tuple[int] | None = None,
    b: ArrayLike | None = None,
    keepdims: bool = False,
) -> ArrayLike:
    return special.logsumexp(a, axis=axis, b=b, keepdims=keepdims)
