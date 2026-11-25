from concurrent.futures import ProcessPoolExecutor
import math
import os
from typing import Any
import numpy as np

try:
    from joblib import Parallel, delayed
except ImportError:
    Parallel, delayed = None, None

from zarena.battle import simulate_duel_step
from zarena.warriors import ArenaFighter


def _monte_carlo_worker(
    batch_size: int,
    child_seed: np.random.SeedSequence,
    f1: ArenaFighter,
    f2: ArenaFighter,
) -> tuple[int, list[int]]:
    """Tâche de calcul grossière (Chunk) exécutée en isolation sur un cœur dédié.
    
    Retourne :
        (f1_wins, turns_list) : nombre de victoires de f1 et liste des durées des duels du lot.
    """
    rng = np.random.default_rng(child_seed)
    f1_wins = 0
    turns_list: list[int] = []

    for _ in range(batch_size):
        winner, turns = simulate_duel_step(f1, f2, rng)
        if winner == 1:
            f1_wins += 1
        turns_list.append(turns)

    return f1_wins, turns_list


def run_parallel_monte_carlo(
    f1: ArenaFighter,
    f2: ArenaFighter,
    n_simulations: int = 50000,
    n_jobs: int = -1,
    seed: int | None = None,
    backend: str = "executor",
) -> dict[str, Any]:
    """Orchestre la simulation distribuée via ProcessPoolExecutor ou joblib."""
    if n_simulations <= 0:
        raise ValueError("Le nombre de simulations doit être strictement positif.")
    if backend not in ("executor", "joblib"):
        raise ValueError("Le backend doit être 'executor' ou 'joblib'.")

    # 1. Détection des cœurs physiques réels
    max_cpus = os.cpu_count() or 1
    workers = max_cpus if (n_jobs == -1 or n_jobs > max_cpus) else max(1, n_jobs)

    # 2. Découpage équilibré de la charge (Chunking)
    base_chunk = n_simulations // workers
    remainder = n_simulations % workers
    chunks = [base_chunk + (1 if i < remainder else 0) for i in range(workers)]
    chunks = [c for c in chunks if c > 0]
    actual_workers = len(chunks)

    # 3. Dérivation formelle des graines indépendantes
    master_ss = np.random.SeedSequence(seed)
    child_seeds = master_ss.spawn(actual_workers)

    # 4. Dispatch selon le backend choisi
    total_f1_wins = 0
    all_turns: list[int] = []

    if backend == "executor":
        with ProcessPoolExecutor(max_workers=actual_workers) as executor:
            futures = [
                executor.submit(_monte_carlo_worker, chunks[i], child_seeds[i], f1, f2)
                for i in range(actual_workers)
            ]
            for f in futures:
                wins, turns = f.result()
                total_f1_wins += wins
                all_turns.extend(turns)

    elif backend == "joblib":
        if Parallel is None:
            raise ImportError("joblib n'est pas installé. Lancez 'pip install joblib'.")

        results = Parallel(n_jobs=actual_workers, backend="loky")(
            delayed(_monte_carlo_worker)(chunks[i], child_seeds[i], f1, f2)
            for i in range(actual_workers)
        )
        for wins, turns in results:
            total_f1_wins += wins
            all_turns.extend(turns)

    # 5. Calcul des grandeurs statistiques (Théorème Central Limite)
    winrate = total_f1_wins / n_simulations
    stderr = math.sqrt(winrate * (1.0 - winrate) / n_simulations)
    ci_95 = (max(0.0, winrate - 1.96 * stderr), min(1.0, winrate + 1.96 * stderr))

    return {
        "winrate": float(winrate),
        "ci_95": (float(ci_95[0]), float(ci_95[1])),
        "turns": all_turns,
        "turns_mean": float(np.mean(all_turns)),
        "n_simulations": n_simulations,
        "workers_used": actual_workers,
        "backend": backend,
    }