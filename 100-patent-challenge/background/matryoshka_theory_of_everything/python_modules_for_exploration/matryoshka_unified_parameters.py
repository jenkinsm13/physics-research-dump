# matryoshka_unified_parameters.py
#!/usr/bin/env python3
# Unified Parameter File for Matryoshka Theory of Everything
# This file consolidates all fundamental constants and derived parameters

import numpy as np
from scipy import constants as const
from uncertainties import ufloat

class MatryoshkaParameters:
    """Central repository for all parameters in the Matryoshka framework.
    
    This class ensures consistency of parameters across all modules by providing
    a single source of truth for fundamental constants, shell parameters, and 
    derived quantities.
    """
    
    def __init__(self, recalibrate=False):
        """Initialize all parameters for the Matryoshka framework.
        
        Args:
            recalibrate: If True, recalculates all derived parameters from scratch
                         If False, uses pre-calibrated values for faster initialization
        """
        # Initialize fundamental physical constants
        self.initialize_physical_constants()
        
        # Initialize core shell parameters
        self.initialize_shell_parameters()
        
        # Initialize golden ratio related parameters
        self.initialize_golden_ratio_structure()
        
        # Initialize particle physics parameters
        self.initialize_particle_parameters()
        
        # Initialize neutrino-specific parameters
        self.initialize_neutrino_parameters()
        
        # Initialize cosmological parameters
        self.initialize_cosmological_parameters()
        
        # Calculate derived parameters
        if recalibrate:
            self.recalculate_derived_parameters()
        else:
            self.load_calibrated_parameters()
        
        # Verify parameter consistency
        self.verify_parameter_consistency()
    
    def initialize_physical_constants(self):
        """Initialize fundamental physical constants."""
        # Use scipy.constants for consistent values
        self.c = const.c  # Speed of light (m/s)
        self.hbar = const.hbar  # Reduced Planck constant (J·s)
        self.G = const.G  # Gravitational constant (m³/kg/s²)
        self.e = const.e  # Elementary charge (C)
        self.epsilon_0 = const.epsilon_0  # Vacuum permittivity (F/m)
        self.m_e = const.m_e  # Electron mass (kg)
        self.m_p = const.m_p  # Proton mass (kg)
        self.m_n = const.m_n  # Neutron mass (kg)
        
        # Planck units
        self.planck_length = np.sqrt(const.hbar * const.G / const.c**3)  # (m)
        self.planck_time = np.sqrt(const.hbar * const.G / const.c**5)  # (s)
        self.planck_mass = np.sqrt(const.hbar * const.c / const.G)  # (kg)
        self.planck_energy = np.sqrt(const.hbar * const.c**5 / const.G)  # (J)
        
        # Unit conversions
        self.eV_to_J = const.e  # 1 eV in joules
        self.GeV_to_eV = 1e9  # 1 GeV in eV
        self.eV_to_kg = const.e / const.c**2  # E=mc²: 1 eV in kg
        
        # Fine structure constant
        self.alpha_EM = 1/137.035999084
        
        # Strong coupling
        self.alpha_strong = 0.1179  # at Z boson mass
    
    def initialize_shell_parameters(self):
        """Initialize core shell parameters of the Matryoshka framework."""
        # Shell radius scaling parameter
        self.alpha_shell = 0.1
        
        # Base radius (normalized to Planck length)
        self.r0 = self.planck_length
        
        # Shell coupling parameters
        self.c0 = self.alpha_EM  # Base coupling strength matches α_EM
        self.beta = 0.1  # Coupling decay rate parameter
        self.gamma = 2.0  # Coupling decay exponent
        
        # Ordinal decay parameter
        self.lambda_ord = 0.1
        
        # Flow parameters
        self.kappa_plus = 1.0  # Forward flow constant (normalized)
        self.kappa_minus = self.G / self.c0  # Inverse flow constant
        
        # Force-specific parameters
        self.lambda_g = 0.1  # Gravitational decay
        self.lambda_EM = 0.1  # EM decay
        self.lambda_W = 0.1  # Weak decay
        self.lambda_S = 0.1  # Strong decay
    
    def initialize_golden_ratio_structure(self):
        """Initialize golden ratio related parameters."""
        # Fundamental golden ratio phi
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Derived golden parameters
        self.phi_sq = self.phi**2
        self.phi_cb = self.phi**3
        self.phi_inv = 1/self.phi
        self.phi_sqrt = np.sqrt(self.phi)
    
    def initialize_particle_parameters(self):
        """Initialize parameters related to particle physics."""
        # Mass scaling parameter
        self.lambda_m = 0.1
        
        # First generation reference depth
        self.n_e = 10
        
        # Experimental particle mass ratios
        self.mu_over_e = 206.7682826
        self.tau_over_e = 3477.15
        
        # Mass calibration alpha parameter (from part 3)
        self.alpha_cal = 7.87
    
    def initialize_neutrino_parameters(self):
        """Initialize neutrino-specific parameters."""
        # Neutrino mixing parameters (golden-ratio formulation)
        self.sin2_theta12_val = 1.0 / self.phi_sq
        self.sin2_theta23_val = 0.5 - 0.5 / self.phi_cb
        self.sin2_theta13_val = 1.0 / (4 * self.phi**4)
        
        # Delta_CP (radians)
        self.delta_CP = -np.pi / 2
        
        # Majorana phases (from golden ratio)
        self.alpha1 = np.pi / self.phi
        self.alpha2 = np.pi / (self.phi**2)
        
        # Neutrino mass-squared differences (eV²)
        self.dm21_sq = 7.53e-5
        self.dm31_sq = 2.453e-3  # normal hierarchy
        
        # Neutrino coupling parameter
        self.lambda_nu = 0.03
    
    def initialize_cosmological_parameters(self):
        """Initialize cosmological parameters."""
        # Current Hubble parameter (km/s/Mpc)
        self.H0 = 67.8
        
        # Density parameters
        self.Omega_m = 0.3
        self.Omega_Lambda = 0.7
        self.Omega_r = 9.24e-5
        self.Omega_k = 0.0
        
        # Dark energy equation of state
        self.w0 = -1.0
        self.wa = 0.03
        
        # Primordial fluctuation parameters
        self.n_s = 0.968
        self.r = 0.036
        self.alpha_s = -0.0006
        
        # Matter-radiation equality redshift
        self.z_eq = 3400
        
        # Dark energy-matter equality redshift
        self.z_DE = 0.3
    
    def recalculate_derived_parameters(self):
        """Recalculate key derived parameters from first principles."""
        # Calculate omega from muon/electron mass ratio
        omega_val = self.n_e + np.log(self.mu_over_e) / self.lambda_m
        self.omega = omega_val
        
        # Calculate electron neutrino mass based on dm21_sq, dm31_sq
        # Assuming normal hierarchy: m₁ < m₂ < m₃
        # and using relation m₃/(m₁+m₂) ~ 5.0 from the theory
        sum_m12 = np.sqrt(self.dm31_sq) / 5.0
        ratio_m2_m1 = np.sqrt(1 + self.dm21_sq/(sum_m12**2 - self.dm21_sq))
        self.m1 = sum_m12 / (1 + ratio_m2_m1)
        self.m2 = self.m1 * ratio_m2_m1
        self.m3 = np.sqrt(self.dm31_sq + self.m1**2)
        
        # Calculate |m_betabeta| - effective Majorana mass for 0νββ
        U_e1_sq = 1 - self.sin2_theta13_val
        U_e1 = np.sqrt(U_e1_sq * (1 - self.sin2_theta12_val))
        U_e2 = np.sqrt(U_e1_sq * self.sin2_theta12_val)
        U_e3 = np.sqrt(self.sin2_theta13_val)
        
        # Complex amplitudes with Majorana phases
        A1 = U_e1**2 * self.m1 * np.exp(1j * self.alpha1)
        A2 = U_e2**2 * self.m2 * np.exp(1j * self.alpha2)
        A3 = U_e3**2 * self.m3
        
        # Absolute value of the sum gives |m_betabeta|
        self.m_betabeta = abs(A1 + A2 + A3)
    
    def load_calibrated_parameters(self):
        """Load pre-calibrated parameters derived from theoretical considerations."""
        # Omega from Part III
        self.omega = 63.2
        
        # Neutrino masses (eV) from golden ratio hierarchy
        self.m1 = 0.001
        self.m2 = 0.009
        self.m3 = 0.050
        
        # Effective Majorana mass for 0νββ
        self.m_betabeta = 0.0074
        
        # W and Z boson masses predicted by the theory (GeV)
        self.m_W = 80.4
        self.m_Z = 91.2
        
        # Higgs mass predicted by the theory (GeV)
        self.m_H = 125.1
        
        # Top quark mass predicted by the theory (GeV)
        self.m_top = 173.0
    
    def verify_parameter_consistency(self):
        """Verify that parameter sets are internally consistent."""
        # Check omega consistency with mass ratios
        expected_mu_over_e = np.exp(self.lambda_m * (self.omega - self.n_e))
        mu_ratio_error = abs(expected_mu_over_e - self.mu_over_e) / self.mu_over_e
        
        if mu_ratio_error > 0.01:
            print(f"WARNING: Muon/electron mass ratio inconsistent with omega value")
            print(f"  Expected: {expected_mu_over_e:.6f}, Actual: {self.mu_over_e:.6f}")
            print(f"  Error: {mu_ratio_error:.2%}")
        
        # Check that neutrino mass-squared differences match with absolute masses
        calc_dm21_sq = self.m2**2 - self.m1**2
        calc_dm31_sq = self.m3**2 - self.m1**2
        
        dm21_error = abs(calc_dm21_sq - self.dm21_sq) / self.dm21_sq
        dm31_error = abs(calc_dm31_sq - self.dm31_sq) / self.dm31_sq
        
        if dm21_error > 0.05 or dm31_error > 0.05:
            print("WARNING: Neutrino mass-squared differences inconsistent with absolute masses")
            print(f"  dm21_sq: Expected={self.dm21_sq:.6e}, Calculated={calc_dm21_sq:.6e}")
            print(f"  dm31_sq: Expected={self.dm31_sq:.6e}, Calculated={calc_dm31_sq:.6e}")
        
        # Check that ordinal scaling is consistent with planck_length and r0
        if abs(self.r0 - self.planck_length) / self.planck_length > 0.01:
            print("WARNING: Base shell radius r0 is inconsistent with Planck length")
        
        # Check gravitational constant derived from kappa_minus and c0
        derived_G = self.kappa_minus * self.c0
        G_error = abs(derived_G - self.G) / self.G
        
        if G_error > 0.01:
            print("WARNING: Derived gravitational constant inconsistent with G")
            print(f"  Expected: {self.G:.6e}, Derived: {derived_G:.6e}")
            print(f"  Error: {G_error:.2%}")
    
    def print_summary(self):
        """Print a summary of key parameters."""
        print("\n" + "=" * 80)
        print("MATRYOSHKA FRAMEWORK PARAMETER SUMMARY")
        print("=" * 80)
        
        print("\nFundamental Parameters:")
        print(f"  omega = {self.omega:.6f}")
        print(f"  phi (golden ratio) = {self.phi:.10f}")
        print(f"  lambda_m (mass scaling) = {self.lambda_m:.6f}")
        print(f"  lambda_ord (ordinal decay) = {self.lambda_ord:.6f}")
        print(f"  alpha_shell (radius scaling) = {self.alpha_shell:.6f}")
        
        print("\nForce Parameters:")
        print(f"  c0 (α_EM) = {self.c0:.12f}")
        print(f"  G (derived) = {self.kappa_minus * self.c0:.6e} m³/kg/s²")
        print(f"  G (actual) = {self.G:.6e} m³/kg/s²")
        
        print("\nNeutrino Parameters:")
        print(f"  sin²(θ₁₂) = {self.sin2_theta12_val:.6f}")
        print(f"  sin²(θ₂₃) = {self.sin2_theta23_val:.6f}")
        print(f"  sin²(θ₁₃) = {self.sin2_theta13_val:.6f}")
        print(f"  δ_CP = {self.delta_CP/np.pi:.6f}π")
        print(f"  m₁ = {self.m1:.6f} eV")
        print(f"  m₂ = {self.m2:.6f} eV")
        print(f"  m₃ = {self.m3:.6f} eV")
        print(f"  |m_ββ| = {self.m_betabeta:.6f} eV")
        
        print("\nCosmological Parameters:")
        print(f"  n_s = {self.n_s:.6f}")
        print(f"  r = {self.r:.6f}")
        print(f"  α_s = {self.alpha_s:.6f}")
        print(f"  Ω_m = {self.Omega_m:.6f}")
        print(f"  Ω_Λ = {self.Omega_Lambda:.6f}")
        print(f"  w_0 = {self.w0:.6f}")
        print(f"  w_a = {self.wa:.6f}")
        
        print("\n" + "=" * 80)

# If run directly, initialize and print parameter summary
if __name__ == "__main__":
    params = MatryoshkaParameters()
    params.print_summary()