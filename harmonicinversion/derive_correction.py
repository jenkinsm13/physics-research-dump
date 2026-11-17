import numpy as np
from scipy.integrate import quad

# ==============================================================================
# FINAL DERIVATION: Temporal Shell Correction from W_void
#
# Objective: Derive the numerical value of the Temporal Shell Correction
# (alpha^{-1}_TS ~ 0.00030469) from the physical properties of the
# Call-of-the-Void potential, W_void.
#
# Hypothesis: The correction is proportional to the integrated variance
# (susceptibility) of the dimensionless vacuum potential.
# ==============================================================================

# --- 1. Define the Dimensionless Potential w(x) ---

# Golden Ratio
phi = (1 + np.sqrt(5)) / 2

def w(x):
    """
    The dimensionless Call-of-the-Void potential, w(x) = W(r/l_P) / E_P.
    This function is derived directly from harmonic_inversion_paper.tex.
    """
    # Gaussian 1 (Attractive)
    A1 = 1 / phi
    mu1 = phi
    sigma1_sq = phi**2
    g1 = A1 * np.exp(-(x - mu1)**2 / (2 * sigma1_sq))

    # Gaussian 2 (Repulsive)
    A2 = 1 / phi**2
    mu2 = phi**2
    sigma2_sq = phi**4
    g2 = A2 * np.exp(-(x - mu2)**2 / (2 * sigma2_sq))
    
    return -g1 + g2

def w_squared(x):
    """The squared potential, to be integrated."""
    return w(x)**2

# --- 2. Calculate the Vacuum Susceptibility (chi_v) ---

# We numerically integrate the squared potential from 0 to infinity.
# This represents the total variance of the potential.
# The quad function returns the integral and an estimated error.
chi_v, integration_error = quad(w_squared, 0, np.inf)


# --- 3. Determine the Normalization Constant (k) ---

# This is the target value for the Temporal Shell Correction we are deriving.
alpha_TS_target = 0.00030469

# The hypothesis is: alpha_TS = k * chi_v
# We solve for k to see if it is a simple, fundamental constant.
k = alpha_TS_target / chi_v


# --- 4. Final Report ---

print("--- DERIVATION OF THE TEMPORAL SHELL CORRECTION ---\n")
print("HYPOTHESIS: alpha^{-1}_TS = k * integral(w(x)^2 dx)")
print("This equates the correction to the normalized variance of the vacuum potential.\n")

print("1. Dimensionless Potential w(x) defined from M-C framework.")
print(f"   phi = {phi:.9f}")

print("\n2. Calculating Vacuum Susceptibility (chi_v)...")
print(f"   chi_v = integral(w(x)^2 dx) from 0 to infinity")
print(f"   Calculated integral value: {chi_v:.9f}")
print(f"   (Numerical integration error: {integration_error:.2e})")

print("\n3. Determining Normalization Constant (k)...")
print(f"   Target alpha^{-1}_TS value: {alpha_TS_target:.9f}")
print(f"   Required k = (alpha^{-1}_TS) / chi_v")
print(f"   Calculated k = {k:.9f}")

# Analyze the result for k
# We are looking for a simple constant. Let's compare k to 1/(4*pi).
four_pi = 4 * np.pi
one_over_four_pi = 1 / four_pi
k_ratio = k / one_over_four_pi

print("\n4. ANALYSIS OF NORMALIZATION CONSTANT:")
print(f"   Is 'k' a fundamental constant? Let's test against 1/(4pi).")
print(f"   1 / (4 * pi) = {one_over_four_pi:.9f}")
print(f"   Ratio of calculated k to 1/(4pi): {k_ratio:.9f}")

if np.isclose(k_ratio, 1.0, atol=1e-4):
    print("\nCONCLUSION: VALIDATION SUCCESSFUL.")
    print("The normalization constant 'k' is confirmed to be 1/(4pi).")
    print("This is the standard normalization factor for converting a source strength")
    print("to a field in 3D space, confirming the physical basis of the model.\n")
    final_correction = (1 / (4 * np.pi)) * chi_v
    print(f"Final Derived Correction = (1/(4pi)) * {chi_v:.6f} = {final_correction:.9f}")
    print(f"This matches the target value {alpha_TS_target:.9f} precisely.")
else:
    print("\nCONCLUSION: VALIDATION FAILED.")
    print("The normalization constant 'k' does not appear to be a simple, fundamental value.") 