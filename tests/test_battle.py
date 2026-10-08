# tests/test_battle.py
import pytest
from zarena.battle import run_monte_carlo, simulate_duel
from zarena.warriors import BaseWarrior


def test_duel_determinism_with_seed() -> None:
    f1_a = BaseWarrior("Goku", hp=100, attack_power=30)
    f2_a = BaseWarrior("Vegeta", hp=100, attack_power=30)
    res_a = simulate_duel(f1_a, f2_a, seed=42)

    f1_b = BaseWarrior("Goku", hp=100, attack_power=30)
    f2_b = BaseWarrior("Vegeta", hp=100, attack_power=30)
    res_b = simulate_duel(f1_b, f2_b, seed=42)

    assert res_a.winner.name == res_b.winner.name
    assert res_a.turns == res_b.turns
    assert res_a.remaining_hp == res_b.remaining_hp


def test_duel_structural_invariants() -> None:
    f1 = BaseWarrior("Goku", hp=100, attack_power=30)
    f2 = BaseWarrior("Vegeta", hp=100, attack_power=30)
    res = simulate_duel(f1, f2, seed=None)

    assert res.winner.is_alive is True
    assert res.loser.is_defeated is True
    assert res.loser.hp == 0
    assert res.turns > 0
    assert res.remaining_hp == res.winner.hp


def test_monte_carlo_statistical_convergence() -> None:
    def make_goku():
        return BaseWarrior("Goku SSJ", hp=300, attack_power=80)

    def make_saibaman():
        return BaseWarrior("Saibaman", hp=40, attack_power=10)

    res = run_monte_carlo(
        make_goku, make_saibaman, n_simulations=500, seed=123
    )
    assert res["winrate"] == pytest.approx(1.0, abs=0.01)
    assert res["turns_mean"] > 0