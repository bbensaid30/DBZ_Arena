# test_exo2.py
from zarena.dummy import TrainingDummy

# 1. Validation de l'invariant constructeur
try:
    TrainingDummy(name="Cible Invalide", max_hp=0)
    assert False, "Erreur : max_hp <= 0 accepté !"
except ValueError:
    pass

# 2. Test de l'encaissement et du plancher à zéro
dummy = TrainingDummy(name="Mannequin Bois", max_hp=50)
assert dummy.current_hp == 50
assert dummy.is_broken() is False

dummy.take_hit(30)
assert dummy.current_hp == 20

dummy.take_hit(40)  # Doit s'arrêter à 0, pas à -20
assert dummy.current_hp == 0
assert dummy.is_broken() is True

# 3. Test de frappe sur mannequin déjà hors service
try:
    dummy.take_hit(10)
    assert False, "Erreur : coup sur cible détruite accepté !"
except RuntimeError:
    pass

print("Exercice 2 validé avec succès !")