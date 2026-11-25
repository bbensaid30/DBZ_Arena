import streamlit as st
from streamlit_folium import st_folium

from app.charts import plot_fighters_radar, plot_turns_distribution
from app.map_utils import build_arenas_map
from zarena.io.loader import load_arenas
from zarena.parallel_engine import run_parallel_monte_carlo
from zarena.warriors import ArenaFighter, Cyborg, SaiyanWarrior

st.set_page_config(page_title="Z-Arena — Simulateur Décisionnel", layout="wide")


def get_fighters_roster() -> dict[str, ArenaFighter]:
    """Construit le catalogue des combattants disponibles."""
    return {
        "Son Goku (SSJ)": SaiyanWarrior("Son Goku", hp=140, ki=100, attack_power=60, rage_multiplier=1.5),
        "Vegeta (Prince)": SaiyanWarrior("Vegeta", hp=135, ki=100, attack_power=62, rage_multiplier=1.6),
        "Son Gohan (SSJ2)": SaiyanWarrior("Son Gohan", hp=150, ki=100, attack_power=65, rage_multiplier=1.8),
        "C-17 (Cyborg)": Cyborg("C-17", hp=160, power=58, shield=12),
    }


@st.cache_data
def cached_load_arenas() -> dict:
    return load_arenas("data/arenas_dbz.geojson")


@st.cache_data(show_spinner="Exécution des simulations Monte-Carlo multi-cœurs...")
def cached_simulation(f1_name: str, f2_name: str, n_sims: int) -> dict:
    roster = get_fighters_roster()
    f1 = roster[f1_name]
    f2 = roster[f2_name]

    # backend="joblib" évite BrokenProcessPool sous Streamlit (macOS/Windows)
    return run_parallel_monte_carlo(
        f1, f2, n_simulations=n_sims, n_jobs=-1, seed=42, backend="joblib"
    )


# --- INTERFACE PRINCIPALE ---
st.title("Z-Arena : Moteur Stochastique & Analyse Décisionnelle")

roster = get_fighters_roster()
fighter_names = list(roster.keys())

with st.sidebar:
    st.header("Configuration de l'Arène")
    f1_choice = st.selectbox("Combattant 1 (Coin Bleu)", fighter_names, index=2)
    f2_choice = st.selectbox("Combattant 2 (Coin Rouge)", fighter_names, index=3)
    n_sims = st.slider(
        "Volume Monte-Carlo (N)", min_value=500, max_value=20_000, value=5_000, step=500
    )

tab_duel, tab_map = st.tabs(
    ["Simulateur de Duel & Télémétrie", "Cartographie des Arènes"]
)

# --- ONGLET 1 : SIMULATEUR ---
with tab_duel:
    if f1_choice == f2_choice:
        st.warning("Veuillez sélectionner deux combattants distincts dans le menu latéral.")
    else:
        res = cached_simulation(f1_choice, f2_choice, n_sims)
        winrate_pct = res["winrate"] * 100
        ci_low, ci_high = res["ci_95"][0] * 100, res["ci_95"][1] * 100

        c1, c2, c3 = st.columns(3)
        c1.metric(f"Taux de victoire ({f1_choice})", f"{winrate_pct:.1f} %")
        c2.metric("Intervalle de Confiance (95 %)", f"[{ci_low:.1f} % ; {ci_high:.1f} %]")
        c3.metric("Durée moyenne", f"{res['turns_mean']:.1f} tours")

        st.divider()

        col_left, col_right = st.columns(2)
        with col_left:
            f1_obj, f2_obj = roster[f1_choice], roster[f2_choice]
            stats_1 = {"PV Max": f1_obj.max_hp, "Attaque": f1_obj.execute_attack()}
            stats_2 = {"PV Max": f2_obj.max_hp, "Attaque": f2_obj.execute_attack()}
            fig_radar = plot_fighters_radar(stats_1, stats_2, f1_choice, f2_choice)
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_right:
            fig_hist = plot_turns_distribution(
                res["turns"], f1_choice, f2_choice
            )
            st.plotly_chart(fig_hist, use_container_width=True)

# --- ONGLET 2 : CARTE ---
with tab_map:
    st.subheader("Répartition Géographique des Arènes de Tournoi")
    min_cap = st.slider(
        "Capacité minimale d'accueil (spectateurs)", 0, 50_000, 0, step=5_000
    )
    arenas_geojson = cached_load_arenas()
    folium_map = build_arenas_map(arenas_geojson, min_capacity=min_cap)
    st_folium(folium_map, width=1000, height=500)