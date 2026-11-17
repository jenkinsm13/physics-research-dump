"""
Neutrino Mass Hierarchy from Shell Depths
This script solves for δω (neutrino shell spacing) and amplitude Cν
given the measured squared-mass differences.
"""
import math
import numpy as np
from scipy.optimize import fsolve
from framework_verification import Constants

# Physical parameters
omega = 20 * math.pi
lambda_m = 1 / math.pi**2
i_e = omega / Constants.PHI**2

# Measured neutrino squared-mass differences (eV^2)
dm21 = 7.53e-5
dm31 = 2.51e-3

# System of equations for δω and Cν
def equations(vars):
    δω, Cν = vars
    i1 = omega + δω
    i2 = omega + Constants.PHI * δω
    i3 = omega + Constants.PHI**2 * δω
    m1 = Cν * math.exp(lambda_m * (i1 - i_e))
    m2 = Cν * math.exp(lambda_m * (i2 - i_e))
    m3 = Cν * math.exp(lambda_m * (i3 - i_e))
    return [m2**2 - m1**2 - dm21, m3**2 - m1**2 - dm31]

# Initial guess: δω ~ 0.1, Cν small
δω_sol, Cν_sol = fsolve(equations, [0.1, 1e-2])
print(f"Neutrino shell spacing δω = {δω_sol:.4f}")
print(f"Neutrino amplitude Cν = {Cν_sol:.5e}")

# Compute absolute masses
m1 = Cν_sol * math.exp(lambda_m * (omega + δω_sol - i_e))
m2 = Cν_sol * math.exp(lambda_m * (omega + Constants.PHI * δω_sol - i_e))
m3 = Cν_sol * math.exp(lambda_m * (omega + Constants.PHI**2 * δω_sol - i_e))
print(f"Neutrino masses (eV): m1={m1:.3e}, m2={m2:.3e}, m3={m3:.3e}")

# Compute and compare squared-mass differences
dm21_pred = m2**2 - m1**2
dm31_pred = m3**2 - m1**2
acc21 = (1 - abs(dm21_pred - dm21) / dm21) * 100
acc31 = (1 - abs(dm31_pred - dm31) / dm31) * 100
print(f"Predicted Δm21² = {dm21_pred:.3e} eV² (Target: {dm21:.3e}) | Accuracy: {acc21:.2f}%")
print(f"Predicted Δm31² = {dm31_pred:.3e} eV² (Target: {dm31:.3e}) | Accuracy: {acc31:.2f}%") 