import streamlit as st

st.set_page_config(page_title="Calculatrice à touches", layout="centered")

st.title("🧮 Calculatrice à touches avec icônes")

# CSS pour uniformiser les boutons
st.markdown("""
    <style>
    div.stButton > button {
        height: 60px;
        width: 60px;
        font-size: 24px;
        margin: 3px;
    }
    
    </style>
    """, unsafe_allow_html=True)


# État de l'expression en session_state pour la persistance
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Fonction pour ajouter un caractère à l'expression
# Fonctions de calcul
def append_to_expression(value):
    st.session_state.expression += str(value)

# Fonction pour évaluer l'expression
def evaluate_expression():
    try:
        result = eval(st.session_state.expression)
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Erreur"

# Fonction pour tout effacer
def clear_expression():
    st.session_state.expression = ""

# Affichage de l'expression actuelle
st.text_input("Expression", value=st.session_state.expression, key="display", disabled=True)

# Définition des boutons avec affichage et valeur logique
buttons = [
    [("7️⃣", "7"), ("8️⃣", "8"), ("9️⃣", "9"), ("➗", "/")],
    [("4️⃣", "4"), ("5️⃣", "5"), ("6️⃣", "6"), ("✖️", "*")],
    [("1️⃣", "1"), ("2️⃣", "2"), ("3️⃣", "3"), ("➖", "-")],
    [("0️⃣", "0"), (".", "."), ("🟰", "="), ("➕", "+")],
]
# Mapping des labels vers les vrais opérateurs pour évaluation
operators = {"➗": "/", "✖️": "*", "➖": "-", "➕": "+"}

for row in buttons:
    cols = st.columns(len(row))
    for idx, (display, value) in enumerate(row):
        if cols[idx].button(display):
            if value == "=":
                evaluate_expression()
            else:
                append_to_expression(value)

# Bouton pour réinitialiser
if st.button("🧹 Effacer", key="effacer"):
    clear_expression()
