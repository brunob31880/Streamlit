import streamlit as st
import requests
import json

st.set_page_config(page_title="Évaluation numérique 🔢", layout="centered")

st.title("Évaluation numérique 🔢")

API_BASE_URL = "http://localhost:8000"

expression = st.text_input("Entrez une expression", "x^3")
values_str = st.text_input('Valeurs (ex: {"x": 2})', '{"x": 2}')

@st.cache_data
def evaluate_expression(expression, values_json_str):
    values = json.loads(values_json_str)
    response = requests.post(
        f"{API_BASE_URL}/evaluate",
        headers={"Content-Type": "application/json"},
        json={"expression": expression, "values": values}
    )
    response.raise_for_status()
    return response.json()

if expression and values_str:
    try:
        result = evaluate_expression(expression, values_str)

        st.success("Évaluation réussie ✅")
        st.write(f"**Expression :** {result['expression']}")
        st.write(f"**Valeurs :** {result['values']}")
        st.write(f"**Résultat :** {result['result']}")
        # ✅ Sauvegarde dans l'historique de session
        if "history_evaluation" not in st.session_state:
            st.session_state.history_evaluation = []

        st.session_state.history_evaluation.append({
            "expression": result['expression'],
            "values": result['values'],
            "result": result['result']
        })

    except json.JSONDecodeError:
        st.error("Erreur de format JSON dans les valeurs.")
    except requests.RequestException as e:
        st.error(f"Erreur lors de la requête : {e}")
    except Exception as e:
        st.error(f"Erreur : {e}")
