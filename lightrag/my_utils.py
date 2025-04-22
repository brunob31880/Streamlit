import asyncio
import nest_asyncio
import os
import requests
import streamlit as st
from lightrag import LightRAG
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import TokenTracker

nest_asyncio.apply()

WORKING_DIR = "./working_dir"
os.makedirs(WORKING_DIR, exist_ok=True)

# Helper to fetch available models from Ollama
@st.cache_data
def fetch_ollama_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        return [model["name"] for model in models]
    except Exception as e:
        st.error(f"Error fetching models: {e}")
        return []

# Initialize RAG with dynamic settings
@st.cache_resource(show_spinner=False)
def initialize_rag(llm_model_name, embedding_model_name):
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name=llm_model_name,
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        llm_model_kwargs={
            "host": "http://localhost:11434",
            "options": {"num_ctx": 32768},
        },
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model=embedding_model_name, host="http://localhost:11434"
            ),
        ),
    )
    asyncio.run(rag.initialize_storages())
    asyncio.run(initialize_pipeline_status())
    return rag

def initialize_session_state():
    """Initialise les variables dans session_state."""
    from db_utils import initialize_db, get_settings
    
    # Initialiser la base de données
    initialize_db()
    
    # Récupérer les paramètres sauvegardés
    saved_settings = get_settings()
    
    # Initialiser les modèles dans session_state
    if saved_settings:
        # Utiliser les modèles sauvegardés en DB
        st.session_state.llm_model = saved_settings["llm_model"]
        st.session_state.embedding_model = saved_settings["embedding_model"]
    else:
        # Valeurs par défaut si aucun paramètre n'est trouvé
        models = fetch_ollama_models()
        default_model = models[0] if models else "llama3.1"
        
        if "llm_model" not in st.session_state:
            st.session_state.llm_model = default_model
        
        if "embedding_model" not in st.session_state:
            st.session_state.embedding_model = default_model
    
    # Initialiser le token tracker
    if "token_tracker" not in st.session_state:
        st.session_state.token_tracker = TokenTracker()
    
    # Initialiser l'objet RAG s'il n'existe pas
    if "rag" not in st.session_state:
        st.session_state.rag = initialize_rag(
            st.session_state.llm_model, 
            st.session_state.embedding_model
        )
