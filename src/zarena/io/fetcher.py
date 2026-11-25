import json
from pathlib import Path
import requests
from zarena.exceptions import DataFetchError


class CapsuleCorpFetcher:
    """Client d'ingestion robuste avec stratégie de mise en cache locale."""

    def __init__(self, base_url: str, cache_dir: str | Path = "data/cache") -> None:
        self.base_url = base_url.rstrip("/")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_remote_warrior(self, warrior_id: int) -> dict:
        url = f"{self.base_url}/warriors/{warrior_id}.json"
        headers = {"User-Agent": "ZArena-Pipeline/1.0"}
        try:
            response = requests.get(url, headers=headers, timeout=5.0)
            if response.status_code != 200:
                raise DataFetchError(
                    f"Échec de l'API : statut HTTP {response.status_code} sur {url}"
                )
            return response.json()
        except requests.RequestException as err:
            raise DataFetchError(
                f"L'API distante est injoignable sur {url} : {err}"
            ) from err

    def get_warrior_data(self, warrior_id: int) -> dict:
        cache_file = self.cache_dir / f"{warrior_id}.json"

        # 1. Stratégie Cache : le fichier est-il présent sur le disque ?
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)

        # 2. Absence de cache : interrogation réseau distante
        data = self.fetch_remote_warrior(warrior_id)

        # 3. Écriture du cache local
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return data