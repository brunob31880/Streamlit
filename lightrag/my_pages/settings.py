import streamlit as st
from my_utils import fetch_ollama_models
from db_utils import save_settings, get_settings

def render():
    st.title("Paramètres")
    print("Page Settings")
    # Récupérer les modèles disponibles
    models = fetch_ollama_models()
    
    # Récupérer les paramètres sauvegardés
    saved_settings = get_settings()
    
    if models:
        # Déterminer les valeurs par défaut
        default_llm = st.session_state.get("llm_model", "")
        default_embedding = st.session_state.get("embedding_model", "")
        
        # Si des paramètres sont sauvegardés en DB, les utiliser
        if saved_settings:
            default_llm = saved_settings["llm_model"]
            default_embedding = saved_settings["embedding_model"]
            st.info(f"Dernière mise à jour des paramètres: {saved_settings['last_updated']}")
        
        # Sélection des modèles
        selected_llm = st.selectbox(
            "Sélectionner un modèle LLM",
            models,
            index=models.index(default_llm) if default_llm in models else 0
        )
        
        selected_embedding = st.selectbox(
            "Sélectionner un modèle d'embedding",
            models,
            index=models.index(default_embedding) if default_embedding in models else 0
        )
        
        # Bouton pour sauvegarder les paramètres
        if st.button("Enregistrer les paramètres", type="primary"):
            # Sauvegarder dans la session state
            st.session_state.llm_model = selected_llm
            st.session_state.embedding_model = selected_embedding
            
            # Sauvegarder dans la base de données
            if save_settings(selected_llm, selected_embedding):
                st.success("Paramètres sauvegardés avec succès dans la base de données!")
                
                # Si les modèles ont changé, afficher un message d'avertissement
                if (default_llm != selected_llm or default_embedding != selected_embedding) and hasattr(st.session_state, "rag"):
                    st.warning("Attention: les modèles ont été modifiés. L'objet RAG sera recréé avec les nouveaux paramètres à la prochaine utilisation.")
            else:
                st.error("Erreur lors de la sauvegarde des paramètres.")
                
    else:
        st.warning("Aucun modèle trouvé. Assurez-vous qu'Ollama est en cours d'exécution.")