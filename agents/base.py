"""Base classes for agents.

Write your own agent by subclassing one of:

* `StepAgent`     - implement `choose_action(game)`; it is asked once per step.
* `PlanningAgent` - implement `plan(game)`; it returns a whole path up front
                    (use `game.copy()` to explore without touching the real game).
* `Agent`         - override `play(game)` yourself for full control.

Agents are identified by `name` in comparisons, so give variants distinct names.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from game import Action, GameState


class IllegalActionError(RuntimeError):
    pass


class Agent(ABC):
    #: Set to True if the agent always plays identically. The comparison tools
    #: will then run it once instead of N times.
    deterministic: bool = False

    def __init__(self, name: str | None = None):
        self.name = name or type(self).__name__

    def reset(self, seed: int | None = None) -> None:
        """Called before every episode. Re-seed any randomness / clear any memory here."""

    @abstractmethod
    def play(self, game: GameState, max_steps: int = 10_000) -> list[Action]:
        """Play on `game` in place until it's over; return the actions taken.

        Contract: when this returns, `game` must be in the final state reached.
        """

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r})"


class StepAgent(Agent):
    """An agent that picks one action at a time."""

    @abstractmethod
    def choose_action(self, game: GameState) -> Action | None:
        """Pick one of `game.legal_actions()`, or None to give up."""

    def play(self, game: GameState, max_steps: int = 10_000) -> list[Action]:
        path: list[Action] = []
        for _ in range(max_steps):
            if game.is_over:
                break
            action = self.choose_action(game)
            if action is None:
                break
            if not game.apply(action):
                raise IllegalActionError(f"{self.name} chose illegal action {action!r}")
            path.append(action)
        return path


class PlanningAgent(Agent):
    """An agent that computes a whole path from the starting state, then executes it."""

    @abstractmethod
    def plan(self, game: GameState) -> list[Action]:
        """Return a list of actions. Must not modify `game` (explore on copies)."""

    def play(self, game: GameState, max_steps: int = 10_000) -> list[Action]:
        path = self.plan(game.copy())[:max_steps]
        for action in path:
            if not game.apply(action):
                raise IllegalActionError(f"{self.name} planned illegal action {action!r}")
        return path
