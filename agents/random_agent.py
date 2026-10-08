from __future__ import annotations

import random

from game import Action, GameState

from .base import StepAgent


class RandomAgent(StepAgent):
    """Picks uniformly among all legal actions (moves and special trades alike)."""

    def __init__(self, name: str | None = None, seed: int | None = None):
        super().__init__(name)
        self.rng = random.Random(seed)

    def reset(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    def choose_action(self, game: GameState) -> Action | None:
        actions = game.legal_actions()
        return self.rng.choice(actions) if actions else None
