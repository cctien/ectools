import os


def subdirectories(x: str, /) -> list[str]:
    """Return all subdirectories of a given directory."""
    if not os.path.isdir(x):
        raise NotADirectoryError(f"{x} is not a directory")

    subdirs = []
    for root, dirs, files in os.walk(x):
        for d in dirs:
            subdirs.append(os.path.join(root, d))

    return subdirs
