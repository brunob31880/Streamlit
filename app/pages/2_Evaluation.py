import streamlit as st
import requests
import json

st.set_page_config(page_title="Évaluation numérique 🔢", layout="centered")

st.title("Évaluation numérique 🔢")

API_BASE_URL = "http://localhost:8000"

expression = st.text_input("Entrez une expression", "x^3")
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
