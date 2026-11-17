import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.interpolate import interp1d
import math

# Define the Temporal Matryoshka Model
# Key principle: Time flows at different rates in nested gravitational structures

# Constants
c = 299792.458  # km/s (speed of light)
G = 6.67430e-11 * (3.086e19)**3 / (1.989e30) / (3.154e7)**2  # km^3/kg/s^2 converted to km^3/M_sun/yr^2
H0_nominal = 70  # km/s/Mpc (nominal Hubble constant)
Mpc_to_km = 3.086e19  # conversion factor

# Define nested structure levels (matryoshka layers)
# Level 0: Cosmic voids (lowest density)
# Level 1: Filaments 
# Level 2: Galaxy clusters
# Level 3: Galaxies
# Level 4: Dense galactic cores

class TemporalMatryoshka:
    def __init__(self):
        # Define characteristic densities for each nesting level (in units of critical density)
        self.rho_levels = np.array([0.1, 0.5, 2.0, 10.0, 100.0])  # relative to critical density
        
        # Define characteristic scales (in Mpc)
        self.scale_levels = np.array([100, 50, 10, 1, 0.01])
        
        # Critical density at z=0 (in M_sun/Mpc^3)
        self.rho_crit_0 = 3 * (H0_nominal / Mpc_to_km)**2 / (8 * np.pi * G * (Mpc_to_km/3.086e19)**3)
        
    def gravitational_time_dilation(self, rho, scale):
        """
        Calculate gravitational time dilation factor for a given density and scale
        Using Schwarzschild metric approximation for weak fields
        """
        # Effective gravitational potential
        phi = -G * rho * self.rho_crit_0 * 4 * np.pi * scale**2 / 3
        
        # Time dilation factor: dt_proper = dt_coordinate * sqrt(1 + 2*phi/c^2)
        # For weak fields: approximately 1 + phi/c^2
        time_dilation = 1 + phi / c**2
        
        return time_dilation
    
    def nested_time_factor(self, z, position_type='void'):
        """
        Calculate cumulative time dilation through nested structures
        position_type: 'void', 'filament', 'cluster', 'galaxy', 'core'
        """
        position_map = {
            'void': 0,
            'filament': 1, 
            'cluster': 2,
            'galaxy': 3,
            'core': 4
        }
        
        level = position_map.get(position_type, 0)
        
        # Cumulative time dilation from all encompassing levels
        total_dilation = 1.0
        
        # Account for cosmic evolution (densities were higher in the past)
        evolution_factor = (1 + z)**3
        
        for i in range(level + 1):
            # Each level contributes to time dilation
            dilation = self.gravitational_time_dilation(
                self.rho_levels[i] * evolution_factor,
                self.scale_levels[i] / (1 + z)  # scales were smaller in the past
            )
            total_dilation *= dilation
            
        return total_dilation
    
    def observed_expansion_rate(self, z_observer, z_source, observer_type='void', source_type='galaxy'):
        """
        Calculate the observed expansion rate accounting for temporal nesting
        """
        # Time dilation at observer
        dt_observer = self.nested_time_factor(z_observer, observer_type)
        
        # Time dilation at source
        dt_source = self.nested_time_factor(z_source, source_type)
        
        # Relative time flow rate
        relative_time_rate = dt_source / dt_observer
        
        # Observed Hubble parameter
        H_observed = H0_nominal * relative_time_rate * (1 + z_source)**1.5
        
        return H_observed

# Create model instance
model = TemporalMatryoshka()

# Demonstrate the mathematical framework
print("TEMPORAL MATRYOSHKA MODEL - Mathematical Framework")
print("="*60)
print("\nKey Equation for Nested Time Dilation:")
print("τ(r,t) = τ₀ ∏ᵢ √(1 - 2GMᵢ/rᵢc²)")
print("\nWhere:")
print("- τ(r,t) = proper time at position r and cosmic time t")
print("- τ₀ = coordinate time")
print("- i indexes nested gravitational structures")
print("- Mᵢ = mass within structure i")
print("- rᵢ = characteristic radius of structure i")

print("\n\nNumerical Example - Time Dilation Factors:")
print("-"*60)
z_test = 0.5
for pos_type in ['void', 'filament', 'cluster', 'galaxy', 'core']:
    td = model.nested_time_factor(z_test, pos_type)
    print(f"At z={z_test}, {pos_type:10s}: τ/τ₀ = {td:.6f}")