# tests/test_cyborg.py
import pytest
from zarena.warriors import Cyborg


@pytest.mark.parametrize(
    "incoming_damage, expected_hp",
    [
        (10, 100),  # 10 <= 15 -> 0 degat
        (15, 100),  # 15 == 15 -> 0 degat
        (35, 80),  # 35 - 15 = 20 degats reels -> 80 PV
        (200, 0),  # 200 - 15 = 185 degats -> 0 PV (ecretage a zero)
    ],
)
def test_cyborg_shield_absorption(
    android_17: Cyborg,
    incoming_damage: int,
    expected_hp: int,
) -> None:
    android_17.take_damage(incoming_damage)
    assert android_17.hp == expected_hp


def test_cyborg_dunder_methods(android_17: Cyborg) -> None:
    # 1. Representation textuelle
    assert str(android_17) == "[C-17 | PV: 100/100]"

    # 2. Instance appelable
    assert android_17() == 50

    # 3. Egalite semantique
    clone = Cyborg(name="C-17", hp=100, power=50, shield=15)
    autre = Cyborg(name="C-18", hp=100, power=50, shield=15)

    assert android_17 == clone
    assert android_17 != autre