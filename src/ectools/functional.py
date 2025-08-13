import functools
import logging
from collections.abc import Callable, Iterable, Sequence, Sized
from types import NoneType
from typing import Any, ParamSpec, TypeVar

from plum import Function, dispatch

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


def identity[t](x: t) -> t:
    return x


def ngt(f: Callable[P, bool], /) -> Callable[P, bool]:
    @functools.wraps(f)
    def ngt_x(*args, **kwargs):
        return not f(*args, **kwargs)

    return ngt_x


def be(y: object, x: object, /) -> bool:
    return x is y


def be_empty(x: Sized, /) -> bool:
    return len(x) == 0


def be_none(x: object, /) -> bool:
    return x is None


def be_not_none(x: object, /) -> bool:
    return x is not None


def tplmap(func: Callable[[T], T], *iterables: Iterable[T]) -> tuple[T, ...]:
    return tuple(map(func, *iterables))


def apply_all[t](functions: Iterable[Callable[[t], Any]], arg: t) -> Sequence[Any]:
    return tuple(f(arg) for f in functions)


zip_strict = functools.partial(zip, strict=True)
zip_str = functools.partial(zip, strict=True)

# def add_none_variant(func):
#     """Decorator that adds a None -> None variant to a dispatched function"""

#     # Create the None variant
#     @dispatch
#     def none_variant(x: NoneType) -> None:
#         return None

#     # Register the None variant with the same name as the original function
#     none_variant.__name__ = func.__name__

#     # If the original function is already dispatched, we need to merge them
#     if hasattr(func, "_dispatch"):
#         # Get the existing dispatcher
#         dispatcher = func._dispatch
#         # Add our None variant to it
#         dispatcher.register(none_variant._dispatch._methods[0])
#         return func
#     else:
#         # If not already dispatched, create a new dispatcher
#         @dispatch
#         def wrapper(*args, **kwargs):
#             return func(*args, **kwargs)

#         wrapper.__name__ = func.__name__

#         # Add the None variant
#         wrapper._dispatch.register(none_variant._dispatch._methods[0])
#         return wrapper


# def add_none_method(func):
#     """
#     A decorator that adds a 'none_method' to the decorated function.
#     This 'none_method' takes a single argument of None type and returns None.
#     """

#     # If the function is not already a plum.Function, make it one.
#     # This allows us to register new methods to it.
#     if not isinstance(func, Function):
#         original_func = func
#         func = Function()

#         # Register the original function's default behavior
#         @func.dispatch()
#         def _(*args, **kwargs):
#             return original_func(*args, **kwargs)

#     # Define the new method that takes None and returns None
#     @func.dispatch(None.__class__)  # Use None.__class__ for the None type
#     def none_implementation(arg: None):
#         """
#         This is the new method that handles None input.
#         """
#         print(f"none_method called with: {arg}")
#         return None

#     return func


# python -m src.ectools.functional
if __name__ == "__main__":
    pass

    # @add_none_variant
    # @dispatch
    # def my_function(x: int) -> int:
    #     return x * 2

    # @dispatch
    # def my_function(x: str) -> str:
    #     return x.upper()

    # # Now you can call:
    # print(my_function(5))  # 10
    # print(my_function("hello"))  # HELLO
    # print(my_function(None))  # None
    # print(my_function(None))  # None

    # @add_none_method
    # @dispatch
    # def my_function(x: int):
    #     print(f"my_function called with int: {x}")
    #     return x * 2

    # @add_none_method
    # @dispatch
    # def my_function(x: str):
    #     print(f"my_function called with str: {x}")
    #     return x.upper()

    # # Now, test the different dispatches
    # print(my_function(5))
    # print(my_function("hello"))
    # print(my_function(None))  # This will call the 'none_method'
    # print("-" * 20)

    # # You can also use it on a standalone function:
    # @add_none_method
    # def another_function(x):
    #     print(f"another_function called with: {x}")
    #     return f"Processed: {x}"

    # print(another_function("world"))
    # print(another_function(123))
    # print(another_function(None))
