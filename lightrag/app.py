import streamlit as st
from my_utils import initialize_session_state
import my_pages.main as main_page
import my_pages.settings as settings_page
import my_pages.ingestion as ingestion_page
import my_pages.chat as chat_page
from lightrag.utils import setup_logger

st.set_page_config(page_title="LightRAG 🚀", layout="wide")
setup_logger("lightrag", level="INFO")


# Liste des pages disponibles
pages = ["Accueil", "Ingestion", "Chat", "Paramètres"]

# Initialisation 
if "page" not in st.session_state:
    # page courante si elle n'existe pas dans session state
    st.session_state.page = "Accueil"
    # Initialisation de l'état de session
    initialize_session_state()


page = st.sidebar.radio(
    "Aller à",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = page

print(f"Page={page} {st.session_state.page}")

# et ensuite on rend la page choisie
if page=="Accueil":
    main_page.render()
elif page=="Ingestion":
    ingestion_page.render()
elif page=="Chat":
    chat_page.render()
else:
    settings_page.render()
