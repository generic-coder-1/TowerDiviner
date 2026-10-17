from __future__ import annotations

from dataclasses import dataclass, field

from .entity import Player
from .helpers import compact_dataclass
from .keys import Keys


# --- Things an agent can do -------------------------------------------------

@dataclass(frozen=True)
class MoveTo:
    """Clear the tower node with this index (fight it / open it / grab it)."""
    node: int


@dataclass(frozen=True)
class UseSpecial:
    """Use SPECIAL_ACTIONS[group][index] (golem / old man / merchant trades)."""
    group: str
    index: int


Action = MoveTo | UseSpecial


# --- Special actions (trades) -----------------------------------------------

@compact_dataclass
class SpecialAction:
    """A trade: positive values are gained, negative values are paid."""

    attack: int = 0
    defense: int = 0
    health: int = 0
    xp: int = 0
    gold: int = 0
    level: int = 0
    keys: Keys = field(default_factory=Keys)

    def possible(self, player: Player) -> bool:
        if player.xp + self.xp < 0:
            return False
        if player.gold + self.gold < 0:
            return False
        if player.health + self.health < 0:
            return False
        if player.defense + self.defense < 0:
            return False
        if player.attack + self.attack < 0:
            return False
        if player.level + self.level < 0:
            return False
        if (player.keys + self.keys).any_negative():
            return False
        return True

    def take_action(self, player: Player) -> bool:
        if not self.possible(player):
            return False

        player.xp += self.xp
        player.gold += self.gold
        player.health += self.health
        player.defense += self.defense
        player.attack += self.attack
        player.keys += self.keys
        player.level += self.level
        return True


SPECIAL_ACTIONS = {
    "golem": [
        SpecialAction(attack=4, gold=-25),
        SpecialAction(defense=4, gold=-25),
        SpecialAction(health=800, gold=-25),
    ],
    "old_man": [
        SpecialAction(attack=5, xp=-30),
        SpecialAction(defense=5, xp=-30),
        SpecialAction(health=1000, attack=7, defense=7, xp=-100, level = 1),
    ],
    "merchant": [
        SpecialAction(keys=Keys(yellow=1), gold=-10),
        SpecialAction(keys=Keys(blue=1), gold=-50),
        SpecialAction(keys=Keys(red=1), gold=-100),
    ],
}
