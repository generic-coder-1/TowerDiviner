"""A tunable heuristic for "how good is this game state / this path?"."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Iterable

from game import Action, GameState


@dataclass(frozen=True)
class HeuristicWeights:
    """Points awarded per unit of each feature. Tweak these to change what 'good' means."""

    win: float = 10_000.0          # reached the top of the tower
    goal_progress: float = 25.0    # per graph hop closer to the goal than at the start
    nodes_completed: float = 1.0   # per node cleared (rewards clearing side rooms a little)
    attack: float = 8.0
    defense: float = 10.0
    health: float = 0.05
    xp: float = 0.5                # potential: can be spent with the old man
    gold: float = 0.5              # potential: can be spent with the golem / merchant
    yellow_key: float = 3.0
    blue_key: float = 8.0
    red_key: float = 10.0
    green_key: float = 10.0
    special_unlocked: float = 5.0  # per unlocked NPC (golem, old man, merchant)


class Heuristic:
    """Scores a GameState (higher is better). Instances are callable: `heuristic(game)`."""

    def __init__(self, weights: HeuristicWeights | None = None):
        self.weights = weights or HeuristicWeights()

    def breakdown(self, game: GameState) -> dict[str, float]:
        """Per-feature contribution to the score. Handy when tuning the weights."""
        w, p, ts = self.weights, game.player, game.tower_state

        dist = game.tower.goal_distances()
        start_distance = dist[0]
        reachable = [dist[n] for n in ts.active_nodes if dist[n] >= 0]
        # No frontier left: we're either at the goal (distance 0) or completely stuck.
        current_distance = 0 if game.is_won else (min(reachable) if reachable else start_distance)

        return {
            "win": w.win if game.is_won else 0.0,
            "goal_progress": w.goal_progress * (start_distance - current_distance),
            "nodes_completed": w.nodes_completed * len(ts.completed_nodes),
            "attack": w.attack * p.attack,
            "defense": w.defense * p.defense,
            "health": w.health * p.health,
            "xp": w.xp * p.xp,
            "gold": w.gold * p.gold,
            "keys": (
                w.red_key * p.keys.red + w.blue_key * p.keys.blue
                + w.yellow_key * p.keys.yellow + w.green_key * p.keys.green
            ),
            "special_unlocked": w.special_unlocked * len(ts.special_actions_unlocked),
        }

    def __call__(self, game: GameState) -> float:
        return sum(self.breakdown(game).values())

    def evaluate_path(
        self,
        path: Iterable[Action],
        start: GameState | None = None,
    ) -> float:
        """Replay `path` from a fresh game (or a copy of `start`) and score where it ends up.

        Returns -inf if the path contains an illegal action.
        """
        game = start.copy() if start is not None else GameState()
        for action in path:
            if not game.apply(action):
                return float("-inf")
        return self(game)

    def weights_dict(self) -> dict[str, float]:
        return asdict(self.weights)


# Anything callable that maps a GameState to a number can be used as a heuristic.
HeuristicFn = Callable[[GameState], float]
