import streamlit as st
import my_pages.accueil as accueil
import my_pages.derive as derive
import my_pages.evaluate as evaluate

st.set_page_config(page_title="🧠 Symbolic Math App", layout="wide")

# ✅ Bandeau de navigation en haut
menu = st.radio(
    "Navigation",
    ["🏠 Accueil", "🧮 Dérivation", "🔢 Évaluation numérique"],
    horizontal=True,
    label_visibility="collapsed",
)

# 🏠 Page d'accueil
if menu == "🏠 Accueil":
    accueil.render()
# 🧮 Page dérivation
elif menu == "🧮 Dérivation":
    derive.render()
# 🔢 Page évaluation numérique
elif menu == "🔢 Évaluation numérique":
    evaluate.render()
