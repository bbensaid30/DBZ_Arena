# test_exo3.py
from zarena.warriors import BaseWarrior

# 1. Validation de l'invariant constructeur
try:
    BaseWarrior(name="Krilin", hp=0, ki=50, attack_power=30)
    assert False, "Erreur : hp <= 0 accepté !"
except ValueError:
    pass

# 2. Test du bornage automatique des propriétés
krilin = BaseWarrior(name="Krilin", hp=100, ki=50, attack_power=35)
assert krilin.hp == 100
assert krilin.ki == 50
assert krilin.is_alive is True
assert krilin.in_critical_state is False
assert krilin.can_blast is True

# Test dépassement de Ki
krilin.ki = 150
assert krilin.ki == 100  # Bloqué à max_ki

# Test encaissement et bascule en état critique
krilin.take_damage(80)  # Reste 20 PV (<= 25 PV)
assert krilin.hp == 20
assert krilin.in_critical_state is True

# Test consommation de Ki et seuil can_blast
krilin.ki = 10
assert krilin.can_blast is False

# Test recharge
krilin.recharge_ki(30)
assert krilin.ki == 40
assert krilin.can_blast is True

# Test coup fatal
krilin.take_damage(50)
assert krilin.hp == 0
assert krilin.is_alive is False

# Test coup sur guerrier déjà K.-O.
try:
    krilin.take_damage(10)
    assert False, "Erreur : coup sur guerrier K.-O. accepté !"
except RuntimeError:
    pass

print("Exercice 3 validé avec succès !")