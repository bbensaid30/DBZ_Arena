# tests/test_parallel_engine.py
import pytest
from zarena.parallel_engine import run_parallel_monte_carlo
from zarena.warriors import SaiyanWarrior, Cyborg


@pytest.fixture
def match_fighters():
    gohan = SaiyanWarrior("Gohan SSJ2", hp=150, ki=100, attack_power=65)
    cell = Cyborg("Perfect Cell", hp=160, power=60, shield=10)
    return gohan, cell


def test_parallel_determinism_with_seed(match_fighters):
    """Deux simulations avec la même graine renvoient les mêmes résultats au bit près."""
    gohan, cell = match_fighters
    res1 = run_parallel_monte_carlo(gohan, cell, n_simulations=5000, n_jobs=2, seed=123)
    res2 = run_parallel_monte_carlo(gohan, cell, n_simulations=5000, n_jobs=2, seed=123)

    assert res1["winrate"] == res2["winrate"]
    assert res1["ci_95"] == res2["ci_95"]


def test_confidence_interval_mathematical_bounds(match_fighters):
    """L'intervalle de confiance encadre la moyenne et est inclus dans [0, 1]."""
    gohan, cell = match_fighters
    res = run_parallel_monte_carlo(gohan, cell, n_simulations=3000, n_jobs=2, seed=42)

    p_hat = res["winrate"]
    ci_low, ci_high = res["ci_95"]

    assert 0.0 <= ci_low <= p_hat <= ci_high <= 1.0


def test_backend_equivalence(match_fighters):
    """ProcessPoolExecutor et joblib produisent le même résultat statistique avec la même graine."""
    gohan, cell = match_fighters
    res_exec = run_parallel_monte_carlo(gohan, cell, n_simulations=5000, n_jobs=2, seed=99, backend="executor")
    res_job = run_parallel_monte_carlo(gohan, cell, n_simulations=5000, n_jobs=2, seed=99, backend="joblib")

    assert res_exec["winrate"] == pytest.approx(res_job["winrate"], abs=1e-5)


@pytest.mark.slow
def test_massive_monte_carlo_scaling(match_fighters):
    """Validation sur un volume massif étiquetée @pytest.mark.slow."""
    gohan, cell = match_fighters
    res = run_parallel_monte_carlo(gohan, cell, n_simulations=50000, n_jobs=-1, seed=999)

    assert res["n_simulations"] == 50000
    ci_low, ci_high = res["ci_95"]
    assert (ci_high - ci_low) / 2.0 < 0.005