import multiprocessing

VALEUR_GLOBALE = 100

def modifier_memoire():
    global VALEUR_GLOBALE
    VALEUR_GLOBALE = 999  # Tentative de modification dans le processus fils
    print(f"[Worker Fils] VALEUR_GLOBALE = {VALEUR_GLOBALE}")

if __name__ == "__main__":
    p = multiprocessing.Process(target=modifier_memoire)
    p.start()
    p.join()  # Attend la fin du worker

    print(f"[Processus Père] VALEUR_GLOBALE = {VALEUR_GLOBALE}")
    assert VALEUR_GLOBALE == 100, "Erreur : la mémoire n'est pas isolée !"