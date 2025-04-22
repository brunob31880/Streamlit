import streamlit as st

st.set_page_config(page_title="🧠 Symbolic Math App", layout="centered")

st.title("🧠 Symbolic Math App avec API externe")
st.header("Bienvenue !")

st.write("Utilisez la barre de navigation à gauche pour choisir une opération.")
st.image("./reflexion.png", width=300)

st.subheader("📝 Historique des derniers calculs")

# Historique des dérivées
if "history_derive" in st.session_state and st.session_state.history_derive:
    st.markdown("### Dérivées récentes")
    for item in st.session_state.history_derive[-5:][::-1]:  # Les 5 derniers, plus récents d'abord
        st.write(f"**Expression :** {item['expression']} → **Dérivée :** {item['derivative']} (variable : {item['variable']})")
else:
    st.write("Aucun calcul de dérivée effectué pour le moment.")

# Historique des évaluations numériques
if "history_evaluation" in st.session_state and st.session_state.history_evaluation:
    st.markdown("### Évaluations numériques récentes")
    for item in st.session_state.history_evaluation[-5:][::-1]:
        st.write(f"**Expression :** {item['expression']} avec **Valeurs :** {item['values']} → **Résultat :** {item['result']}")
else:
    st.write("Aucune évaluation numérique effectuée pour le moment.")
