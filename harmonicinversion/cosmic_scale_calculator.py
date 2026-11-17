#!/usr/bin/env python3
"""
Calculate the number of temporal shells needed to span from Planck scale 
to the observable universe using the Matryoshka-Chronon framework
"""

import numpy as np

def calculate_required_shells():
    """Calculate shells needed to span cosmic scales"""
    
    # Physical constants
    planck_length = 1.616e-35  # meters
    observable_universe = 8.8e26  # meters (diameter)
    golden_ratio = 1.618  # φ for shell spacing
    
    # Calculate number of shells needed
    # Each shell radius = planck_length * φ^i
    # We need: planck_length * φ^n >= observable_universe
    # Therefore: n >= log(observable_universe / planck_length) / log(φ)
    
    ratio = observable_universe / planck_length
    n_shells_needed = int(np.ceil(np.log(ratio) / np.log(golden_ratio)))
    
    print("=== COSMIC SCALE ANALYSIS ===")
    print(f"Planck Length: {planck_length:.3e} m")
    print(f"Observable Universe: {observable_universe:.3e} m")
    print(f"Scale Ratio: {ratio:.3e}")
    print(f"Golden Ratio: {golden_ratio}")
    print(f"Required Shells: {n_shells_needed}")
    
    # Verify the calculation
    final_radius = planck_length * (golden_ratio ** n_shells_needed)
    print(f"Final Shell Radius: {final_radius:.3e} m")
    print(f"Coverage Factor: {final_radius / observable_universe:.2f}")
    
    # Show key scale transitions
    print("\n=== KEY SCALE TRANSITIONS ===")
    scales = {
        "Planck Length": 1.616e-35,
        "Proton Radius": 8.414e-16,
        "Atomic Radius": 5.29e-11,
        "Human Scale": 1.0,
        "Earth Radius": 6.371e6,
        "Solar System": 1.5e11,
        "Light Year": 9.461e15,
        "Milky Way": 9.461e20,
        "Observable Universe": 8.8e26
    }
    
    for name, size in scales.items():
        shell_index = int(np.log(size / planck_length) / np.log(golden_ratio))
        print(f"  {name:20s}: Shell {shell_index:3d} ({size:.3e} m)")
    
    return n_shells_needed

if __name__ == "__main__":
    n_shells = calculate_required_shells()
    print(f"\n*** RECOMMENDATION: Use {n_shells} shells for full cosmic coverage ***")