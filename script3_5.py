import streamlit as st

# Titre principal de la page
st.title("Calculatrice simple avec Sidebar 🧮")

# Dans la sidebar, on place le choix de l'opération avec un Radio Button
operation = st.sidebar.radio(
    "Que voulez-vous faire ?",
    ("Addition", "Soustraction", "Multiplication", "Division")
)

# Saisie des deux nombres dans la page principale
a = st.number_input("Entrez le premier nombre", value=0)
b = st.number_input("Entrez le second nombre", value=0)

# Bouton pour déclencher le calcul
if st.button("Calculer"):
    # Selon l'opération choisie, on effectue le calcul
    if operation == "Addition":
        st.write(f"Résultat : {a + b}")
    elif operation == "Soustraction":
        st.write(f"Résultat : {a - b}")
    elif operation == "Multiplication":
        st.write(f"Résultat : {a * b}")
    elif operation == "Division":
        if b != 0:
            st.write(f"Résultat : {a / b}")
        else:
            st.error("Erreur : division par zéro.")
