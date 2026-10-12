"""Tower layout. Each floor builder takes the stairs node below and returns the stairs node above."""
from __future__ import annotations

from .graph import TowerGraph, TowerNode
from .keys import Keys
from .monsters import Monster


def build_tower() -> TowerGraph:
    tower = TowerGraph()
    stair = entry_floor(tower)
    stair = first_floor(tower, stair)
    stair = second_floor(tower, stair)
    stair = third_floor(tower, stair)
    stair = fourth_floor(tower, stair)
    stair = fifth_floor(tower, stair)
    stair = sixth_floor(tower, stair)
    stair = seventh_floor(tower, stair)
    return tower


def entry_floor(tower: TowerGraph) -> int:
    tower.current_floor = "entry floor"
    tower.current_location = "entrance"
    first_gate = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [])
    return first_gate


def first_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "first floor"
    # entrance
    tower.current_location = "entrance"
    red_key = tower.add_node(TowerNode(key_gain=Keys(red=1)), [stairs])
    red_key_door = tower.add_node(TowerNode(key_required=Keys(red=1)), [red_key])


    # Health side room
    tower.current_location = "Health room"
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [red_key_door])
    priest = tower.add_node(TowerNode(monster=Monster.Priest), [door])
    g_slime = tower.add_node(TowerNode(monster=Monster.GreenSlime), [priest])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [g_slime])
    tower.add_node(TowerNode(monster=Monster.BigSlime, health_gain=800, key_gain=Keys(yellow=2)), [bat])

    # Holy emblem side room
    tower.current_location = "Holy Emblem"
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [red_key_door])
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton, attack_gain=3, health_gain=200, key_gain=Keys(yellow=1)), [door])
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton), [skeleton])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [skeleton])
    skeleton_b = tower.add_node(TowerNode(monster=Monster.SkeletonB, defense_gain=3, key_gain=Keys(yellow=1, blue=1)), [door])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [skeleton_b])
    tower.add_node(TowerNode(monster=Monster.SkeletonB, health_gain=900, key_gain=Keys(yellow=2)), [door])

    # Zombie Side room
    tower.current_location = "Key room"
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [red_key_door])
    tower.add_node(TowerNode(monster=Monster.Zombie, key_gain=Keys(yellow=4, blue=1)), [door])

    # exit
    tower.current_location = "Exit"
    first_green = tower.add_node(TowerNode(monster=Monster.GreenSlime), [red_key_door])
    first_red = tower.add_node(TowerNode(monster=Monster.RedSlime), [first_green])
    second_green = tower.add_node(TowerNode(monster=Monster.GreenSlime), [first_red])
    end_key = tower.add_node(TowerNode(key_gain=Keys(yellow=1)), [second_green])
    return end_key


def second_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "Second floor"
    # TODO: add side room
    return stairs


def third_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "Third floor"
    # entrance
    tower.current_location = "entrance"
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [stairs])
    g_slime = tower.add_node(TowerNode(monster=Monster.GreenSlime), [bat])
    g_slime = tower.add_node(TowerNode(monster=Monster.GreenSlime), [g_slime])  # from here we can go to a side room

    # sword side room
    tower.current_location = "Sword room"
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [g_slime])
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton, key_gain=Keys(yellow=3)), [door])
    r_slime1 = tower.add_node(TowerNode(monster=Monster.RedSlime), [skeleton])
    r_slime2 = tower.add_node(TowerNode(monster=Monster.RedSlime), [skeleton])
    tower.add_node(TowerNode(attack_gain=10), [r_slime1, r_slime2])

    # mid_hallway
    tower.current_location = "Middle hallway"
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [g_slime])
    r_slime = tower.add_node(TowerNode(monster=Monster.RedSlime), [bat])
    hallway_bat = tower.add_node(TowerNode(monster=Monster.Bat, key_gain=Keys(yellow=3)), [r_slime])

    # golem side room
    tower.current_location = "Golem room"
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton), [hallway_bat])
    tower.add_node(TowerNode(key_required=Keys(yellow=1), special_actions_granted=["golem"]), [skeleton])

    # health side room
    tower.current_location = "Health room"
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [hallway_bat])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [door])
    r_slime1 = tower.add_node(TowerNode(monster=Monster.RedSlime), [door])
    r_slime2 = tower.add_node(TowerNode(monster=Monster.RedSlime), [door])
    tower.add_node(TowerNode(defense_gain=3, attack_gain=3, health_gain=500, key_gain=Keys(yellow=2)), [bat, r_slime1, r_slime2])

    # exit
    tower.current_location = "Exit"
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [hallway_bat])
    r_slime = tower.add_node(TowerNode(monster=Monster.RedSlime), [bat])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [r_slime])
    r_slime = tower.add_node(TowerNode(monster=Monster.RedSlime), [bat])
    return r_slime


def fourth_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "Fourth floor"
    # entrance
    tower.current_location = "entrance"
    r_slime = tower.add_node(TowerNode(monster=Monster.RedSlime), [stairs])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [r_slime])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [bat])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [bat])
    big_slime = tower.add_node(TowerNode(monster=Monster.BigSlime), [door])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [big_slime])
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton, health_gain=400), [door])
    big_slime = tower.add_node(TowerNode(monster=Monster.BigSlime), [skeleton])

    # Prison room
    tower.current_location = "Prison room"
    door = tower.add_node(TowerNode(key_required=Keys(blue=1)), [big_slime])
    zombie = tower.add_node(TowerNode(monster=Monster.Zombie, attack_gain=6), [door])
    tower.add_node(TowerNode(monster=Monster.Zombie), [zombie])  # dead end
    tower.add_node(TowerNode(monster=Monster.Zombie), [zombie])  # dead end
    gate_a = tower.add_node(TowerNode(monster=Monster.GateA), [zombie])
    door = tower.add_node(TowerNode(key_required=Keys(red=1)), [gate_a])
    big_bat = tower.add_node(TowerNode(monster=Monster.BigBat, defense_gain=6), [door])
    tower.add_node(TowerNode(monster=Monster.BigBat), [big_bat])  # dead end
    tower.add_node(TowerNode(monster=Monster.BigBat), [big_bat])  # dead end
    tower.add_node(TowerNode(monster=Monster.RedBat), [big_bat])
    # TODO! Figure out what happens after this point (try to free the prisoner?)

    # exit
    tower.current_location = "Exit"
    big_slime = tower.add_node(TowerNode(monster=Monster.BigSlime, health_gain=400), [big_slime])
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton), [big_slime])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [skeleton])
    big_slime = tower.add_node(TowerNode(monster=Monster.BigSlime), [door])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [big_slime])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [door])
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [bat])
    r_slime = tower.add_node(TowerNode(monster=Monster.RedSlime), [bat])
    return r_slime


def fifth_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "Fifth floor"
    # shortest route up
    tower.current_location = "entrance"
    entrance_bat = tower.add_node(TowerNode(monster=Monster.Bat), [stairs])
    tower.current_location = "shortcut"
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [entrance_bat])
    shortcut_door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [bat])
    blue_door = tower.add_node(TowerNode(key_required=Keys(blue=1), key_gain=Keys(yellow=1), defense_gain=3), [shortcut_door])
    exit_door_1 = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [blue_door])

    # side route
    tower.current_location = "Side route"
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [entrance_bat])
    big_slime = tower.add_node(TowerNode(monster=Monster.BigSlime), [bat])
    big_slime = tower.add_node(TowerNode(monster=Monster.BigSlime), [big_slime])

    # xp route
    tower.current_location = "Old man room"
    priest = tower.add_node(TowerNode(monster=Monster.Priest, attack_gain=3, health_gain=200), [big_slime])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [priest])
    tower.add_node(TowerNode(monster=Monster.BigBat, defense_gain=3, attack_gain=3, special_actions_granted=["old_man"]), [door])
    tower.add_node(TowerNode(monster=Monster.BigBat, key_gain=Keys(red=1, blue=1, yellow=1)), [door])

    # atrium
    tower.current_location = "Atrium"
    bat = tower.add_node(TowerNode(monster=Monster.Bat), [big_slime])
    skeleton = tower.add_node(TowerNode(monster=Monster.Skeleton), [bat])
    skeleton_b_1 = tower.add_node(TowerNode(monster=Monster.SkeletonB), [skeleton])
    skeleton_b_2 = tower.add_node(TowerNode(monster=Monster.SkeletonB), [skeleton])
    tower.add_node(TowerNode(special_actions_granted=["merchant"]), [skeleton_b_1, skeleton_b_2])

    # shield room + other goodies
    tower.current_location = "Shield room"
    zombie = tower.add_node(TowerNode(monster=Monster.Zombie), [skeleton])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [zombie])
    priest_1 = tower.add_node(TowerNode(monster=Monster.Priest), [door])
    priest_2 = tower.add_node(TowerNode(monster=Monster.Priest), [door])
    tower.add_node(TowerNode(key_gain=Keys(yellow=2, blue=1)), [priest_1, priest_2])
    priest_1 = tower.add_node(TowerNode(monster=Monster.Priest), [door])
    priest_2 = tower.add_node(TowerNode(monster=Monster.Priest), [door])
    tower.add_node(TowerNode(health_gain=500), [priest_1, priest_2])
    skeleton_b_1 = tower.add_node(TowerNode(monster=Monster.SkeletonB), [door])
    skeleton_b_2 = tower.add_node(TowerNode(monster=Monster.SkeletonB), [door])
    tower.add_node(TowerNode(defense_gain=10), [skeleton_b_1, skeleton_b_2])

    # zombie corridor (part of the shortest route)
    tower.current_location = "Zombie corridor"
    tower.add_node(TowerNode(monster=Monster.Zombie), [shortcut_door, skeleton])

    # alternative exit
    tower.current_location = "Alt. Exit"
    gate_a = tower.add_node(TowerNode(monster=Monster.GateA), [skeleton])
    exit_door_2 = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [gate_a])

    tower.current_location = "Exit"
    stairs = tower.add_node(TowerNode(), [exit_door_1, exit_door_2])
    return stairs

def sixth_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "Sixth floor"
    #Straight route
    tower.current_location = "Straight route"
    double_door = tower.add_node(TowerNode(key_required=Keys(yellow=2)), [stairs])

    #upper route
    tower.current_location = "Upper route"
    door = tower.add_node(TowerNode(key_required=Keys(blue=1)), [stairs])
    exit_b_bat = tower.add_node(TowerNode(monster=Monster.BigBat), [door])

    #Side hallway
    tower.current_location = "Side hallway"
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [exit_b_bat])
    b_bat = tower.add_node(TowerNode(monster=Monster.BigBat), [door])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [b_bat])
    b_bat = tower.add_node(TowerNode(monster=Monster.BigBat), [door])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [b_bat])
    b_bat = tower.add_node(TowerNode(monster=Monster.BigBat), [door])
    superion = tower.add_node(TowerNode(monster=Monster.Superion, key_gain=Keys(yellow=3)), [b_bat])

    #Gate hallway
    tower.current_location = "Gate hallway"
    door_gate = tower.add_node(TowerNode(key_required=Keys(red=1), monster=Monster.GateA, attack_gain=3, defense_gain=3), [superion])

    #Wing room
    tower.current_location = "Wing room"
    door = tower.add_node(TowerNode(key_required=Keys(blue=1), monster=Monster.RedBat, key_gain=Keys(yellow=2)), [door_gate])
    skeleton_c_1 = tower.add_node(TowerNode(monster=Monster.SkeletonC), [door])
    skeleton_c_2 = tower.add_node(TowerNode(monster=Monster.SkeletonC), [door])
    wing = tower.add_node(TowerNode(), [skeleton_c_1, skeleton_c_2]) #This is the Wing, I don't know what it does yet

    #Coin room
    tower.current_location = "Coin room"
    door = tower.add_node(TowerNode(key_required=Keys(blue=1), monster=Monster.RedBat, key_gain=Keys(yellow=3)), [door_gate])
    slime_lord_1 = tower.add_node(TowerNode(monster=Monster.SlimeLord), [door])
    slime_lord_2 = tower.add_node(TowerNode(monster=Monster.SlimeLord), [door])
    coin = tower.add_node(TowerNode(), [slime_lord_1, slime_lord_2]) #This is the coin, I don't know what it does yet (probably gives money?)

    #Health room
    tower.current_location = "Health room"
    superion = tower.add_node(TowerNode(monster=Monster.Superion, key_gain=Keys(yellow=3)), [superion])
    door_magician_a = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [superion])
    rock_1 = tower.add_node(TowerNode(monster=Monster.Rock), [door_magician_a])
    rock_2 = tower.add_node(TowerNode(monster=Monster.Rock), [door_magician_a])
    health = tower.add_node(TowerNode(health_gain=500), [rock_1, rock_2])

    #exit
    tower.current_location = "Exit"
    exit = tower.add_node(TowerNode(), [exit_b_bat, double_door])
    return exit

def seventh_floor(tower: TowerGraph, stairs: int) -> int:
    tower.current_floor = "Seventh floor"
    #skeleton side
    tower.current_location = "Skeleton side"
    skeleton_door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [stairs])
    skeleton_c = tower.add_node(TowerNode(monster=Monster.SkeletonC, attack_gain=3), [skeleton_door])
    skeleton_c = tower.add_node(TowerNode(monster=Monster.SkeletonC), [skeleton_c])

    #bat side
    tower.current_location = "Bat side"
    red_bat_1 = tower.add_node(TowerNode(monster=Monster.RedBat), [skeleton_c])
    red_bat_2 = tower.add_node(TowerNode(monster=Monster.RedBat), [skeleton_c])
    defense_up = tower.add_node(TowerNode(defense_gain=3), [red_bat_1, red_bat_2])
    door = tower.add_node(TowerNode(key_required=Keys(yellow=1)), [red_bat_2]) #this door technically leads down, but you cannot access it when going up, you have to go through the skeletons first, that is why it will not connect to anything

    #Goodie room
    tower.current_location = "Goodies room"
    door = tower.add_node(TowerNode(key_required=Keys(red=1), key_gain=Keys(blue=4, yellow=2), health_gain=1300, defense_gain=3, attack_gain=3), [stairs])

    #cross access
    tower.current_location = "Cross - Bottom"
    cross_bottom = tower.add_node(TowerNode(key_required=Keys(blue=1), monster=Monster.TheMagic), [door])
    tower.current_location = "Cross - Right"
    cross_right = tower.add_node(TowerNode(key_required=Keys(blue=1), monster=Monster.TheMagic), [skeleton_door])
    tower.current_location = "Cross - Top"
    cross_top = tower.add_node(TowerNode(key_required=Keys(blue=1), monster=Monster.TheMagic), [skeleton_c])
    tower.current_location = "Cross - Left"
    cross_left = tower.add_node(TowerNode(key_required=Keys(blue=1), monster=Monster.TheMagic), [red_bat_2])
    tower.current_location = "Cross"
    cross = tower.add_node(TowerNode(), [cross_bottom, cross_right, cross_top, cross_left]) #I don't know what the cross does yet

    #exit
    tower.current_location = "Exit"
    exit = tower.add_node(TowerNode(), [skeleton_c])
    return exit
