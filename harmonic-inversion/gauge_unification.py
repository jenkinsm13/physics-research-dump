"""
Gauge Coupling Unification in the Matryoshka Framework
This script solves for the unification shell index where g1=g2=g3.
"""
import sympy as sp
import math

# Define symbols
n, g10, g20, g30, b1, b2, b3, n0 = sp.symbols('n g10 g20 g30 b1 b2 b3 n0')

# Define running couplings as functions of shell index n
g1 = g10 * sp.exp(-b1 * (n - n0))
g2 = g20 * sp.exp(-b2 * (n - n0))
g3 = g30 * sp.exp(-b3 * (n - n0))

# Solve unification condition g1(n)=g2(n)=g3(n)
solutions = sp.solve([g1 - g2, g2 - g3], (n, n0))
print("Symbolic solutions for (n_U, n0):", solutions)

# Numerical evaluation using typical Standard Model values at electroweak scale
sol_num = {
    g10: 0.357,  # U(1) coupling at EW scale
    g20: 0.652,  # SU(2) coupling at EW scale
    g30: 1.217,  # SU(3) coupling at EW scale
    b1: 0.016,   # U(1) beta coefficient
    b2: 0.035,   # SU(2) beta coefficient
    b3: 0.045,   # SU(3) beta coefficient
    n0: 63.2127  # Electroweak shell index ~ ω
}

# Extract n_U value from first solution
if solutions:
    nU_expr = solutions[0][0]
    nU_val = nU_expr.subs(sol_num)
    print(f"Predicted gauge unification shell index n_U ≈ {float(nU_val):.2f}")
else:
    print("No exact symbolic solution found. Computing approximate pairwise unification shells...")
    # Compute approximate n_U from g1=g2 and g2=g3
    g10_val = sol_num[g10]
    g20_val = sol_num[g20]
    g30_val = sol_num[g30]
    b1_val = sol_num[b1]
    b2_val = sol_num[b2]
    b3_val = sol_num[b3]
    n0_val = sol_num[n0]
    nU12 = n0_val + math.log(g10_val/g20_val)/(b1_val - b2_val)
    nU23 = n0_val + math.log(g20_val/g30_val)/(b2_val - b3_val)
    nU_avg = (nU12 + nU23) / 2
    print(f"n_U from g1=g2: {nU12:.2f}")
    print(f"n_U from g2=g3: {nU23:.2f}")
    print(f"Average approximate n_U: {nU_avg:.2f}") 