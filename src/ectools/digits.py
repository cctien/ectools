from decimal import Decimal, localcontext
import logging

import numpy as np


logger = logging.getLogger(__name__)


def trailing_zeros_count(s: str) -> int:
    return len(s) - len(s.rstrip("0"))


def non_trailing_zeros_count(s: str) -> int:
    assert s.count(".") <= 1, "String should not contain more than one decimal point"
    return len(s) - trailing_zeros_count(s) - s.count(".")


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_digit(s: str) -> bool:
    return s.isdigit()


def is_scientific_notation(s: str) -> bool:
    try:
        float(s)
        return "e" in s.lower()
    except ValueError:
        return False


def convert_to_scientific_if_longer(x: str, max_length: int = 3) -> str:
    assert is_number(x), f"Value {x} is not a number"
    if is_scientific_notation(x) or len(x) <= max_length:
        return x

    with localcontext() as ctx:
        ctx.prec = len(x)
        num_decimal = Decimal(x)

    digits_after_decimal = non_trailing_zeros_count(x) - 1
    output = f"{num_decimal:.{digits_after_decimal}e}"
    assert np.isclose(float(output), float(x)), f"Conversion error: {output} != {x}"
    logger.debug(f"Converted {x} to {output}")
    return output


if __name__ == "__main__":
    from .logging import set_root_logger

    set_root_logger(stream={"level": "DEBUG"})

    convert_to_scientific_if_longer("1000")
    convert_to_scientific_if_longer("1000000000")
    convert_to_scientific_if_longer("999")
    convert_to_scientific_if_longer("12345678901234567890")
    convert_to_scientific_if_longer("1234567890.1234567890")
    convert_to_scientific_if_longer("100")
