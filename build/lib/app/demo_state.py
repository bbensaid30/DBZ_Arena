import streamlit as st

st.title("Démonstration : Variable Locale vs Session State")

# --- APPROCHE 1 : VARIABLE PYTHON CLASSIQUE (ÉCHEC) ---
compteur_naif = 0
if st.button("Incrémenter le compteur naïf"):
    compteur_naif += 1
st.write(f"Compteur naïf (remis à zéro à chaque rerun) : **{compteur_naif}**")

st.divider()

# --- APPROCHE 2 : PERSISTANCE VIA st.session_state (SUCCÈS) ---
# 1. Initialisation uniquement lors de la toute première visite
if "compteur_persistant" not in st.session_state:
    st.session_state["compteur_persistant"] = 0

# 2. Modification de l'état lors du clic
if st.button("Incrémenter le compteur persistant"):
    st.session_state["compteur_persistant"] += 1

st.write(f"Compteur persistant (conservé en mémoire) : **{st.session_state['compteur_persistant']}**")