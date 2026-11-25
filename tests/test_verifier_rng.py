# tests/verifier_rng.py
import numpy as np

master_ss = np.random.SeedSequence(2026)
s1, s2 = master_ss.spawn(2)

rng1 = np.random.default_rng(s1)
rng2 = np.random.default_rng(s2)

echantillons_1 = rng1.random(100_000)
echantillons_2 = rng2.random(100_000)

assert not np.array_equal(echantillons_1, echantillons_2), "Erreur : flux identiques !"
correlation = np.corrcoef(echantillons_1, echantillons_2)[0, 1]
assert abs(correlation) < 0.01, f"Erreur : corrélation anormale ({correlation})"

print(f"Indépendance stochastique validée avec succès (Corrélation r = {correlation:.5f}).")