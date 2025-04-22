import streamlit as st

def render():
    st.title("LightRAG - Assistant documentaire")
    print("Page Main")
    st.markdown("""
    ## Bienvenue sur votre assistant documentaire intelligent
    
    Cette application vous permet d'analyser et d'interagir avec vos documents grâce à la technologie RAG (Retrieval Augmented Generation).
    
    ### Comment utiliser cette application :
    
    1. **Ingestion** : Commencez par télécharger vos documents dans la page d'ingestion.
    2. **Chat** : Posez des questions sur vos documents dans la page de chat.
    3. **Paramètres** : Configurez les modèles LLM et d'embedding dans la page des paramètres.
    
    ### Fonctionnalités disponibles :
    
    - Support de plusieurs formats de documents (PDF, DOCX, TXT, etc.)
    - Différents modes de requête (naïve, local, global, hybrid)
    - Réponses en streaming
    - Suivi des documents ingérés et des conversations
    """)
    
    # Boutons pour naviguer directement vers les pages principales
    col1, col2 = st.columns(2)
    
    with col1:
        # https://docs.streamlit.io/develop/api-reference/widgets/st.button
        if st.button("Ingérer des documents",icon="🗂️",use_container_width=True):
            st.session_state.page = "Ingestion"
            st.rerun()
    
    with col2:
        if st.button("💬 Discuter avec mes documents",use_container_width=True):
            st.session_state.page = "Chat"
            st.rerun()
    
    # Afficher des statistiques si disponibles
    try:
        from db_utils import get_ingested_files, get_query_count
        # ligne séparatrice
        st.markdown("---")
        st.subheader("Statistiques")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ingested_files = get_ingested_files()
            # https://docs.streamlit.io/develop/api-reference/data/st.metric
            st.metric("Documents ingérés", len(ingested_files))
        
        with col2:
            query_count = get_query_count()
            st.metric("Questions posées", query_count)
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des statistiques: {e}")