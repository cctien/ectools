import functools
from collections.abc import Callable, Iterable, Reversible, Sequence, Sized
from functools import partial as prt
from functools import reduce
from itertools import chain as ctn
from operator import is_, not_
from typing import Any, overload

# from plum import dispatch


def identit[T](x: T) -> T:
    return x


def appl[S, T](f: Callable[[S], T], x: S) -> T:
    return f(x)


def appll[S, T](x: S, f: Callable[[S], T]) -> T:
    return f(x)


def params_revers(f):
    @functools.wraps(f)
    def _f(*args):
        return f(*reversed(args))

    return _f


@overload
def cmp[A]() -> Callable[[A], A]: ...


@overload
def cmp[**A, B](f: Callable[A, B]) -> Callable[A, B]: ...


@overload
def cmp[**A, B, C](f2: Callable[[B], C], f1: Callable[[A], B]) -> Callable[A, C]: ...


@overload
def cmp[**A, B, C, D](
    f3: Callable[[C], D], f2: Callable[[B], C], f1: Callable[[A], B]
) -> Callable[A, D]: ...


@overload
def cmp[**A, B, C, D, E](
    f4: Callable[[D], E], f3: Callable[[C], D], f2: Callable[[B], C], f1: Callable[[A], B]
) -> Callable[A, E]: ...


@overload
def cmp[**A, B, C, D, E, F](
    f5: Callable[[E], F],
    f4: Callable[[D], E],
    f3: Callable[[C], D],
    f2: Callable[[B], C],
    f1: Callable[A, B],
) -> Callable[A, F]: ...


@overload
def cmp[**A, B, C, D, E, F, G](
    f6: Callable[[F], G],
    f5: Callable[[E], F],
    f4: Callable[[D], E],
    f3: Callable[[C], D],
    f2: Callable[[B], C],
    f1: Callable[A, B],
) -> Callable[A, G]: ...


def cmp(*fs: Callable[..., Any]) -> Callable[..., Any]:
    def apply_composed(x):
        return reduce(appll, ctn([identit], reversed(fs)), x)

    return apply_composed


@overload
def cmpl[A]() -> Callable[[A], A]: ...


@overload
def cmpl[**A, B](f: Callable[A, B]) -> Callable[A, B]: ...


@overload
def cmpl[**A, B, C](f1: Callable[A, B], f2: Callable[[B], C]) -> Callable[A, C]: ...


@overload
def cmpl[**A, B, C, D](
    f1: Callable[A, B], f2: Callable[[B], C], f3: Callable[[C], D]
) -> Callable[A, D]: ...


@overload
def cmpl[**A, B, C, D, E](
    f1: Callable[A, B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E]
) -> Callable[A, E]: ...


@overload
def cmpl[**A, B, C, D, E, F](
    f1: Callable[A, B],
    f2: Callable[[B], C],
    f3: Callable[[C], D],
    f4: Callable[[D], E],
    f5: Callable[[E], F],
) -> Callable[A, F]: ...


@overload
def cmpl[**A, B, C, D, E, F, G](
    f1: Callable[A, B],
    f2: Callable[[B], C],
    f3: Callable[[C], D],
    f4: Callable[[D], E],
    f5: Callable[[E], F],
    f6: Callable[[F], G],
) -> Callable[A, G]: ...


def cmpl(*fs: Callable) -> Callable:
    def apply_composed(x):
        return reduce(appll, ctn([identit], fs), x)

    return apply_composed


# @dispatch
# def foldl[Acc, In](f: Callable[[Acc, In], Acc], init: Acc, iterable: Reversible[In]) -> Acc:
#     return reduce(f, iterable, init)


# @dispatch
def foldl[Acc, In](f: Callable[[Acc, In], Acc], init: Acc) -> Callable[[Iterable[In]], Acc]:
    def crr_foldl(iterable: Iterable[In]) -> Acc:
        return reduce(f, iterable, init)

    return crr_foldl


# @dispatch
# def foldr[Acc, In](f: Callable[[In, Acc], Acc], init: Acc, iterable: Reversible[In]) -> Acc:
#     return reduce(params_revers(f), reversed(iterable), init)


# @dispatch
def foldr[Acc, In](f: Callable[[In, Acc], Acc], init: Acc) -> Callable[[Reversible[In]], Acc]:
    def crr_foldr(iterable: Reversible[In]) -> Acc:
        return reduce(params_revers(f), reversed(iterable), init)

    return crr_foldr


def be_none(x: object, /) -> bool:
    return x is None


def be_not_none(x: object, /) -> bool:
    return x is not None


_be_none = prt(is_, None)

_be_not_none = cmp(not_, _be_none)


def apply_all[t](functions: Iterable[Callable[[t], Any]], arg: t) -> Sequence[Any]:
    return tuple(f(arg) for f in functions)


def be(y: object, x: object, /) -> bool:
    return x is y


def ngt[**P](f: Callable[P, bool], /) -> Callable[P, bool]:
    @functools.wraps(f)
    def ngt_x(*args, **kwargs):
        return not f(*args, **kwargs)

    return ngt_x


# ================================================================

# from types import NoneType

# from plum import Function, dispatch

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
