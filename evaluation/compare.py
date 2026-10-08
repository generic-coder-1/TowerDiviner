"""Compare several agents on equal terms."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence

from .heuristic import Heuristic, HeuristicFn
from .runner import AgentReport, RunResult, run_agent

if TYPE_CHECKING:
    from agents.base import Agent


@dataclass
class Comparison:
    reports: dict[str, AgentReport]
    n_runs: int

    # --- tables -------------------------------------------------------------

    def rows(self) -> list[dict]:
        """One dict per agent, ordered by win rate then mean score. Easy to feed to pandas."""
        rows = [
            {
                "agent": r.agent_name,
                "runs": r.runs,
                "win_rate": r.win_rate,
                "mean_score": r.mean_score,
                "best_score": r.best_score,
                "mean_nodes": r.mean_nodes,
                "best_nodes": r.best_nodes,
                "shortest_win": r.shortest_win,
                "mean_seconds": r.mean_seconds,
            }
            for r in self.reports.values()
        ]
        return sorted(rows, key=lambda row: (row["win_rate"], row["mean_score"]), reverse=True)

    def summary_table(self) -> str:
        header = ["Agent", "Runs", "Win %", "Mean score", "Best score", "Mean nodes", "Best nodes", "Shortest win", "Sec/run"]
        body = [
            [
                row["agent"],
                str(row["runs"]),
                f"{100 * row['win_rate']:.1f}",
                f"{row['mean_score']:.1f}",
                f"{row['best_score']:.1f}",
                f"{row['mean_nodes']:.1f}",
                str(row["best_nodes"]),
                "-" if row["shortest_win"] is None else str(row["shortest_win"]),
                f"{row['mean_seconds']:.3f}",
            ]
            for row in self.rows()
        ]
        return _format_table(header, body)

    # --- head to head -------------------------------------------------------

    def _paired(self, a: str, b: str) -> list[tuple[RunResult, RunResult]]:
        """Pair runs by seed. A deterministic agent has one run, which pairs with every seed."""
        ra, rb = self.reports[a].results, self.reports[b].results
        return [(ra[i % len(ra)], rb[i % len(rb)]) for i in range(max(len(ra), len(rb)))]

    def head_to_head(self, a: str, b: str) -> tuple[int, int, int]:
        """(a wins, b wins, ties) per seed. A win of the game beats a non-win; otherwise higher score wins."""
        wins = losses = ties = 0
        for run_a, run_b in self._paired(a, b):
            if run_a.rank_key > run_b.rank_key:
                wins += 1
            elif run_a.rank_key < run_b.rank_key:
                losses += 1
            else:
                ties += 1
        return wins, losses, ties

    def head_to_head_table(self) -> str:
        """Matrix of 'row beats column' counts, formatted as W-L-T."""
        names = [row["agent"] for row in self.rows()]
        body = []
        for a in names:
            cells = [a]
            for b in names:
                if a == b:
                    cells.append("-")
                else:
                    w, l, t = self.head_to_head(a, b)
                    cells.append(f"{w}-{l}-{t}")
            body.append(cells)
        return _format_table(["row vs col (W-L-T)", *names], body)

    def report(self) -> str:
        return (
            f"Agent comparison ({self.n_runs} runs per stochastic agent, same seeds for everyone)\n\n"
            f"{self.summary_table()}\n\n"
            f"Head to head (winning the game first, then final heuristic score; paired by seed):\n\n"
            f"{self.head_to_head_table()}\n"
        )


def compare_agents(
    agents: Sequence[Agent],
    n_runs: int = 100,
    base_seed: int = 0,
    heuristic: HeuristicFn | None = None,
    max_steps: int = 10_000,
) -> Comparison:
    """Run every agent on the same seeds and bundle the results.

    Agent names must be unique - pass `name=...` when constructing variants.
    """
    names = [a.name for a in agents]
    if len(set(names)) != len(names):
        raise ValueError(f"Agent names must be unique, got {names}")

    heuristic = heuristic or Heuristic()
    reports = {
        agent.name: run_agent(agent, n_runs, base_seed, heuristic, max_steps)
        for agent in agents
    }
    return Comparison(reports, n_runs)


def _format_table(header: list[str], body: list[list[str]]) -> str:
    widths = [max(len(row[i]) for row in [header, *body]) for i in range(len(header))]
    def fmt(row):
        return "  ".join(cell.ljust(w) if i == 0 else cell.rjust(w) for i, (cell, w) in enumerate(zip(row, widths)))
    lines = [fmt(header), "  ".join("-" * w for w in widths), *(fmt(r) for r in body)]
    return "\n".join(lines)
