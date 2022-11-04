from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        """ Returns a 'Weapon' class instance by its 'name' field. """
        weapons = self._get_equipment_data().weapons
        for weapon in weapons:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        """ Returns an 'Armor' class instance by its 'name' field. """
        armors = self._get_equipment_data().armors
        for armor in armors:
            if armor.name == armor_name:
                return armor

    def get_weapons_names(self) -> List[str]:
        """ Returns a list of "name" fields of the Weapon class instances. """
        weapons = self._get_equipment_data().weapons
        return [weapon.name for weapon in weapons]

    def get_armors_names(self) -> List[str]:
        """ Returns a list of "name" fields of the Armor class instances. """
        armors = self._get_equipment_data().armors
        return [armor.name for armor in armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """ Loads json to EquipmentData dataclass. """
        equipment_file = open("./data/equipment.json")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
