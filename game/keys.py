from __future__ import annotations

from dataclasses import astuple

from .helpers import compact_dataclass


@compact_dataclass(frozen=True)
class Keys:
    """An immutable bundle of keys. Supports +, -, and >= / <= (component-wise)."""

    red: int = 0
    blue: int = 0
    yellow: int = 0

    def __add__(self, other):
        if not isinstance(other, Keys):
            return NotImplemented
        return Keys(*(a + b for a, b in zip(astuple(self), astuple(other))))

    def __sub__(self, other):
        if not isinstance(other, Keys):
            return NotImplemented
        return Keys(*(a - b for a, b in zip(astuple(self), astuple(other))))

    def __ge__(self, other):
        """True if we hold at least as many keys of *every* colour."""
        if not isinstance(other, Keys):
            return NotImplemented
        return all(a >= b for a, b in zip(astuple(self), astuple(other)))

    def __le__(self, other):
        if not isinstance(other, Keys):
            return NotImplemented
        return other >= self

    def total(self) -> int:
        return sum(astuple(self))

    def any_negative(self) -> bool:
        return any(v < 0 for v in astuple(self))
