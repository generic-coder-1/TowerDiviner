"""Small dataclass helpers shared by the game modules."""
from __future__ import annotations

from dataclasses import MISSING, dataclass, fields


def _default_for(f):
    if f.default is not MISSING:
        return f.default
    if f.default_factory is not MISSING:
        return f.default_factory()
    return MISSING  # required field: never equals a real value, so it's always shown


def _repr_non_defaults(self):
    parts = [
        f"{f.name}={getattr(self, f.name)!r}"
        for f in fields(self)
        if f.repr and getattr(self, f.name) != _default_for(f)
    ]
    return f"{type(self).__name__}({', '.join(parts)})"


def compact_dataclass(cls=None, **kwargs):
    """Like @dataclass, but repr only shows fields that differ from their defaults."""

    def wrap(cls):
        cls = dataclass(repr=False, **kwargs)(cls)
        cls.__repr__ = _repr_non_defaults
        return cls

    return wrap if cls is None else wrap(cls)
