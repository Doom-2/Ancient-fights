from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    """
    Basic class of skill
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    @property
    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Checks whether unit can use skill or not,
        and calls the 'use_effect()' method or returns an appropriate message.
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()

        return f"{self.user.name} tried to use {self.name} but he didn't have enough stamina."


class FuryPunch(Skill):
    name = "Fury Punch"
    stamina = 6
    damage = 12

    def skill_effect(self) -> str:
        """
        Using of skill logic.
        Target gets the damage while attacker's stamina decreases.
        Returns an appropriate message.
        """
        self.target.get_damage(self.damage)
        self.user.stamina -= self.stamina

        return f"{self.user.name} uses {self.name} and deals {self.damage} damage to the opponent."


class HardShot(Skill):
    name = "Hard Shot"
    stamina = 5
    damage = 15

    def skill_effect(self):

        self.target.get_damage(self.damage)
        self.user.stamina -= self.stamina

        return f"{self.user.name} uses {self.name} and deals {self.damage} damage to opponent."
