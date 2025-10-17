from collections.abc import Iterator, Mapping
from threading import Lock
from types import MappingProxyType
from typing import Callable, Generic, TypeVar, overload

T = TypeVar("T")


class Registry(Generic[T]):
    """
    Read-only mapping interface; mutation only via .register().
    - name is required (positional) for clarity
    - overwrite guard
    - possibly freeze after setup
    """

    def __init__(self, *, allow_overwrite: bool = False):
        self._registry: dict[str, T] = {}
        self._allow_overwrite = allow_overwrite
        self._frozen = False
        self._lock = Lock()

    def __getitem__(self, key: str) -> T:
        return self._registry[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._registry)

    def __len__(self) -> int:
        return len(self._registry)

    def __repr__(self) -> str:
        status = "frozen" if self._frozen else "mutable"
        return f"Registry({len(self)} items, {status})"

    @overload
    def register(self, name: str, item: T, *, overwrite: bool | None = None) -> T: ...

    @overload
    def register(
        self, name: str, item: None = None, *, overwrite: bool | None = None
    ) -> Callable[[T], T]: ...

    def register(self, name: str, item: T | None = None, *, overwrite: bool | None = None):
        """
        Usage:
            @reg.register("add")
            def add(x: int, y: int) -> int: ...

            def mul(x: int, y: int) -> int: ...
            reg.register("mul", mul)

        `overwrite`: per-call override (defaults to `allow_overwrite` set in __init__).
        """
        ow = self._allow_overwrite if overwrite is None else overwrite

        # Direct registration: reg.register("name", item)
        if item is not None:
            return self._register(name, item, ow)

        # Decorator usage: @reg.register("name")
        def decorator(f: T) -> T:
            return self._register(name, f, ow)

        return decorator

    def _register(self, name: str, item: T, overwrite: bool) -> T:
        with self._lock:
            if self._frozen:
                raise ValueError("Registry is frozen (read-only).")
            if not overwrite and name in self._registry:
                raise KeyError(f"'{name}' already registered.")
            self._registry[name] = item
            return item

    def get(self, key: str, /, default: T | None = None) -> T | None:
        """Get an item with an optional default value."""
        return self._registry.get(key, default)

    def freeze(self) -> None:
        """Prevent any further registrations."""
        with self._lock:
            self._frozen = True

    def snapshot(self) -> Mapping[str, T]:
        """Return an immutable view suitable for external sharing."""
        return MappingProxyType(self._registry)
