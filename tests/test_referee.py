# tests/test_referee.py
from zarena.referee import safe_attack_round
from zarena.warriors import BaseWarrior


def test_safe_attack_round_nominal() -> None:
    # Cas nominal (bloc else)
    goku = BaseWarrior("Goku", hp=100, attack_power=30)
    vegeta = BaseWarrior("Vegeta", hp=100, attack_power=25)

    msg = safe_attack_round(attacker=goku, defender=vegeta)
    assert msg == "Assaut réussi : 30 dégâts infligés."
    assert vegeta.hp == 70


def test_safe_attack_round_defender_already_fainted() -> None:
    # Cas cible K.-O. (bloc except FighterFaintedError)
    goku = BaseWarrior("Goku", hp=100, attack_power=30)
    vegeta = BaseWarrior("Vegeta", hp=10, attack_power=25)
    vegeta.take_damage(10)  # vegeta tombe à 0 PV

    msg = safe_attack_round(attacker=goku, defender=vegeta)
    assert msg == "Coup impossible : défenseur déjà hors combat."


def test_safe_attack_round_invalid_damage_raises_stat_error() -> None:
    # Cas anomalie statistique (bloc except InvalidStatError)
    class CorruptedWarrior(BaseWarrior):

        def execute_attack(self) -> int:
            return -50  # Dégâts négatifs illégaux

    glitch = CorruptedWarrior("Glitch", hp=100, attack_power=10)
    vegeta = BaseWarrior("Vegeta", hp=100, attack_power=25)

    msg = safe_attack_round(attacker=glitch, defender=vegeta)
    assert msg == "Anomalie de combat : statistiques invalides."