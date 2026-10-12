from __future__ import annotations

from dataclasses import field

from .actions import SPECIAL_ACTIONS, Action, MoveTo, UseSpecial
from .entity import Player
from .floors import build_tower
from .graph import TowerGraph, TowerState
from .helpers import compact_dataclass


@compact_dataclass
class GameState:
    """Everything needed to play: the player, the (static) tower, and progress through it."""

    player: Player = field(default_factory=Player)
    tower: TowerGraph = field(default_factory=build_tower)
    tower_state: TowerState = field(default_factory=TowerState)

    # --- copying / hashing (for search agents) ------------------------------

    def copy(self) -> GameState:
        """Independent copy. The tower graph is never mutated during play, so it's shared."""
        return GameState(self.player.copy(), self.tower, self.tower_state.copy())

    def signature(self) -> tuple:
        """Hashable fingerprint of the state; equal signatures mean equal futures."""
        p = self.player
        return (
            frozenset(self.tower_state.completed_nodes),
            (p.attack, p.defense, p.health, p.xp, p.gold, p.keys),
            frozenset(self.tower_state.special_actions_unlocked),
        )

    # --- querying -----------------------------------------------------------

    def legal_moves(self) -> list[MoveTo]:
        return [
            MoveTo(n)
            for n in sorted(self.tower_state.get_active_nodes())
            if self.tower.nodes[n][0].completable(self.player)
        ]

    def legal_special_actions(self) -> list[UseSpecial]:
        result = []
        for group in sorted(self.tower_state.special_actions_unlocked):
            for i, action in enumerate(SPECIAL_ACTIONS[group]):
                if action.possible(self.player):
                    result.append(UseSpecial(group, i))
        return result

    def legal_actions(self) -> list[Action]:
        return [*self.legal_moves(), *self.legal_special_actions()]

    @property
    def is_won(self) -> bool:
        return self.tower.goal in self.tower_state.completed_nodes

    @property
    def is_over(self) -> bool:
        """Won, or stuck with nothing left to do."""
        return self.is_won or not self.legal_actions()

    # --- acting -------------------------------------------------------------

    def move_to_node(self, node: int) -> bool:
        return self.tower_state.try_complete_node(self.tower, self.player, node)

    def take_special_action(self, group: str, index: int) -> bool:
        if group not in self.tower_state.special_actions_unlocked:
            return False
        return SPECIAL_ACTIONS[group][index].take_action(self.player)

    def apply(self, action: Action) -> bool:
        """Perform an action. Returns False (and changes nothing) if it isn't legal."""
        if isinstance(action, MoveTo):
            return self.move_to_node(action.node)
        if isinstance(action, UseSpecial):
            return self.take_special_action(action.group, action.index)
        raise TypeError(f"Unknown action type: {action!r}")

    def apply_path(self, path: list[Action]) -> bool:
        """Apply actions in order; stops and returns False at the first illegal one."""
        return all(self.apply(a) for a in path)
