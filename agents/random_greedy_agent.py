from __future__ import annotations
import random

from game import Action, GameState
from evaluation.heuristic import Heuristic, HeuristicFn

from .base import StepAgent

EPSILON = 10


class RandomGreedyAgent(StepAgent):
    """Takes a random action that is at most EPSILON away from the highest-scoring state right now."""

    def __init__(self, heuristic: HeuristicFn | None = None, name: str | None = None, seed: int | None = None):
        super().__init__(name)
        self.rng = random.Random(seed)
        self.heuristic = heuristic or Heuristic()

    def reset(self, seed: int | None = None) -> None:
            self.rng = random.Random(seed)

    def choose_action(self, game: GameState) -> Action | None:
        best_actions, best_score = [], float("-inf")
        for action in game.legal_actions():
            child = game.copy()
            child.apply(action)
            score = self.heuristic(child)
            if score > best_score:
                best_score = score
                best_actions.clear()
            if best_score - score < EPSILON:
                best_actions.append(action)
        return random.choice(best_actions) if len(best_actions) else None 
