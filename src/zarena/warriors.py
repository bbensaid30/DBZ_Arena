# src/zarena/warriors.py

from abc import ABC, abstractmethod

from zarena.exceptions import (
    FighterFaintedError,
    InvalidStatError,
    NotEnoughKiError,
)

class ArenaFighter(ABC):
    """Interface formelle contractuelle pour tout combattant d'arène."""

    def __init__(self, name: str, hp: int) -> None:
        if hp <= 0:
            raise InvalidStatError("Les points de vie doivent être > 0.")
        self.name = name
        self.max_hp = hp
        self._hp = hp

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))

    @property
    @abstractmethod
    def is_defeated(self) -> bool:
        pass

    @abstractmethod
    def execute_attack(self) -> int:
        pass

    @abstractmethod
    def take_damage(self, amount: int) -> None:
        pass

class BaseWarrior(ArenaFighter):
    """Guerrier standard de Z-Arena doté de PV et de Ki encapsulés."""

    def __init__(
        self, name: str, hp: int, ki: int = 50, attack_power: int = 30
    ) -> None:
        if hp <= 0 or ki < 0 or attack_power <= 0:
            raise InvalidStatError("Statistiques initiales invalides.")
        self.name = name
        self.max_hp = hp
        self.max_ki = 100
        self.attack_power = attack_power

        self.hp = hp
        self.ki = ki

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))

    @property
    def ki(self) -> int:
        return self._ki

    @ki.setter
    def ki(self, value: int) -> None:
        self._ki = max(0, min(value, self.max_ki))

    @property
    def is_alive(self) -> bool:
        return self._hp > 0

    @property
    def is_defeated(self) -> bool:
        return not self.is_alive

    @property
    def in_critical_state(self) -> bool:
        return self._hp <= self.max_hp // 4

    @property
    def can_blast(self) -> bool:
        return self._ki >= 20

    def recharge_ki(self, amount: int = 20) -> None:
        if amount <= 0:
            raise InvalidStatError("Le montant de recharge doit être positif.")
        self.ki += amount

    def compute_damage(self) -> int:
        return self.attack_power

    def execute_attack(self) -> int:
        return self.compute_damage()

    def take_damage(self, amount: int) -> None:
        if not self.is_alive:
            raise FighterFaintedError(f"{self.name} est déjà K.-O. !")
        if amount < 0:
            raise InvalidStatError("Les dégâts doivent être positifs.")
        self.hp -= amount

class SaiyanWarrior(BaseWarrior):
    """Guerrier Saiyan bénéficiant de la rage du combattant et d'attaques de Ki."""

    def __init__(
        self,
        name: str,
        hp: int,
        ki: int = 50,
        attack_power: int = 40,
        rage_multiplier: float = 1.5,
    ) -> None:
        super().__init__(name=name, hp=hp, ki=ki, attack_power=attack_power)
        if rage_multiplier <= 1.0:
            raise InvalidStatError(
                f"Le multiplicateur de rage doit être > 1.0 (reçu : {rage_multiplier})"
            )
        self.rage_multiplier = rage_multiplier

    def compute_damage(self) -> int:
        if self.in_critical_state:
            return int(super().compute_damage() * self.rage_multiplier)
        return super().compute_damage()

    def blast_attack(self) -> int:
        if not self.can_blast:
            raise NotEnoughKiError("Ki insuffisant pour un Kikoha !")
        self.ki -= 20
        return self.compute_damage() * 2

class Cyborg(ArenaFighter):
    """Combattant mécanique réduisant passivement les dégâts reçus."""

    def __init__(
        self, name: str, hp: int, power: int, shield: int = 10
    ) -> None:
        super().__init__(name=name, hp=hp)
        if power <= 0 or shield < 0:
            raise InvalidStatError("Caractéristiques mécaniques invalides.")
        self.power = power
        self.shield = shield

    @property
    def is_defeated(self) -> bool:
        return self.hp == 0

    def execute_attack(self) -> int:
        return self.power

    def take_damage(self, amount: int) -> None:
        if self.is_defeated:
            raise FighterFaintedError(f"{self.name} est déjà détruit !")
        if amount < 0:
            raise InvalidStatError("Les dégâts doivent être positifs.")
        actual_damage = max(0, amount - self.shield)
        self.hp -= actual_damage

    def __repr__(self) -> str:
        return f"Cyborg(name='{self.name}', hp={self.hp}, power={self.power}, shield={self.shield})"

    def __str__(self) -> str:
        return f"[{self.name} | PV: {self.hp}/{self.max_hp}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cyborg):
            return False
        return self.name == other.name and self.hp == other.hp

    def __call__(self) -> int:
        return self.execute_attack()