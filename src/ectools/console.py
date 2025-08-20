import pprint as std_pprint_lib
from typing import Any

import rich as rich_lib
import wadler_lindig as wadler_lindig_lib


def pprint(x: Any = None, /, *, rich: bool = True, wadler_lindig: bool = True) -> None:
    if x is None:
        print()
        return
    match (rich, wadler_lindig):
        case (True, True):
            rich_lib.print(wadler_lindig_lib.pformat(x))
        case (True, False):
            rich_lib.print(x)
        case (False, True):
            wadler_lindig_lib.pprint(x)
        case (False, False):
            std_pprint_lib.pprint(x)
    return


def _test() -> None:
    import math

    import numpy as np

    data = {
        "a": 12,
        "b": True,
        "c": "word",
        "d": np.pi,
        "e": 2.718281828459045235360287471352,
        "f": (1 + math.sqrt(5)) / 2,
    }

    pprint("print")
    print(data)
    pprint()

    pprint("pprint from the standard library")
    pprint(data, rich=False, wadler_lindig=False)
    pprint()

    pprint("wadler_lindig=True , rich=False")
    pprint(data, rich=False)
    pprint()

    pprint("wadler_lindig=False , rich=True")
    pprint(data, wadler_lindig=False)
    pprint()

    pprint("wadler_lindig=True , rich=True")
    pprint("rich.print ∘ wadler_lindig.pformat")
    pprint(data)
    pprint()


# python -m src.ectools.console
if __name__ == "__main__":
    _test()
