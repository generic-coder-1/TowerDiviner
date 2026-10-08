from __future__ import annotations

from game import Action, GameState
from evaluation.heuristic import Heuristic, HeuristicFn

from .base import PlanningAgent


class BeamSearchAgent(PlanningAgent):
    """Keeps the `beam_width` best-scoring partial playthroughs at each step.

    States reached by different action orders (e.g. clearing two rooms in either
    order) are merged, so the beam isn't wasted on duplicates.
    """

    deterministic = True

    def __init__(self, beam_width: int = 100, heuristic: HeuristicFn | None = None, name: str | None = None):
        super().__init__(name or f"BeamSearch(w={beam_width})")
        self.beam_width = beam_width
        self.heuristic = heuristic or Heuristic()

    def plan(self, game: GameState) -> list[Action]:
        beam: list[tuple[GameState, list[Action]]] = [(game, [])]
        best_score, best_path = self.heuristic(game), []

        while beam:
            candidates: dict[tuple, tuple[float, GameState, list[Action]]] = {}
            for state, path in beam:
                if state.is_won:
                    return path
                for action in state.legal_actions():
                    child = state.copy()
                    child.apply(action)
                    key = child.signature()
                    if key in candidates:
                        continue
                    candidates[key] = (self.heuristic(child), child, path + [action])

            ranked = sorted(candidates.values(), key=lambda c: c[0], reverse=True)
            if ranked and ranked[0][0] > best_score:
                best_score, best_path = ranked[0][0], ranked[0][2]
            beam = [(s, p) for _, s, p in ranked[: self.beam_width]]

        return best_path  # every branch dead-ended; return the best partial run
