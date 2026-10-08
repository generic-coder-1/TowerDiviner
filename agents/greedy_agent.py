from __future__ import annotations

from game import Action, GameState
from evaluation.heuristic import Heuristic, HeuristicFn

from .base import StepAgent


class GreedyAgent(StepAgent):
    """Takes whichever action leads to the highest-scoring state right now."""

    deterministic = True

    def __init__(self, heuristic: HeuristicFn | None = None, name: str | None = None):
        super().__init__(name)
        self.heuristic = heuristic or Heuristic()

    def choose_action(self, game: GameState) -> Action | None:
        best_action, best_score = None, float("-inf")
        for action in game.legal_actions():
            child = game.copy()
            child.apply(action)
            score = self.heuristic(child)
            if score > best_score:
                best_action, best_score = action, score
        return best_action
