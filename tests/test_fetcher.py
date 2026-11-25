import json
from pathlib import Path
import pytest
from zarena.exceptions import DataFetchError
from zarena.io.fetcher import CapsuleCorpFetcher
from zarena.io.loader import (
    get_style_multiplier,
    load_arenas,
    load_style_matrix,
    extract_arena_coordinates,
    build_style_lookup
)


def test_fetcher_cache_miss_queries_api_and_saves_to_disk(
    requests_mock, tmp_path: Path
) -> None:
    api_url = "https://api.capsulecorp.com"
    warrior_payload = {"id": 1, "name": "Son Goku", "hp_base": 120}
    requests_mock.get(f"{api_url}/warriors/1.json", json=warrior_payload)

    fetcher = CapsuleCorpFetcher(base_url=api_url, cache_dir=tmp_path)
    cache_file = tmp_path / "1.json"
    assert cache_file.exists() is False

    data = fetcher.get_warrior_data(1)

    assert data["name"] == "Son Goku"
    assert cache_file.exists() is True
    with open(cache_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == warrior_payload


def test_fetcher_cache_hit_does_not_call_network(
    requests_mock, tmp_path: Path
) -> None:
    api_url = "https://api.capsulecorp.com"
    fetcher = CapsuleCorpFetcher(base_url=api_url, cache_dir=tmp_path)

    cache_file = tmp_path / "1.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({"id": 1, "name": "Goku Local"}, f)

    # Aucun mock déclaré : si le réseau est appelé, le test échoue
    data = fetcher.get_warrior_data(1)
    assert data["name"] == "Goku Local"


def test_fetcher_api_error_without_cache_raises_data_fetch_error(
    requests_mock, tmp_path: Path
) -> None:
    api_url = "https://api.capsulecorp.com"
    requests_mock.get(f"{api_url}/warriors/999.json", status_code=404)

    fetcher = CapsuleCorpFetcher(base_url=api_url, cache_dir=tmp_path)

    with pytest.raises(DataFetchError, match="Échec de l'API"):
        fetcher.get_warrior_data(999)


def test_loader_style_matrix_and_arenas(tmp_path: Path) -> None:
    # 1. Validation de la matrice tabulaire CSV
    csv_file = tmp_path / "styles.csv"
    csv_file.write_text(
        "style,Saiyan,Cyborg\nCorps-a-corps,1.0,0.5\nKi,1.0,0.5\n",
        encoding="utf-8",
    )

    df = load_style_matrix(csv_file)
    assert df.loc["Corps-a-corps", "Cyborg"] == 0.5
    assert get_style_multiplier(df, "Corps-a-corps", "Saiyan") == 1.0

    with pytest.raises(ValueError, match="Style d'attaque non répertorié"):
        get_style_multiplier(df, "Inconnu", "Saiyan")

    with pytest.raises(ValueError, match="Race défensive non répertoriée"):
        get_style_multiplier(df, "Corps-a-corps", "Inconnu")

    # 2. Validation du dictionnaire de recherche rapide (Monte-Carlo)
    lookup = build_style_lookup(df)
    assert lookup["Corps-a-corps"]["Cyborg"] == 0.5
    assert lookup["Ki"]["Saiyan"] == 1.0

    # 3. Validation de la collection GeoJSON et conversion Folium
    arena_feature = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [3.8767, 43.6108]},
        "properties": {"name": "Arène Montpellier"},
    }
    geojson_file = tmp_path / "arenas.geojson"
    geojson_file.write_text(
        json.dumps({
            "type": "FeatureCollection",
            "features": [arena_feature],
        }),
        encoding="utf-8",
    )

    data = load_arenas(geojson_file)
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 1

    # Inversion RFC 7946 [lon, lat] -> Folium (lat, lon)
    lat, lon = extract_arena_coordinates(arena_feature)
    assert (lat, lon) == (43.6108, 3.8767)

    # Rejet d'un schéma invalide
    bad_geojson = tmp_path / "bad.geojson"
    bad_geojson.write_text(
        json.dumps({"type": "InvalidSchema"}), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="GeoJSON"):
        load_arenas(bad_geojson)