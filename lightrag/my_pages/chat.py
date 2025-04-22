import streamlit as st
import asyncio
import inspect
from lightrag import QueryParam
from db_utils import insert_query_and_answer, get_ingested_files

# Fonction pour streamer les réponses
async def print_stream(response_stream):
    output = ""
    async for chunk in response_stream:
        output += chunk
        yield output

def render():
    st.title("Chat avec vos documents")
    print("Page Chat")
    # Vérifier si des documents ont été ingérés
    ingested_files = get_ingested_files()
    if not ingested_files:
        st.warning("Aucun document n'a été ingéré. Veuillez d'abord ajouter des documents dans la page d'ingestion.")
        return
    
    # Initialiser l'historique du chat s'il n'existe pas
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Afficher l'historique du chat
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]  
        # https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
        if role == "user":
            st.chat_message("user").write(content)
        else:
            st.chat_message("assistant").write(content)
    
    # Options de requête
    with st.sidebar:
        st.subheader("Options de requête")
        mode = st.selectbox(
            "Mode de recherche:",
            ["naive", "local", "global", "hybrid"],
            help="naive: sans RAG, local: recherche locale, global: recherche globale, hybrid: combinaison"
        )
        use_stream = st.checkbox("Réponse en streaming", value=True)
        
    # Input pour la question
    question = st.chat_input("Posez votre question sur les documents...")
    
    if question:
        # Afficher la question de l'utilisateur
        st.chat_message("user").write(question)
        
        # Ajouter à l'historique
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        # Préparer l'affichage de la réponse
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Paramètres de la requête
            param = QueryParam(mode=mode,stream=use_stream)
            
            # Obtenir la réponse
            # A voir https://github.com/HKUDS/LightRAG Conversation History Support possibilité de gerer l'historique
            response = st.session_state.rag.query(question, param=param)
            
            # Gérer la réponse (streaming ou non)
            if use_stream and inspect.isasyncgen(response):
                # Réponse en streaming
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                final_response = ""
                
                async def run_stream():
                    nonlocal final_response
                    async for text in print_stream(response):
                        response_placeholder.markdown(text)
                        final_response = text
                
                loop.run_until_complete(run_stream())
                loop.close()
                
                # Stocker la réponse finale pour l'historique
                response_text = final_response
            else:
                # Réponse non streaming
                response_text = response
                response_placeholder.markdown(response_text)
            
            # Ajouter à l'historique
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            
            # Enregistrer dans la base de données
            insert_query_and_answer(
                question, 
                response_text, 
                st.session_state.llm_model, 
                st.session_state.embedding_model
            )
            
        # Afficher l'utilisation des tokens (optionnel)
        if hasattr(st.session_state, 'token_tracker'):
            st.sidebar.markdown("### Utilisation des tokens")
            st.sidebar.write(st.session_state.token_tracker.get_usage())