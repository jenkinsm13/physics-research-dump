import numpy as np
from scipy.integrate import quad

# ==============================================================================
# DERIVATION OF THE TEMPORAL SHELL CORRECTION
#
# Objective: Derive the Temporal Shell Correction from the vacuum
# susceptibility, as determined by the Call-of-the-Void potential, W_void.
# This script represents a return to the core task after a flawed analysis.
# ==============================================================================

# --- 1. Define the Dimensionless Potential w(x) and its derivatives ---

phi = (1 + np.sqrt(5)) / 2

def w(x):
    """ The dimensionless Call-of-the-Void potential, w(x). """
    g1 = (1 / phi) * np.exp(-(x - phi)**2 / (2 * phi**2))
    g2 = (1 / phi**2) * np.exp(-(x - phi**2)**2 / (2 * phi**4))
    return -g1 + g2

def w_second_derivative(x):
    """ The analytical second derivative of w(x). """
    # Parameters for g1''(x)
    A1 = 1 / phi
    mu1 = phi
    s1_sq = phi**2
    term1 = (A1 / s1_sq) * (((x - mu1)**2 / s1_sq) - 1) * np.exp(-(x - mu1)**2 / (2 * s1_sq))

    # Parameters for g2''(x)
    A2 = 1 / phi**2
    mu2 = phi**2
    s2_sq = phi**4
    term2 = (A2 / s2_sq) * (((x - mu2)**2 / s2_sq) - 1) * np.exp(-(x - mu2)**2 / (2 * s2_sq))
    
    return -term1 + term2

def w_first_derivative(x):
    """ The analytical first derivative of w(x). """
    # Parameters for g1'(x)
    A1 = 1 / phi
    mu1 = phi
    s1_sq = phi**2
    term1 = -A1 * (x - mu1) / s1_sq * np.exp(-(x - mu1)**2 / (2 * s1_sq))

    # Parameters for g2'(x)
    A2 = 1 / phi**2
    mu2 = phi**2
    s2_sq = phi**4
    term2 = -A2 * (x - mu2) / s2_sq * np.exp(-(x - mu2)**2 / (2 * s2_sq))
    
    return -term1 + term2

# --- 2. Calculate the Vacuum Susceptibility (chi_v) ---

def integrand_for_chi(x):
    """
    The integrand for susceptibility: (w'(x))^2
    This represents the total integrated "strain energy" of the vacuum field,
    a measure of its total potential for response.
    """
    deriv = w_first_derivative(x)
    return deriv**2

# The integration is performed over the physically relevant region *between*
# the two primary shells of the potential: from phi to phi^2.
chi_v, integration_error = quad(integrand_for_chi, phi, phi**2)


# --- 3. Determine the Normalization Constant (k) ---

# The target value for the Temporal Shell Correction.
alpha_TS_target = 0.00030469

# Hypothesis: alpha_TS = k * chi_v
k = alpha_TS_target / chi_v


# --- 4. Final Report ---

print("--- DERIVATION VIA VACUUM SUSCEPTIBILITY (ATTEMPT 3) ---\n")
print("MODEL: alpha^{-1}_TS = k * integral[phi, phi^2]( (w'(x))^2 dx)")
print("This model identifies the correction with the field's strain energy.\n")

print(f"1. Calculated Vacuum Susceptibility (chi_v): {chi_v:.9f}")
print(f"   (Numerical integration error: {integration_error:.2e})\n")

print(f"2. Determining Normalization Constant (k)...")
print(f"   Target alpha^{-1}_TS value: {alpha_TS_target:.9f}")
print(f"   Required k = (alpha^{-1}_TS) / chi_v = {k:.9f}\n")

# Analysis of the normalization constant k.
if np.isclose(k, -1.0) or np.isclose(k, 1.0):
    print("CONCLUSION: VALIDATION SUCCESSFUL.")
else:
    print("CONCLUSION: VALIDATION FAILED.")
    print("The normalization constant 'k' does not resolve to a simple integer.")
    print("The physical model for the susceptibility integral is likely incomplete.") 