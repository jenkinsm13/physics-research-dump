import numpy as np
import matplotlib.pyplot as plt
# Import PySpice libraries
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import * # To use units like u_V, u_A, u_Ohm

# --- 1. Define the Physical Model (Our "Secret Sauce") ---
# This is a simplified version of our FDTD physics, designed to be called by SPICE.

PARAMS = {
    'a': 0.1, 'b': 1.0, 'c': 0.1, 'gamma_A': 0.2, 'gamma_Th': 0.2,
    'alpha_A': 0.15, 'omega': 1.85,
    'coupling_factor': 1e-9 # How strongly voltage affects the field (C/V)
}

# Global state variables for our crystal model (it has memory)
psi_c = -2.236 # Start in the high-energy well
psi_p = -2.236
last_t = 0.0

def dVdPsi(psi, p=PARAMS):
    return 4 * p['a'] * psi**3 - 2 * p['b'] * psi + p['c']

def ferroelectric_current(v_crystal, t):
    """
    This function is the digital twin of the ferroelectric crystal.
    It calculates the current through the crystal based on the applied voltage and its internal state (psi).
    """
    global psi_c, psi_p, last_t
    
    dt = t - last_t
    if dt <= 1e-12: # Avoid division by zero at the start or with tiny steps
        return 0.0

    gamma_total = PARAMS['gamma_A'] + PARAMS['gamma_Th']
    
    # The external voltage acts as a force on the psi field
    force_potential = -dVdPsi(psi_c)
    force_external = v_crystal * PARAMS['coupling_factor'] # Voltage drives the field
    
    # Simplified Euler update for the psi field (instead of full FDTD)
    damping_term = gamma_total * (psi_c - psi_p) / dt
    psi_f = 2*psi_c - psi_p + dt**2 * (force_potential + force_external - damping_term)

    # The changing psi field induces a polarization current
    dPsidt = (psi_f - psi_p) / (2 * dt)
    polarization_current = dPsidt * 1e-6 # Scaling factor to get Amperes

    # Update state for next time step
    psi_p, psi_c = psi_c, psi_f
    last_t = t
    
    return polarization_current

# --- 2. Define the Virtual Test Bench using PySpice ---

def run_hardware_simulation():
    print("Running virtual hardware (SPICE) simulation...")
    
    # Create the circuit object
    circuit = Circuit('MVP Test Bench')
    
    # Define the input signal (our Arbitrary Waveform Generator)
    sim_time = 60e-3 # 60 ms simulation
    steps = 1000
    t_points = np.linspace(0, sim_time, steps)
    # Scale omega correctly for time in seconds
    v_points = 10 * PARAMS['alpha_A'] * np.cos(PARAMS['omega'] * t_points / (1e-3)) 
    
    # Create PWL data string in the proper SPICE format
    pwl_pairs = []
    for t, v in zip(t_points, v_points):
        pwl_pairs.append(f"{t:.12e}")
        pwl_pairs.append(f"{v:.12e}")
    
    pwl_string = "PWL(" + " ".join(pwl_pairs) + ")"
    
    # Create the PWL voltage source using the proper PySpice syntax
    # Changed 'in' to 'input_node' to avoid Python keyword conflict
    circuit.V('input', 'input_node', circuit.gnd, pwl_string)

    # Add the Load Resistor (our energy extraction component)
    R_load = 50@u_Ohm
    circuit.R('load', 'input_node', 'crystal_node', R_load)

    # For now, let's use a simpler model instead of the behavioral source with Python function
    # We'll add a simple resistor to represent the crystal for initial testing
    circuit.R('crystal', 'crystal_node', circuit.gnd, 1@u_kOhm)

    # --- 3. Run the Simulation and Analyze Results ---
    
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=sim_time/steps, end_time=sim_time)
    
    print("SPICE simulation complete. Analyzing results.")

    # Extract the data from the simulation results
    time = np.array(analysis.time)
    input_voltage = np.array(analysis['input_node'])
    crystal_voltage = np.array(analysis['crystal_node'])
    
    # Current is the voltage drop across R_load divided by its resistance
    current = (input_voltage - crystal_voltage) / R_load.value

    # Calculate instantaneous power
    power_input = input_voltage * current
    power_extracted = current**2 * R_load.value
    
    # Integrate power over time to get energy
    energy_input = np.trapezoid(power_input, time)
    energy_extracted = np.trapezoid(power_extracted, time)
    net_gain = energy_extracted - energy_input

    # --- 4. Plot the Results (like an oscilloscope) ---
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    ax1.set_title('Virtual Oscilloscope: Voltages and Currents')
    ax1.plot(time * 1000, input_voltage, 'b-', label='Input Voltage (V_in)')
    ax1.plot(time * 1000, crystal_voltage, 'r-', label='Crystal Voltage (V_out)')
    ax1_twin = ax1.twinx()
    ax1_twin.plot(time * 1000, current * 1000, 'g--', label='Current (I_out)')
    ax1.set_ylabel('Voltage (V)')
    ax1_twin.set_ylabel('Current (mA)', color='g')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2.set_title('Power Analysis')
    ax2.plot(time * 1000, power_input, 'm-', label='Input Power (W)')
    ax2.plot(time * 1000, power_extracted, 'c-', label='Extracted Power (W)')
    ax2.axhline(0, color='k', lw=0.5)
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Power (W)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

    print("\n--- Final Hardware Simulation Results ---")
    print(f"Total Energy Input by AWG:   {energy_input * 1e6:.4f} uJ")
    print(f"Total Energy Extracted by Load: {energy_extracted * 1e6:.4f} uJ")
    print(f"Net Energy Gain:             {net_gain * 1e6:.4f} uJ")
    
    if net_gain > 0:
        print("\nSUCCESS: The simulation predicts a net positive energy gain.")
    else:
        print("\nNOTE: The simulation predicts a net energy loss. Parameters need tuning.")

if __name__ == '__main__':
    # Reset state variables before each run
    psi_c = -2.236
    psi_p = -2.236
    last_t = 0.0
    run_hardware_simulation()