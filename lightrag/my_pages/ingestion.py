import streamlit as st
from unstructured.partition.auto import partition
from tempfile import NamedTemporaryFile
from db_utils import initialize_db, insert_ingested_file, get_ingested_files

def render():
    st.title("Ingestion de Documents")
    print("Page Ingestion")
    
    # Afficher la liste des fichiers déjà ingérés
    ingested_files = get_ingested_files()
    if ingested_files:
        st.subheader("Fichiers déjà ingérés")
        for file in ingested_files:
            file_name = file['filename']
            st.write(f"- {file['filename']} ({file['page_count']} pages)")
    else:
        st.info("Aucun fichier ingéré pour le moment.")
    
    # Upload de nouveaux fichiers
    # https://docs.streamlit.io/develop/api-reference/text/st.subheader
    st.subheader("Ajouter un nouveau document")
    uploaded_file = st.file_uploader("Choisissez un fichier", type=["txt", "docx", "pptx", "csv", "pdf"])
    
    if uploaded_file is not None:
        # Vérifier si le fichier est déjà ingéré
        if any(file['filename'] == uploaded_file.name for file in ingested_files):
            st.warning(f"Le fichier {uploaded_file.name} a déjà été ingéré.")
            return
            
        # Sauvegarder temporairement le fichier uploadé
        with NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
            
        if st.button("Traiter le document"):
            # Extraction avec unstructured
            try:
                st.info("Traitement du document en cours...")
                elements = partition(filename=temp_file_path)
                total_elements = len(elements)
                
                # Identifier le nombre de pages
                total_pages = len(set(
                    element.metadata.get('page_number') 
                    for element in elements 
                    if isinstance(element.metadata, dict) and 'page_number' in element.metadata
                ))
                
                # Enregistrer dans la base de données
                insert_ingested_file(uploaded_file.name, total_pages)
                
                # Afficher la progression
                progress_bar = st.progress(0)
                progress_text = st.empty()
                
                # Insertion dans le RAG
                for idx, element in enumerate(elements, start=1):
                    text_content = element.text.strip()
                    if text_content:
                        st.session_state.rag.insert(text_content)
                    
                    # Mettre à jour la barre de progression
                    progress_bar.progress(idx / total_elements)
                    progress_text.write(f"Insertion de l'élément {idx} sur {total_elements}")
                
                st.success(f"Document '{uploaded_file.name}' ingéré avec succès! {total_elements} éléments traités.")
                
                # Rafraîchir la page pour voir le nouveau fichier dans la liste
                st.rerun()
                
            except Exception as e:
                st.error(f"Erreur lors du traitement du document : {e}")