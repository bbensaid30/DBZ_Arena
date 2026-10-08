# test_exo4.py
from zarena.exceptions import InvalidStatError, NotEnoughKiError
from zarena.warriors import BaseWarrior, SaiyanWarrior

# 1. Validation de l'invariant constructeur
try:
    SaiyanWarrior(
        name="Broly", hp=100, ki=50, attack_power=40, rage_multiplier=0.8
    )
    assert False, "Erreur : rage_multiplier <= 1.0 accepté !"
except InvalidStatError:
    pass

# 2. Saiyan en état nominal (Vegeta)
vegeta = SaiyanWarrior(
    name="Vegeta", hp=100, ki=30, attack_power=50, rage_multiplier=2.0
)
assert vegeta.compute_damage() == 50  # Attaque physique nominale

# 3. Attaque Ki (Kikoha)
degats_kikoha = vegeta.blast_attack()
assert degats_kikoha == 100  # 50 * 2
assert vegeta.ki == 10  # 30 - 20 = 10

# Test échec Ki insuffisant (< 20)
try:
    vegeta.blast_attack()
    assert False, "Erreur : Kikoha sans Ki suffisant accepté !"
except NotEnoughKiError:
    pass

# 4. Activation Zenkai (Santé critique <= 25 PV)
vegeta.take_damage(80)  # Reste 20 PV
assert vegeta.in_critical_state is True
assert vegeta.compute_damage() == 100  # 50 * 2.0 (rage Zenkai activée !)

print("Exercice 4 validé avec succès !")