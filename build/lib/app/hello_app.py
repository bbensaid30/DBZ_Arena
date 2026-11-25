import streamlit as st

# 1. Configuration globale de la page (toujours en premier !)
st.set_page_config(
    page_title="Z-Arena — Tableau de Bord",
    layout="wide",
)

# 2. En-tête principal
st.title("Simulateur Stochastique Z-Arena")
st.markdown("Interface décisionnelle d'analyse des affrontements du *Cell Game*.")

# 3. Panneau latéral de configuration
with st.sidebar:
    st.header("Paramètres du Duel")
    n_sims = st.slider("Nombre de simulations", min_value=100, max_value=10_000, value=1_000, step=100)
    st.info(f"Configuration prête pour {n_sims} duels.")

# 4. Affichage en colonnes et indicateurs KPI
col1, col2, col3 = st.columns(3)
col1.metric(label="Combattant 1", value="Son Gohan SSJ2", delta="Attaque +25%")
col2.metric(label="Combattant 2", value="Perfect Cell", delta="Bouclier 10")
col3.metric(label="Volume Monte-Carlo", value=f"{n_sims:,} duels")