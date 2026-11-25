# src/zarena/io/loader.py
import json
from pathlib import Path
import pandas as pd

def load_style_matrix(filepath: str | Path = "data/styles_combat.csv") -> pd.DataFrame:
    """Charge et valide la matrice des multiplicateurs de style de combat."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier de styles de combat introuvable : {path}")

    df = pd.read_csv(path, index_col=0)
    return df.astype(float)


def get_style_multiplier(
    df: pd.DataFrame, attack_style: str, defender_race: str
) -> float:
    """Extrait le coefficient multiplicateur à l'intersection du style et de la race."""
    if attack_style not in df.index:
        raise ValueError(f"Style d'attaque non répertorié : {attack_style}")
    if defender_race not in df.columns:
        raise ValueError(f"Race défensive non répertoriée : {defender_race}")

    return float(df.loc[attack_style, defender_race])


def build_style_lookup(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Convertit la table Pandas en dictionnaire imbriqué optimisé pour Monte-Carlo."""
    return df.to_dict(orient="index")


def load_arenas(filepath: str | Path = "data/arenas_dbz.geojson") -> dict:
    """Charge et valide la structure formelle d'un fichier GeoJSON d'arènes."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier cartographique introuvable : {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if (
        data.get("type") != "FeatureCollection"
        or "features" not in data
        or not isinstance(data["features"], list)
    ):
        raise ValueError(
            "Le fichier ne respecte pas le schéma GeoJSON FeatureCollection."
        )

    return data


def extract_arena_coordinates(feature: dict) -> tuple[float, float]:
    """Extrait la position géographique au format attendu par Folium (latitude, longitude)."""
    coordinates = feature["geometry"]["coordinates"]
    lon, lat = coordinates[0], coordinates[1]
    return float(lat), float(lon)