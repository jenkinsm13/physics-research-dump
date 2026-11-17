import numpy as np
import matplotlib.pyplot as plt

# --- 1. Define the Physical Environment and Simulation Grid ---

PARAMS = {
    'a': 0.1, 'b': 1.0, 'c': 0.1,
    'gamma_A': 0.2,
    'gamma_Th': 0.2,
    'alpha_A': 0.15, 'omega': 1.85,
    'COUPLING_FACTOR': 1e-9 # NEW: Converts field velocity to electrical current
}

# Grid and Time Parameters
NX, NY, NZ = 40, 40, 40  # Reduced grid for faster characterization
L = 100.0
DX, DY, DZ = L / NX, L / NY, L / NZ
C_SPEED = 1.0
CFL = 0.05
DT = CFL * min(DX, DY, DZ) / C_SPEED

# --- 2. Define Physical Functions (Unchanged) ---

def V(psi, p=PARAMS):
    return p['a'] * psi**4 - p['b'] * psi**2 + p['c'] * psi

def dVdPsi(psi, p=PARAMS):
    return 4 * p['a'] * psi**3 - 2 * p['b'] * psi + p['c']

# --- 3. Core Simulation Engine for Characterization ---

def get_response(input_voltage_amplitude, num_steps=2000):
    """
    Runs the FDTD simulation for a fixed input voltage to find the steady-state current response.
    This is the core of the device characterization.
    """
    t_final = num_steps * DT
    
    # -- Initialize Fields --
    psi_range = np.linspace(-4, 4, 1000)
    potential_values = V(psi_range)
    minima_indices = (np.diff(np.sign(np.diff(potential_values))) > 0).nonzero()[0] + 1
    psi_high_well = psi_range[minima_indices[0]]

    psi_p = np.full((NX, NY, NZ), psi_high_well)
    psi_c = np.full((NX, NY, NZ), psi_high_well)
    alpha_p = np.zeros((NX, NY, NZ))
    alpha_c = np.zeros((NX, NY, NZ))

    # -- FDTD Loop --
    gamma_total = PARAMS['gamma_A'] + PARAMS['gamma_Th']
    measured_currents = []

    for n in range(num_steps):
        t = n * DT
        
        # Update Alpha Field (External Stimulus)
        alpha_f = np.zeros_like(alpha_c)
        # Simplified update (boundary effects ignored for this characterization)
        # The input voltage is now the source term for the alpha field
        alpha_f[1:-1, 1:-1, 1:-1] = input_voltage_amplitude

        # Update Psi Field (Material Response)
        psi_f = np.zeros_like(psi_c)
        damping_factor_num = (1 - gamma_total * DT / 2)
        damping_factor_den = (1 + gamma_total * DT / 2)
        
        # Vectorized update for speed
        laplacian_psi = (np.roll(psi_c, -1, axis=0) + np.roll(psi_c, 1, axis=0) - 2*psi_c) / DX**2 + \
                        (np.roll(psi_c, -1, axis=1) + np.roll(psi_c, 1, axis=1) - 2*psi_c) / DY**2 + \
                        (np.roll(psi_c, -1, axis=2) + np.roll(psi_c, 1, axis=2) - 2*psi_c) / DZ**2
        force_potential = -dVdPsi(psi_c)
        force_computation = 2 * alpha_c * psi_c
        
        term1 = (2*psi_c - psi_p * damping_factor_num) / damping_factor_den
        term2 = (DT**2 / damping_factor_den) * (laplacian_psi + force_potential + force_computation)
        psi_f = term1 + term2
        
        # Stability check
        if not np.all(np.isfinite(psi_f)):
            return np.nan # Return NaN if simulation diverges

        # Update fields
        psi_p, psi_c = psi_c, psi_f
        alpha_p, alpha_c = alpha_c, alpha_f

        # Measure "current" - the collective velocity of the psi field
        if n > num_steps // 2: # Measure after system starts to settle
             v_field_psi = (psi_f - psi_p) / (2 * DT)
             # Current is the volume integral of charge velocity
             total_current = PARAMS['COUPLING_FACTOR'] * np.sum(v_field_psi)
             measured_currents.append(total_current)

    # Return the average of the steady-state current
    return np.mean(measured_currents)

# --- 4. Device Characterization and Visualization ---

def characterize_device():
    """
    Sweeps through a range of input voltages to generate the device's I-V curve.
    """
    print("🔬 Starting device characterization...")
    
    voltages = np.linspace(-0.5, 0.5, 41) # Sweep from -0.5V to 0.5V
    currents = []
    
    for i, v in enumerate(voltages):
        print(f"  Simulating point {i+1}/{len(voltages)}: V_in = {v:.3f} V")
        current = get_response(v)
        currents.append(current)
    
    print("✅ Characterization complete.")
    
    # --- 5. Generate Behavioral Model Proxy ---
    # Fit a polynomial to the I-V data to create a fast proxy model.
    # A 7th-degree polynomial should be sufficient to capture the non-linearity.
    print("\n\n🔬 Generating behavioral model proxy...")
    
    # Remove any NaN values that result from simulation divergence
    voltages = np.array(voltages)
    currents = np.array(currents)
    finite_indices = np.isfinite(currents)
    
    if np.any(~finite_indices):
        print("  WARNING: Some simulation points diverged and were excluded from the fit.")
    
    v_fit = voltages[finite_indices]
    i_fit = currents[finite_indices]
    
    # Fit polynomial: I = f(V)
    degree = 7
    coeffs = np.polyfit(v_fit, i_fit, degree)
    
    # Create the polynomial function for plotting the fit
    p = np.poly1d(coeffs)
    
    print(f"✅ Behavioral model generated (Polynomial of degree {degree}).")
    
    # Format the expression for PySpice's behavioral source
    pyspice_expression = "I(v_in) = "
    for i, c in enumerate(reversed(coeffs)):
        power = i
        if power == 0:
            pyspice_expression += f"{c:e}"
        elif power == 1:
            pyspice_expression += f" + {c:e}*V(in)"
        else:
            pyspice_expression += f" + {c:e}*PWR(V(in),{power})"
    print("\nPySpice Behavioral Source Expression:")
    print("-------------------------------------")
    print(pyspice_expression)
    print("-------------------------------------")
    
    # Plot I-V Curve and the polynomial fit
    plt.figure(figsize=(10, 7))
    plt.plot(voltages, currents, 'bo-', label='Simulated I-V Data')
    plt.plot(v_fit, p(v_fit), 'r--', lw=2, label=f'Polynomial Fit (degree {degree})')
    plt.title('Digital Twin: Device I-V Characteristic')
    plt.xlabel('Input Voltage (V)')
    plt.ylabel('Output Current (A)')
    plt.grid(True)
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    characterize_device() 