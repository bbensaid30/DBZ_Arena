import os
import multiprocessing
import psutil

nb_logiques = os.cpu_count()
print(f"Cœurs logiques détectés par l'OS : {nb_logiques}")

try:
    nb_physiques = psutil.cpu_count(logical=False)
    print(f"Coeurs physiques réels            : {nb_physiques}")
except ImportError:
    print("(Installez psutil via 'pip install psutil' pour distinguer coeurs physiques et logiques)")