import pytest

from agents import BeamSearchAgent, GreedyAgent, RandomAgent
from evaluation import Heuristic, HeuristicWeights, compare_agents, run_agent, run_episode
from game import GameState, MoveTo


def test_heuristic_rewards_progress():
    h = Heuristic()
    game = GameState()
    before = h(game)
    game.apply(MoveTo(0))
    assert h(game) > before


def test_heuristic_prefers_winning_paths():
    h = Heuristic()
    win = GameState()
    win.apply_path(BeamSearchAgent(50).plan(win.copy()))
    assert win.is_won and h(win) > h(GameState()) + 5_000


def test_breakdown_sums_to_score():
    h, game = Heuristic(), GameState()
    assert sum(h.breakdown(game).values()) == pytest.approx(h(game))


def test_weights_are_tunable():
    attack_lover = Heuristic(HeuristicWeights(attack=1000))
    assert attack_lover(GameState()) > Heuristic()(GameState())


def test_evaluate_path():
    h = Heuristic()
    assert h.evaluate_path([MoveTo(0)]) > h.evaluate_path([])
    assert h.evaluate_path([MoveTo(42)]) == float("-inf")


def test_run_episode_records_results():
    result = run_episode(RandomAgent(), seed=3)
    assert result.steps == len(result.path)
    replay = GameState()
    assert replay.apply_path(result.path) and replay.is_won == result.won


def test_deterministic_agents_run_once():
    assert run_agent(GreedyAgent(), n_runs=20).runs == 1
    assert run_agent(RandomAgent(), n_runs=20).runs == 20


def test_compare_agents():
    cmp = compare_agents([RandomAgent(), GreedyAgent(), BeamSearchAgent(20)], n_runs=30)
    assert cmp.reports["BeamSearch(w=20)"].win_rate == 1.0
    wins, losses, ties = cmp.head_to_head("BeamSearch(w=20)", "GreedyAgent")
    assert (wins, losses, ties) == (1, 0, 0)
    w, l, t = cmp.head_to_head("RandomAgent", "BeamSearch(w=20)")
    assert w + l + t == 30
    assert "BeamSearch(w=20)" in cmp.report()


def test_compare_requires_unique_names():
    with pytest.raises(ValueError):
        compare_agents([RandomAgent(), RandomAgent()], n_runs=2)
    compare_agents([RandomAgent(name="a"), RandomAgent(name="b")], n_runs=2)
