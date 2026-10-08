# src/zarena/battle.py
from dataclasses import dataclass
from typing import Callable
import numpy as np
from zarena.warriors import ArenaFighter


@dataclass(frozen=True)
class DuelResult:
    """Synthese immuable d'un affrontement dans Z-Arena."""

    winner: ArenaFighter
    loser: ArenaFighter
    turns: int
    remaining_hp: int


def simulate_duel(
    f1: ArenaFighter,
    f2: ArenaFighter,
    seed: int | None = None,
) -> DuelResult:
    """Simule un duel stochastique tour par tour jusqu'au K.-O."""
    rng = np.random.default_rng(seed)
    turns = 0

    while not f1.is_defeated and not f2.is_defeated:
        turns += 1

        # 1. Attaque de f1 avec facteur d'alea physique U ~ [0.85, 1.15]
        u1 = rng.uniform(0.85, 1.15)
        degats_f1 = int(f1.execute_attack() * u1)
        f2.take_damage(degats_f1)

        if f2.is_defeated:
            break

        # 2. Riposte de f2 avec facteur d'alea
        u2 = rng.uniform(0.85, 1.15)
        degats_f2 = int(f2.execute_attack() * u2)
        f1.take_damage(degats_f2)

    winner = f1 if not f1.is_defeated else f2
    loser = f2 if winner == f1 else f1

    return DuelResult(
        winner=winner,
        loser=loser,
        turns=turns,
        remaining_hp=winner.hp,
    )


def run_monte_carlo(
    f1_factory: Callable[[], ArenaFighter],
    f2_factory: Callable[[], ArenaFighter],
    n_simulations: int = 1000,
    seed: int | None = None,
) -> dict[str, float]:
    """Estime le winrate de f1 par simulations de Monte Carlo."""
    rng = np.random.default_rng(seed)
    f1_wins = 0
    total_turns = 0

    for _ in range(n_simulations):
        # On fabrique des combattants frais pour chaque iteration
        f1 = f1_factory()
        f2 = f2_factory()
        # On derive une graine unique par duel pour isoler le tirage
        duel_seed = int(rng.integers(0, 1_000_000))
        result = simulate_duel(f1, f2, seed=duel_seed)

        if result.winner.name == f1.name:
            f1_wins += 1
        total_turns += result.turns

    winrate = f1_wins / n_simulations
    return {
        "winrate": winrate,
        "turns_mean": total_turns / n_simulations,
    }