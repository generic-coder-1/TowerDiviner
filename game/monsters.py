from __future__ import annotations

from enum import Enum

from .entity import Entity


class Monster(Enum):
    """Monster roster. Each value is (attack, defense, health, xp, gold)."""

    GreenSlime = (20, 1, 50, 1, 1)
    RedSlime = (15, 2, 70, 2, 2)
    Bat = (20, 5, 100, 3, 3)
    Skeleton = (25, 5, 110, 4, 5)
    SkeletonB = (40, 20, 150, 6, 8)
    BigSlime = (35, 10, 200, 5, 5)
    Priest = (50, 25, 125, 7, 10)
    Zombie = (75, 45, 300, 10, 13)
    BigBat = (65, 30, 150, 8, 10)
    RedBat = (160, 90, 550, 25, 20)
    GateA = (150, 90, 450, 19, 22)
    Superion = (200, 110, 100, 25, 30)
    SkeletonC = (90, 50, 400, 12, 15)
    SlimeLord = (250, 150, 700, 30, 32)
    Rock = (115, 65, 500, 15, 15)

    def __init__(self, attack, defense, health, xp, gold):
        self.stats = Entity(attack, defense, health, xp, gold)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
