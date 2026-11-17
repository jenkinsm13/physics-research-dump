import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =============================================================================
# --- 1. Foundational Constants & FDTD Parameters
# =============================================================================
c0 = 299792458.0      # Speed of light in vacuum (m/s)
mu0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)
eps0 = 1 / (mu0 * c0**2)  # Permittivity of free space (F/m)

# =============================================================================
# --- 1. Matryoshka Temporal Shell Framework: Core Constants
# =============================================================================
PLANCK_LENGTH = 1.616255e-35
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2

# FDTD Parameters
Nz = 500
dz = 1e-11 # Spatial step must be fine enough to resolve shell structure
dt = dz / (2 * c0)
simulation_steps = 8000

# =============================================================================
# --- 2. Matryoshka Physics Implementation
# =============================================================================
def map_position_to_shell_index(z, r0=PLANCK_LENGTH, phi=GOLDEN_RATIO):
    """Maps a physical coordinate z to the nearest temporal shell index i."""
    # r_i = r0 * phi^i  =>  i = log_phi(z / r0)
    return np.log(z / r0) / np.log(phi)

def get_void_potential(psi, shell_index, A=1.0, B=0.9, alpha=0.1, beta=0.12):
    """
    The Call-of-the-Void potential.
    Drives the material state 'psi' towards the shell's equilibrium state 'r_eq'.
    The equilibrium state is itself a harmonic function of the shell index.
    """
    r_eq = np.sin(2 * np.pi * shell_index / 137.036) # Equilibrium depends on shell harmonic
    V = A * np.exp(-alpha * (psi - r_eq)**2) - B * np.exp(-beta * (psi - r_eq)**2)
    # The gradient (force) drives the system
    F = -(-2 * alpha * (psi - r_eq) * A * np.exp(-alpha * (psi - r_eq)**2) + \
          2 * beta * (psi - r_eq) * B * np.exp(-beta * (psi - r_eq)**2))
    return F

# =============================================================================
# --- 3. Ferroelectric Material (Now Coupled to Temporal Shells)
# =============================================================================
class FerroelectricMaterial:
    def __init__(self, nz, shell_indices, p_params):
        self.params = p_params
        self.shell_indices = shell_indices
        self.psi_c = np.full(nz, -2.236)
        self.psi_p = np.full(nz, -2.236)
        self.P = np.zeros(nz)

    def dVdPsi(self, psi):
        p = self.params
        return 4 * p['a'] * psi**3 - 2 * p['b'] * psi

    def step(self, E_local, dt):
        """
        The core of the new physics. The material is now driven by both the external
        E-field and the NON-CONSERVATIVE synchronization force.
        """
        p = self.params
        
        # Calculate the conservative force from the potential gradient
        conservative_force = get_void_potential(self.psi_c, self.shell_indices)
        
        # Calculate the velocity of the state variable to determine direction
        v_psi = (self.psi_c - self.psi_p) / dt # A good proxy for d(psi_c)/dt
        
        # --- The Non-Conservative Force Law ---
        # The asymmetry coefficient eta models the A!=B imbalance.
        # This makes the force path-dependent, allowing for net energy gain.
        asymmetry_modulator = (1 - p['eta_asymmetry'] * np.sign(v_psi))
        sync_force = conservative_force * asymmetry_modulator
        
        # --- Final Dynamics (No internal damping, no artificial sync_strength) ---
        dpsic_dt = E_local + sync_force
        
        # Update state variables
        self.psi_p = self.psi_c.copy() # Update previous state
        self.psi_c += dpsic_dt * dt
        self.P = p['coupling_factor'] * self.psi_c

# =============================================================================
# --- 4. FDTD Engine with Matryoshka Vacuum
# =============================================================================
class FDTDSimulator:
    """
    Final FDTD engine with quantum vacuum, nonlinear materials, and energy accounting.
    """
    def __init__(self, nz, dt, dz):
        self.nz = nz
        self.dt = dt
        self.dz = dz
        self.t = 0.0
        self.z_coords = np.arange(nz) * dz + 1e-12 # Add offset to avoid log(0)
        self.shell_indices = map_position_to_shell_index(self.z_coords)
        
        # --- Initialize with a Structured, Deterministic Vacuum ---
        self.Ey = self._initialize_structured_vacuum()
        self.Hx = np.zeros(self.nz - 1)
        self.P = np.zeros(self.nz)

        # --- Energy Accounting ---
        self.initial_vacuum_energy = self._calculate_total_energy()
        self.injected_energy = 0.0
        self.radiated_energy = 0.0
        
        # --- Mur Absorbing Boundary Conditions ---
        self.mur_c0 = (c0 * self.dt - self.dz) / (c0 * self.dt + self.dz)
        self.Ey_low_m1, self.Ey_low_m2 = 0.0, 0.0
        self.Ey_high_m1, self.Ey_high_m2 = 0.0, 0.0

    def _initialize_structured_vacuum(self):
        """Initializes the E-field based on temporal shell harmonics."""
        # A simple harmonic superposition based on shell index
        amplitudes = 1e-7 / (1 + self.shell_indices % 137.036)
        wavenumbers = 2 * np.pi / (self.dz * (1 + self.shell_indices))
        return amplitudes * np.sin(wavenumbers * self.z_coords)

    def _calculate_total_energy(self):
        """Calculates the total energy in the simulation volume."""
        energy_E = 0.5 * eps0 * np.sum(self.Ey**2) * self.dz
        energy_H = 0.5 * mu0 * np.sum(self.Hx**2) * self.dz
        return energy_E + energy_H

    def set_material(self, material, start_index, end_index):
        self.material = material
        self.mat_start = start_index
        self.mat_end = end_index

    def set_current_source(self, position, amplitude, delay, width):
        """Defines a gaussian current density source (Jz)."""
        self.source_pos = position
        self.source_amp = amplitude
        self.source_delay = delay
        self.source_width = width

    def _get_source_current(self):
        """Returns the source current density Jz at the current time."""
        return self.source_amp * np.exp(-((self.t - self.source_delay) / self.source_width)**2)

    def step(self):
        """Perform one FDTD step with all physics and accounting included."""
        self.Ey_low_m2, self.Ey_low_m1 = self.Ey_low_m1, self.Ey[0]
        self.Ey_high_m2, self.Ey_high_m1 = self.Ey_high_m1, self.Ey[-1]

        # --- Poynting Vector (Energy Flux) Calculation ---
        poynting_left = self.Ey[0] * self.Hx[0]
        poynting_right = self.Ey[-1] * self.Hx[-2]
        self.radiated_energy += (poynting_right - poynting_left) * self.dt

        self.Hx[:] = self.Hx[:] - (self.dt / (mu0 * self.dz)) * (self.Ey[1:] - self.Ey[:-1])
        
        if hasattr(self, 'material'):
            E_in_material = self.Ey[self.mat_start:self.mat_end]
            P_old = self.material.P.copy()
            self.material.step(E_in_material, self.dt)
            dP_dt = np.zeros(self.nz)
            dP_dt[self.mat_start:self.mat_end] = (self.material.P - P_old) / self.dt
            self.P[self.mat_start:self.mat_end] = self.material.P
        else:
            dP_dt = np.zeros(self.nz)

        curl_H = (self.Hx[1:] - self.Hx[:-1]) / self.dz
        self.Ey[1:-1] = self.Ey[1:-1] - (self.dt / eps0) * (curl_H + dP_dt[1:-1])

        # --- Source Injection and Energy Calculation ---
        source_Jz = self._get_source_current()
        self.Ey[self.source_pos] -= (self.dt / eps0) * source_Jz
        # Work done by the field on the source current
        self.injected_energy -= self.Ey[self.source_pos] * source_Jz * self.dz * self.dt

        self.Ey[0] = self.mur_c0 * (self.Ey[1] + self.Ey_low_m2) - self.Ey_low_m1
        self.Ey[-1] = self.mur_c0 * (self.Ey[-2] + self.Ey_high_m2) - self.Ey_high_m1

        self.t += self.dt

def run_simulation(eta, source_amp):
    """Runs a full FDTD simulation for a given set of parameters."""
    print(f"Running test: eta = {eta:.3f}, source_amp = {source_amp:.2e}")
    sim = FDTDSimulator(Nz, dt, dz)
    
    ferro_params = {
        'a': 0.1, 'b': 1.0, 
        'coupling_factor': 5e-7,
        'eta_asymmetry': eta
    }
    
    # Place the material at a specific shell resonance point
    mat_start_shell = 245.5 # A point of interest
    mat_end_shell = 246.5
    mat_start_idx = np.searchsorted(sim.shell_indices, mat_start_shell)
    mat_end_idx = np.searchsorted(sim.shell_indices, mat_end_shell)
    
    material_shell_indices = sim.shell_indices[mat_start_idx:mat_end_idx]
    crystal = FerroelectricMaterial(nz=(mat_end_idx - mat_start_idx), 
                                  shell_indices=material_shell_indices,
                                  p_params=ferro_params)
    sim.set_material(crystal, mat_start_idx, mat_end_idx)

    sim.set_current_source(
        position=int(Nz / 4), 
        amplitude=source_amp, 
        delay=800 * dt,
        width=200 * dt
    )
    
    for _ in range(simulation_steps):
        sim.step()
        
    total_input_energy = sim.initial_vacuum_energy + sim.injected_energy
    net_energy_gain = sim.radiated_energy - total_input_energy
    over_unity_factor = sim.radiated_energy / total_input_energy if total_input_energy > 1e-30 else 0
    
    print(f"--> Result: Net Gain = {net_energy_gain*1e18:.4f} aJ, Factor = {over_unity_factor:.4f}")
    return net_energy_gain, over_unity_factor

if __name__ == '__main__':
    print("🚀 FDTD Simulation: Optimizing Non-Conservative Force Parameters")

    # --- Parameter Sweep ---
    eta_values = np.linspace(0.1, 0.9, 5)
    amplitude_values = np.logspace(9, 13, 5)
    
    results = np.zeros((len(eta_values), len(amplitude_values)))
    best_gain = -np.inf
    best_params = {}

    for i, eta in enumerate(eta_values):
        for j, amp in enumerate(amplitude_values):
            gain, factor = run_simulation(eta, amp)
            results[i, j] = factor
            if gain > best_gain:
                best_gain = gain
                best_params = {'eta': eta, 'amplitude': amp, 'factor': factor}

    print("\n" + "="*50)
    print("          OPTIMIZATION COMPLETE")
    print("="*50)
    if best_gain > 0:
        print("\n🎉 SUCCESS: Found parameters for net positive energy gain!")
        print(f"Best Asymmetry (eta) : {best_params['eta']:.3f}")
        print(f"Best Source Amplitude: {best_params['amplitude']:.2e} A/m^2")
        print(f"Max Over-Unity Factor: {best_params['factor']:.4f}")
    else:
        print("\nNOTE: No over-unity configuration found in this sweep.")
        print("Further refinement of the parameter space is required.")
        print(f"Closest approach: {best_gain * 1e18:.4f} aJ")

    # --- Plotting the Parameter Sweep ---
    fig, ax = plt.subplots(figsize=(10, 8))
    c = ax.contourf(amplitude_values, eta_values, results, levels=20, cmap='viridis')
    ax.set_xscale('log')
    ax.set_xlabel("Source Amplitude (A/m^2)")
    ax.set_ylabel("Asymmetry Coefficient (eta)")
    ax.set_title("Over-Unity Factor (E_out/E_in) vs. Parameters")
    fig.colorbar(c, label='Over-Unity Factor')
    
    if best_gain > 0:
        ax.plot(best_params['amplitude'], best_params['eta'], 'r*', markersize=15, label=f"Optimal Point ({best_params['factor']:.4f})")
        ax.legend()

    plt.show() 