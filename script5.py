import streamlit as st

# Titre principal
st.title("🧠 Application avec Sidebar")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Accueil", "Dérivation", "Évaluation"])

# Page d'accueil
if page == "Accueil":
    st.header("Bienvenue dans l'application Streamlit !")
    st.write("Utilisez la barre de navigation à gauche pour choisir une opération.")
    st.image("./reflexion.png", width=300)

# Page de dérivation (exemple simple)
elif page == "Dérivation":
    st.header("Calcul de dérivée symbolique 🧮")

    expression = st.text_input("Entrez une expression (ex: x**2 + 3*x + 2)", "x**2 + 3*x + 2")
    variable = st.text_input("Variable (ex: x)", "x")

    if st.button("Dériver"):
        try:
            from sympy import symbols, diff
            var = symbols(variable)
            derivative = diff(expression, var)
            st.latex(f"\\frac{{d}}{{d{variable}}} \\left( {expression} \\right) = {derivative}")
            st.success(f"Résultat : {derivative}")
        except Exception as e:
            st.error(f"Erreur : {e}")

# Page d'évaluation numérique (exemple simple)
elif page == "Évaluation":
    st.header("Évaluation numérique 🔢")

    expression = st.text_input("Entrez une expression (ex: x**2 + 3*x + 2)", "x**2 + 3*x + 2")
    value = st.number_input("Valeur de x", value=1.0)

    if st.button("Évaluer"):
        try:
            from sympy import symbols, lambdify
            var = symbols("x")
            expr = lambdify(var, expression, "math")
            result = expr(value)
            st.success(f"Résultat : {result}")
            st.latex(f"{expression.replace('**', '^')} \\text{{ pour }} x={value} \\text{{ donne }} {result}")
        except Exception as e:
            st.error(f"Erreur : {e}")
