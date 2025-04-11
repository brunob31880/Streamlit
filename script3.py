import streamlit as st

st.title("Choix de l'opération")

option = st.selectbox(
    "Que voulez-vous faire ?",
    ("Addition", "Soustraction", "Multiplication", "Division")
)

a = st.number_input("Entrez le premier nombre", value=0)
b = st.number_input("Entrez le second nombre", value=0)

if st.button("Calculer"):
    if option == "Addition":
        st.write(f"Résultat : {a + b}")
    elif option == "Soustraction":
        st.write(f"Résultat : {a - b}")
    elif option == "Multiplication":
        st.write(f"Résultat : {a * b}")
    elif option == "Division":
        if b != 0:
            st.write(f"Résultat : {a / b}")
        else:
            st.error("Erreur : division par zéro.")
