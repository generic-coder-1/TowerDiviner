from __future__ import annotations

import random

from game import Action, GameState

from .base import StepAgent


class SpecialRandomAgent(StepAgent):
    """Picks uniformly among all legal actions but will prefer special actions."""

    def __init__(self, name: str | None = None, seed: int | None = None):
        super().__init__(name)
        self.rng = random.Random(seed)

    def reset(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    def choose_action(self, game: GameState) -> Action | None:
        actions = game.legal_special_actions()
        if not len(actions):
             actions = game.legal_moves()
        return self.rng.choice(actions) if actions else None
