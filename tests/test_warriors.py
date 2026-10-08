# Solution tests/test_warriors.py
import pytest
from zarena.exceptions import FighterFaintedError, InvalidStatError
from zarena.warriors import BaseWarrior


def test_base_warrior_creation_nominal() -> None:
    krilin = BaseWarrior(name="Krilin", hp=100, ki=50, attack_power=30)
    assert krilin.name == "Krilin"
    assert krilin.hp == 100
    assert krilin.max_hp == 100
    assert krilin.ki == 50
    assert krilin.attack_power == 30
    assert krilin.is_alive is True
    assert krilin.is_defeated is False


def test_base_warrior_take_damage_nominal() -> None:
    warrior = BaseWarrior(name="Krilin", hp=100, ki=50, attack_power=30)
    warrior.take_damage(35)
    assert warrior.hp == 65


def test_base_warrior_invalid_initial_stats_raises() -> None:
    with pytest.raises(InvalidStatError):
        BaseWarrior(name="Invalide", hp=0, ki=10, attack_power=20)

    with pytest.raises(InvalidStatError):
        BaseWarrior(name="Invalide", hp=50, ki=-5, attack_power=20)

    with pytest.raises(InvalidStatError):
        BaseWarrior(name="Invalide", hp=50, ki=10, attack_power=0)


def test_base_warrior_take_damage_clamping_at_zero() -> None:
    warrior = BaseWarrior(name="Krilin", hp=100, ki=50, attack_power=30)
    warrior.take_damage(150)
    assert warrior.hp == 0
    assert warrior.is_alive is False
    assert warrior.is_defeated is True


def test_base_warrior_take_damage_when_already_defeated_raises() -> None:
    warrior = BaseWarrior(name="Krilin", hp=50, ki=40, attack_power=30)
    warrior.take_damage(50)
    assert warrior.hp == 0

    with pytest.raises(FighterFaintedError, match="déjà K.-O."):
        warrior.take_damage(10)

def test_base_warrior_recharge_ki_nominal() -> None:
    krilin = BaseWarrior(name="Krilin", hp=100, ki=30, attack_power=20)
    krilin.recharge_ki(25)
    assert krilin.ki == 55


def test_base_warrior_recharge_ki_clamping_at_max() -> None:
    krilin = BaseWarrior(name="Krilin", hp=100, ki=90, attack_power=20)
    krilin.recharge_ki(50)  # 90 + 50 = 140 -> plafonné à max_ki (100)
    assert krilin.ki == 100


def test_base_warrior_recharge_ki_negative_amount_raises() -> None:
    krilin = BaseWarrior(name="Krilin", hp=100, ki=50, attack_power=20)
    with pytest.raises(InvalidStatError, match="positif"):
        krilin.recharge_ki(-10)