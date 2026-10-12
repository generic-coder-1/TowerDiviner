"""Run agents on the game and record how they did."""
from __future__ import annotations

import statistics
import sys
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

from game import Action, GameState, Player

from .heuristic import Heuristic, HeuristicFn

if TYPE_CHECKING:  # avoid a runtime import cycle: agents import evaluation.heuristic
    from agents.base import Agent


@dataclass
class RunResult:
    agent_name: str
    seed: int
    won: bool
    steps: int
    nodes_completed: int
    score: float                 # heuristic score of the final state
    seconds: float
    final_player: Player
    path: list[Action] = field(repr=False)

    @property
    def rank_key(self) -> tuple[bool, float]:
        """Used to rank runs: winning beats not winning, then higher heuristic score."""
        return (self.won, self.score)


@dataclass
class AgentReport:
    """Aggregate statistics over all of one agent's runs."""

    agent_name: str
    results: list[RunResult]

    @property
    def runs(self) -> int:
        return len(self.results)

    @property
    def win_rate(self) -> float:
        return sum(r.won for r in self.results) / self.runs

    @property
    def mean_score(self) -> float:
        return statistics.fmean(r.score for r in self.results)

    @property
    def best_score(self) -> float:
        return max(r.score for r in self.results)

    @property
    def mean_nodes(self) -> float:
        return statistics.fmean(r.nodes_completed for r in self.results)

    @property
    def best_nodes(self) -> int:
        return max(r.nodes_completed for r in self.results)

    @property
    def mean_seconds(self) -> float:
        return statistics.fmean(r.seconds for r in self.results)

    @property
    def shortest_win(self) -> int:
        wins = [r.steps for r in self.results if r.won]
        return min(wins) if wins else sys.maxsize

    @property
    def best_run(self) -> RunResult:
        return max(self.results, key=lambda r: r.rank_key)

    
    @property
    def shortest_run(self) -> RunResult:
        return min([result for result in self.results if result.won], key=lambda r: r.steps)


def run_episode(
    agent: Agent,
    seed: int = 0,
    heuristic: HeuristicFn | None = None,
    max_steps: int = 10_000,
    game_factory: Callable[[], GameState] = GameState,
) -> RunResult:
    heuristic = heuristic or Heuristic()
    game = game_factory()
    agent.reset(seed)

    start = time.perf_counter()
    path = agent.play(game, max_steps=max_steps)
    elapsed = time.perf_counter() - start

    return RunResult(
        agent_name=agent.name,
        seed=seed,
        won=game.is_won,
        steps=len(path),
        nodes_completed=len(game.tower_state.completed_nodes),
        score=heuristic(game),
        seconds=elapsed,
        final_player=game.player.copy(),
        path=path,
    )


def run_agent(
    agent: Agent,
    n_runs: int = 100,
    base_seed: int = 0,
    heuristic: HeuristicFn | None = None,
    max_steps: int = 10_000,
    game_factory: Callable[[], GameState] = GameState,
) -> AgentReport:
    """Run `agent` n_runs times with seeds base_seed, base_seed+1, ...

    Deterministic agents (`agent.deterministic`) are run once since repeats would be identical.
    """
    runs = 1 if agent.deterministic else n_runs
    results = [
        run_episode(agent, base_seed + i, heuristic, max_steps, game_factory)
        for i in range(runs)
    ]
    return AgentReport(agent.name, results)
