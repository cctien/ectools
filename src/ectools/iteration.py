from collections.abc import Callable, Iterable
from functools import partial as prt
from itertools import filterfalse
from operator import is_

from .collection import len_0

filter_not_none: Callable[[Iterable], Iterable] = prt(filterfalse, prt(is_, None))
filter_not_empty: Callable[[Iterable], Iterable] = prt(filterfalse, len_0)
