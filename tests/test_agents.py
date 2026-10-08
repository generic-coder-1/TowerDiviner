import pytest

from agents import (BeamSearchAgent, GreedyAgent, IllegalActionError, PlanningAgent,
                    RandomAgent, StepAgent)
from game import GameState, MoveTo


def play(agent):
    game = GameState()
    path = agent.play(game)
    return game, path


def test_random_agent_is_reproducible_given_a_seed():
    a, b = RandomAgent(), RandomAgent()
    a.reset(7), b.reset(7)
    assert play(a)[1] == play(b)[1]


def test_paths_replay_to_the_same_state():
    game, path = play(GreedyAgent())
    replay = GameState()
    assert replay.apply_path(path)
    assert replay.signature() == game.signature()


def test_beam_search_beats_the_tower():
    game, path = play(BeamSearchAgent(beam_width=50))
    assert game.is_won
    assert GameState().apply_path(path)


def test_step_agent_subclass_only_needs_choose_action():
    class FirstLegal(StepAgent):
        def choose_action(self, game):
            actions = game.legal_actions()
            return actions[0] if actions else None

    game, path = play(FirstLegal())
    assert len(path) > 0 and game.is_over


def test_planning_agent_subclass_only_needs_plan():
    class JustOpenTheGate(PlanningAgent):
        def plan(self, game):
            return [MoveTo(0)]

    game, path = play(JustOpenTheGate())
    assert path == [MoveTo(0)] and 0 in game.tower_state.completed_nodes


def test_illegal_actions_are_reported():
    class Cheater(StepAgent):
        def choose_action(self, game):
            return MoveTo(99)

    with pytest.raises(IllegalActionError):
        play(Cheater())
