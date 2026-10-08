# test_exo6.py
from zarena.warriors import Cyborg

c1 = Cyborg(name="C-18", hp=90, power=55, shield=10)
c2 = Cyborg(name="C-18", hp=90, power=55, shield=10)
c3 = Cyborg(name="C-18", hp=40, power=55, shield=10)

# 1. Diagnostic textuel
assert repr(c1) == "Cyborg(name='C-18', hp=90, power=55, shield=10)"
assert str(c1) == "[C-18 | PV: 90/90]"

# 2. Égalité sémantique
assert c1 == c2
assert c1 != c3
assert (c1 == "texte") is False

# 3. Instance appelable
assert c1() == 55

print("Exercice 6 validé avec succès !")