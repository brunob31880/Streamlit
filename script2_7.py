import streamlit as st

st.set_page_config(page_title="Interaction simple 🚀", layout="wide")

st.title("Interaction simple 🚀")

# Champ de saisie
name = st.text_input("Quel est votre nom ?", key="name_input")

# Initialiser une variable dans la session state pour le message
if "message" not in st.session_state:
    st.session_state.message = ""

# Définir la fonction callback
def dire_bonjour():
    st.session_state.message = f"Bonjour, {st.session_state.name_input} !"

# Bouton avec callback
st.button("Dire bonjour", on_click=dire_bonjour)

# Afficher le message s'il existe
if st.session_state.message:
    st.write(st.session_state.message)
