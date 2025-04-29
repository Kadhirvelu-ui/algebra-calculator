# Ultimate Algebra Calculator with All Features
# Install required packages: pip install streamlit sympy

import streamlit as st
import sympy as sp
from sympy import (
    sqrt, Rational, Eq, latex, symbols,
    solve, simplify, factor, expand, nsimplify,
    degree, diff, integrate, series
)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Page configuration
st.set_page_config(
    page_title="Ultimate Algebra Calculator",
    layout="wide",
    page_icon="🧮",
    initial_sidebar_state="expanded"
)

# Define mathematical symbols
x, y, z = symbols('x y z')

def add_to_history(operation, problem, solution):
    """Store calculation history"""
    st.session_state.history.append({
        'operation': operation,
        'problem': problem,
        'solution': solution
    })

def show_history():
    """Display calculation history"""
    if st.session_state.history:
        st.sidebar.subheader("📜 Calculation History")
        for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            with st.sidebar.expander(f"{i}. {item['operation']}"):
                st.write("**Problem:**")
                st.latex(item['problem'])
                st.write("**Solution:**")
                st.latex(item['solution'])

def quadratic_solver():
    st.header("🔍 Quadratic Equation Solver")
    st.markdown("Solve equations of form: **ax² + bx + c = 0**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Enter coefficient a:", value=1.0, step=0.1)
    with col2:
        b = st.number_input("Enter coefficient b:", value=0.0, step=0.1)
    with col3:
        c = st.number_input("Enter coefficient c:", value=0.0, step=0.1)
    
    if st.button("Solve Quadratic Equation", type="primary"):
        if a == 0:
            st.error("Coefficient 'a' cannot be zero for quadratic equations!")
        else:
            eq = a*x**2 + b*x + c
            solutions = solve(eq, x)
            
            st.subheader("🎯 Solutions")
            st.latex(f"Equation: {latex(eq)} = 0")
            add_to_history("Quadratic Solver", f"{latex(eq)} = 0", f"{[latex(sol) for sol in solutions]}")
            
            discriminant = b**2 - 4*a*c
            st.write("**Discriminant Analysis:**")
            st.latex(f"D = b^2 - 4ac = {discriminant}")
            
            if discriminant > 0:
                st.write("Two distinct real roots")
            elif discriminant == 0:
                st.write("One real root (repeated)")
            else:
                st.write("Two complex roots")
            
            for i, sol in enumerate(solutions, 1):
                exact_sol = nsimplify(sol, tolerance=1e-9)
                st.latex(f"x_{i} = {latex(exact_sol)}")
                st.caption(f"Decimal approximation: ≈ {sol.evalf(5)}")
            
            vertex_form = a*(x + b/(2*a))**2 + (c - b**2/(4*a))
            st.subheader("📊 Graphical Analysis")
            st.latex(f"Vertex form: {latex(vertex_form)}")
            st.write(f"Vertex at: ({-b/(2*a):.2f}, {c - b**2/(4*a):.2f})")

def expression_simplifier():
    st.header("✨ Expression Simplifier")
    expr_input = st.text_area(
        "Enter expression to simplify:",
        value="(x + 1)**2 - (x - 1)**2",
        height=70
    )
    
    if st.button("Simplify Expression", type="primary") and expr_input:
        try:
            expr = sp.sympify(expr_input)
            simplified = simplify(expr)
            
            st.subheader("Simplified Result")
            st.latex(f"{latex(expr)} \\Rightarrow {latex(simplified)}")
            add_to_history("Simplifier", latex(expr), latex(simplified))
            
            if len(str(expr)) > 30:
                st.subheader("🔧 Simplification Steps")
                st.write("1. Expand all terms:")
                expanded = expand(expr)
                st.latex(f"{latex(expr)} = {latex(expanded)}")
                st.write("2. Combine like terms:")
                st.latex(f"{latex(expanded)} = {latex(simplified)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def polynomial_factorizer():
    st.header("🧩 Polynomial Factorizer")
    poly_input = st.text_area(
        "Enter polynomial to factor:",
        value="x**3 - 2*x**2 - 5*x + 6",
        height=70
    )
    
    if st.button("Factor Polynomial", type="primary") and poly_input:
        try:
            poly = sp.sympify(poly_input)
            factored = factor(poly)
            
            st.subheader("Factored Form")
            st.latex(f"{latex(poly)} = {latex(factored)}")
            add_to_history("Factorizer", latex(poly), latex(factored))
            
            roots = solve(poly, x)
            if roots:
                st.subheader("🎯 Roots")
                for i, root in enumerate(roots, 1):
                    exact_root = nsimplify(root, tolerance=1e-9)
                    st.latex(f"x_{i} = {latex(exact_root)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def binomial_expander():
    st.header("➗ Binomial Expander")
    binomial_input = st.text_area(
        "Enter binomial to expand:",
        value="(x + 2)**5",
        height=70
    )
    
    if st.button("Expand Binomial", type="primary") and binomial_input:
        try:
            binomial = sp.sympify(binomial_input)
            expanded = expand(binomial)
            
            st.subheader("Expanded Form")
            st.latex(f"{latex(binomial)} = {latex(expanded)}")
            add_to_history("Binomial Expander", latex(binomial), latex(expanded))
            
            if binomial.is_Pow and binomial.args[1].is_Integer:
                n = binomial.args[1]
                st.subheader("🔧 Binomial Theorem Steps")
                st.latex(f"(a + b)^n = \\sum_{{k=0}}^{n} \\binom{{n}}{{k}} a^{{n-k}}b^k")
                st.latex(f"Here a = {latex(binomial.args[0].args[0])}, b = {latex(binomial.args[0].args[1])}, n = {n}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def equation_system_solver():
    st.header("🧩 System of Equations Solver (x,y,z)")
    st.markdown("Solve systems of 2 or 3 linear equations")
    
    num_eq = st.radio("Number of equations:", [2, 3], horizontal=True)
    
    st.subheader("Enter Equations")
    eq_inputs = []
    default_eqs = [
        ["x + y = 2", "2x - y = 1"],
        ["x + y + z = 6", "2x - y + 3z = 14", "-x + 2y - z = -3"]
    ]
    
    for i in range(num_eq):
        eq = st.text_input(
            f"Equation {i+1}:", 
            default_eqs[num_eq-2][i],
            key=f"eq_{i}"
        )
        eq_inputs.append(eq)
    
    if st.button("Solve System", type="primary"):
        try:
            equations = []
            variables = [x, y, z][:num_eq+1]
            
            for eq_str in eq_inputs:
                if "=" in eq_str:
                    lhs, rhs = eq_str.split("=")
                    equations.append(Eq(sp.sympify(lhs), sp.sympify(rhs)))
                else:
                    st.error("Equations must contain '=' sign")
                    return
            
            solutions = solve(equations, variables)
            
            if not solutions:
                st.error("No solution exists (system may be inconsistent)")
            else:
                st.success("Solution Found!")
                for var, val in solutions.items():
                    st.latex(f"{latex(var)} = {latex(val)}")
                
                prob_str = "\\begin{cases}" + "\\\\".join([latex(eq) for eq in equations]) + "\\end{cases}"
                sol_str = "\\\\".join([f"{latex(k)}={latex(v)}" for k,v in solutions.items()])
                add_to_history("System Solver", prob_str, sol_str)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Ensure equations are properly formatted and consistent")

def main():
    st.title("🧮 Ultimate Algebra Calculator")
    st.markdown("""
    Solve, simplify, factor, and expand algebraic expressions with complete step-by-step solutions.
    """)
    
    operation = st.sidebar.selectbox(
        "Select Operation:",
        [
            "Quadratic Equation Solver", 
            "Expression Simplifier",
            "Polynomial Factorizer",
            "Binomial Expander",
            "System of Equations Solver"  # New feature added here
        ],
        index=0
    )
    
    st.divider()
    
    if operation == "Quadratic Equation Solver":
        quadratic_solver()
    elif operation == "Expression Simplifier":
        expression_simplifier()
    elif operation == "Polynomial Factorizer":
        polynomial_factorizer()
    elif operation == "Binomial Expander":
        binomial_expander()
    elif operation == "System of Equations Solver":
        equation_system_solver()
    
    show_history()
    
    st.divider()
    st.caption("""
    **Notation Guide:**
    - Use * for multiplication (2*x)
    - Use ** or ^ for exponents (x**2 or x^2)
    - Use sqrt() for square roots
    - For fractions: (numerator)/(denominator)
    """)

if __name__ == "__main__":
    main()