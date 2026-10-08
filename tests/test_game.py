from game import (SPECIAL_ACTIONS, Entity, GameState, Keys, Monster, MoveTo, Player,
                  TowerGraph, TowerNode, UseSpecial, build_tower)


def test_combat_loses_expected_health():
    # damage given 9 -> 6 rounds to kill 50hp; they hit for 10 on the 5 rounds before it dies
    assert Player().can_beat(Monster.GreenSlime.stats) == 50


def test_combat_edge_cases():
    wall = Entity(10, 10, 10, 0, 0)
    assert Entity(5, 0, 10, 0, 0).can_beat(wall) is None            # can't scratch them
    assert Entity(30, 50, 10, 0, 0).can_beat(Monster.Bat.stats) == 0  # they can't scratch us
    assert Entity(10, 0, 10, 0, 0).can_beat(Entity(10, 0, 10, 0, 0)) == 0   # we strike first
    assert Entity(10, 0, 10, 0, 0).can_beat(Entity(10, 0, 20, 0, 0)) is None


def test_defeat_applies_loot_and_damage():
    p = Player()
    lost = p.try_defeat(Monster.GreenSlime.stats)
    assert (p.health, p.xp, p.gold) == (1000 - lost, 1, 1)


def test_failed_fight_changes_nothing():
    p = Player(attack=1)
    before = p.copy()
    assert p.try_defeat(Monster.Zombie.stats) is None
    assert p == before


def test_keys_arithmetic_and_ordering():
    a, b = Keys(yellow=2, red=1), Keys(yellow=1)
    assert a + b == Keys(yellow=3, red=1)
    assert a - b == Keys(yellow=1, red=1)
    assert a >= b and b <= a
    assert not (b >= a)
    assert Keys(blue=5) >= Keys()            # the notebook's strict '>' got this wrong
    assert not (Keys(yellow=5) >= Keys(blue=1))


def test_graph_edges_are_bidirectional():
    g = TowerGraph()
    a = g.add_node(TowerNode(), [])
    b = g.add_node(TowerNode(), [a])
    assert b in g.nodes[a][1] and a in g.nodes[b][1]
    assert g.goal == b and g.goal_distances() == [1, 0]


def test_special_action_requires_resources():
    poor = Player()
    assert not SPECIAL_ACTIONS["golem"][0].possible(poor)           # costs 25 gold
    rich = Player(gold=25)
    assert SPECIAL_ACTIONS["golem"][0].take_action(rich) and rich.attack == 14 and rich.gold == 0


def test_new_game_starts_at_the_gate():
    game = GameState()
    assert game.legal_actions() == [MoveTo(0)]
    assert not game.is_won and not game.is_over


def test_apply_illegal_action_returns_false_and_changes_nothing():
    game = GameState()
    before = game.signature()
    assert not game.apply(MoveTo(50))                  # not active
    assert not game.apply(UseSpecial("golem", 0))      # not unlocked
    assert game.signature() == before


def test_copy_is_independent():
    game = GameState()
    clone = game.copy()
    clone.apply(MoveTo(0))
    assert game.signature() != clone.signature()
    assert game.tower_state.completed_nodes == set()
    assert game.player.keys == Keys(red=1, blue=1, yellow=1)


def test_goal_is_reachable_in_the_graph():
    tower = build_tower()
    assert tower.goal_distances()[0] > 0
