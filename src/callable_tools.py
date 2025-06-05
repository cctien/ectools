from collections.abc import Mapping
from dataclasses import make_dataclass, field
from functools import wraps
from inspect import signature, isclass
import logging
import time
from typing import get_type_hints, Any

from dacite import from_dict, Config, DaciteError

logger = logging.getLogger(__name__)


def time_and_log(func):
    """A decorator to time a function and log its execution time."""

    @wraps(func)  # Preserves the original function's metadata
    def wrapper_time_and_log(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(f"Function `{func.__name__}` took {elapsed_time:.6f} seconds to execute.")
        return result

    return wrapper_time_and_log


def function_to_dataclass(func):
    """
    Converts a function's parameters to a dataclass, preserving:
    - Type hints (only for parameters that have them)
    - Default values (only for parameters that have them)
    """
    sig = signature(func)
    type_hints = get_type_hints(func)

    fields = []
    for name, param in sig.parameters.items():
        # Skip *args and **kwargs
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue

        field_def = (name,)
        field_def += (type_hints.get(name, Any),)
        if param.default is not param.empty:
            field_def += (field(default=param.default),)

        fields.append(field_def)

    # Create the dataclass
    return make_dataclass(f"{func.__name__.capitalize()}Params", fields, frozen=False)


def unpack(func):
    """Decorator to automatically convert dictionaries to dataclass instances using dacite."""
    sig = signature(func)
    param_types = get_type_hints(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Bind the provided arguments to the function's parameters
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()  # Apply default values for missing parameters

        # Process all arguments (both positional and keyword)
        for param_name, value in bound_args.arguments.items():
            if param_name in param_types:
                param_type = param_types[param_name]
                if isclass(param_type) and hasattr(param_type, "__dataclass_fields__"):
                    if isinstance(value, Mapping):
                        bound_args.arguments[param_name] = from_dict(
                            data_class=param_type,
                            data=value,
                            config=Config(cast=[int, float, str, bool]),
                        )
        return func(*bound_args.args, **bound_args.kwargs)
