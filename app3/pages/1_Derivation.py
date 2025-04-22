import streamlit as st
import requests

st.set_page_config(page_title="Dérivation 🧮", layout="centered")

st.title("Calcul de dérivée symbolique 🧮")

API_BASE_URL = "http://localhost:8000"

expression = st.text_input("Entrez une expression", "x^3")
variable = st.text_input("Variable (ex: x)", "x")

# ✅ Utilisation du cache pour éviter les appels répétés
@st.cache_data
def derive_expression(expression, variable):
    response = requests.post(
        f"{API_BASE_URL}/derive",
        headers={"Content-Type": "application/json"},
        json={"expression": expression, "variable": variable}
    )
    response.raise_for_status()
    return response.json()

# ✅ Affichage du bouton pour vider le cache
if st.button("Vider le cache"):
    derive_expression.clear()
    st.success("Cache vidé avec succès ✅")

# ✅ Appel automatique quand les deux champs sont remplis
if expression.strip() and variable.strip():
    with st.spinner("Calcul en cours..."):
        try:
            result = derive_expression(expression, variable)
            st.success("Calcul réussi ✅")
            st.write(f"**Expression :** {result['expression']}")
            st.write(f"**Dérivée :** {result['derivative']}")
            # ✅ Sauvegarde dans l'historique de session
            if "history_derive" not in st.session_state:
                st.session_state.history_derive = []

            st.session_state.history_derive.append({
                "expression": result['expression'],
                "variable": variable,
                "derivative": result['derivative']
            })

        except requests.RequestException as e:
            st.error(f"Erreur lors de la requête : {e}")
        except Exception as e:
            st.error(f"Erreur : {e}")
else:
    st.info("Veuillez remplir les deux champs pour calculer la dérivée.")
