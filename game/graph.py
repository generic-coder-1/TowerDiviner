from __future__ import annotations

from collections import deque
from dataclasses import field

from game.actions import SPECIAL_ACTIONS, Action, MoveTo, SpecialAction, UseSpecial

from .entity import Player
from .helpers import compact_dataclass
from .keys import Keys
from .monsters import Monster


@compact_dataclass
class TowerNode:
    """One thing standing between the player and the next area.

    A node can hold a monster, require keys, and/or grant stats, keys and
    special actions. Completing it applies all of that to the player.
    """

    monster: Monster | None = None
    defense_gain: int = 0
    attack_gain: int = 0
    health_gain: int = 0
    level_gain: int = 0
    gold_gain: int = 0
    key_gain: Keys | None = None
    key_required: Keys | None = None
    special_actions_granted: list[str] = field(default_factory=list)

    def completable(self, player: Player) -> bool:
        if self.monster and player.can_beat(self.monster.stats) is None:
            return False
        if self.key_required and not (player.keys >= self.key_required):
            return False
        return True

    def try_complete(self, player: Player) -> bool:
        if not self.completable(player):
            return False

        if self.monster:
            player.try_defeat(self.monster.stats)
        if self.key_required:
            player.keys -= self.key_required
        if self.key_gain:
            player.keys += self.key_gain

        player.attack += self.attack_gain
        player.defense += self.defense_gain
        player.health += self.health_gain
        player.level += self.level_gain
        player.gold += self.gold_gain
        return True


@compact_dataclass
class TowerGraph:
    """The tower as an undirected graph. Node 0 is the start, the last node is the goal."""

    nodes: list[tuple[TowerNode, list[int]]] = field(default_factory=list)
    unlocks: dict[int, list[str]] = field(default_factory=dict)
    node_annotation: list[tuple[str, str]] = field(default_factory=list)
    current_floor: str = ""
    current_location: str = ""
    _goal_distances: list[int] | None = field(default=None, init=False, repr=False, compare=False)

    def add_node(self, node: TowerNode, connected: list[int], unlock_conditions: list[str] | None = None) -> int:
        node_index = len(self.nodes)
        self.nodes.append((node, list(connected)))
        self.node_annotation.append((self.current_floor, self.current_location))
        for neighbor in connected:
            self.nodes[neighbor][1].append(node_index)
        if unlock_conditions:
            self.unlocks[node_index] = unlock_conditions
        self._goal_distances = None
        return node_index

    def __len__(self) -> int:
        return len(self.nodes)

    @property
    def goal(self) -> int:
        """The goal is the last node added (the stairs at the top of the tower)."""
        return len(self.nodes) - 1

    def goal_distances(self) -> list[int]:
        """Hop count from every node to the goal, ignoring doors and monsters."""
        if self._goal_distances is None:
            dist = [-1] * len(self.nodes)
            dist[self.goal] = 0
            queue = deque([self.goal])
            while queue:
                current = queue.popleft()
                for neighbor in self.nodes[current][1]:
                    if dist[neighbor] == -1:
                        dist[neighbor] = dist[current] + 1
                        queue.append(neighbor)
            self._goal_distances = dist
        return self._goal_distances

    def print_path_with_annotations(self, path: list[Action]):
        floor = None
        location = None
        
        for action in path:
            if isinstance(action, MoveTo):
                node_floor, node_location = self.node_annotation[action.node]
                if node_floor != floor:
                    print(f"Floor: {node_floor}")
                    floor = node_floor
                    location = None
                if node_location != location:
                    print(f"\tLocation: {node_location}")
                    location = node_location
                print(f"\t\tNode {action.node:03d}: {self.nodes[action.node]}")
            elif isinstance(action, UseSpecial):
                sp_action = SPECIAL_ACTIONS[action.group][action.index]
                print(f"\t\tTrade: {action.group}, {sp_action}")



@compact_dataclass
class TowerState:
    """Which nodes are done / reachable, and which special actions are unlocked."""

    completed_nodes: set[int] = field(default_factory=set)
    # active nodes are nodes that have not been completed yet but can be reached
    active_nodes: set[int] = field(default_factory=lambda: {0})
    locked_active_nodes: set[int] = field(default_factory=lambda: {0})
    special_actions_unlocked: set[str] = field(default_factory=set)

    def copy(self) -> TowerState:
        return TowerState(
            set(self.completed_nodes),
            set(self.active_nodes),
            set(self.special_actions_unlocked),
        )

    def is_node_unlocked(self, tower: TowerGraph, node_i: int) -> bool:
        return all(cond in self.special_actions_unlocked for cond in tower.unlocks[node_i])

    def get_active_nodes(self) -> set[int]:
        return self.active_nodes

    def try_complete_node(self, tower: TowerGraph, player: Player, index: int) -> bool:
        if index not in self.active_nodes:
            return False

        if not self.is_node_unlocked(tower, index):
            return False

        node, next_nodes = tower.nodes[index]
        if not node.try_complete(player):
            return False

        self.completed_nodes.add(index)
        self.active_nodes.remove(index)
        self.special_actions_unlocked.update(node.special_actions_granted)

        for next_node in next_nodes:
            if next_node not in self.completed_nodes:
                if self.is_node_unlocked(next_node):
                    self.active_nodes.add(next_node)
                else:
                    self.locked_active_nodes.add(next_node)
        
        if len(node.special_actions_granted) != 0:
            for node_i in tower.unlocks.keys():
                if self.is_node_unlocked(tower, node_i) and node_i in self.locked_active_nodes:
                    self.locked_active_nodes.remove(node_i)
                    self.active_nodes.add(node_i)

        return True

    def get_unlocked_special_actions(self) -> set[str]:
        return self.special_actions_unlocked
