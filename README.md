# Tower of the Sorcerer solver

A deterministic simulator for Tower of the Sorcerer, plus a harness for writing agents
that try to beat it and comparing how they do.

```
game/         the simulation (no agent or scoring code in here)
agents/       Agent base classes + example agents (random, greedy, beam search)
evaluation/   path/state heuristic, episode runner, agent comparison
tests/        pytest suite
run_comparison.py   compare the built-in agents from the command line
```

## Quick start

```bash
python run_comparison.py --runs 500      # compare agents
python -m pytest                         # run tests
```

```python
from game import GameState, MoveTo

game = GameState()
game.legal_actions()          # [MoveTo(node=0)]
game.apply(MoveTo(0))         # True if legal, False (and no change) if not
game.is_won, game.is_over
```

An **action** is either `MoveTo(node)` (clear a node: fight, open a door, grab an item)
or `UseSpecial(group, index)` (a golem / old man / merchant trade, once unlocked).
The goal is the last node of the tower graph (`game.tower.goal`).

## Writing an agent

Subclass `StepAgent` and implement `choose_action`:

```python
from agents import StepAgent

class MyAgent(StepAgent):
    def choose_action(self, game):
        actions = game.legal_actions()
        return actions[0] if actions else None   # None = give up
```

Or subclass `PlanningAgent` and return a whole path from `plan(game)`; use `game.copy()` to explore
without touching the real game (`game.signature()` gives a hashable state for dedup).
For total control, subclass `Agent` and implement `play(game)`.

Override `reset(seed)` to re-seed randomness between episodes, and set `deterministic = True`
if the agent always plays identically (the runner then runs it once instead of N times).

## Heuristic

`evaluation.Heuristic` scores a state (higher = better) from weighted features: reaching the goal,
graph-distance progress, attack/defense/health, keys, spendable xp/gold, unlocked NPCs.
Weights live in `HeuristicWeights`.

```python
from evaluation import Heuristic, HeuristicWeights
h = Heuristic(HeuristicWeights(defense=15))
h(game)                         # score a state
h.breakdown(game)               # per-feature contributions, for tuning
h.evaluate_path(path)           # replay a path from a fresh game and score the end state (-inf if illegal)
```

Any `callable(GameState) -> float` works as a heuristic for the agents that take one.

## Comparing agents

```python
from evaluation import compare_agents
cmp = compare_agents([RandomAgent(), GreedyAgent(), MyAgent(name="mine")], n_runs=500)
print(cmp.report())             # summary table + head-to-head matrix
cmp.rows()                      # list of dicts (pandas-friendly)
cmp.reports["mine"].best_run    # RunResult with the full path
```

Every agent gets the same seeds. Agent names must be unique (pass `name=`). In head-to-head,
winning the game beats not winning; otherwise the higher heuristic score wins.