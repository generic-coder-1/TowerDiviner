from __future__ import annotations

import math
from dataclasses import field, replace

from .helpers import compact_dataclass
from .keys import Keys


@compact_dataclass
class Entity:
    attack: int
    defense: int
    health: int
    xp: int
    gold: int

    def can_beat(self, opponent: Entity) -> int | None:
        """Health we would lose winning against `opponent`, or None if we can't win.

        We always strike first, so we survive if we kill the opponent no later
        than the turn on which they would kill us.
        """
        damage_given = max(0, self.attack - opponent.defense)
        damage_taken = max(0, opponent.attack - self.defense)

        if damage_given == 0:
            return None  # we can never hurt them
        if damage_taken == 0:
            return 0  # they can never hurt us

        turns_until_we_die = math.ceil(self.health / damage_taken)
        turns_until_they_die = math.ceil(opponent.health / damage_given)

        if turns_until_they_die <= turns_until_we_die:
            return (turns_until_they_die - 1) * damage_taken
        return None

    def try_defeat(self, opponent: Entity) -> int | None:
        """Fight `opponent`. On a win, apply the health loss and loot. Returns health lost."""
        health_lost = self.can_beat(opponent)
        if health_lost is not None:
            self.xp += opponent.xp
            self.gold += opponent.gold
            self.health -= health_lost
        return health_lost


@compact_dataclass
class Player(Entity):
    attack: int = 10
    defense: int = 10
    health: int = 1000
    xp: int = 0
    gold: int = 0
    keys: Keys = field(default_factory=lambda: Keys(red=1, blue=1, yellow=1))

    def copy(self) -> Player:
        # Keys is immutable, so a shallow copy is a full copy.
        return replace(self)
