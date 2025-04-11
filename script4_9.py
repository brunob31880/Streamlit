import streamlit as st

st.set_page_config(page_title="Calculatrice à touches", layout="centered")

st.title("🧮 Calculatrice à touches avec icônes")

# CSS pour uniformiser les boutons
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

# État de l'expression en session_state pour la persistance
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Fonction pour ajouter un caractère à l'expression
def append_to_expression(char):
    st.session_state.expression += str(char)

# Fonction pour évaluer l'expression
def evaluate_expression():
    print(st.session_state.expression)
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

# Créer la grille de boutons avec des icônes
# Définition des boutons avec affichage et valeur logique
buttons = [
    [("7️⃣", "7"), ("8️⃣", "8"), ("9️⃣", "9"), ("➗", "/")],
    [("4️⃣", "4"), ("5️⃣", "5"), ("6️⃣", "6"), ("✖️", "*")],
    [("1️⃣", "1"), ("2️⃣", "2"), ("3️⃣", "3"), ("➖", "-")],
    [("0️⃣", "0"), (".", "."), ("🟰", "="), ("➕", "+")],
]

# Mapping des labels vers les vrais opérateurs pour évaluation
operators = {"➗": "/", "✖️": "*", "➖": "-", "➕": "+"}


def calculus(val):
    if val == "=":
        evaluate_expression()
    else:
        append_to_expression(operators.get(val, val))

for row in buttons:
    cols = st.columns(len(row))
    for idx, (display, value) in enumerate(row):
        tap=cols[idx].button(display, on_click=calculus,args=(value, ))

# Bouton pour réinitialiser
clear=st.button("🧹 Effacer", key="effacer", on_click=clear_expression)