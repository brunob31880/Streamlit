import streamlit as st

def render():
    st.title("🧠 Symbolic Math App avec API externe")
    st.header("Bienvenue !")

    st.write("Utilisez le bandeau ci-dessus pour choisir une opération.")
    st.image("./reflexion.png", width=300)
    
    # ✅ Bouton pour réinitialiser l'historique
    if st.button("🗑️ Vider l'historique"):
        st.session_state.history_derive = []
        st.session_state.history_evaluation = []
        st.success("Historique vidé avec succès ✅")

    # ✅ Affichage amélioré de l'historique
    # Historique des dérivées
    if "history_derive" in st.session_state and st.session_state.history_derive:
        st.markdown("### 🧮 Dérivées récentes")
        for item in st.session_state.history_derive[-5:][::-1]:
            with st.container():
                st.write(f"**Expression :** `{item['expression']}`")
                st.write(f"**Variable :** `{item['variable']}`")
                st.write(f"**Dérivée :** `{item['derivative']}`")
                st.markdown("---")
    else:
        st.info("Aucun calcul de dérivée effectué pour le moment.")

    # Historique des évaluations numériques
    if "history_evaluation" in st.session_state and st.session_state.history_evaluation:
        st.markdown("### 🔢 Évaluations numériques récentes")
        for item in st.session_state.history_evaluation[-5:][::-1]:
            with st.container():
                st.write(f"**Expression :** `{item['expression']}`")
                st.write(f"**Valeurs :** `{item['values']}`")
                st.write(f"**Résultat :** `{item['result']}`")
                st.markdown("---")
    else:
        st.info("Aucune évaluation numérique effectuée pour le moment.")