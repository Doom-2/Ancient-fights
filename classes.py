from skills import Skill, FuryPunch, HardShot
from dataclasses import dataclass


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack_rate: float
    armor_rate: float
    stamina_rate: float
    skill: Skill


# Initializing 2 instances of 'UnitClass' and storing them into dict

WarriorClass = UnitClass("Warrior", 60.0, 30.0, 0.8, 1.2, 0.9, FuryPunch())

ThiefClass = UnitClass("Thief", 50.0, 25.0, 1.5, 1.0, 1.2, HardShot())

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
