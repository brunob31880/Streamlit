import streamlit as st

st.title("Hello Streamlit 👋")

a=st.text_input("Quel est votre nom ?")

print(a)

st.write(f"Bonjour, {a} !")