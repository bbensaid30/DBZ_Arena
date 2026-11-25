import folium
from zarena.io.loader import extract_arena_coordinates

ENV_COLORS: dict[str, str] = {
    "Plaine": "green",
    "Sanctuaire": "blue",
    "Désert": "orange",
}


def build_arenas_map(geojson_data: dict, min_capacity: int = 0) -> folium.Map:
    """Construit une carte Folium interactive des arènes filtrées par capacité."""
    carte = folium.Map(location=[43.6, 5.0], zoom_start=4, tiles="OpenStreetMap")

    for feature in geojson_data["features"]:
        props = feature["properties"]
        capacity = props.get("capacity", 0)

        if capacity >= min_capacity:
            lat, lon = extract_arena_coordinates(feature)
            env = props.get("environment", "Inconnu")
            color = ENV_COLORS.get(env, "red")

            texte_popup = (
                f"{props['name']} — "
                f"Environnement : {env} — "
                f"Capacité : {capacity} spectateurs"
            )

            folium.Marker(
                location=[lat, lon],
                popup=texte_popup,
                tooltip=f"{props['name']} ({env})",
                icon=folium.Icon(color=color, icon="star"),
            ).add_to(carte)

    return carte

if __name__ == "__main__":
    from zarena.io.loader import load_arenas

    donnees_geojson = load_arenas("data/arenas_dbz.geojson")
    carte_test = build_arenas_map(donnees_geojson, min_capacity=0)
    carte_test.save("test_carte.html")
    print("Carte générée avec succès : ouvrez 'test_carte.html' dans votre navigateur.")