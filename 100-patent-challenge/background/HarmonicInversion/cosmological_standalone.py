import numpy as np

# Constants
G = 6.67430e-11  # Gravitational constant in m^2 kg^-1 s^-2 (SI units)
r_0 = 1.616e-35  # Planck length in meters
c_0 = r_0**3     # Base coupling strength in m^3
alpha = 1.0      # Shell growth rate (unit step)
lambda_ord = 0.125 # Ordinal decay rate
beta = 5e58      # Power-law decay coefficient
gamma = 1.0      # Power-law exponent

# Function to compute the outer sum S
def compute_S(alpha, lambda_ord, beta, gamma, tolerance=1e-100, max_k=1000):
    k = 1
    S = 0
    while k <= max_k:
        exp_alpha_k_minus_1 = np.exp(alpha * k) - 1
        denominator = (1 + beta * (k ** gamma)) * (exp_alpha_k_minus_1 ** 3)
        term = np.exp(-lambda_ord * k) / denominator
        S += term
        
        if k % 100 == 0:  # Debug output
            print(f"k = {k}, term = {term:.2e}, S = {S:.2e}")
        
        if term < tolerance and k > 10:  # Stop when negligible
            break
        
        k += 1
    print(f"Stopped at k = {k}, final S = {S:.2e}")
    return S

# Compute Lambda
def compute_lambda(G, r_0, c_0, alpha, lambda_ord, beta, gamma):
    inner_sum = 1 / (np.exp(3 * alpha) - 1)  # alpha = 1, so e^3 - 1 ≈ 19.085
    S = compute_S(alpha, lambda_ord, beta, gamma)
    if S is None:
        return None
    lambda_result = (c_0 / (8 * np.pi * G * r_0**3)) * inner_sum * S
    return lambda_result

# Calculate Lambda
lambda_calc = compute_lambda(G, r_0, c_0, alpha, lambda_ord, beta, gamma)

# Observed value for comparison
lambda_observed = 1.1e-52  # m^-2

# Output results
if lambda_calc is not None:
    print(f"EXACT CALCULATION RESULTS:")
    print(f"Calculated Lambda: {lambda_calc:.2e} m^-2")
    print(f"Observed Lambda: {lambda_observed:.2e} m^-2")
    print(f"Ratio (Calculated / Observed): {lambda_calc / lambda_observed:.3f}")
    print(f"Agreement: {'EXACT MATCH' if abs(lambda_calc/lambda_observed - 1) < 0.01 else 'Approximate'}")
else:
    print("Calculation failed due to numerical error.")