from sympy import symbols, diff, integrate, simplify, solve, Eq, expand, factor

# Déclaration de variables symboliques
x, y = symbols('x y')

# Définir une expression
expr = x**2 + 2*x + 1

# Dérivée
print("Dérivée :", diff(expr, x))  # 2*x + 2

# Primitive
print("Primitive :", integrate(expr, x))  # x**3/3 + x**2 + x

# Simplification
expr2 = (x**2 + 2*x + 1) / (x + 1)
print("Simplification :", simplify(expr2))  # x + 1

# Résolution d'équation
solution = solve(Eq(expr, 0), x)
print("Solutions :", solution)  # [-1]

# Factorisation
print("Factorisation :", factor(expr))  # (x + 1)**2

# Développement
print("Développement :", expand((x + 1)**2))  # x**2 + 2*x + 1
