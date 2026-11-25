import time
from zarena.parallel_engine import run_parallel_monte_carlo
from zarena.warriors import SaiyanWarrior, Cyborg

if __name__ == "__main__":
    gohan = SaiyanWarrior("Gohan SSJ2", hp=150, ki=100, attack_power=65)
    cell = Cyborg("Perfect Cell", hp=160, power=60, shield=10)

    tailles = [10_000, 100_000, 1_000_000, 10_000_000]

    print(f"{'N':>10} | {'T_seq (s)':>10} | {'T_exec (s)':>10} | {'T_joblib (s)':>12} | {'Speedup Exec':>12}")
    print("-" * 65)

    for N in tailles:
        # Séquentiel (P = 1)
        t0 = time.perf_counter()
        run_parallel_monte_carlo(gohan, cell, n_simulations=N, n_jobs=1, seed=42)
        t_seq = time.perf_counter() - t0

        # Multi-cœurs ProcessPoolExecutor
        t0 = time.perf_counter()
        run_parallel_monte_carlo(gohan, cell, n_simulations=N, n_jobs=-1, seed=42, backend="executor")
        t_exec = time.perf_counter() - t0

        # Multi-cœurs joblib
        t0 = time.perf_counter()
        run_parallel_monte_carlo(gohan, cell, n_simulations=N, n_jobs=-1, seed=42, backend="joblib")
        t_job = time.perf_counter() - t0

        speedup = t_seq / t_exec
        print(f"{N:>10,d} | {t_seq:>10.3f} | {t_exec:>10.3f} | {t_job:>12.3f} | {speedup:>11.2f}x")