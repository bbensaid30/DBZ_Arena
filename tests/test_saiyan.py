# tests/test_saiyan.py
import pytest
from zarena.exceptions import NotEnoughKiError
from zarena.warriors import SaiyanWarrior


def test_saiyan_nominal_damage(saiyan_vegeta: SaiyanWarrior) -> None:
    assert saiyan_vegeta.compute_damage() == 40


def test_saiyan_zenkai_rage_activation(saiyan_vegeta: SaiyanWarrior) -> None:
    saiyan_vegeta.take_damage(80)  # Tombe à 20 PV (<= 25 PV max)
    assert saiyan_vegeta.in_critical_state is True
    # 40 * 2.0 = 80
    assert saiyan_vegeta.compute_damage() == 80


def test_saiyan_blast_attack_nominal(saiyan_vegeta: SaiyanWarrior) -> None:
    degats = saiyan_vegeta.blast_attack()
    assert degats == 80  # 40 * 2
    assert saiyan_vegeta.ki == 30  # 50 - 20


def test_saiyan_blast_attack_insufficient_ki_raises(
    saiyan_vegeta: SaiyanWarrior,
) -> None:
    saiyan_vegeta.ki = 10
    assert saiyan_vegeta.can_blast is False

    with pytest.raises(NotEnoughKiError, match="Ki insuffisant"):
        saiyan_vegeta.blast_attack()