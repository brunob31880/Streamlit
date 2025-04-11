# On importe la bibliothèque Streamlit
import streamlit as st

# On configure la page web Streamlit :
# - Titre de l'onglet du navigateur : "Interaction simple 🚀"
# - Layout 'wide' pour utiliser toute la largeur de la fenêtre
st.set_page_config(page_title="Interaction simple 🚀", layout="wide")

# On affiche un titre principal en haut de la page
st.title("Interaction simple 🚀")

# On crée un champ de saisie pour que l'utilisateur entre son nom
# La valeur saisie est stockée dans la variable 'name'
name = st.text_input("Quel est votre nom ?")

# On crée un bouton intitulé "Dire bonjour"
# Si l'utilisateur clique dessus, le bloc suivant s'exécute
if st.button("Dire bonjour"):
    # Quand le bouton est cliqué, on affiche un message personnalisé
    # avec le nom que l'utilisateur a saisi dans le champ 'name'
    st.write(f"Bonjour, {name} !")
