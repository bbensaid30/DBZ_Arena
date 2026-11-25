import time
from concurrent.futures import ThreadPoolExecutor

# --- CAS 1 : TÂCHE I/O-BOUND (Attente réseau ou disque simulée) ---
def tache_io(id_tache: int) -> None:
    time.sleep(1.0)  # Simule 1 seconde d'attente d'une requête PokéAPI

# --- CAS 2 : TÂCHE CPU-BOUND (Calcul mathématique pur) ---
def tache_cpu(id_tache: int) -> int:
    total = 0
    for i in range(15_000_000):  # Calcul intensif sur le processeur
        total += i
    return total

if __name__ == "__main__":
    print("=== EXPÉRIENCE 1A : TÂCHES I/O-BOUND (Attente) ===")
    t0 = time.perf_counter()
    tache_io(1)
    tache_io(2)
    print(f"I/O Séquentiel (1 fil) : {time.perf_counter() - t0:.2f} s")

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(tache_io, [1, 2]))
    print(f"I/O Multi-threads (2 fils) : {time.perf_counter() - t0:.2f} s")

    print("\n=== EXPÉRIENCE 1B : TÂCHES CPU-BOUND (Calcul Pur) ===")
    t0 = time.perf_counter()
    tache_cpu(1)
    tache_cpu(2)
    print(f"CPU Séquentiel (1 fil) : {time.perf_counter() - t0:.2f} s")

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(tache_cpu, [1, 2]))
    print(f"CPU Multi-threads (2 fils) : {time.perf_counter() - t0:.2f} s")