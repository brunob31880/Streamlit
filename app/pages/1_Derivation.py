import streamlit as st
import requests

st.set_page_config(page_title="Dérivation 🧮", layout="centered")

st.title("Calcul de dérivée symbolique 🧮")

API_BASE_URL = "http://localhost:8000"

expression = st.text_input("Entrez une expression", "x^3")
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
