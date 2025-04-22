import streamlit as st
import asyncio

# Exemple de chat statique avec streaming asynchrone simulé et affichage de logs

async def fake_stream(text: str, delay: float = 0.2):
    """
    Générateur asynchrone qui utilise yield pour renvoyer progressivement
    des morceaux de texte (ici mot par mot), simulant un flux (streaming).
    Chaque appel à 'yield' suspend l'exécution de la fonction et renvoie
    la valeur courante au consommateur. Lors de la reprise, l'exécution
    reprend juste après le yield.
    """
    words = text.split()
    current = ""
    for word in words:
        current += word + " "
        # 'yield' renvoie 'current' au code appelant et suspend la fonction ici
        yield current
        # Après le yield, on attend un petit délai avant de continuer
        await asyncio.sleep(delay)


def main():
    st.set_page_config(page_title="Chat Statique avec Logs Streaming", layout="wide")
    st.title("💬 Chat statique avec streaming asynchrone et logs")

    # Initialisation de l'historique
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "assistant", "content": "Bonjour ! Posez-moi une question pour voir le streaming."}
        ]

    # Affichage de l'historique
    for msg in st.session_state.history:
        st.chat_message(msg['role']).write(msg['content'])

    # Saisie utilisateur
    user_input = st.chat_input("Votre question...")
    if not user_input:
        return

    # Affichage de la question
    st.chat_message("user").write(user_input)
    st.session_state.history.append({"role": "user", "content": user_input})

    # Réponse pré-écrite
    full_response = (
        "Ceci est une réponse d'exemple, déjà écrite, sans appel à une IA. "
        "Le texte s'affiche progressivement pour simuler le streaming asynchrone."
    )

    # Containers pour la réponse streaming et les logs
    assistant = st.chat_message("assistant")
    placeholder = assistant.empty()
    log_container = st.sidebar.expander("📄 Logs de streaming").empty()
    logs = []

    # Préparer et lancer le streaming asynchrone
    stream = fake_stream(full_response, delay=0.1)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _run_stream():
        nonlocal logs
        # Boucle asynchrone qui consomme le générateur
        async for chunk in stream:
            # Affiche le texte actuel
            placeholder.write(chunk)
            # Enregistre et affiche les logs
            logs.append(f"Yielded chunk: '{chunk.strip()}'")
            log_container.write("\n".join(logs))

    loop.run_until_complete(_run_stream())
    loop.close()

    # Sauvegarde de la réponse complète dans l'historique
    st.session_state.history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
