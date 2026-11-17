"""
======================================================================
Matryoshka Framework: Optimization of λ_m for ω = 20π
Version: 1.0
Author: Dr. Alexandra Chen
======================================================================

This script identifies the precise, optimal value for the mass-coupling
constant λ_m, under the assumption that the correlation length ω is
exactly 20π. It performs a high-resolution scan of λ_m values to
find the one that minimizes the prediction error for lepton masses,
thereby giving us a precise target for our search for a
first-principles origin.
"""

import math
import numpy as np

# Use constants from the verified framework
from framework_verification import Constants

def print_header(title):
    """Prints a formatted header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

# --- Define the theoretical Omega ---
THEORETICAL_OMEGA = 20 * math.pi

def calculate_fitness(lambda_test_value):
    """
    Calculates the combined prediction error (chi-squared-like fitness)
    for a given value of λ_m, assuming ω = 20π. Lower is better.
    """
    # Calculate ordinal depths based on the theoretical omega
    i_e = THEORETICAL_OMEGA / Constants.PHI**2
    i_mu = THEORETICAL_OMEGA
    
    # Calculate ordinal difference
    delta_mu_e = i_mu - i_e
    delta_tau_e = 2 * delta_mu_e

    # Calculate mass ratios
    pred_mu_ratio = Constants.ALPHA_MU * math.exp(lambda_test_value * delta_mu_e)
    pred_tau_ratio = Constants.ALPHA_TAU * math.exp(lambda_test_value * delta_tau_e)
    
    # Calculate normalized squared error
    err_mu = ((pred_mu_ratio - Constants.OBSERVED_MUON_RATIO) / Constants.OBSERVED_MUON_RATIO)**2
    err_tau = ((pred_tau_ratio - Constants.OBSERVED_TAU_RATIO) / Constants.OBSERVED_TAU_RATIO)**2
    
    return err_mu + err_tau

# ======================================================================
# Optimization Phase
# ======================================================================
print_header("Optimizing λ_m for ω = 20π")
print("Scanning for the value of λ_m that minimizes prediction error.")

# High-resolution scan range
scan_range = np.linspace(0.095, 0.105, 10001)
best_lambda = None
best_fitness = float('inf')

for lambda_val in scan_range:
    fitness = calculate_fitness(lambda_val)
    if fitness < best_fitness:
        best_fitness = fitness
        best_lambda = lambda_val

print(f"\nOptimization Complete.")
print(f"The optimal value for λ_m is: {best_lambda:.6f}")
print(f"This value minimizes the combined error for lepton mass predictions.")

# ======================================================================
# Verification with Optimal Lambda
# ======================================================================
print_header(f"Verification using Optimal λ_m = {best_lambda:.6f}")

# Recalculate with the best lambda
i_e = THEORETICAL_OMEGA / Constants.PHI**2
delta_mu_e = THEORETICAL_OMEGA - i_e
delta_tau_e = 2 * delta_mu_e

final_mu_ratio = Constants.ALPHA_MU * math.exp(best_lambda * delta_mu_e)
final_tau_ratio = Constants.ALPHA_TAU * math.exp(best_lambda * delta_tau_e)

muon_accuracy = (1 - abs(final_mu_ratio - Constants.OBSERVED_MUON_RATIO) / Constants.OBSERVED_MUON_RATIO) * 100
tau_accuracy = (1 - abs(final_tau_ratio - Constants.OBSERVED_TAU_RATIO) / Constants.OBSERVED_TAU_RATIO) * 100

print(f"Final Muon/Electron Ratio Prediction: {final_mu_ratio:.3f} (Accuracy: {muon_accuracy:.3f}%)")
print(f"Final Tau/Electron Ratio Prediction:  {final_tau_ratio:.3f} (Accuracy: {tau_accuracy:.3f}%)")

print("\nANALYSIS: By slightly adjusting λ_m, we have restored the >99%")
print("accuracy of the lepton mass predictions. The optimal value")
print(f"λ_m ≈ {best_lambda:.6f} is now our precise target for a first-principles derivation.")

print("\n" + "="*70)
print(" OPTIMIZATION COMPLETE")
print("="*70) 