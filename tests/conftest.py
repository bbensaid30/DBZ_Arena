# tests/conftest.py
import pytest
from zarena.warriors import BaseWarrior, Cyborg, SaiyanWarrior


@pytest.fixture
def sample_warrior() -> BaseWarrior:
    """Combattant standard Yamcha."""
    return BaseWarrior(name="Yamcha", hp=80, ki=30, attack_power=25)


@pytest.fixture
def saiyan_vegeta() -> SaiyanWarrior:
    """Guerrier Saiyan Vegeta doté d'un multiplicateur de rage 2.0."""
    return SaiyanWarrior(
        name="Vegeta",
        hp=100,
        ki=50,
        attack_power=40,
        rage_multiplier=2.0,
    )


@pytest.fixture
def android_17() -> Cyborg:
    """Cyborg C-17 doté d'un bouclier mécanique de 15 points."""
    return Cyborg(name="C-17", hp=100, power=50, shield=15)