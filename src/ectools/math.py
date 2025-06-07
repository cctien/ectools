import math


def isclose_to_int(x: float, /, **kwargs) -> bool:
    return math.isclose(x, round(x), **kwargs)
