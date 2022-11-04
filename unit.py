from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional, Type


class BaseUnit(ABC):
    """ Base unit class. """

    def __init__(self, name: str, unit_class: UnitClass):
        """ Uses some UnitClass attributes during initialization. """

        self.player_skip_step = False
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = ...  # initialized further in method
        self.armor = ...
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    @property
    def article(self) -> str:
        """ Selects the correct article to insert into the battle statistics before nouns """
        if self.weapon.name[0].lower() in ('a', 'e', 'i', 'o', 'u', 'y'):
            return 'an'
        else:
            return 'a'

    def equip_weapon(self, weapon: Weapon):
        """ Equips unit with weapon. """
        self.weapon = weapon
        return f"{self.name} equipped with {self.weapon.name} weapon."

    def equip_armor(self, armor: Armor):
        """ Equips unit with armor. """
        self.armor = armor
        return f"{self.name} equipped with {self.armor.name} armor."

    def _count_damage(self, target: BaseUnit) -> float:
        """
        Counts damage to target, decreases stamina of both players during attack and defence,
        calls 'get_damage' method and returns counted damage in rounded form.
        """

        # Check whether an attacker can use a weapon or does not have enough stamina to do so
        if self.stamina >= self.weapon.stamina_per_hit:
            damage_from_weapon = round(self.weapon.damage * self.unit_class.attack_rate, 1)
            self.stamina -= self.weapon.stamina_per_hit
        else:
            damage_from_weapon = 0

        # Check whether a target can use an armor or does not have enough stamina to do so
        if target.stamina > target.armor.stamina_per_turn:
            target_armor = round(target.armor.defence * target.unit_class.armor_rate, 1)
            target.stamina -= round(target.armor.stamina_per_turn * target.unit_class.stamina_rate, 1)
        else:
            target_armor = 0

        total_damage = damage_from_weapon - target_armor

        # Stamina cannot be negative
        if self.stamina < 0:
            self.stamina = 0
        elif target.stamina < 0:
            target.stamina = 0

        target.get_damage(total_damage)

        return round(total_damage, 1)

    def get_damage(self, damage: float) -> None:
        """ If damage is done, decreases the unit health. """
        if damage > 0:
            self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """ Method will be redefined in child classes. """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Checks the '_is_skill_used' flag and returns either an appropriate message
        or calls 'use()' method of the basic Skill class.
        """
        if self._is_skill_used:
            return "Skill has already used."
        else:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Checks if you (player unit) have enough stamina to kick,
        if you could deal damage, if your opponent could defend himself
        and returns the corresponding message.
        """

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} tried to use {self.article} {self.weapon.name}, but he didn't have enough stamina."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.name} using {self.article} {self.weapon.name}" \
                   f" breaks through opponent's {target.armor.name} and deals him {damage} damage."

        return f"{self.name} using {self.article} {self.weapon.name} hits the opponent, but his {target.armor.name} protects him."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Logic for enemy (computer) hit.
        Adds logic with a 10 percent chance of using skill.
        """
        some_value = 7
        if randint(1, 10) == some_value and not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina:
            self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} tried to use {self.article} {self.weapon.name}, but he didn't have enough stamina."

        damage = self._count_damage(target)

        if damage > 0:
            return f"{self.name} using {self.article} {self.weapon.name}" \
                   f" breaks through your {target.armor.name} and deals you {damage} damage."

        return f"{self.name} using {self.article} {self.weapon.name} hits you, but your {target.armor.name} protects you."
