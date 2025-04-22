# 📚 Mémo Streamlit  
## ✅ Multipage et Cache dans Streamlit

---

## 1. **Structure d’une application multipage**

### Deux approches :

### 🌟 **A. Multipage "officiel" de Streamlit**

- Créez un dossier `pages/` à côté de votre fichier principal (`app.py`).
- Tous les `.py` dans `pages/` deviennent des pages automatiquement accessibles dans la sidebar **sans coder de navigation**.
  
**Avantage** : Rapide à mettre en place.

**Inconvénient** : Moins de contrôle, difficile si vous voulez personnaliser la navigation ou garder des états partagés avancés.

### 🌟 **B. Multipage "manuelle" (recommandé pour contrôle total)**

- Créez un dossier personnalisé (`my_pages/`, `modules/`, etc.).
- Créez un fichier `app.py` principal avec votre propre navigation :

```python
import streamlit as st
import my_pages.main as main_page
import my_pages.settings as settings_page

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main", "Settings"])

if page == "Main":
    main_page.render()
elif page == "Settings":
    settings_page.render()
```

- Vous contrôlez totalement :
  - L’ordre d’exécution.
  - Le style de navigation.
  - Les données partagées avec `st.session_state`.

---

## 2. **Comprendre l’ordre d'exécution**

- Streamlit **ré-exécute tout le script** à chaque interaction utilisateur.
- Le fichier principal est toujours exécuté **de haut en bas**.
- Seule la fonction `render()` de la page sélectionnée est exécutée dans la navigation personnalisée.
- Les autres pages sont "importées", mais leur contenu hors fonction n’est pas exécuté.

**Donc :**
✔️ Mettez tout le code de chaque page **dans des fonctions** pour éviter des exécutions indésirables.

---

## 3. **Utiliser le cache Streamlit**

Deux décorateurs importants :

### 🔹 `@st.cache_data`

- **Pour stocker des résultats de calcul ou des appels API.**
- Exemple typique : chargement d’un fichier, appel HTTP, requête SQL.

```python
@st.cache_data
def fetch_data(param):
    return api_call(param)
```

- Améliore les performances en évitant de refaire le calcul ou l’appel si les paramètres sont les mêmes.

- ❗ Attention : pour les types non-hashables (comme les dict), utilisez des chaînes JSON ou des tuples.

---

### 🔹 `@st.cache_resource`

- **Pour stocker des ressources ou objets lourds en mémoire.**
- Exemple : modèle IA, client base de données, moteur de recherche local.

```python
@st.cache_resource
def initialize_model():
    return load_model()
```

- Garde l’objet en mémoire pour réutilisation efficace.

---

### 🧩 Astuce pro :

Vous pouvez vider le cache quand nécessaire :

```python
fetch_data.clear()
initialize_model.clear()
```

Et ajouter un TTL pour rafraîchir automatiquement après un certain temps :

```python
@st.cache_data(ttl=3600)  # Cache valide pour 1 heure
def fetch_data(param):
    ...
```

---

## 4. **Session State (`st.session_state`)**

- Sert à **partager des données** entre les pages ou conserver des états.
- Exemples :
  - Stocker les paramètres choisis dans les settings.
  - Mémoriser un historique d’actions.
  - Conserver des résultats calculés.

```python
if "param" not in st.session_state:
    st.session_state.param = default_value
```

---

## 🏁 Conclusion simple :

| Besoin | Solution |
|--------|-----------|
| Naviguer entre plusieurs pages avec contrôle total | Multipage manuel avec `st.sidebar.radio()` |
| Eviter de recalculer des données stables | `@st.cache_data` |
| Eviter de recréer des objets lourds (modèles, connexions) | `@st.cache_resource` |
| Partager des états ou résultats entre les pages | `st.session_state` |