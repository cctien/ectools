import os.path
from os.path import *


def stem(x: str, /) -> str:
    return os.path.splitext(x)[0]


def ext(x: str, /) -> str:
    return os.path.splitext(x)[1]


def basestem(x: str, /) -> str:
    return os.path.splitext(os.path.basename(x))[0]
