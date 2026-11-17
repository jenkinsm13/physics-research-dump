import numpy as np
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# --- 1. PROPER PHYSICS MODEL ---
# All physics are now encapsulated here. No "cheating" post-simulation.

PARAMS = {
    # Classical Ferroelectric Parameters
    'a': 0.1, 'b': 1.0, 'c': 0.1, 'gamma_A': 0.2, 'gamma_Th': 0.2,
    'alpha_A': 0.15, 'omega': 1.85,
    'coupling_factor': 1e-9,

    # "Honest" Active Model Parameters
    # Condition for triggering the active energy release
    'active_psi_crossing_threshold': 100.0, # Required speed of psi change (d_psi/dt)
    # Finite energy source for the active effect
    'zpe_reservoir_initial': 1e-9, # Joules. Finite energy available to be released.
    'zpe_release_rate': 1e-3,      # Rate at which reservoir energy is converted to power.
}

# --- Global State Variables for the Simulation Callback ---
# These track the internal state of our single component over time.
psi_c = -2.236
psi_p = -2.236
last_t = 0.0
zpe_reservoir = PARAMS['zpe_reservoir_initial']
# A flag to control which model the function uses.
IS_ACTIVE_MODEL_ENABLED = False


def dVdPsi(psi, p=PARAMS):
    """Calculates the classical potential gradient of the psi field."""
    return 4 * p['a'] * psi**3 - 2 * p['b'] * psi + p['c']


def active_ferroelectric_current(v_crystal, t):
    """
    This is the core of the "proper" simulation.
    It calculates the component's current based ENTIRELY on its internal state and inputs.
    Any over-unity effect MUST emerge from the V-I characteristic defined here.
    """
    global psi_c, psi_p, last_t, zpe_reservoir, IS_ACTIVE_MODEL_ENABLED

    dt = t - last_t
    if dt <= 1e-12:
        return 0.0

    # --- Part A: Classical Ferroelectric Response (Always Active) ---
    gamma_total = PARAMS['gamma_A'] + PARAMS['gamma_Th']
    force_potential = -dVdPsi(psi_c)
    force_external = v_crystal * PARAMS['coupling_factor']
    damping_term = gamma_total * (psi_c - psi_p) / dt
    psi_f = 2*psi_c - psi_p + dt**2 * (force_potential + force_external - damping_term)
    dPsidt = (psi_f - psi_p) / (2 * dt)
    classical_current = dPsidt * 1e-6 # This part is generally dissipative.

    # --- Part B: Conditional Active Response (The Hypothetical "ZPE Tap") ---
    active_current = 0.0
    if IS_ACTIVE_MODEL_ENABLED:
        # Condition Check: Is the component in a state to release energy?
        psi_velocity = abs(dPsidt)
        is_transitioning_fast = psi_velocity > PARAMS['active_psi_crossing_threshold']
        is_reservoir_non_empty = zpe_reservoir > 0

        if is_transitioning_fast and is_reservoir_non_empty:
            # If triggered, release a pulse of power from the reservoir.
            power_to_release = PARAMS['zpe_release_rate'] * zpe_reservoir
            
            # Convert power to current (I = P/V).
            # The negative sign means for a positive voltage, we source a negative current.
            # This is the definition of sourcing power.
            if abs(v_crystal) > 1e-6: # Avoid division by zero
                active_current = -power_to_release / v_crystal
            
            # Deplete the finite energy reservoir. This is crucial for an "honest" model.
            energy_released_this_step = power_to_release * dt
            zpe_reservoir -= energy_released_this_step

    # --- Update State and Return Total Current ---
    psi_p, psi_c = psi_c, psi_f
    last_t = t
    
    # The simulator will see the sum of the two behaviors.
    return classical_current + active_current


# --- 2. SIMULATION AND ANALYSIS HARNESS ---

def run_simulation(r_load_value=50, use_active_model=False):
    """
    Sets up and runs a single, honest SPICE simulation.
    """
    print(f"\n--- Running {'ACTIVE' if use_active_model else 'CLASSICAL'} Model ---")
    print(f"R_load = {r_load_value} Ohm")

    # Reset state variables for a clean run
    global psi_c, psi_p, last_t, zpe_reservoir, IS_ACTIVE_MODEL_ENABLED
    psi_c = -2.236
    psi_p = -2.236
    last_t = 0.0
    zpe_reservoir = PARAMS['zpe_reservoir_initial']
    IS_ACTIVE_MODEL_ENABLED = use_active_model

    # --- Circuit Setup ---
    circuit = Circuit('Emergent Physics Test Bench')
    sim_time = 60e-3
    steps = 1000
    t_points = np.linspace(0, sim_time, steps)
    v_points = 10 * PARAMS['alpha_A'] * np.cos(PARAMS['omega'] * t_points / (1e-3))
    
    pwl_values = [item for pair in zip(t_points, v_points) for item in pair]
    pwl_string = 'PWL(' + ' '.join([f'{v:.12e}' for v in pwl_values]) + ')'
    circuit.V('input', 'input_node', circuit.gnd, pwl_string)

    R_load = r_load_value@u_Ohm
    circuit.R('load', 'input_node', 'crystal_node', R_load)
    
    # Define the Behavioral Source that will call our Python function
    circuit.B('crystal', 'crystal_node', 'gnd',
              current_expression='I(t) = py_func(v(crystal_node), time)')

    # --- Run Simulation ---
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    
    # --- THIS IS THE DEFINITIVE FIX ---
    # Use the def_function() method to link the name 'py_func' to our Python function
    simulator.def_function(active_ferroelectric_current, 'py_func')
    # ---------------------------------

    analysis = simulator.transient(step_time=sim_time/steps, end_time=sim_time)

    # --- Honest Analysis (No Post-Processing Cheats) ---
    time = np.array(analysis.time)
    input_voltage = np.array(analysis['input_node'])
    crystal_voltage = np.array(analysis['crystal_node'])
    
    current = (input_voltage - crystal_voltage) / R_load.value
    power_input = input_voltage * current
    power_extracted = current**2 * R_load.value
    
    energy_input = np.trapezoid(power_input, time)
    energy_extracted = np.trapezoid(power_extracted, time)
    net_gain = energy_extracted - energy_input

    print(f"Total Energy Input:     {energy_input * 1e6:.4f} µJ")
    print(f"Total Energy Extracted: {energy_extracted * 1e6:.4f} µJ")
    print(f"Net Energy Gain:        {net_gain * 1e6:.4f} µJ")
    print(f"Final ZPE Reservoir:    {zpe_reservoir * 1e9 :.4f} / {PARAMS['zpe_reservoir_initial']*1e9:.2f} nJ")

    if net_gain > 0:
        print(">>> SUCCESS: Over-unity behavior EMERGED from the model.")
    else:
        print(">>> NOTE: Net energy loss observed, as expected for a passive system.")
        
    return net_gain, time, input_voltage, crystal_voltage, current


# --- 3. EXPERIMENT ORCHESTRATION ---

if __name__ == '__main__':
    # Define the experiment parameters
    R_LOAD_OPTIMAL = 500  # A guess for the load resistance

    # --- Run Baseline (Classical Model) ---
    classical_gain, _, _, _, _ = run_simulation(
        r_load_value=R_LOAD_OPTIMAL, 
        use_active_model=False
    )

    # --- Run Experiment (Active Model) ---
    active_gain, time, v_in, v_out, current = run_simulation(
        r_load_value=R_LOAD_OPTIMAL, 
        use_active_model=True
    )

    # --- Final Visualization and Comparison ---
    print("\n\n" + "="*50)
    print("      FINAL EXPERIMENT RESULTS")
    print("="*50)

    # 1. Plot the dynamics of the ACTIVE case
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2)

    # Oscilloscope plot
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_title(f'Active Model Dynamics (R_load = {R_LOAD_OPTIMAL}Ω)', fontsize=14)
    ax1.plot(time * 1000, v_in, 'b-', label='Input Voltage (V_in)')
    ax1.plot(time * 1000, v_out, 'r-', label='Crystal Voltage (V_out)')
    ax1.set_ylabel('Voltage (V)')
    ax1.grid(True)
    ax1_twin = ax1.twinx()
    ax1_twin.plot(time * 1000, current * 1000, 'g--', alpha=0.7, label='Load Current (mA)')
    ax1_twin.set_ylabel('Current (mA)', color='g')
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))

    # Power plot
    ax2 = fig.add_subplot(gs[1, :], sharex=ax1)
    ax2.plot(time * 1000, (v_in * current), label='Input Power (W)')
    ax2.plot(time * 1000, (current**2 * R_LOAD_OPTIMAL), label='Extracted Power (W)')
    ax2.axhline(0, color='k', lw=0.5)
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Power (W)')
    ax2.grid(True)
    ax2.legend()
    
    # Comparison Bar Chart
    ax3 = fig.add_subplot(gs[2, 0])
    categories = ['Classical Model', 'Active Model']
    gains_uJ = [classical_gain * 1e6, active_gain * 1e6]
    colors = ['#d9534f' if g <= 0 else '#5cb85c' for g in gains_uJ]
    bars = ax3.bar(categories, gains_uJ, color=colors)
    ax3.axhline(0, color='k', lw=0.5)
    ax3.set_ylabel('Net Energy Gain (µJ)')
    ax3.set_title('Experiment vs. Control', fontsize=14)
    ax3.bar_label(bars, fmt='%.2f µJ')

    # Parameter Display
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')
    ax4.set_title('Active Model Parameters', fontsize=14)
    param_text = (
        f"ZPE Reservoir: {PARAMS['zpe_reservoir_initial']*1e9:.1f} nJ\n"
        f"Release Rate: {PARAMS['zpe_release_rate']}\n"
        f"Psi Velocity Threshold: {PARAMS['active_psi_crossing_threshold']}"
    )
    ax4.text(0.5, 0.5, param_text, ha='center', va='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="wheat", alpha=0.5))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.suptitle('Proper Simulation of Emergent Over-Unity Behavior', fontsize=18, weight='bold')
    plt.show()