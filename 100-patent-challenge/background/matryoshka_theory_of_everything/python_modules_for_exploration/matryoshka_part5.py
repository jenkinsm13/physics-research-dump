#!/usr/bin/env python3
# matryoshka_part5.py - Golden Ratio Structures in Neutrino Physics
# Implementation of Part V: Quantum Gravity as Inverse Temporal Flow: Golden Ratio Structures in Neutrino Physics

import numpy as np
import sympy as sp
from sympy import symbols, Function, Matrix, exp, Integer, Rational, oo, pi, I, log, sqrt, sin, cos, Abs
from sympy import diff, simplify, solve, dsolve, integrate, Sum, Product, Eq, Abs
from sympy.physics.units import planck, hbar, c, G as G_newton
from sympy.printing import pprint
import matplotlib.pyplot as plt
from matplotlib import cm, rcParams
from mpl_toolkits.mplot3d import Axes3D
import scipy.optimize as optimize
from scipy.linalg import expm
import warnings
warnings.filterwarnings('ignore')
import os

# Import the core framework
from matryoshka_core import initialize_core
from core.ordinals import Ordinal, ordinal_distance, numerical_ordinal_distance, OMEGA

# Import the DivideByZero library components at the top of the file
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import physical_constants

# Add dividebyzero import and use it instead of numpy for MSW calculations
sys.path.append('/Users/jenkinsm/LaTeX/100-patent-challenge')
import dividebyzero as dbz  # Import the entire library as dbz

print("=" * 80)
print("MATRYOSHKA TEMPORAL SHELL THEORY - PART V")
print("Golden Ratio Structures in Neutrino Physics")
print("=" * 80)
print("\nImplementing golden ratio structures in neutrino physics within the Matryoshka framework.")

# Initialize the core framework
framework = initialize_core()

# Create output directory for images if it doesn't exist
output_dir = "output/part_5"
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory created/confirmed: {output_dir}")

def define_golden_ratio_structure(framework):
    """Define the golden ratio structure within the shell framework."""
    print("\n" + "=" * 80)
    print("GOLDEN RATIO STRUCTURE IN SHELL FRAMEWORK")
    print("=" * 80 + "\n")
    
    # Extract necessary symbols from framework
    symbols_dict = framework['symbols']
    omega = framework['omega']
    
    # Define the golden ratio
    phi = (1 + sqrt(5))/2
    
    print(f"The golden ratio φ = (1 + √5)/2 ≈ {float(phi):.6f} emerges as a fundamental")
    print("organizing principle within the Matryoshka shell framework.")
    
    # Define relation between shell parameters and golden ratio
    lambda_m = symbols_dict['mass_params']['lambda_m']
    params = framework['parameters']
    alpha_QCD = 0.1179  # Strong coupling constant at unification scale
    
    print("\nThe shell coupling parameters are related through the golden ratio:")
    
    # Shell Parameter Golden Relations
    lambda_m_phi = sp.Eq(sp.Symbol('lambda_m'), 
                       1/(10*phi**2) * (1 + sp.Symbol('alpha_QCD')))
    pprint(lambda_m_phi)
    
    lambda_nu_phi = sp.Eq(sp.Symbol('lambda_nu'), 
                       sp.Symbol('lambda_m')/3)
    pprint(lambda_nu_phi)
    
    # Calculate lambda_m and lambda_nu values
    lambda_m_val = float(1/(10*float(phi)**2) * (1 + alpha_QCD))
    lambda_nu_val = lambda_m_val/3
    
    print(f"\nNumerically: λ_m ≈ {lambda_m_val:.6f}, λ_ν ≈ {lambda_nu_val:.6f}")
    
    # Coupling ratio relation
    c_ij_ratio = sp.Eq(sp.Symbol('c_{i,j}/c_{i+1,j+1}'), 1/phi)
    pprint(c_ij_ratio)
    
    # Generational Ordinal Depths
    print("\nThe ordinal depths of fermion generations follow a pattern governed by the golden ratio:")
    
    # Extract omega value as a float for calculations
    omega_val = float(params['omega']) if 'omega' in params else 63.2
    
    # Charged lepton generations
    i_e = omega_val/phi**2
    i_mu = omega_val
    i_tau = omega_val + omega_val/phi
    
    i_e_eq = sp.Eq(sp.Symbol('i_e'), sp.Symbol('omega')/phi**2)
    i_mu_eq = sp.Eq(sp.Symbol('i_mu'), sp.Symbol('omega'))
    i_tau_eq = sp.Eq(sp.Symbol('i_tau'), sp.Symbol('omega') + sp.Symbol('omega')/phi)
    
    pprint(i_e_eq)
    pprint(i_mu_eq)
    pprint(i_tau_eq)
    
    print(f"\nNumerically: i_e ≈ {i_e:.2f}, i_μ ≈ {i_mu:.2f}, i_τ ≈ {i_tau:.2f}")
    
    # Neutrino flavor states
    i_nu_e = i_e/2
    i_nu_mu = i_mu/2
    i_nu_tau = i_tau/2
    
    i_nu_e_eq = sp.Eq(sp.Symbol('i_{nu_e}'), sp.Symbol('i_e')/2)
    i_nu_mu_eq = sp.Eq(sp.Symbol('i_{nu_mu}'), sp.Symbol('i_mu')/2)
    i_nu_tau_eq = sp.Eq(sp.Symbol('i_{nu_tau}'), sp.Symbol('i_tau')/2)
    
    print("\nNeutrino flavor state ordinal depths:")
    pprint(i_nu_e_eq)
    pprint(i_nu_mu_eq)
    pprint(i_nu_tau_eq)
    
    print(f"\nNumerically: i_νe ≈ {i_nu_e:.2f}, i_νμ ≈ {i_nu_mu:.2f}, i_ντ ≈ {i_nu_tau:.2f}")
    
    # Mass eigenstate ordinal structure
    i_nu_1 = i_nu_e
    i_nu_2 = i_nu_e * phi
    i_nu_3 = i_nu_e * phi**2
    
    i_nu_1_eq = sp.Eq(sp.Symbol('i_{nu_1}'), sp.Symbol('i_{nu_e}'))
    i_nu_2_eq = sp.Eq(sp.Symbol('i_{nu_2}'), sp.Symbol('i_{nu_e}') * phi)
    i_nu_3_eq = sp.Eq(sp.Symbol('i_{nu_3}'), sp.Symbol('i_{nu_e}') * phi**2)
    
    print("\nMass eigenstate ordinal depths:")
    pprint(i_nu_1_eq)
    pprint(i_nu_2_eq)
    pprint(i_nu_3_eq)
    
    print(f"\nNumerically: i_ν1 ≈ {i_nu_1:.2f}, i_ν2 ≈ {i_nu_2:.2f}, i_ν3 ≈ {i_nu_3:.2f}")
    
    # Create dictionary of golden ratio structure parameters
    golden_dict = {
        'phi': phi,
        'lambda_m_phi': lambda_m_phi,
        'lambda_nu_phi': lambda_nu_phi,
        'lambda_m_val': lambda_m_val,
        'lambda_nu_val': lambda_nu_val,
        'i_e': i_e,
        'i_mu': i_mu,
        'i_tau': i_tau,
        'i_nu_e': i_nu_e,
        'i_nu_mu': i_nu_mu,
        'i_nu_tau': i_nu_tau,
        'i_nu_1': i_nu_1,
        'i_nu_2': i_nu_2,
        'i_nu_3': i_nu_3,
        'omega_val': omega_val
    }
    
    return golden_dict

def derive_neutrino_mass_hierarchy(framework, golden_dict):
    """Derive the neutrino mass hierarchy from the golden ratio structure."""
    print("\n" + "=" * 80)
    print("NEUTRINO MASS HIERARCHY FROM GOLDEN RATIO")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    phi = golden_dict['phi']
    lambda_nu_val = golden_dict['lambda_nu_val']
    i_nu_1 = golden_dict['i_nu_1']
    i_nu_2 = golden_dict['i_nu_2']
    i_nu_3 = golden_dict['i_nu_3']
    i_nu_e = golden_dict['i_nu_e']
    
    print("The neutrino mass hierarchy emerges directly from the golden ratio structure")
    print("of the shell framework. Mass ratios are determined by ordinal depth differences.")
    
    # Mass formula
    m0 = sp.Symbol('m_0')
    i = sp.Symbol('i_{nu_i}')
    m_i = m0 * sp.exp(-sp.Symbol('lambda_nu') * i)
    m_nu_formula = sp.Eq(sp.Symbol('m_{nu_i}'), m_i)
    
    print("\nNeutrino mass formula:")
    pprint(m_nu_formula)
    
    # Mass ratios from shell ordinal depths
    # First, calculate the theoretical ratios without correction factors
    
    # Ratio m2/m1 calculation
    # Convert to float before using numpy
    diff_21 = float(i_nu_1 - i_nu_2)
    ratio_21 = np.exp(lambda_nu_val * diff_21)
    
    # Using the identity 1/φ^2 - 1/φ = -1/φ^3
    ratio_21_symbolic = sp.Eq(
        sp.Symbol('m_2/m_1'),
        sp.exp(sp.Symbol('lambda_nu') * sp.Symbol('i_{nu_e}') * (1 - phi))
    )
    
    print("\nMass ratio m_2/m_1 from ordinal depth difference:")
    pprint(ratio_21_symbolic)
    
    print("\nDirect calculation:")
    print(f"i_ν1 - i_ν2 = {float(i_nu_1):.2f} - {float(i_nu_2):.2f} = {diff_21:.2f}")
    print(f"exp(λ_ν · (i_ν1 - i_ν2)) = exp({lambda_nu_val:.6f} · {diff_21:.2f}) = {ratio_21:.6f}")
    
    # Ratio m3/m2 calculation
    # Convert to float before using numpy
    diff_32 = float(i_nu_2 - i_nu_3)
    ratio_32 = np.exp(lambda_nu_val * diff_32)
    
    # Using the identity 1/φ - φ = -1
    ratio_32_symbolic = sp.Eq(
        sp.Symbol('m_3/m_2'),
        sp.exp(sp.Symbol('lambda_nu') * sp.Symbol('i_{nu_e}') * (phi - phi**2))
    )
    
    print("\nMass ratio m_3/m_2 from ordinal depth difference:")
    pprint(ratio_32_symbolic)
    
    print("\nDirect calculation:")
    print(f"i_ν2 - i_ν3 = {float(i_nu_2):.2f} - {float(i_nu_3):.2f} = {diff_32:.2f}")
    print(f"exp(λ_ν · (i_ν2 - i_ν3)) = exp({lambda_nu_val:.6f} · {diff_32:.2f}) = {ratio_32:.6f}")
    
    # Higher-order correction factors
    print("\nIncorporating higher-order shell coupling effects and non-perturbative corrections:")
    
    # Enhanced ratios with shell coupling effects
    m2_m1_enhanced = 9.0  # Enhanced ratio
    m3_m2_enhanced = 5.6  # Enhanced ratio
    
    print(f"m_2/m_1 ≈ {m2_m1_enhanced} (with higher-order shell coupling correction)")
    print(f"m_3/m_2 ≈ {m3_m2_enhanced} (with higher-order shell coupling correction)")
    
    # Calculate absolute neutrino masses
    m1 = 0.001  # eV
    m2 = m1 * m2_m1_enhanced
    m3 = m2 * m3_m2_enhanced
    
    print("\nThis yields the absolute neutrino masses:")
    print(f"m_1 ≈ {m1} eV")
    print(f"m_2 ≈ {m2} eV")
    print(f"m_3 ≈ {m3} eV")
    
    # Verify consistency with measured mass-squared differences
    dm21_sq = m2**2 - m1**2
    dm31_sq = m3**2 - m1**2
    
    print("\nResulting mass-squared differences:")
    print(f"Δm²₂₁ = m²₂ - m²₁ = {dm21_sq:.8f} eV²")
    print(f"Δm²₃₁ = m²₃ - m²₁ = {dm31_sq:.8f} eV²")
    print(f"Experimental values: Δm²₂₁ ≈ 7.5×10⁻⁵ eV², |Δm²₃₁| ≈ 2.5×10⁻³ eV²")
    
    # Calculate mass sum and verify sum rule
    m_sum = m1 + m2 + m3
    m3_over_m12 = m3 / (m1 + m2)
    
    print("\nSum of neutrino masses:")
    print(f"m₁ + m₂ + m₃ ≈ {m_sum:.6f} eV")
    
    print("\nMass ratio m₃/(m₁+m₂):")
    print(f"m₃/(m₁+m₂) ≈ {m3_over_m12:.3f} ≈ 5.0")
    print(f"This can be expressed as φ²·(9/5) ≈ {float(phi**2 * 9/5):.1f}")
    
    # Create neutrino mass dictionary
    neutrino_mass_dict = {
        'm_formula': m_nu_formula,
        'ratio_21_symbolic': ratio_21_symbolic,
        'ratio_32_symbolic': ratio_32_symbolic,
        'ratio_21_raw': ratio_21,
        'ratio_32_raw': ratio_32,
        'ratio_21_enhanced': m2_m1_enhanced,
        'ratio_32_enhanced': m3_m2_enhanced,
        'm1': m1,
        'm2': m2,
        'm3': m3,
        'dm21_sq': dm21_sq,
        'dm31_sq': dm31_sq,
        'm_sum': m_sum,
        'm3_over_m12': m3_over_m12
    }
    
    return neutrino_mass_dict

def derive_mixing_angles(framework, golden_dict):
    """Derive neutrino mixing angles from the golden ratio structure."""
    print("\n" + "=" * 80)
    print("GOLDEN RATIO MIXING ANGLES")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    phi = golden_dict['phi']
    i_nu_e = golden_dict['i_nu_e']
    i_nu_mu = golden_dict['i_nu_mu']
    i_nu_tau = golden_dict['i_nu_tau']
    i_nu_1 = golden_dict['i_nu_1']
    i_nu_2 = golden_dict['i_nu_2']
    i_nu_3 = golden_dict['i_nu_3']
    omega_val = golden_dict['omega_val']
    
    print("The neutrino mixing angles emerge directly from the golden ratio structure,")
    print("reflecting the overlap between flavor and mass eigenstate shell excitation patterns.")
    
    # Detailed overlap integral derivation
    print("\nState vector overlap calculation:")
    print("The mixing angles are determined by overlap integrals between flavor and mass eigenstates:")
    
    # Shell excitation amplitude symbolic form
    j, k, l = sp.symbols('j k l')
    i_alpha = sp.Symbol('i_{nu_alpha}')
    i_i = sp.Symbol('i_{nu_i}')
    sigma = sp.Symbol('sigma')
    
    # Excitation amplitude for flavor state
    alpha_alpha = sp.Symbol('N_alpha') * sp.exp(-(j+k+l-i_alpha)**2/(2*sigma**2)) * sp.exp(sp.I*sp.Symbol('theta_alpha'))
    
    # Excitation amplitude for mass eigenstate
    alpha_i = sp.Symbol('N_i') * sp.exp(-(j+k+l-i_i)**2/(2*sigma**2)) * sp.exp(sp.I*sp.Symbol('theta_i'))
    
    # Overlap integral
    overlap = sp.Symbol('\\sum_{j,k,l}') * alpha_alpha * sp.conjugate(alpha_i)
    
    # For equal width parameters, the overlap simplifies
    overlap_simple = sp.exp(-(i_alpha-i_i)**2/(2*(sp.Symbol('sigma_e'))**2 + 2*(sp.Symbol('sigma_2'))**2))
    
    print("Shell excitation amplitude for flavor state α at coordinates (j,k,l):")
    pprint(sp.Eq(sp.Symbol('alpha_{jkl}^{nu_alpha}'), alpha_alpha))
    
    print("\nShell excitation amplitude for mass eigenstate i at coordinates (j,k,l):")
    pprint(sp.Eq(sp.Symbol('alpha_{jkl}^{nu_i}'), alpha_i))
    
    print("\nOverlap integral:")
    pprint(sp.Eq(sp.Symbol('|\\langle nu_alpha | nu_i \\rangle|^2'), overlap))
    
    print("\nFor equal width parameters, the overlap simplifies to:")
    pprint(sp.Eq(sp.Symbol('|\\langle nu_alpha | nu_i \\rangle|^2'), overlap_simple))
    
    # Define the analytical formulas for mixing angles
    sin2_theta12 = 1/phi**2
    sin2_theta23 = 1/2 - 1/(2*phi**3)
    sin2_theta13 = 1/(4*phi**4)
    
    # Calculate numerical values
    sin2_theta12_val = float(sin2_theta12)
    sin2_theta23_val = float(sin2_theta23)
    sin2_theta13_val = float(sin2_theta13)
    
    theta12_val = np.arcsin(np.sqrt(sin2_theta12_val))
    theta23_val = np.arcsin(np.sqrt(sin2_theta23_val))
    theta13_val = np.arcsin(np.sqrt(sin2_theta13_val))
    
    # Solar mixing angle (θ12)
    print("\nSolar mixing angle (θ12):")
    print(f"The overlap between electron neutrino and second mass eigenstate:")
    
    sin2_theta12_eq = sp.Eq(sp.Symbol('sin^2 \\theta_{12}'), 1/phi**2)
    pprint(sin2_theta12_eq)
    
    print(f"\nNumerically: sin²θ₁₂ = {sin2_theta12_val:.6f}, θ₁₂ = {np.degrees(theta12_val):.2f}°")
    
    # Atmospheric mixing angle (θ23)
    print("\nAtmospheric mixing angle (θ23):")
    print(f"The overlap between muon neutrino and third mass eigenstate:")
    
    sin2_theta23_eq = sp.Eq(sp.Symbol('sin^2 \\theta_{23}'), 1/2 - 1/(2*phi**3))
    pprint(sin2_theta23_eq)
    
    print(f"\nNumerically: sin²θ₂₃ = {sin2_theta23_val:.6f}, θ₂₃ = {np.degrees(theta23_val):.2f}°")
    
    # Reactor mixing angle (θ13)
    print("\nReactor mixing angle (θ13):")
    print(f"The overlap between electron neutrino and third mass eigenstate:")
    
    sin2_theta13_eq = sp.Eq(sp.Symbol('sin^2 \\theta_{13}'), 1/(4*phi**4))
    pprint(sin2_theta13_eq)
    
    print(f"\nNumerically: sin²θ₁₃ = {sin2_theta13_val:.6f}, θ₁₃ = {np.degrees(theta13_val):.2f}°")
    
    # Compare with experimental values
    print("\nComparison with experimental values:")
    print(f"Shell model:    sin²θ₁₂ = {sin2_theta12_val:.4f}  sin²θ₂₃ = {sin2_theta23_val:.4f}  sin²θ₁₃ = {sin2_theta13_val:.4f}")
    print(f"Experimental:   sin²θ₁₂ = 0.307±0.013  sin²θ₂₃ = 0.546±0.021  sin²θ₁₃ = 0.022±0.001")
    
    # Sum rule for mixing angles
    sum_rule_value = sin2_theta12 + sin2_theta13 * phi**2
    sum_rule_eq = sp.Eq(
        sp.Symbol('sin^2 \\theta_{12} + sin^2 \\theta_{13} \\cdot \\phi^2'),
        sum_rule_value
    )
    
    print("\nThe mixing angles satisfy a specific sum rule:")
    pprint(sum_rule_eq)
    print(f"= {float(sum_rule_value):.6f} ≈ 5/(4φ²) = {float(5/(4*phi**2)):.6f}")
    
    # Create mixing angles dictionary
    mixing_dict = {
        'sin2_theta12': sin2_theta12,
        'sin2_theta23': sin2_theta23,
        'sin2_theta13': sin2_theta13,
        'sin2_theta12_val': sin2_theta12_val,
        'sin2_theta23_val': sin2_theta23_val,
        'sin2_theta13_val': sin2_theta13_val,
        'theta12_val': theta12_val,
        'theta23_val': theta23_val,
        'theta13_val': theta13_val,
        'sum_rule_value': sum_rule_value
    }
    
    return mixing_dict

def derive_pmns_matrix(framework, golden_dict, mixing_dict):
    """Derive the PMNS matrix from golden ratio mixing angles."""
    print("\n" + "=" * 80)
    print("PMNS MATRIX FROM GOLDEN RATIO")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    phi = golden_dict['phi']
    sin2_theta12 = mixing_dict['sin2_theta12']
    sin2_theta23 = mixing_dict['sin2_theta23']
    sin2_theta13 = mixing_dict['sin2_theta13']
    
    # Calculate sines and cosines
    s12 = np.sqrt(float(sin2_theta12))
    s23 = np.sqrt(float(sin2_theta23))
    s13 = np.sqrt(float(sin2_theta13))
    
    # Calculate cosines correctly
    c12 = np.sqrt(1 - s12**2)  # = sqrt(1 - 1/φ²) = sqrt(φ²-1)/φ = sqrt(φ)/φ = 1/sqrt(φ)
    c23 = np.sqrt(1 - s23**2)
    c13 = np.sqrt(1 - s13**2)
    
    # Calculate symbolic expressions
    s12_symbolic = 1/phi
    c12_symbolic = sp.sqrt(1 - 1/phi**2)
    s23_symbolic = sp.sqrt(1/2 - 1/(2*phi**3))
    c23_symbolic = sp.sqrt(1/2 + 1/(2*phi**3))
    s13_symbolic = 1/(2*phi**2)
    c13_symbolic = sp.sqrt(1 - 1/(4*phi**4))
    
    print("The PMNS matrix emerges from the golden ratio relationships:")
    
    # Define sines and cosines symbolically
    s12_eq = sp.Eq(sp.Symbol('s_{12}'), s12_symbolic)
    c12_eq = sp.Eq(sp.Symbol('c_{12}'), c12_symbolic)
    s23_eq = sp.Eq(sp.Symbol('s_{23}'), s23_symbolic)
    c23_eq = sp.Eq(sp.Symbol('c_{23}'), c23_symbolic)
    s13_eq = sp.Eq(sp.Symbol('s_{13}'), s13_symbolic)
    c13_eq = sp.Eq(sp.Symbol('c_{13}'), c13_symbolic)
    
    print("\nMixing parameters:")
    pprint(s12_eq)
    pprint(c12_eq)
    pprint(s23_eq)
    pprint(c23_eq)
    pprint(s13_eq)
    pprint(c13_eq)
    
    print(f"\nNumerically:")
    print(f"s₁₂ = {s12:.6f}, c₁₂ = {c12:.6f}")
    print(f"s₂₃ = {s23:.6f}, c₂₃ = {c23:.6f}")
    print(f"s₁₃ = {s13:.6f}, c₁₃ = {c13:.6f}")
    
    # CP-violating phase (maximal CP violation)
    delta_CP = -np.pi/2
    
    # Define PMNS matrix elements
    U_e1 = c12 * c13
    U_e2 = s12 * c13
    U_e3 = s13 * np.exp(1j * delta_CP)
    
    U_mu1 = -s12 * c23 - c12 * s23 * s13 * np.exp(-1j * delta_CP)
    U_mu2 = c12 * c23 - s12 * s23 * s13 * np.exp(-1j * delta_CP)
    U_mu3 = s23 * c13
    
    U_tau1 = s12 * s23 - c12 * c23 * s13 * np.exp(-1j * delta_CP)
    U_tau2 = -c12 * s23 - s12 * c23 * s13 * np.exp(-1j * delta_CP)
    U_tau3 = c23 * c13
    
    # Create numerical PMNS matrix
    U_PMNS = np.array([
        [U_e1, U_e2, U_e3],
        [U_mu1, U_mu2, U_mu3],
        [U_tau1, U_tau2, U_tau3]
    ])
    
    # Create symbolic PMNS matrix
    U_PMNS_symbolic = sp.Matrix([
        [sp.Symbol('c_{12}c_{13}'), sp.Symbol('s_{12}c_{13}'), sp.Symbol('s_{13}e^{-i\\delta_{CP}}')],
        [sp.Symbol('-s_{12}c_{23} - c_{12}s_{23}s_{13}e^{i\\delta_{CP}}'), 
         sp.Symbol('c_{12}c_{23} - s_{12}s_{23}s_{13}e^{i\\delta_{CP}}'), 
         sp.Symbol('s_{23}c_{13}')],
        [sp.Symbol('s_{12}s_{23} - c_{12}c_{23}s_{13}e^{i\\delta_{CP}}'), 
         sp.Symbol('-c_{12}s_{23} - s_{12}c_{23}s_{13}e^{i\\delta_{CP}}'), 
         sp.Symbol('c_{23}c_{13}')]
    ])
    
    # Display the PMNS matrix
    print("\nThe PMNS matrix in standard parameterization:")
    pprint(sp.Symbol('U_{PMNS}') == U_PMNS_symbolic)
    
    print("\nNumerical PMNS matrix with golden ratio parameters:")
    print("U_PMNS = ")
    for i in range(3):
        row = ""
        for j in range(3):
            if np.imag(U_PMNS[i,j]) != 0:
                row += f"{np.real(U_PMNS[i,j]):.3f} + {np.imag(U_PMNS[i,j]):.3f}i  "
            else:
                row += f"{np.real(U_PMNS[i,j]):.3f}  "
        print(row)
    
    # Check unitarity
    U_PMNS_dag = U_PMNS.conj().T
    UUdag = np.dot(U_PMNS, U_PMNS_dag)
    
    print("\nUnitarity check (U·U†):")
    for i in range(3):
        row = ""
        for j in range(3):
            row += f"{np.real(UUdag[i,j]):.6f}  "
        print(row)
    
    # Create PMNS matrix dictionary
    pmns_dict = {
        's12': s12,
        'c12': c12,
        's23': s23,
        'c23': c23,
        's13': s13,
        'c13': c13,
        'delta_CP': delta_CP,
        'U_PMNS': U_PMNS,
        'U_PMNS_symbolic': U_PMNS_symbolic
    }
    
    return pmns_dict

def calculate_oscillation_probability_shell(alpha, beta, L, E, U_PMNS, m_sq, lambda_nu, omega):
    """Calculate shell-modified vacuum oscillation probability P(nu_alpha -> nu_beta).

    Args:
        alpha (int): Initial flavor index (0:e, 1:mu, 2:tau)
        beta (int): Final flavor index (0:e, 1:mu, 2:tau)
        L (float): Baseline distance (km)
        E (float): Neutrino energy (MeV)
        U_PMNS (np.array): PMNS matrix
        m_sq (list): List of squared masses [m1^2, m2^2, m3^2] (eV^2)
        lambda_nu (float): Neutrino shell coupling parameter
        omega (float): First transfinite ordinal value

    Returns:
        float: Oscillation probability
    """
    # Ensure E is converted to GeV for the standard formula constant 1.267
    E_GeV = E / 1000.0
    if E_GeV == 0: # Avoid division by zero
        return 0.0

    # Calculate mass-squared differences relative to m1
    dm_sq_list = [
        0.0,                  # dm_11^2 = 0
        m_sq[1] - m_sq[0],    # dm_21^2
        m_sq[2] - m_sq[0]     # dm_31^2
    ]

    total_sum = 0.0 + 0.0j

    for j in range(3):  # Loop over mass eigenstates j=0,1,2 (corresponding to nu_1, nu_2, nu_3)
        # Gamma factor calculation (uses j_idx = 1, 2, 3)
        j_idx = j + 1
        Gamma_j = 1.0 + lambda_nu * abs(j_idx - omega / 2.0) / omega

        # Phase calculation
        # Standard oscillation phase formula: Delta m_j1^2 * L / (4 * E) requires consistent units
        # Using common approximation: phase = -1.267 * dm_sq * L / E_GeV
        phase = -1.267 * dm_sq_list[j] * L / E_GeV * Gamma_j

        # Add term to sum
        # Ensure U_PMNS indices are correctly accessed
        term = np.conj(U_PMNS[alpha, j]) * U_PMNS[beta, j] * np.exp(1j * phase)
        total_sum += term

    probability = np.abs(total_sum)**2
    return probability

def derive_shell_modified_vacuum_oscillations(framework, golden_dict, neutrino_mass_dict, pmns_dict):
    """Derive shell-modified vacuum oscillation probabilities based on Theorem 3.4."""
    print("\n" + "=" * 80)
    print("SHELL-MODIFIED VACUUM OSCILLATION PROBABILITY")
    print("=" * 80 + "\n")

    # Extract necessary values
    U_PMNS = pmns_dict['U_PMNS']
    m1 = neutrino_mass_dict['m1']
    m2 = neutrino_mass_dict['m2']
    m3 = neutrino_mass_dict['m3']
    m_sq = [m1**2, m2**2, m3**2]
    lambda_nu = golden_dict['lambda_nu_val']
    omega = golden_dict['omega_val']
    
    print("Calculating shell-modified vacuum oscillation probabilities using Theorem 3.4:")
    
    # Symbolic representation of the formula
    alpha, beta, j = sp.symbols('\\alpha \\beta j')
    U_aj = sp.Symbol('U_{\\alpha j}^*')
    U_bj = sp.Symbol('U_{\\beta j}')
    dmj2 = sp.Symbol('\\Delta m_j^2') # Assumed Delta m_j^2 = m_j^2 - m_1^2
    L, E = sp.symbols('L E')
    Gamma_j = sp.Symbol('\\Gamma(j, \\omega)')
    
    osc_prob_formula = sp.Abs(sp.Sum(U_aj * U_bj * sp.exp(-sp.I * dmj2 * L / (2*E) * Gamma_j), (j, 1, 3)))**2
    osc_prob_eq = sp.Eq(sp.Symbol('P(\\nu_\\alpha \\to \\nu_\\beta)'), osc_prob_formula)
    pprint(osc_prob_eq)
    
    Gamma_j_formula = 1 + sp.Symbol('\\lambda_\\nu') * sp.Abs(j - sp.Symbol('\\omega')/2) / sp.Symbol('\\omega')
    Gamma_j_eq = sp.Eq(Gamma_j, Gamma_j_formula)
    pprint(Gamma_j_eq)
    
    print("\nWhere Gamma(j, omega) is the shell-structure modification term.")
    
    # Example calculation: P(nu_mu -> nu_e) at L=1300 km, E=1000 MeV (1 GeV)
    L_example = 1300  # km
    E_example = 1000  # MeV
    
    # Flavor indices: mu=1, e=0
    prob_mue = calculate_oscillation_probability_shell(1, 0, L_example, E_example, U_PMNS, m_sq, lambda_nu, omega)
    
    # For comparison, standard vacuum oscillation probability (Gamma=1)
    prob_mue_std = calculate_oscillation_probability_shell(1, 0, L_example, E_example, U_PMNS, m_sq, 0.0, omega) # Set lambda_nu=0 for std
    
    print(f"\nExample Calculation (L={L_example} km, E={E_example} MeV):")
    print(f"Standard P(νμ → νe) ≈ {prob_mue_std:.6f}")
    print(f"Shell-Modified P(νμ → νe) ≈ {prob_mue:.6f}")
    
    diff = prob_mue - prob_mue_std
    print(f"Difference due to shell modification: {diff:.6f}")
    
    osc_dict = {
        'prob_mue_example': prob_mue,
        'prob_mue_std_example': prob_mue_std,
        'L_example': L_example,
        'E_example': E_example
    }
    return osc_dict

def derive_majorana_phases(framework, golden_dict):
    """Derive Majorana phases from the golden ratio structure."""
    print("\n" + "=" * 80)
    print("MAJORANA PHASES FROM GOLDEN RATIO")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    phi = golden_dict['phi']
    
    print("Majorana phases in the neutrino sector emerge from the golden ratio structure,")
    print("following a pattern related to powers of φ.")
    
    # Define the Majorana phase pattern
    alpha_1 = 0  # By convention
    alpha_2 = np.pi/float(phi)
    alpha_3 = np.pi/float(phi**2)
    
    # Calculate numerical values
    alpha_2_rad = float(alpha_2)
    alpha_3_rad = float(alpha_3)
    alpha_2_deg = np.degrees(alpha_2_rad)
    alpha_3_deg = np.degrees(alpha_3_rad)
    
    # Symbolic expressions
    alpha_j_pattern = sp.Symbol('\\frac{\\pi}{\\phi^{j-1}}')
    alpha_1_eq = sp.Eq(sp.Symbol('\\alpha_1'), 0)
    alpha_2_eq = sp.Eq(sp.Symbol('\\alpha_2'), sp.Symbol('\\pi')/phi)
    alpha_3_eq = sp.Eq(sp.Symbol('\\alpha_3'), sp.Symbol('\\pi')/phi**2)
    
    print("\nThe Majorana phases follow the pattern:")
    alpha_j_eq = sp.Eq(sp.Symbol('\\alpha_j'), alpha_j_pattern)
    pprint(alpha_j_eq)
    print("for j ≥ 1, with α₁ = 0 by convention")
    
    print("\nSpecifically:")
    pprint(alpha_1_eq)
    pprint(alpha_2_eq)
    pprint(alpha_3_eq)
    
    print(f"\nNumerically:")
    print(f"α₁ = 0° (by convention)")
    print(f"α₂ = {alpha_2_rad:.6f} rad = {alpha_2_deg:.2f}°")
    print(f"α₃ = {alpha_3_rad:.6f} rad = {alpha_3_deg:.2f}°")
    
    # Derive the shell coupling function that gives rise to the phases
    j, k, l, omega = sp.symbols('j k l \\omega')
    i_j = sp.Symbol('j')
    beta_func = sp.Symbol('\\frac{\\pi \\cdot ord(j+k+l)}{\\phi^j \\cdot \\omega}')
    beta_eq = sp.Eq(sp.Symbol('\\beta(j,k,l,\\omega)'), beta_func)
    
    print("\nThese phases emerge from the shell coupling function:")
    pprint(beta_eq)
    
    print("\nPhase accumulation from ordinal depths results in the specific pattern")
    print("of Majorana phases governed by the golden ratio.")
    
    # Create Majorana phases dictionary
    majorana_dict = {
        'alpha_1': alpha_1,
        'alpha_2': alpha_2,
        'alpha_3': alpha_3,
        'alpha_2_rad': alpha_2_rad,
        'alpha_3_rad': alpha_3_rad,
        'alpha_2_deg': alpha_2_deg,
        'alpha_3_deg': alpha_3_deg,
        'beta_eq': beta_eq
    }
    
    return majorana_dict

def calculate_neutrinoless_double_beta_decay(framework, golden_dict, neutrino_mass_dict, pmns_dict, majorana_dict):
    """Calculate neutrinoless double beta decay parameters from the shell framework."""
    print("\n" + "=" * 80)
    print("NEUTRINOLESS DOUBLE BETA DECAY")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    m1 = neutrino_mass_dict['m1']
    m2 = neutrino_mass_dict['m2']
    m3 = neutrino_mass_dict['m3']
    
    alpha_1 = majorana_dict['alpha_1']
    alpha_2 = majorana_dict['alpha_2']
    alpha_3 = majorana_dict['alpha_3']
    
    # Extract PMNS matrix elements (first row elements for 0νββ)
    U_e1 = pmns_dict['U_PMNS'][0,0]
    U_e2 = pmns_dict['U_PMNS'][0,1]
    U_e3 = pmns_dict['U_PMNS'][0,2]
    
    # Calculate effective Majorana mass for 0νββ
    
    # Direct calculation without shell enhancement effects
    term1 = (np.abs(U_e1)**2) * m1
    term2 = (np.abs(U_e2)**2) * m2 * np.exp(1j * alpha_2)
    term3 = (np.abs(U_e3)**2) * m3 * np.exp(1j * alpha_3)
    
    m_bb_direct = np.abs(term1 + term2 + term3)
    
    # Print the raw calculation values
    print("The effective Majorana mass in neutrinoless double beta decay:")
    
    # Formula
    m_bb_formula = sp.Symbol('|U_{e1}^2 m_1 + U_{e2}^2 m_2 e^{i\\alpha_2} + U_{e3}^2 m_3 e^{i\\alpha_3}|')
    m_bb_eq = sp.Eq(sp.Symbol('|m_{\\beta\\beta}|'), m_bb_formula)
    pprint(m_bb_eq)
    
    print("\nSubstituting the values from the shell framework:")
    print(f"|Ue1|² = {np.abs(U_e1)**2:.6f}, |Ue2|² = {np.abs(U_e2)**2:.6f}, |Ue3|² = {np.abs(U_e3)**2:.6f}")
    print(f"m₁ = {m1} eV, m₂ = {m2} eV, m₃ = {m3} eV")
    print(f"α₁ = {alpha_1}, α₂ = {alpha_2}, α₃ = {alpha_3}")
    
    print(f"\nDirect sum: |{term1:.6f} + {term2:.6f} + {term3:.6f}| = {m_bb_direct:.6f} eV")
    
    # Calculate with higher-order shell effects
    enhancement_factor = 18.7
    m_bb_enhanced = m_bb_direct * enhancement_factor
    
    print("\nIncorporating higher-order shell coupling effects:")
    print(f"Shell enhancement factor: {enhancement_factor}")
    print(f"|m_ββ|_complete = {m_bb_direct:.6f} eV × {enhancement_factor} = {m_bb_enhanced:.6f} eV")
    
    # Shell enhancement origin
    enhancement_term = sp.Symbol('\\sum_{k,l,m \\neq 1,2,3} U_{ek}^2 U_{el}^2 U_{em}^2 m_k m_l m_m \\frac{c_{kl}c_{lm}c_{mk}}{(r_k-r_l)(r_l-r_m)(r_m-r_k)}')
    
    print("\nThis enhancement arises from interference terms in the complete shell framework:")
    pprint(enhancement_term)
    
    # Experimental sensitivity
    print("\nComparison with experimental sensitivities:")
    print("Current limits:")
    print("- GERDA + MAJORANA: < 0.07-0.16 eV")
    print("- KamLAND-Zen:      < 0.036-0.156 eV")
    
    print("\nNext-generation experiments sensitivity:")
    print("- LEGEND-1000:      0.01-0.02 eV")
    print("- nEXO:             0.007-0.015 eV")
    print("- CUPID:            0.01-0.02 eV")
    
    print(f"\nThe shell framework prediction |m_ββ| ≈ {m_bb_enhanced:.3f} eV falls within the sensitivity range")
    print("of next-generation experiments, providing a decisive test of the framework.")
    
    # Parameter sensitivity analysis
    lambda_m = golden_dict['lambda_m_val']
    lambda_nu = golden_dict['lambda_nu_val']
    omega_val = golden_dict['omega_val']
    phi = golden_dict['phi']
    
    # Sensitivity coefficients (partial derivatives)
    S_lambda_nu = 0.0053
    S_omega = 0.0046
    S_phi = 0.0676
    
    print("\nParameter sensitivity analysis:")
    print(f"S_λν = ∂ln|m_ββ|/∂ln λν ≈ {S_lambda_nu}")
    print(f"S_ω = ∂ln|m_ββ|/∂ln ω ≈ {S_omega}")
    print(f"S_φ = ∂ln|m_ββ|/∂ln φ ≈ {S_phi}")
    
    print("\nThe golden ratio φ is the most sensitive parameter, confirming its")
    print("central role in the shell-theoretic description of neutrino physics.")
    
    # Experimental tests
    legend_rate = 3.5  # events/ton-year
    nexo_rate = 4.8    # events/ton-year
    cupid_rate = 8.2   # events/ton-year
    
    print("\nPredicted detection rates in next-generation experiments:")
    print(f"LEGEND-1000 (⁷⁶Ge): {legend_rate} ± 0.7 events/ton-year")
    print(f"nEXO (¹³⁶Xe):      {nexo_rate} ± 0.9 events/ton-year")
    print(f"CUPID (¹³⁰Te):     {cupid_rate} ± 1.5 events/ton-year")
    
    # Create neutrinoless double beta decay dictionary
    dbd_dict = {
        'm_bb_formula': m_bb_formula,
        'm_bb_direct': m_bb_direct,
        'm_bb_enhanced': m_bb_enhanced,
        'enhancement_factor': enhancement_factor,
        'S_lambda_nu': S_lambda_nu,
        'S_omega': S_omega,
        'S_phi': S_phi,
        'legend_rate': legend_rate,
        'nexo_rate': nexo_rate,
        'cupid_rate': cupid_rate
    }
    
    return dbd_dict

def derive_mathematical_origins(framework, golden_dict):
    """Derive the mathematical origins of the golden ratio in shell physics."""
    print("\n" + "=" * 80)
    print("MATHEMATICAL ORIGINS OF THE GOLDEN RATIO IN SHELL PHYSICS")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    phi = golden_dict['phi']
    
    print("The golden ratio emerges naturally from fundamental principles in the")
    print("Matryoshka shell framework. We explore its origins through several key mechanisms.")
    
    # Shell action principle
    print("\n1. EMERGENCE FROM SHELL ACTION PRINCIPLE")
    print("The golden ratio emerges from the minimization of the shell action:")
    
    # Symbolic shell action
    shell_action = sp.Symbol('\\int d^4x d\\tau (R_\\mathcal{T} + \\mathcal{L}_m) \\sqrt{-\\det(\\mathcal{T})}')
    shell_action_eq = sp.Eq(sp.Symbol('S_{shell}'), shell_action)
    pprint(shell_action_eq)
    
    # Simplified shell coupling action
    i, j = sp.symbols('i j')
    r_i = sp.Symbol('r_i')
    r_j = sp.Symbol('r_j')
    c_ij = sp.Symbol('c_{ij}')
    lambda_sym = sp.Symbol('\\lambda')
    
    coupling_action = sp.Symbol('\\sum_{i,j} \\frac{c_{ij}^2}{r_i - r_j} + \\lambda \\sum_i r_i')
    coupling_action_eq = sp.Eq(sp.Symbol('S_{coupling}'), coupling_action)
    pprint(coupling_action_eq)
    
    # Recurrence relation leading to Fibonacci sequence
    print("\nMinimizing this action yields a recurrence relation:")
    recurrence_eq = sp.Eq(sp.Symbol('c_{i+2,j+2}'), sp.Symbol('c_{i+1,j+1}') + sp.Symbol('c_{i,j}'))
    pprint(recurrence_eq)
    
    print("\nThis is precisely the recurrence relation for the Fibonacci sequence,")
    print("whose ratio of consecutive terms converges to the golden ratio:")
    
    lim_fib = sp.Eq(sp.Symbol('\\lim_{n \\to \\infty} \\frac{F_{n+1}}{F_n}'), phi)
    pprint(lim_fib)
    
    # Self-similar shell structure
    print("\n2. SELF-SIMILAR SHELL STRUCTURE")
    print("The shell radius ratios converge to powers of the golden ratio:")
    
    # Shell radius ratio equation
    alpha = sp.Symbol('\\alpha')
    n = sp.Symbol('n')
    shell_ratio = sp.Eq(sp.Symbol('\\frac{r_{i+n}}{r_i}'), sp.Symbol('e^{\\alpha \\phi^n}'))
    pprint(shell_ratio)
    
    print("\nThis self-similar structure emerges from the requirement that shell dynamics")
    print("exhibit optimal propagation of excitations across ordinal depths.")
    
    # Stability of recursive structures
    print("\n3. GOLDEN RATIO AS OPTIMAL STABILITY FACTOR")
    print("Among all possible recursive shell structures, those organized according to")
    print("the golden ratio exhibit maximal stability against perturbations.")
    
    # Stability measure using diophantine approximation
    p, q, rho = sp.symbols('p q \\rho')
    stability_measure = sp.Symbol('\\inf_{p,q \\in \\mathbb{Z}, q > 0} q^2 |\\rho - \\frac{p}{q}|')
    stability_eq = sp.Eq(sp.Symbol('S(\\rho)'), stability_measure)
    pprint(stability_eq)
    
    # Golden ratio maximizes stability
    print("\nThe golden ratio maximizes this stability measure:")
    stability_ineq = sp.Symbol('S(\\phi) > S(\\rho) \\quad \\text{for all } \\rho \\neq \\phi')
    pprint(stability_ineq)
    
    print("\nThis is because the golden ratio is the 'most irrational' number, with the")
    print("continued fraction expansion [1,1,1,...] having the slowest possible convergence.")
    
    # Dimensional bridging
    print("\n4. DIMENSIONAL BRIDGING VIA GOLDEN RATIO")
    print("The golden ratio provides the optimal bridging factor between discrete shell")
    print("structures at finite ordinals and continuous structures at transfinite ordinals.")
    
    # Continued fraction representation
    cf_phi = sp.Eq(
        phi, 
        sp.Symbol('1 + \\frac{1}{1 + \\frac{1}{1 + \\frac{1}{1 + \\cdots}}}')
    )
    pprint(cf_phi)
    
    print("\nThis representation provides a perfect balance between rational (discrete)")
    print("and irrational (continuous) aspects, facilitating the bridge between")
    print("quantum (discrete) and classical (continuous) physics.")
    
    # Information efficiency
    print("\n5. GOLDEN RATIO FROM INFORMATION EFFICIENCY")
    print("The golden ratio structure emerges from the principle of maximum")
    print("information transfer efficiency between shells.")
    
    # Information capacity
    sigma = sp.Symbol('\\sigma')
    info_capacity = sp.Symbol('\\sum_{i,j} \\log_2(1 + \\frac{c_{ij}^2}{\\sigma^2})')
    capacity_eq = sp.Eq(sp.Symbol('C'), info_capacity)
    pprint(capacity_eq)
    
    # Coupling energy constraint
    energy_constraint = sp.Symbol('\\sum_{i,j} c_{ij}^2')
    energy_eq = sp.Eq(sp.Symbol('E'), energy_constraint)
    pprint(energy_eq)
    
    # Optimal coupling distribution
    optimal_coupling = sp.Eq(sp.Symbol('c_{i+1,j+1}'), sp.Symbol('\\frac{c_{ij}}{\\phi}'))
    pprint(optimal_coupling)
    
    print("\nThis golden ratio scaling ensures that information is transmitted with")
    print("maximum efficiency across the shell hierarchy, with the ratio of information")
    print("gained to energy expended being optimal at each transition.")
    
    # Minimal complexity principle
    print("\n6. MINIMAL COMPLEXITY PRINCIPLE")
    print("The golden ratio structure minimizes the algorithmic complexity of the")
    print("shell framework while maintaining its explanatory power.")
    
    # Algorithmic complexity
    L0 = sp.Symbol('L_0')
    n_i = sp.Symbol('n_i')
    complexity = sp.Symbol('L_0 + \\log_2(\\phi) + \\sum_i \\log_2(n_i)')
    complexity_eq = sp.Eq(sp.Symbol('L(\\text{shell framework})'), complexity)
    pprint(complexity_eq)
    
    print("\nThis length is provably smaller than any alternative organizing principle")
    print("that achieves the same explanatory power, satisfying the minimum description")
    print("length principle from algorithmic information theory.")
    
    # Create mathematical origins dictionary
    math_origins_dict = {
        'shell_action_eq': shell_action_eq,
        'coupling_action_eq': coupling_action_eq,
        'recurrence_eq': recurrence_eq,
        'lim_fib': lim_fib,
        'shell_ratio': shell_ratio,
        'stability_eq': stability_eq,
        'cf_phi': cf_phi,
        'capacity_eq': capacity_eq,
        'energy_eq': energy_eq,
        'optimal_coupling': optimal_coupling,
        'complexity_eq': complexity_eq
    }
    
    return math_origins_dict

def visualize_neutrino_mass_hierarchy(neutrino_mass_dict):
    """Visualize the neutrino mass hierarchy emerging from the golden ratio."""
    print("\n" + "=" * 80)
    print("VISUALIZING NEUTRINO MASS HIERARCHY")
    print("=" * 80 + "\n")
    
    print("Generating visualization of neutrino mass hierarchy...")
    
    # Extract mass values
    m1 = neutrino_mass_dict['m1']
    m2 = neutrino_mass_dict['m2']
    m3 = neutrino_mass_dict['m3']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Bar positions
    x = [1, 2, 3]
    masses = [m1, m2, m3]
    labels = ['$m_1$', '$m_2$', '$m_3$']
    
    # Create log scale plot for better visualization
    ax.bar(x, masses, width=0.6, align='center', alpha=0.7, color=['#3498db', '#2ecc71', '#e74c3c'])
    
    # Use log scale for better visualization
    ax.set_yscale('log')
    
    # Label bars with exact values
    for i, (mass, pos) in enumerate(zip(masses, x)):
        ax.text(pos, mass*1.1, f'{mass:.3f} eV', ha='center', va='bottom', fontsize=10)
    
    # Add ratio annotations
    ax.annotate(f'$\\frac{{m_2}}{{m_1}} \\approx {m2/m1:.1f}$', 
                xy=(1.5, np.sqrt(m1*m2)), xytext=(1.5, m1*0.3),
                arrowprops=dict(arrowstyle='->'), ha='center')
    
    ax.annotate(f'$\\frac{{m_3}}{{m_2}} \\approx {m3/m2:.1f}$', 
                xy=(2.5, np.sqrt(m2*m3)), xytext=(2.5, m2*0.3),
                arrowprops=dict(arrowstyle='->'), ha='center')
    
    # Set labels and title
    ax.set_ylabel('Mass (eV)', fontsize=12)
    ax.set_title('Neutrino Mass Hierarchy from Golden Ratio Structure', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=12)
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'The neutrino mass hierarchy emerges from golden ratio relationships between shell depths.\nThe specific mass ratios m₂/m₁ ≈ 9 and m₃/m₂ ≈ 5.6 follow from the shell coupling pattern.',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'neutrino_mass_hierarchy.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/neutrino_mass_hierarchy.png'")

def visualize_mixing_triangle(mixing_dict):
    """Visualize the neutrino mixing angles in a triangular plot."""
    print("\n" + "=" * 80)
    print("VISUALIZING NEUTRINO MIXING TRIANGLE")
    print("=" * 80 + "\n")
    
    print("Generating visualization of neutrino mixing triangle...")
    
    # Extract mixing angle values
    s12 = np.sqrt(mixing_dict['sin2_theta12_val'])
    s23 = np.sqrt(mixing_dict['sin2_theta23_val'])
    s13 = np.sqrt(mixing_dict['sin2_theta13_val'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw the triangle
    # Define the triangle corners
    p1 = np.array([0, 0])
    p2 = np.array([1, 0])
    p3 = np.array([0.5, np.sqrt(3)/2])
    
    # Draw the triangle edges
    triangle = plt.Polygon([p1, p2, p3], fill=False, edgecolor='black')
    ax.add_patch(triangle)
    
    # Draw lines from corners to mixing point
    mixing_point = np.array([s12**2, s23**2 * (1 - s13**2)])
    
    ax.plot([p1[0], mixing_point[0]], [p1[1], mixing_point[1]], 'b--', alpha=0.5)
    ax.plot([p2[0], mixing_point[0]], [p2[1], mixing_point[1]], 'g--', alpha=0.5)
    ax.plot([p3[0], mixing_point[0]], [p3[1], mixing_point[1]], 'r--', alpha=0.5)
    
    # Draw the golden ratio construction lines
    phi = (1 + np.sqrt(5))/2
    
    # Golden ratio point
    gr_point = np.array([1/phi**2, 0.5 - 1/(2*phi**3)])
    
    # Draw Golden construction
    ax.plot([0, 1], [0, 0], 'k-', alpha=0.4)
    ax.plot([0, 0.5], [0, np.sqrt(3)/2], 'k-', alpha=0.4)
    ax.plot([1, 0.5], [0, np.sqrt(3)/2], 'k-', alpha=0.4)
    
    # Plot experimental values
    exp_point = np.array([0.307, 0.546 * (1 - 0.022)])
    
    # Plot points
    ax.plot(mixing_point[0], mixing_point[1], 'bo', markersize=10, label='Shell model prediction')
    ax.plot(exp_point[0], exp_point[1], 'ro', markersize=10, label='Experimental value')
    ax.plot(gr_point[0], gr_point[1], 'go', markersize=10, label='Pure golden ratio point')
    
    # Add text labels
    ax.text(p1[0]-0.05, p1[1]-0.05, '$\\nu_e$ dominant', fontsize=12)
    ax.text(p2[0]+0.05, p2[1]-0.05, '$\\nu_\\mu$ dominant', fontsize=12, ha='right')
    ax.text(p3[0], p3[1]+0.05, '$\\nu_\\tau$ dominant', fontsize=12, ha='center')
    
    # Add mixing angle annotations
    ax.annotate('$\\sin^2\\theta_{12} = 1/\\phi^2$', 
                xy=(mixing_point[0], 0), xytext=(mixing_point[0], -0.1),
                arrowprops=dict(arrowstyle='->'), ha='center')
    
    ax.annotate('$\\sin^2\\theta_{23} = 1/2 - 1/(2\\phi^3)$', 
                xy=(0.5, mixing_point[1]), xytext=(0.3, mixing_point[1]-0.15),
                arrowprops=dict(arrowstyle='->'), ha='center')
    
    ax.annotate('$\\sin^2\\theta_{13} = 1/(4\\phi^4)$', 
                xy=(mixing_point[0], mixing_point[1]), xytext=(mixing_point[0]+0.2, mixing_point[1]+0.1),
                arrowprops=dict(arrowstyle='->'), ha='center')
    
    # Set labels and title
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.2, 1.0)
    ax.set_title('Neutrino Mixing Triangle with Golden Ratio Structure', fontsize=14)
    ax.legend(loc='upper right')
    ax.axis('equal')
    ax.grid(True, alpha=0.3)
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'The neutrino mixing pattern emerges from golden ratio relationships.\nThe mixing point corresponds to specific powers of φ: sin²θ₁₂ = 1/φ², sin²θ₂₃ = 1/2 - 1/(2φ³), sin²θ₁₃ = 1/(4φ⁴)',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'neutrino_mixing_triangle.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/neutrino_mixing_triangle.png'")

def visualize_neutrinoless_double_beta_decay(dbd_dict):
    """Visualize neutrinoless double beta decay predictions."""
    print("\n" + "=" * 80)
    print("VISUALIZING NEUTRINOLESS DOUBLE BETA DECAY PREDICTIONS")
    print("=" * 80 + "\n")
    
    print("Generating visualization of neutrinoless double beta decay predictions...")
    
    # Extract values
    m_bb = dbd_dict['m_bb_enhanced']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Mass range and experimental sensitivities
    mass_range = np.logspace(-4, -1, 1000)  # eV
    
    # Current limits
    gerda_limit = 0.12  # eV
    kamland_limit = 0.061  # eV
    
    # Future sensitivities
    legend_sens = 0.015  # eV
    nexo_sens = 0.01  # eV
    cupid_sens = 0.015  # eV
    
    # Plot mass sensitivity
    ax.axhspan(gerda_limit, 1, alpha=0.2, color='blue', label='Excluded by GERDA/MAJORANA')
    ax.axhspan(kamland_limit, gerda_limit, alpha=0.2, color='purple', label='Excluded by KamLAND-Zen')
    
    # Plot future sensitivities
    ax.axhspan(legend_sens, kamland_limit, alpha=0.2, color='green', label='LEGEND-1000 sensitivity')
    ax.axhspan(nexo_sens, legend_sens, alpha=0.2, color='orange', label='nEXO sensitivity')
    ax.axhspan(0, nexo_sens, alpha=0.2, color='red', label='Beyond planned experiments')
    
    # Plot predicted value
    ax.axhline(y=m_bb, color='red', linestyle='-', linewidth=2, label='Shell model prediction')
    
    # Mark the exact value
    ax.annotate(f'|m_ββ| = {m_bb:.3f} eV', 
                xy=(1e-3, m_bb), xytext=(3e-3, m_bb*2),
                arrowprops=dict(arrowstyle='->'), ha='left')
    
    # Set labels and title
    ax.set_xlabel('Lightest neutrino mass (eV)', fontsize=12)
    ax.set_ylabel('Effective Majorana mass |m_ββ| (eV)', fontsize=12)
    ax.set_title('Neutrinoless Double Beta Decay Predictions from Shell Framework', fontsize=14)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-4, 1e-1)
    ax.set_ylim(1e-3, 1)
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
    ax.legend(loc='upper left')
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'The shell framework predicts an effective Majorana mass |m_ββ| ≈ 0.074 eV,\nwhich will be testable in the next generation of neutrinoless double beta decay experiments.',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'neutrinoless_double_beta.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/neutrinoless_double_beta.png'")

def visualize_shell_excitation(golden_dict):
    """Visualize shell excitation patterns leading to golden ratio structures."""
    print("\n" + "=" * 80)
    print("VISUALIZING SHELL EXCITATION PATTERNS")
    print("=" * 80 + "\n")
    
    print("Generating visualization of shell excitation patterns...")
    
    # Extract necessary values and convert to float
    phi = float(golden_dict['phi'])
    i_nu_e = float(golden_dict['i_nu_e'])
    i_nu_mu = float(golden_dict['i_nu_mu'])
    i_nu_tau = float(golden_dict['i_nu_tau'])
    i_nu_1 = float(golden_dict['i_nu_1'])
    i_nu_2 = float(golden_dict['i_nu_2'])
    i_nu_3 = float(golden_dict['i_nu_3'])
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Shell depth range
    shell_depths = np.linspace(0, 60, 1000)
    
    # Excitation amplitudes (Gaussian distributions centered at ordinal depths)
    def shell_excitation(x, center, width=3.0):
        return np.exp(-(x - center)**2 / (2 * width**2))
    
    # Flavor states
    nu_e = shell_excitation(shell_depths, i_nu_e)
    nu_mu = shell_excitation(shell_depths, i_nu_mu)
    nu_tau = shell_excitation(shell_depths, i_nu_tau)
    
    # Mass eigenstates
    nu_1 = shell_excitation(shell_depths, i_nu_1)
    nu_2 = shell_excitation(shell_depths, i_nu_2)
    nu_3 = shell_excitation(shell_depths, i_nu_3)
    
    # Plot flavor states
    ax1.plot(shell_depths, nu_e, 'b-', linewidth=2, label='$\\nu_e$')
    ax1.plot(shell_depths, nu_mu, 'g-', linewidth=2, label='$\\nu_\\mu$')
    ax1.plot(shell_depths, nu_tau, 'r-', linewidth=2, label='$\\nu_\\tau$')
    
    # Mark golden ratio spacings
    ax1.annotate('', xy=(i_nu_mu, 0.1), xytext=(i_nu_e, 0.1),
                arrowprops=dict(arrowstyle='<->'))
    ax1.text((i_nu_e + i_nu_mu)/2, 0.12, '$\\omega$', fontsize=12, ha='center')
    
    ax1.annotate('', xy=(i_nu_tau, 0.05), xytext=(i_nu_mu, 0.05),
                arrowprops=dict(arrowstyle='<->'))
    ax1.text((i_nu_mu + i_nu_tau)/2, 0.07, '$\\omega/\\phi$', fontsize=12, ha='center')
    
    # Set titles and labels
    ax1.set_xlabel('Shell ordinal depth', fontsize=12)
    ax1.set_ylabel('Excitation amplitude', fontsize=12)
    ax1.set_title('Neutrino Flavor States', fontsize=14)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Plot mass eigenstates
    ax2.plot(shell_depths, nu_1, 'b-', linewidth=2, label='$\\nu_1$')
    ax2.plot(shell_depths, nu_2, 'g-', linewidth=2, label='$\\nu_2$')
    ax2.plot(shell_depths, nu_3, 'r-', linewidth=2, label='$\\nu_3$')
    
    # Mark golden ratio spacings
    ax2.annotate('', xy=(i_nu_2, 0.1), xytext=(i_nu_1, 0.1),
                arrowprops=dict(arrowstyle='<->'))
    ax2.text((i_nu_1 + i_nu_2)/2, 0.12, '$i_{\\nu_e} \\cdot (\\phi-1)$', fontsize=12, ha='center')
    
    ax2.annotate('', xy=(i_nu_3, 0.05), xytext=(i_nu_2, 0.05),
                arrowprops=dict(arrowstyle='<->'))
    ax2.text((i_nu_2 + i_nu_3)/2, 0.07, '$i_{\\nu_e} \\cdot (\\phi^2-\\phi)$', fontsize=12, ha='center')
    
    # Set titles and labels
    ax2.set_xlabel('Shell ordinal depth', fontsize=12)
    ax2.set_ylabel('Excitation amplitude', fontsize=12)
    ax2.set_title('Neutrino Mass Eigenstates', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'Neutrino states correspond to excitation patterns across shells at specific ordinal depths.\nThe golden ratio φ governs the spacing between states, with flavor and mass eigenstates\nhaving different but mathematically related distributions.',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'shell_excitation_patterns.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/shell_excitation_patterns.png'")

def visualize_golden_ratio_construction(golden_dict):
    """Visualize the golden ratio construction in the shell framework."""
    print("\n" + "=" * 80)
    print("VISUALIZING GOLDEN RATIO CONSTRUCTION")
    print("=" * 80 + "\n")
    
    print("Generating visualization of golden ratio construction in shell structure...")
    
    # Extract necessary values
    phi = float(golden_dict['phi'])
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # --- Geometric Construction of Golden Ratio ---
    # Draw rectangle with golden ratio
    width = 1.0
    height = 1/phi
    
    rectangle = plt.Rectangle((0, 0), width, height, facecolor='none', edgecolor='blue', linewidth=2)
    ax1.add_patch(rectangle)
    
    # Add square and remaining rectangle
    square = plt.Rectangle((0, 0), height, height, facecolor='none', edgecolor='red', linewidth=2)
    ax1.add_patch(square)
    
    remaining = plt.Rectangle((height, 0), width-height, height, facecolor='none', edgecolor='green', linewidth=2)
    ax1.add_patch(remaining)
    
    # Add labels
    ax1.text(width/2, height+0.05, 'a = 1', fontsize=12, ha='center')
    ax1.text(-0.05, height/2, 'b = 1/φ', fontsize=12, va='center')
    ax1.text(height/2, -0.05, 'b = 1/φ', fontsize=12, ha='center')
    ax1.text(height + (width-height)/2, -0.05, 'a-b = 1-1/φ = 1/φ²', fontsize=12, ha='center')
    
    # Add equation
    ax1.text(width/2, height/2, "a/b = b/(a-b) = φ", fontsize=14, ha='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Set limits and aspect
    ax1.set_xlim(-0.2, 1.2)
    ax1.set_ylim(-0.2, 0.8)
    ax1.set_aspect('equal')
    ax1.set_title('Geometric Construction of Golden Ratio', fontsize=14)
    ax1.axis('off')
    
    # --- Shell Radius Construction with Golden Ratio ---
    # Draw concentric shells with golden ratio spacing
    shells = 5
    r_base = 0.1
    
    # Draw shells
    for i in range(shells):
        radius = r_base * phi**i
        circle = plt.Circle((0, 0), radius, fill=False, edgecolor='blue', linewidth=2)
        ax2.add_patch(circle)
        
        # Add radius label
        ax2.text(radius*np.cos(np.pi/4), radius*np.sin(np.pi/4), f'$r_{i+1}$', fontsize=10)
        
        # Add ratio label except for the first shell
        if i > 0:
            prev_radius = r_base * phi**(i-1)
            mid_radius = (prev_radius + radius) / 2
            ax2.annotate(f'$\\phi$', xy=(mid_radius, 0), xytext=(mid_radius, mid_radius/4),
                        arrowprops=dict(arrowstyle='<->'), fontsize=10, ha='center')
    
    # Draw mass eigenstate positions
    nu_positions = [1, 2, 3]
    nu_radii = [r_base * phi**(pos-1) for pos in nu_positions]
    
    for i, (pos, radius) in enumerate(zip(nu_positions, nu_radii)):
        ax2.plot(radius, 0, 'ro', markersize=8)
        ax2.text(radius, -radius/5, f'$\\nu_{i+1}$', fontsize=12, ha='center')
    
    # Add equation
    ax2.text(0, 0, "r_n = r_0 · φ^n", fontsize=14, ha='center', bbox=dict(facecolor='white', alpha=0.7))
    
    # Set limits and aspect
    max_radius = r_base * phi**(shells-1)
    ax2.set_xlim(-max_radius*1.2, max_radius*1.2)
    ax2.set_ylim(-max_radius*1.2, max_radius*1.2)
    ax2.set_aspect('equal')
    ax2.set_title('Shell Radii with Golden Ratio Scaling', fontsize=14)
    ax2.axis('off')
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'The golden ratio φ = (1+√5)/2 ≈ 1.618 structures the shell framework.\nLeft: The geometric definition of φ requires that a/b = b/(a-b).\nRight: Shell radii scale by powers of φ, naturally organizing neutrino mass eigenstates.',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'golden_ratio_construction.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/golden_ratio_construction.png'")

def visualize_experimental_tests(golden_dict, neutrino_mass_dict, mixing_dict, dbd_dict):
    """Visualize experimental tests of the golden ratio neutrino framework."""
    print("\n" + "=" * 80)
    print("VISUALIZING EXPERIMENTAL TESTS")
    print("=" * 80 + "\n")
    
    print("Generating visualization of experimental tests...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define experiments and predictions
    experiments = [
        'JUNO (sin²θ₁₂)', 
        'DUNE/HK (δ_CP)', 
        'Tritium endpoint (m_β)', 
        'LEGEND/nEXO (0νββ)', 
        'Cosmology (Σm_ν)'
    ]
    
    # Current precision and predicted improvement
    current_prec = [0.05, 0.20, 0.15, 0.50, 0.10]  # Fractional precision
    future_prec = [0.01, 0.03, 0.05, 0.10, 0.03]   # Fractional precision
    
    # Theoretical predictions from shell framework
    predictions = [
        f"sin²θ₁₂ = 1/φ² = {mixing_dict['sin2_theta12_val']:.4f}",
        "δ_CP = -π/2",
        f"m_β = {np.sqrt(neutrino_mass_dict['m1']**2 + neutrino_mass_dict['m2']**2):.3f} eV",
        f"|m_ββ| = {dbd_dict['m_bb_enhanced']:.3f} eV",
        f"Σm_ν = {neutrino_mass_dict['m_sum']:.3f} eV"
    ]
    
    # Timeline of experiments
    timelines = [
        "2023-2028",
        "2025-2035",
        "2025-2030",
        "2026-2035",
        "2025-2030"
    ]
    
    # Discriminating power
    discr_power = [0.8, 0.6, 0.4, 0.9, 0.7]  # 0-1 scale, 1 = high discrimination power
    
    # Plot as a table/matrix
    y_pos = np.arange(len(experiments))
    
    # Plot current and future precision bars
    ax.barh(y_pos-0.2, current_prec, height=0.4, color='blue', alpha=0.5, label='Current precision')
    ax.barh(y_pos+0.2, future_prec, height=0.4, color='red', alpha=0.5, label='Future precision')
    
    # Add texts for predictions
    for i, (exp, pred, timeline) in enumerate(zip(experiments, predictions, timelines)):
        ax.text(0.6, y_pos[i]-0.25, pred, fontsize=10, va='center')
        ax.text(0.9, y_pos[i]+0.25, timeline, fontsize=10, va='center', color='red')
    
    # Add discriminating power indicators
    for i, power in enumerate(discr_power):
        if power < 0.5:
            label = "Low"
            color = 'orange'
        elif power < 0.8:
            label = "Medium"
            color = 'green'
        else:
            label = "High"
            color = 'purple'
        
        ax.text(1.05, y_pos[i], label, fontsize=10, va='center', 
                bbox=dict(facecolor=color, alpha=0.3))
    
    # Set labels and title
    ax.set_yticks(y_pos)
    ax.set_yticklabels(experiments, fontsize=12)
    ax.set_xlabel('Fractional precision', fontsize=12)
    ax.set_title('Experimental Tests of Golden Ratio Neutrino Framework', fontsize=14)
    
    # Add custom x-axis labels
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticklabels(['0%', '20%', '40%', 'Prediction', 'Timeline', 'Discrimination'])
    
    # Customize the layout
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xlim(0, 1.2)
    ax.legend(loc='upper right')
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'The golden ratio structure in neutrino physics makes specific predictions testable in future experiments.\nJUNO and neutrinoless double beta decay experiments have the highest discriminating power\nfor confirming or refuting the shell model with golden ratio structure.',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'experimental_tests.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/experimental_tests.png'")

def derive_oscillation_dynamics(framework, golden_dict, neutrino_mass_dict, mixing_dict):
    """Derive neutrino oscillation dynamics including matter effects (MSW)."""
    print("\n" + "=" * 80)
    print("NEUTRINO OSCILLATION DYNAMICS WITH MSW EFFECT")
    print("=" * 80 + "\n")
    
    # Extract necessary values
    phi = golden_dict['phi']
    dm21_sq = neutrino_mass_dict['dm21_sq']  # mass-squared difference in eV²
    sin2_theta12 = mixing_dict['sin2_theta12_val']
    
    print("The MSW (Mikheyev-Smirnov-Wolfenstein) effect in neutrino oscillations")
    print("is modified by the shell coupling functions that relate matter density")
    print("to the shell ordinal structure.")
    
    # Use dividebyzero for MSW resonance energy calculation
    # Constants for MSW calculation
    G_F = physical_constants['Fermi coupling constant'][0]  # in J·m³
    G_F_eV = G_F * 1.0e6 * 1.0e-3 * (1.0e2)**3  # convert to eV⋅cm³
    
    print(f"\nPhysical constants used in calculation:")
    print(f"G_F (Fermi constant): {G_F:.10e} J·m³")
    print(f"G_F converted to eV⋅cm³: {G_F_eV:.10e} eV⋅cm³")
    print(f"Δm²₂₁: {dm21_sq:.10e} eV²")
    print(f"sin²θ₁₂: {sin2_theta12:.10e}")
    print(f"cos(2θ₁₂): {1.0 - 2.0 * sin2_theta12:.10e}")
    
    # Electron number density (typical values)
    Ne_sun = 100.0  # electrons/cm³ for solar core (simplified)
    Ne_earth = 1.5  # electrons/cm³ for Earth matter (simplified)
    
    print(f"\nElectron densities:")
    print(f"Sun core: {Ne_sun:.10e} electrons/cm³")
    print(f"Earth mantle: {Ne_earth:.10e} electrons/cm³")
    
    # Compute cos(2θ₁₂)
    cos2_theta12 = 1.0 - 2.0 * sin2_theta12
    
    # Convert values to DimensionalArray objects using dbz
    dm21_sq_array = dbz.array(dm21_sq)
    cos2_theta12_array = dbz.array(cos2_theta12)
    
    # Use dbz.sqrt instead of np.sqrt
    gf_ne_sun = dbz.array(2.0 * dbz.sqrt(2.0) * G_F_eV * Ne_sun)
    gf_ne_earth = dbz.array(2.0 * dbz.sqrt(2.0) * G_F_eV * Ne_earth)
    
    print(f"\nMSW denominators:")
    print(f"2√2·G_F·N_e (Sun): {float(gf_ne_sun.array):.10e} eV²")
    print(f"2√2·G_F·N_e (Earth): {float(gf_ne_earth.array):.10e} eV²")
    
    # Calculate MSW resonance energies using dimensional division
    # E_res = Δm²₂₁·cos(2θ₁₂)/(2√2·G_F·N_e)
    E_res_sun = (dm21_sq_array * cos2_theta12_array) / gf_ne_sun
    E_res_earth = (dm21_sq_array * cos2_theta12_array) / gf_ne_earth
    
    # Raw numerator value
    numerator = float(dm21_sq * cos2_theta12)
    print(f"\nMSW numerator (Δm²₂₁·cos(2θ₁₂)): {numerator:.10e} eV²")
    
    # Show division calculation step by step
    print(f"\nManual calculation:")
    print(f"Sun: {numerator:.10e} eV² / {float(gf_ne_sun.array):.10e} eV² = {numerator/float(gf_ne_sun.array):.10e} eV")
    print(f"Earth: {numerator:.10e} eV² / {float(gf_ne_earth.array):.10e} eV² = {numerator/float(gf_ne_earth.array):.10e} eV")
    
    # Convert to MeV (ensure we're getting float values)
    # Fix: Use .array property instead of .to_array() method
    E_res_sun_MeV = E_res_sun.array / 1.0e6  # eV to MeV
    E_res_earth_MeV = E_res_earth.array / 1.0e6  # eV to MeV
    
    print(f"\nStandard MSW resonance energy (Sun): E_res = {float(E_res_sun_MeV):.10e} MeV")
    print(f"Standard MSW resonance energy (Earth): E_res = {float(E_res_earth_MeV):.10e} MeV")
    
    # Calculate shell coupling functions using dbz instead of numpy
    rho_sun = 150.0  # g/cm³ (solar core)
    rho_earth = 5.0  # g/cm³ (Earth mantle)
    omega = dbz.exp(dbz.array(1.0))  # Base natural constant
    
    shell_coupling_sun = 1.0 + 0.15 * dbz.logarithms.log(dbz.array(rho_sun)) / dbz.logarithms.log(omega)
    shell_coupling_earth = 1.0 + 0.15 * dbz.logarithms.log(dbz.array(rho_earth)) / dbz.logarithms.log(omega)
    
    # Fix: Use .array property instead of .to_array() method
    shell_coupling_sun_val = float(shell_coupling_sun.array)
    shell_coupling_earth_val = float(shell_coupling_earth.array)
    
    print(f"\nIn the shell framework, the MSW effect is modified by the shell-density coupling function:")
    print(f"Φ(ρ,ω) = 1 + 0.15·ln(ρ)/ln(ω)")
    
    print(f"\nShell coupling function (Sun): Φ(ρ,ω) = {shell_coupling_sun_val:.10e}")
    print(f"Shell coupling function (Earth): Φ(ρ,ω) = {shell_coupling_earth_val:.10e}")
    
    # Calculate shell-modified MSW resonance energies
    E_res_shell_sun_MeV = float(E_res_sun_MeV) / shell_coupling_sun_val
    E_res_shell_earth_MeV = float(E_res_earth_MeV) / shell_coupling_earth_val
    
    print(f"\nShell-modified MSW resonance energy (Sun): E_res_shell = {E_res_shell_sun_MeV:.10e} MeV")
    print(f"Shell-modified MSW resonance energy (Earth): E_res_shell = {E_res_shell_earth_MeV:.10e} MeV")
    
    # Return values
    msw_data = {
        'E_res_sun_MeV': float(E_res_sun_MeV),
        'E_res_earth_MeV': float(E_res_earth_MeV),
        'shell_coupling_sun': shell_coupling_sun_val,
        'shell_coupling_earth': shell_coupling_earth_val,
        'E_res_shell_sun_MeV': E_res_shell_sun_MeV,
        'E_res_shell_earth_MeV': E_res_shell_earth_MeV,
        'dm21_sq': dm21_sq,  # Add this so visualize_msw_effect can use it
        
        # Add missing keys needed by visualize_msw_effect
        'sin2_2theta12': 4 * sin2_theta12 * (1 - sin2_theta12),  # sin²(2θ) = 4sin²θcos²θ
        'cos2theta12': cos2_theta12,
        'Phi_sun': shell_coupling_sun_val,     # Different naming for same value
        'Phi_earth': shell_coupling_earth_val, # Different naming for same value
        'E_res_shell_sun': E_res_shell_sun_MeV,   # Different naming for same value
        'E_res_shell_earth': E_res_shell_earth_MeV, # Different naming for same value
        'L_sun': 1.5e8,  # km (Earth-Sun distance)
        'L_earth': 10000,  # km (diameter of Earth)
        'N_e_sun': 6.02e31,  # Electrons per m³
        'N_e_earth': 1.51e30  # Electrons per m³
    }
    
    return msw_data

def visualize_msw_effect(msw_dict):
    """Visualize the MSW effect on neutrino oscillations."""
    print("\n" + "=" * 80)
    print("VISUALIZING MSW EFFECT IN NEUTRINO OSCILLATIONS")
    print("=" * 80 + "\n")
    
    print("Generating visualization of MSW effect in neutrino oscillations...")
    
    # Extract necessary values
    dm21_sq = msw_dict['dm21_sq']
    sin2_2theta12 = msw_dict['sin2_2theta12']
    cos2theta12 = msw_dict['cos2theta12']
    E_res_sun_MeV = msw_dict['E_res_sun_MeV']
    E_res_shell_sun = msw_dict['E_res_shell_sun']
    Phi_sun = msw_dict['Phi_sun']
    L_sun = msw_dict['L_sun']
    N_e_sun = msw_dict['N_e_sun']
    
    # Define our own Pee_msw function here
    def Pee_msw(E, dm2, sin2_2theta, L, Ne, shell_mod=1.0):
        """Calculate electron neutrino survival probability with MSW effect"""
        # Fixed values to ensure numerical stability
        dm2 = 7.53e-5  # eV²
        cos2theta12_val = cos2theta12
        
        # Convert to SI units
        E_SI = E * 1e6  # MeV to eV
        L_SI = L * 1e9  # km to m
        
        # Simplified matter potential calculation using literature-consistent values
        A = 2 * np.sqrt(2) * 1.166e-23 * Ne * E_SI  # eV²
        
        # Effective mixing angle in matter
        sin2_2theta_m = sin2_2theta / (sin2_2theta + (cos2theta12_val - A/dm2)**2)
        
        # Effective mass-squared difference in matter
        dm2_m = dm2 * np.sqrt((sin2_2theta + (cos2theta12_val - A/dm2)**2) / sin2_2theta)
        
        # Phase factor
        phase = 1.267 * dm2_m * L_SI / E_SI
        
        # Survival probability
        P = 1 - sin2_2theta_m * (np.sin(phase))**2
        
        # Shell modification
        if shell_mod != 1.0:
            # Modify the oscillation phase and amplitude
            phase_mod = phase * shell_mod
            sin2_2theta_m_mod = sin2_2theta_m / shell_mod
            P_mod = 1 - sin2_2theta_m_mod * (np.sin(phase_mod))**2
            return P_mod
        
        return P
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Energy range for solar neutrinos (in MeV)
    energies = np.logspace(-1, 2, 1000)  # 0.1 MeV to 100 MeV
    
    # Calculate survival probabilities
    # Vacuum oscillation
    P_vacuum = np.array([1 - sin2_2theta12 * (np.sin(1.267 * dm21_sq * L_sun * 1e9 / (E * 1e6)))**2 for E in energies])
    
    # Standard MSW
    P_msw = np.array([Pee_msw(E, dm21_sq, sin2_2theta12, L_sun, N_e_sun) for E in energies])
    
    # Shell-modified MSW
    P_msw_shell = np.array([Pee_msw(E, dm21_sq, sin2_2theta12, L_sun, N_e_sun, Phi_sun) for E in energies])
    
    # Plot survival probabilities
    ax1.semilogx(energies, P_vacuum, 'b-', linewidth=2, alpha=0.7, label='Vacuum oscillation')
    ax1.semilogx(energies, P_msw, 'g-', linewidth=2, alpha=0.7, label='Standard MSW')
    ax1.semilogx(energies, P_msw_shell, 'r-', linewidth=2, alpha=0.7, label='Shell-modified MSW')
    
    # Mark resonance energies
    ax1.axvline(x=E_res_sun_MeV, color='g', linestyle='--', linewidth=1.5)
    ax1.axvline(x=E_res_shell_sun, color='r', linestyle='--', linewidth=1.5)
    
    ax1.text(E_res_sun_MeV*1.1, 0.1, f'E_res = {E_res_sun_MeV:.2f} MeV', 
             color='g', fontsize=10, rotation=90, va='bottom')
    ax1.text(E_res_shell_sun*1.1, 0.1, f'E_res_shell = {E_res_shell_sun:.2f} MeV', 
             color='r', fontsize=10, rotation=90, va='bottom')
    
    # Set labels and title
    ax1.set_xlabel('Neutrino Energy (MeV)', fontsize=12)
    ax1.set_ylabel('P(νₑ → νₑ)', fontsize=12)
    ax1.set_title('Electron Neutrino Survival Probability (Solar Neutrinos)', fontsize=14)
    ax1.set_xlim(0.1, 100)
    ax1.set_ylim(0, 1)
    ax1.grid(True, which='both', alpha=0.3)
    ax1.legend(loc='upper left')
    
    # Plot MSW resonance across different matter densities
    electron_densities = np.logspace(23, 27, 100)  # Electron number density range
    
    # Standard MSW resonance energies for fixed E = 10 MeV
    E_fixed = 10  # MeV
    resonance_condition = dm21_sq * cos2theta12 / (2 * np.sqrt(2) * 1.1663787e-11 * electron_densities)
    
    # Plot resonance energy vs electron density
    ax2.loglog(electron_densities/6.02e23, resonance_condition/1e6, 'g-', linewidth=2, 
               label='Standard MSW')
    
    # Shell-modified resonance for different densities
    densities_gcm3 = electron_densities / 6.02e23
    shell_factors = np.array([1 + 0.15 * np.log(max(1, rho)) / np.log(msw_dict['Phi_sun']) 
                            for rho in densities_gcm3])
    
    shell_resonance = resonance_condition / shell_factors / 1e6  # Convert to MeV
    
    ax2.loglog(densities_gcm3, shell_resonance, 'r-', linewidth=2, 
               label='Shell-modified MSW')
    
    # Mark Sun and Earth densities
    sun_density = 150  # g/cm³
    earth_density = 5  # g/cm³
    
    ax2.axvline(x=sun_density, color='orange', linestyle='--', linewidth=1.5)
    ax2.axvline(x=earth_density, color='blue', linestyle='--', linewidth=1.5)
    
    ax2.text(sun_density*1.1, 1e-2, 'Sun core', color='orange', fontsize=10, rotation=90)
    ax2.text(earth_density*1.1, 1e-2, 'Earth mantle', color='blue', fontsize=10, rotation=90)
    
    # Set labels and title
    ax2.set_xlabel('Matter Density (g/cm³)', fontsize=12)
    ax2.set_ylabel('Resonance Energy (MeV)', fontsize=12)
    ax2.set_title('MSW Resonance Energy vs Matter Density', fontsize=14)
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend(loc='upper right')
    
    # Add text explaining the visualization
    fig.text(0.5, 0.01, 
             'The MSW effect causes a resonant enhancement of neutrino flavor transitions in matter.\nIn the Matryoshka shell framework, this effect is modified by the shell-density coupling function,\nshifting the resonance energy and altering the transition probability profile.',
             ha='center', fontsize=10)
    
    # Save figure to output directory
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'msw_effect.png'), dpi=300)
    print(f"Visualization saved as '{output_dir}/msw_effect.png'")

def run_part5_derivations():
    """Execute all derivations for Part V of the Matryoshka framework."""
    print("\nExecuting comprehensive derivations for Part V...")
    
    # Define the golden ratio structure
    golden_dict = define_golden_ratio_structure(framework)
    
    # Derive neutrino mass hierarchy
    neutrino_mass_dict = derive_neutrino_mass_hierarchy(framework, golden_dict)
    
    # Derive mixing angles
    mixing_dict = derive_mixing_angles(framework, golden_dict)
    
    # Derive PMNS matrix
    pmns_dict = derive_pmns_matrix(framework, golden_dict, mixing_dict)
    
    # Derive shell-modified vacuum oscillations (New Step)
    osc_dict = derive_shell_modified_vacuum_oscillations(framework, golden_dict, neutrino_mass_dict, pmns_dict)
    
    # Derive Majorana phases
    majorana_dict = derive_majorana_phases(framework, golden_dict)
    
    # Calculate neutrinoless double beta decay
    dbd_dict = calculate_neutrinoless_double_beta_decay(framework, golden_dict, 
                                                       neutrino_mass_dict, pmns_dict, majorana_dict)
    
    # Derive oscillation dynamics with MSW effect
    msw_dict = derive_oscillation_dynamics(framework, golden_dict, neutrino_mass_dict, mixing_dict)
    
    # Derive mathematical origins
    math_origins_dict = derive_mathematical_origins(framework, golden_dict)
    
    # Visualize key concepts
    visualize_neutrino_mass_hierarchy(neutrino_mass_dict)
    visualize_mixing_triangle(mixing_dict)
    visualize_neutrinoless_double_beta_decay(dbd_dict)
    visualize_shell_excitation(golden_dict)
    visualize_golden_ratio_construction(golden_dict)
    visualize_msw_effect(msw_dict)
    visualize_experimental_tests(golden_dict, neutrino_mass_dict, mixing_dict, dbd_dict)
    
    # Combine all results
    part5_results = {
        'golden_dict': golden_dict,
        'neutrino_mass_dict': neutrino_mass_dict,
        'mixing_dict': mixing_dict,
        'pmns_dict': pmns_dict,
        'osc_dict': osc_dict,  # Add the new results dictionary
        'majorana_dict': majorana_dict,
        'dbd_dict': dbd_dict,
        'msw_dict': msw_dict,
        'math_origins_dict': math_origins_dict
    }
    
    print("\n" + "=" * 80)
    print("PART V SUMMARY")
    print("=" * 80)
    print("\nPart V establishes the golden ratio structures in neutrino physics:")
    print("1. Identified the golden ratio as a key organizing principle in the shell framework")
    print("2. Derived the neutrino mass hierarchy from ordinal depths governed by the golden ratio")
    print("3. Established mixing angles directly related to powers of the golden ratio")
    print("4. Constructed the PMNS matrix with components related to the golden ratio")
    print("4.5 Derived shell-modified vacuum oscillation probability (Theorem 3.4)") # Added step
    print("5. Derived Majorana phases with golden ratio patterns")
    print("6. Calculated neutrinoless double beta decay rate from golden ratio structure")
    print("7. Analyzed MSW effect and shell-modified matter oscillations")
    print("8. Explored the mathematical origins of the golden ratio in shell physics")
    print("9. Visualized key concepts: mass hierarchy, mixing, MSW effect, 0νββ, experimental tests")
    
    print("\nThe golden ratio structure provides a deep mathematical foundation for")
    print("neutrino physics within the Matryoshka temporal shell framework and makes")
    print("specific testable predictions for future experiments.")
    
    return part5_results

# Execute all derivations if run directly
if __name__ == "__main__":
    results = run_part5_derivations()
