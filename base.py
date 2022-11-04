from typing import Optional
from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """
    The class inherits from the BaseSingleton class,
    so its only instance will be created.
    One arena for both players.
    """
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        """
        'New game' button logic.
        Initialize player instances.
        """
        self.game_is_running = True
        self.player = player
        self.enemy = enemy

    def _check_players_hp(self) -> Optional[str]:
        """ Health check of both players. """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "The draw"
        elif self.player.hp > 0 and self.enemy.hp <= 0:
            self.battle_result = f"{self.player.name} wins the battle"
        else:
            self.battle_result = f"{self.player.name} lost the battle"

        return self._end_game()

    def _stamina_regeneration(self) -> None:
        """ Increment of stamina of both players by a certain constant. """

        units = [self.player, self.enemy]

        for unit in units:
            unit.stamina += round(self.STAMINA_PER_ROUND * unit.unit_class.stamina_rate, 1)
            if unit.stamina > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina

    def next_turn(self) -> Optional[str]:
        """
        Automatic next turn logic. Starts after the player's turn or after pressing 'Skip turn' button.
        Writes the auxiliary result of the enemy's turn to a variable
        for the correct final output if his turn was last.
        """
        self._stamina_regeneration()
        enemy_log = self.enemy.hit(self.player)
        finish_result = self._check_players_hp()
        if finish_result:
            return finish_result
        else:
            return enemy_log

    def _end_game(self):
        """
        'End game' button logic.
        Resets the 'self._instances' filed of parent BaseSingleton metaclass as well.
        """
        self._instances = {}
        self.game_is_running = False

        return self.battle_result

    def player_hit(self) -> str:
        """
        'Hit' button logic.
        Calls the 'next_turn()' method (computer's turn) after the player's turn.
        """
        player_result = self.player.hit(self.enemy)
        enemy_result = self.next_turn()

        return f'{player_result}<br>{enemy_result}'

    def player_use_skill(self) -> str:
        """
        'Use skill' button logic.
        Calls the 'next_turn()' method (computer's turn) after the player's turn.
        """
        player_result = self.player.use_skill(self.enemy)
        enemy_result = self.next_turn()

        return f'{player_result}<br>{enemy_result}'
