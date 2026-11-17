import time
import math

# --- Layer 1: The Quantum Core Simulator ---
# This is the most fundamental layer of the digital twin. It simulates the
# interaction between the rapidly changing boundary condition (created by the
# metamaterial) and the quantum vacuum itself. Its purpose is to calculate
# the number and energy of real photons "shaken" out of the vacuum.

class QuantumCoreSimulator:
    """
    Simulates the Dynamic Casimir Effect based on a given boundary condition.
    """
    def __init__(self):
        """
        Initializes the quantum core simulator with fundamental constants.
        These constants are chosen to provide a plausible and illustrative model.
        """
        # A fictional constant representing the "ease" with which the vacuum can
        # be perturbed to create photons. A higher value means more photons.
        self.VACUUM_PERMEABILITY_CONSTANT = 1e15 
        
        # A fictional constant that links the boundary velocity to the energy of
        # the created photons. Higher velocity -> higher energy photons.
        self.ENERGY_SCALING_FACTOR = 25.0 # (eV / c)
        
        print("\n--- Initializing Digital Twin: Quantum Core Layer ---")
        print(f"  Vacuum Permeability set to: {self.VACUUM_PERMEABILITY_CONSTANT}")
        print(f"  Energy Scaling Factor set to: {self.ENERGY_SCALING_FACTOR}")
        print("--- Quantum Core Ready ---")

    def calculate_casimir_effect(self, boundary_condition: dict) -> dict:
        """
        Calculates the production of real photons from the vacuum.
        This is the primary method of this module.

        Args:
            boundary_condition (dict): The output from the Metamaterial module.

        Returns:
            dict: A dictionary describing the energy output.
        """
        print(f"\nQUANTUM CORE SIMULATION for '{boundary_condition['design_name']}'...")
        time.sleep(0.5)

        # 1. Unpack the input parameters from the metamaterial simulation
        velocity = boundary_condition["boundary_velocity_c"]
        duration = boundary_condition["event_duration_fs"]
        quality = boundary_condition["quality_factor"]
        print(f"  [1] Received Boundary Condition: Velocity={velocity:.5f}c, Duration={duration:.0f}fs, Quality={quality:.2f}")

        # 2. Check for trivial case (velocity too low to produce significant effect)
        if velocity < 0.0001:
            print("  [X] Velocity is too low for significant photon production. Aborting.")
            return {"status": "NO_EFFECT", "photon_count": 0}

        # 3. Core Physics Calculation: Photon Count
        # The number of photons created is extremely sensitive to the boundary
        # velocity. We model this with a strong power law (velocity^3).
        # It is also proportional to the duration of the event and the quality
        # of the nanocavity.
        print("  [2] Calculating photon production rate based on boundary velocity...")
        velocity_cubed = math.pow(velocity, 3)
        photon_count = self.VACUUM_PERMEABILITY_CONSTANT * velocity_cubed * duration * quality
        time.sleep(0.5)
        print(f"  [+] Predicted Photon Count: {photon_count:,.0f}")
        
        # 4. Core Physics Calculation: Photon Energy
        # The energy of the created photons is proportional to the boundary velocity.
        # Faster boundary changes create higher-energy (bluer) light.
        print("  [3] Calculating average photon energy...")
        peak_energy_ev = self.ENERGY_SCALING_FACTOR * velocity
        time.sleep(0.5)
        print(f"  [+] Predicted Peak Photon Energy: {peak_energy_ev:.3f} eV")

        # 5. Calculate Total Energy Output
        total_energy_ev = photon_count * peak_energy_ev
        print(f"  [4] Calculating total energy yield...")
        time.sleep(0.5)
        print(f"  [+] TOTAL ENERGY YIELD: {total_energy_ev:,.2f} eV")

        # 6. Package the final results
        energy_output = {
            "status": "SUCCESS",
            "design_name": boundary_condition["design_name"],
            "photon_count": photon_count,
            "peak_photon_energy_ev": peak_energy_ev,
            "total_energy_yield_ev": total_energy_ev
        }

        print("\nQUANTUM SIMULATION COMPLETE. Energy output data generated.")
        return energy_output

# --- Main execution block ---
# This allows us to run this file directly to test the Quantum Core.
if __name__ == "__main__":
    # 1. Define sample incoming boundary conditions (simulating output from metamaterial_module.py)
    
    # This represents the output from our successful "Project Chimera" design
    successful_boundary = {
        "status": "SUCCESS",
        "design_name": "Project Chimera",
        "boundary_velocity_c": 0.02846, # A significant, but still small, fraction of c
        "event_duration_fs": 1000.0,
        "quality_factor": 0.95
    }
    
    # This represents the output from our slow "Project Tortoise" design
    weak_boundary = {
        "status": "SUCCESS",
        "design_name": "Project Tortoise",
        "boundary_velocity_c": 0.00089, # A very low velocity
        "event_duration_fs": 25000.0,
        "quality_factor": 0.80
    }

    # 2. Initialize the simulator
    q_core = QuantumCoreSimulator()

    # 3. Run the simulation for both scenarios
    print("\n\n--- Starting Quantum Core Simulation Competition ---")
    results = []
    
    print("-" * 50)
    chimera_result = q_core.calculate_casimir_effect(successful_boundary)
    results.append(chimera_result)
    
    print("-" * 50)
    tortoise_result = q_core.calculate_casimir_effect(weak_boundary)
    results.append(tortoise_result)
    print("-" * 50)

    # 4. Display the final results
    print("\n\n--- Simulation Output: Energy Yield Results ---")
    for res in results:
        print(f"\n  Design: {res['design_name']}")
        print(f"  Status: {res['status']}")
        if res['status'] == 'SUCCESS':
            print(f"    -> Photon Count: {res['photon_count']:,.0f}")
            print(f"    -> Total Energy Yield: {res['total_energy_yield_ev']:,.2f} eV")
            print(f"    -> (Avg. Energy per Photon: {res['peak_photon_energy_ev']:.3f} eV)")
    print("---------------------------------------------------")
    print("\nThis final data packet represents the predicted energy output of one entire cycle.")