import streamlit as st

st.title("Interaction simple 🚀")

name = st.text_input("Quel est votre nom ?")

if st.button("Dire bonjour"):
    st.write(f"Bonjour, {name} !")
