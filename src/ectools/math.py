import math
from typing import TypeAlias

import numpy as np
from numpy.typing import ArrayLike
from scipy import special

number_like: TypeAlias = bool | int | float | complex


def isclose_to_int(x: float, /, **kwargs) -> bool:
    return math.isclose(x, round(x), **kwargs)


def logsumexp(
    a: ArrayLike,
    b: ArrayLike | None = None,
    axis: int | tuple[int] | None = None,
    keepdims: bool = False,
) -> np.ndarray:
    return special.logsumexp(a, axis=axis, b=b, keepdims=keepdims)


def _logsumexp_numpy(
    a: ArrayLike,
    b: ArrayLike | None = None,
    axis: int | tuple[int] | None = None,
    keepdims: bool = False,
) -> np.ndarray:
    if b is None:
        b = np.ones_like(a)
    return np.log(np.sum(b * np.exp(a), axis=axis, keepdims=keepdims))


def _module_test() -> None:
    # Test isclose_to_int
    assert isclose_to_int(1.0)
    assert not isclose_to_int(1.1)
    assert isclose_to_int(1.00000000000001, rel_tol=1e-9)

    # Test logsumexp
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([0.5, 1.5, 2.5])
    assert np.isclose(logsumexp(a, b=b), _logsumexp_numpy(a, b=b))

    a = np.random.rand(12)
    b = np.random.rand(12)
    assert np.isclose(logsumexp(a, b=b), _logsumexp_numpy(a, b=b))

    print("All tests passed.")


# python -m src.ectools.math
if __name__ == "__main__":
    _module_test()
