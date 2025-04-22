import sqlite3
import os
from datetime import datetime

DB_PATH = "lightrag.db"

def initialize_db():
    """Initialise la base de données en créant les tables nécessaires si elles n'existent pas."""
    print("Initialize DB")
    if not os.path.exists(DB_PATH):
        # La base de données n'existe pas, donc on la crée
        with open(DB_PATH, "w"):
            pass  # Crée le fichier vide si nécessaire

        execute_query("""
            CREATE TABLE IF NOT EXISTS ingested_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                ingestion_date TEXT NOT NULL,
                page_count INTEGER
            );
        """, commit=True)

        execute_query("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                query_date TEXT NOT NULL,
                model_used TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                file_id INTEGER,
                FOREIGN KEY (file_id) REFERENCES ingested_files(id)
            );
        """, commit=True)

        execute_query("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                answer TEXT NOT NULL,
                answer_date TEXT NOT NULL,
                query_id INTEGER,
                FOREIGN KEY (query_id) REFERENCES queries(id)
            );
        """, commit=True)

        # Nouvelle table pour les paramètres
        execute_query("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                llm_model TEXT NOT NULL,
                embedding_model TEXT NOT NULL,
                last_updated TEXT NOT NULL
            );
        """, commit=True)
    else:
        # Vérifier si la table settings existe déjà, sinon la créer
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings';")
        if not cursor.fetchone():
            execute_query("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    llm_model TEXT NOT NULL,
                    embedding_model TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                );
            """, commit=True)
        conn.close()


def get_query_count():
    """Retourne le nombre total de questions posées."""
    conn = sqlite3.connect('lightrag.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM queries")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_db_connection():
    """Établit une connexion à la base de données SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    return conn

def execute_query(query, params=(), commit=False):
    """Exécute une requête SQL avec ou sans commit."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    if commit:
        conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

def insert_ingested_file(filename, page_count=None):
    """Insère un enregistrement de fichier ingéré dans la base de données."""
    ingestion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query("""
        INSERT INTO ingested_files (filename, ingestion_date, page_count)
        VALUES (?, ?, ?)
    """, (filename, ingestion_date, page_count), commit=True)

def insert_query_and_answer(question, answer, model_used, embedding_model, file_id=None):
    """Insère une question et sa réponse associée dans la base de données dans une seule transaction."""
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Démarrer une transaction explicite
        cursor.execute("BEGIN")

        # Insérer la question
        query_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO queries (question, query_date, model_used, embedding_model, file_id)
            VALUES (?, ?, ?, ?, ?)
        """, (question, query_date, model_used, embedding_model, file_id))

        # Récupérer l'ID de la question insérée
        query_id = cursor.lastrowid

        # Insérer la réponse
        answer_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO answers (answer, answer_date, query_id)
            VALUES (?, ?, ?)
        """, (answer, answer_date, query_id))

        # Valider la transaction
        conn.commit()

        # Fermer la connexion
        conn.close()

        return query_id  # Retourner l'ID de la question insérée

    except sqlite3.Error as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print(f"Erreur lors de l'insertion : {e}")
        return None

def get_ingested_files():
    """Récupère tous les fichiers ingérés de la base de données."""
    return execute_query("SELECT * FROM ingested_files")

def get_queries():
    """Récupère toutes les questions posées de la base de données."""
    return execute_query("SELECT * FROM queries")

def get_answers():
    """Récupère toutes les réponses générées de la base de données."""
    return execute_query("SELECT * FROM answers")

# Fonctions pour gérer les paramètres
def save_settings(llm_model, embedding_model):
    """Sauvegarde les paramètres de modèle dans la base de données."""
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Vérifier si des paramètres existent déjà
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM settings")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        # Insérer de nouveaux paramètres
        execute_query("""
            INSERT INTO settings (id, llm_model, embedding_model, last_updated)
            VALUES (1, ?, ?, ?)
        """, (llm_model, embedding_model, last_updated), commit=True)
    else:
        # Mettre à jour les paramètres existants
        execute_query("""
            UPDATE settings
            SET llm_model = ?, embedding_model = ?, last_updated = ?
            WHERE id = 1
        """, (llm_model, embedding_model, last_updated), commit=True)
    
    return True

def get_settings():
    """Récupère les paramètres de modèle de la base de données."""
    result = execute_query("SELECT llm_model, embedding_model, last_updated FROM settings WHERE id = 1")
    if result:
        return {
            "llm_model": result[0]["llm_model"],
            "embedding_model": result[0]["embedding_model"],
            "last_updated": result[0]["last_updated"]
        }
    return None
