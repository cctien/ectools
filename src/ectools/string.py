import difflib
import re
from collections.abc import Sequence
from functools import partial as prt
from typing import Any

import rich
import wadler_lindig


def pprint(x: Any, /) -> None:
    rich.print(wadler_lindig.pformat(x))


def upper_camel_case(x: str, /) -> str:
    return "".join(w.capitalize() for w in re.split(r"[_\W]+", x))


def snake_case(x: str, /) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", x).strip("_").lower()


def space_case(x: str, /) -> str:
    return re.sub(r"[_\.]+", " ", x).strip()


def ensure_blank_line_before_left_bracket(x: str, /) -> str:
    # the pattern matches a line starting with '[' that does not have a blank line before it; useful for toml file creation
    return re.sub(r"(?<!\n\n)(\n)(?=\[)", "\n\n", x)


def have_newlines_at_the_end(s: str, /, n: int) -> str:
    return s.rstrip("\n") + "\n" * n


def normalized_spaces(s: str, num_spaces: int) -> str:
    return re.sub(r" +", " " * num_spaces, s)


def normalized_double_spaces(s: str, num_spaces: int) -> str:
    return re.sub(r" {2,}", " " * num_spaces, s)


def sp(n: int, /) -> str:
    return " " * n


def nl(n: int, /) -> str:
    return "\n" * n


have_1_newline_at_the_end = prt(have_newlines_at_the_end, n=1)


def string_diff(text1: str, text2: str, fromfile: str = "", tofile: str = ""):
    text1_lines = text1.splitlines(keepends=True)
    text2_lines = text2.splitlines(keepends=True)
    diff = difflib.unified_diff(text1_lines, text2_lines, fromfile=fromfile, tofile=tofile)
    return "".join(diff)


def join(x: Sequence[str]) -> str:
    return "".join(x)


# def to_underscore(x: str, /) -> str:
#     return re.sub(r"[^a-zA-Z0-9]", "_", x)

# python -m src.ectools.string
if __name__ == "__main__":
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
    print()

    pprint("wadler_lindig.pprint")
    wadler_lindig.pprint(data)
    print()

    pprint("rich.print")
    rich.print(data)
    print()

    pprint("rich.print ∘ wadler_lindig.pformat")
    pprint(data)

    pprint(f"to_upper_camel_case: {upper_camel_case("this_is_to_upper_camel_case")}")

    sa = "this is a line\nthis is still the same\nthis is the third line\nthis is the fourth line\n"
    sb = "this is a line\nthis is still the same\nthis is just another line\nthis is the fourth line\n"
    string_diff_result = string_diff(sa, sb)
    print(sa)
    print(sb)
    print(string_diff_result)
