# test_exo5.py
from zarena.warriors import BaseWarrior, ArenaFighter, Cyborg

# 1. Vérification de l'interdiction d'instancier l'abstrait
try:
    ArenaFighter(name="Fantôme", hp=100)  # type: ignore
    assert False, "Erreur : instanciation directe d'ArenaFighter autorisée !"
except TypeError:
    pass

# 2. Test du Cyborg
c17 = Cyborg(name="C-17", hp=100, power=60, shield=15)
assert isinstance(c17, ArenaFighter)
assert c17.execute_attack() == 60

c17.take_damage(35)  # 35 - 15 = 20 dégâts réels
assert c17.hp == 80
assert c17.is_defeated is False

# 3. Test du Polymorphisme : combat générique sans distinction d'espèce
krilin = BaseWarrior(name="Krilin", hp=100, ki=50, attack_power=40)
assert isinstance(krilin, ArenaFighter)


def duel_un_tour(f1: ArenaFighter, f2: ArenaFighter) -> None:
    degats = f1.execute_attack()
    f2.take_damage(degats)


duel_un_tour(krilin, c17)  # Krilin (40) frappe C-17 (bouclier 15) -> 25 dégâts
assert c17.hp == 55

print("Exercice 5 validé avec succès !")