# tests/test_records.py
import json
from pathlib import Path
import pytest
from zarena.battle import run_monte_carlo, simulate_duel
from zarena.records import export_duel_summary
from zarena.warriors import BaseWarrior, Cyborg


def test_export_duel_summary(tmp_path: Path) -> None:
    f1 = BaseWarrior("Goku", hp=100, attack_power=40)
    f2 = BaseWarrior("Vegeta", hp=100, attack_power=30)
    result = simulate_duel(f1, f2, seed=42)

    export_path = tmp_path / "archives" / "duel.json"
    export_duel_summary(result, export_path)

    assert export_path.exists() is True

    with open(export_path, encoding="utf-8") as f:
        data = json.load(f)

    assert data["winner"] == result.winner.name
    assert data["turns"] == result.turns
    assert data["remaining_hp"] == result.remaining_hp


@pytest.mark.slow
def test_massive_monte_carlo_tagged_slow() -> None:
    def make_krilin():
        return BaseWarrior("Krilin", hp=100, attack_power=35)

    def make_c17():
        return Cyborg("C-17", hp=100, power=40, shield=10)

    res = run_monte_carlo(
        make_krilin, make_c17, n_simulations=5000, seed=999
    )
    assert 0.0 <= res["winrate"] <= 1.0
    assert res["turns_mean"] > 0