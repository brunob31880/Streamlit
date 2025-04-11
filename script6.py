import streamlit as st
import requests
import json

st.title("🧠 Symbolic Math App avec API externe")

# Sidebar de navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Dériver une expression", "Évaluer numériquement"])

# API endpoints
API_BASE_URL = "http://localhost:8000"

# Page d'accueil
if page == "Accueil":
    st.header("Bienvenue !")
    st.write("Utilisez le menu de gauche pour choisir une opération.")

# Page de dérivation
elif page == "Dériver une expression":
    st.header("Calcul de dérivée symbolique 🧮")

    expression = st.text_input("Entrez une expression", "")
    variable = st.text_input("Variable (ex: x)", "x")

    if st.button("Dériver"):
        with st.spinner("Calcul en cours..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/derive",
                    headers={"Content-Type": "application/json"},
                    json={"expression": expression, "variable": variable}
                )
                response.raise_for_status()
                result = response.json()

                st.success("Calcul réussi ✅")
                st.write(f"**Expression :** {result['expression']}")
                st.write(f"**Dérivée :** {result['derivative']}")
            except requests.RequestException as e:
                st.error(f"Erreur lors de la requête : {e}")
            except Exception as e:
                st.error(f"Erreur : {e}")

# Page d'évaluation numérique
elif page == "Évaluer numériquement":
    st.header("Évaluation numérique 🔢")

    expression = st.text_input("Entrez une expression", "")
    values_str = st.text_input('Valeurs (ex: {"x": 2})', '{"x": 2}')

    if st.button("Évaluer"):
        with st.spinner("Évaluation en cours..."):
            try:
                values = json.loads(values_str)
                response = requests.post(
                    f"{API_BASE_URL}/evaluate",
                    headers={"Content-Type": "application/json"},
                    json={"expression": expression, "values": values}
                )
                response.raise_for_status()
                result = response.json()

                st.success("Évaluation réussie ✅")
                st.write(f"**Expression :** {result['expression']}")
                st.write(f"**Valeurs :** {result['values']}")
                st.write(f"**Résultat :** {result['result']}")
            except json.JSONDecodeError:
                st.error("Erreur de format JSON dans les valeurs.")
            except requests.RequestException as e:
                st.error(f"Erreur lors de la requête : {e}")
            except Exception as e:
                st.error(f"Erreur : {e}")
