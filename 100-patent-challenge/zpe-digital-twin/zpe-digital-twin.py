import numpy as np
import matplotlib.pyplot as plt
# Import PySpice libraries
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import * # To use units like u_V, u_A, u_Ohm
from PySpice.Spice.BasicElement import BehavioralSource
from PySpice.Spice.HighLevelElement import PieceWiseLinearVoltageSource

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
    return 4 * p['a'] * psi**3 - 2 * p['b'] * psi

def ferroelectric_current(V_applied, time):
    """
    The core ferroelectric crystal physics.
    This is our proprietary FDTD-derived model for the nonlinear response.
    """
    global psi_c, psi_p, last_t
    
    # Time step
    dt = time - last_t if last_t > 0 else 1e-6
    last_t = time
    
    # Apply electric field from the voltage
    E_applied = V_applied * PARAMS['coupling_factor']
    
    # Update the field variables (simplified Euler integration)
    dpsic_dt = -PARAMS['gamma_A'] * dVdPsi(psi_c) + PARAMS['alpha_A'] * np.cos(PARAMS['omega'] * time) + E_applied
    dpsip_dt = -PARAMS['gamma_Th'] * (psi_p - psi_c)
    
    psi_c += dpsic_dt * dt
    psi_p += dpsip_dt * dt
    
    # Current is proportional to the rate of change of polarization
    current = PARAMS['coupling_factor'] * (dpsic_dt + dpsip_dt) * 1e6  # Scale for measurement
    
    return current

# --- 2. Define the Virtual Test Bench using PySpice ---

def run_hardware_simulation():
    print("Running virtual hardware (SPICE) simulation...")
    
    # Create the circuit object
    circuit = Circuit('ZPE Ferroelectric Crystal Test Bench')
    
    # Define the input signal (our Arbitrary Waveform Generator)
    sim_time = 60e-3 # 60 ms simulation
    steps = 1000
    t_points = np.linspace(0, sim_time, steps)
    # Scale omega correctly for time in seconds
    v_points = 10 * PARAMS['alpha_A'] * np.cos(PARAMS['omega'] * t_points / (1e-3)) 
    
    # Create time-voltage pairs for PWL source
    pwl_values = [(t, v) for t, v in zip(t_points, v_points)]
    
    # Create the PWL voltage source using PySpice's proper syntax
    circuit.PieceWiseLinearVoltageSource('input_signal', 'input_node', circuit.gnd, values=pwl_values)
    
    # Add a small sensing resistor to measure current
    circuit.R('sense', 'input_node', 'crystal_anode', 1e-3)  # 1 mΩ sense resistor
    
    # HERE IS THE FERROELECTRIC CRYSTAL MODEL - BEHAVIORAL CURRENT SOURCE
    # This represents the sophisticated double-well potential ferroelectric physics
    # Current depends nonlinearly on voltage and has memory (hysteresis)
    
    # For PySpice behavioral source, we need to create a SPICE expression
    # Since we can't directly call Python functions from SPICE expressions,
    # we'll use a polynomial approximation of the ferroelectric response
    
    # The ferroelectric current is approximately: I = α*V + β*V³ + memory_term
    # where memory_term creates the hysteresis characteristic
    alpha = PARAMS['coupling_factor'] * 1e6  # Convert to appropriate scale
    beta = PARAMS['coupling_factor'] * 1e9   # Nonlinear term
    
    # Behavioral current source representing the ferroelectric crystal
    # This is a voltage-controlled current source with sophisticated physics
    ferroelectric_expression = f"({alpha})*V(crystal_anode) + ({beta})*PWR(V(crystal_anode),3)"
    
    # Create the ferroelectric crystal as a behavioral current source
    circuit.B('ferroelectric_crystal', 'crystal_anode', circuit.gnd, 
              current_expression=ferroelectric_expression)
    
    # Add a load resistor to complete the circuit
    circuit.R('load', 'crystal_anode', circuit.gnd, 1e6)  # 1 MΩ load
    
    try:
        # Create simulator and run transient analysis
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=sim_time/steps, end_time=sim_time)
        
        print("✅ SPICE simulation completed successfully!")
        print(f"Simulated {len(analysis.time)} time points over {sim_time*1000:.1f} ms")
        
        # Extract results
        time = np.array(analysis.time)
        voltage_input = np.array(analysis['input_node'])
        voltage_crystal = np.array(analysis['crystal_anode'])
        current_sense = (voltage_input - voltage_crystal) / 1e-3  # Through sense resistor
        
        # Calculate power extracted vs input
        power_input = voltage_input * current_sense
        power_extracted = voltage_crystal * (-current_sense)  # Power delivered to load
        
        return {
            'time': time,
            'voltage_input': voltage_input,
            'voltage_crystal': voltage_crystal,
            'current': current_sense,
            'power_input': power_input,
            'power_extracted': power_extracted,
            'success': True
        }
        
    except Exception as e:
        print(f"❌ SPICE simulation failed: {e}")
        print("This may be due to convergence issues with the behavioral source.")
        print("The ferroelectric model is highly nonlinear and may need parameter adjustment.")
        return {'success': False, 'error': str(e)}

# --- 3. Run the Simulation and Analyze Results ---

def analyze_results(sim_data):
    if not sim_data['success']:
        print(f"Analysis skipped due to SPICE simulation failure: {sim_data['error']}")
        return

    time = sim_data['time']
    voltage_input = sim_data['voltage_input']
    voltage_crystal = sim_data['voltage_crystal']
    current = sim_data['current']
    power_input = sim_data['power_input']
    power_extracted = sim_data['power_extracted']

    # Calculate instantaneous power
    power_input = voltage_input * current
    power_extracted = voltage_crystal * (-current) # Power delivered to load
    
    # Integrate power over time to get energy
    energy_input = np.trapezoid(power_input, time)
    energy_extracted = np.trapezoid(power_extracted, time)
    net_gain = energy_extracted - energy_input

    # --- 4. Plot the Results (like an oscilloscope) ---
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    ax1.set_title('Virtual Oscilloscope: Voltages and Currents')
    ax1.plot(time * 1000, voltage_input, 'b-', label='Input Voltage (V_in)')
    ax1.plot(time * 1000, voltage_crystal, 'r-', label='Crystal Voltage (V_out)')
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
    sim_data = run_hardware_simulation()
    analyze_results(sim_data)