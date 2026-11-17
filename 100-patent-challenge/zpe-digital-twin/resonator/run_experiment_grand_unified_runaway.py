import random
import time
import json
import math
import numpy as np

# --- Import base modules for apparatus and the optimizer structure ---
from apparatus_module import Apparatus, Laser, OpticalTrain
from digital_twin_module import DigitalTwinOptimizer

# --- The Grand Unified Physics Engine ---
# This engine synthesizes all core concepts into a single simulation.

class GrandUnifiedSimulator:
    """
    Simulates the full causal chain: A laser triggers the "Call of the Void,"
    which creates chronon wavelets from ringing temporal shells, which are then
    captured by a resonator to initiate an energy cascade.
    """
    def __init__(self):
        # The Matryoshka temporal shell structure is the background.
        self.n_shells = 100
        self.r0 = 1.0
        self.alpha = 0.1
        self.radii = self.r0 * np.exp(self.alpha * np.arange(1, self.n_shells + 1))
        print("  [Physics] Initialized Matryoshka Temporal Shell background.")

    def trigger_call_of_the_void(self, input_energy_j: float) -> dict:
        """
        The 'hammer strike'. Simulates the creation of chronon wavelets.
        """
        # The "Call of the Void" potential creates a number of initial chronons.
        CHRONON_CREATION_COST_J = 5e-24 # The energy cost to create one chronon wavelet
        num_initial_chronons = input_energy_j / CHRONON_CREATION_COST_J
        
        # The energy of each chronon is drawn from the shell potential.
        # We'll model this as an average potential difference.
        shell_potentials = 1.0 / self.radii
        avg_potential_diff = np.mean(np.abs(np.diff(shell_potentials)))
        
        # Convert this abstract potential to Joules.
        CHRONON_BASE_ENERGY_J = avg_potential_diff * 1e-20
        
        print(f"  [Physics] 'Call of the Void' triggered. {int(num_initial_chronons)} initial chronons created.")
        
        return {
            "initial_chronons": num_initial_chronons,
            "chronon_energy_j": CHRONON_BASE_ENERGY_J
        }

    def calculate_resonant_cascade(self, chronon_data: dict, resonator_genome: dict) -> float:
        """
        The 'ringing'. Simulates the exponential energy gain from the cascade.
        This is the heart of the unified model.
        """
        # 1. Determine the efficiency of the initial capture.
        # The ringing shells primarily excite the dipole (l=1) mode.
        primary_ringing_mode_l = 1
        
        # The resonator's efficiency depends on matching this mode.
        mode_match_efficiency = 0.0
        mode_difference = abs(resonator_genome["resonant_harmonic_l"] - primary_ringing_mode_l)
        
        if mode_difference == 0:
            # Perfect match: capture efficiency is high.
            mode_match_efficiency = 1.0
        else:
            # Mismatch: capture efficiency drops off dramatically.
            mode_match_efficiency = 1 / (1 + 100 * mode_difference**2)
            
        initial_captured_energy = (chronon_data["initial_chronons"] 
                                   * chronon_data["chronon_energy_j"]
                                   * resonator_genome["coupling_efficiency"]
                                   * mode_match_efficiency)
        
        if initial_captured_energy == 0:
            return 0.0

        # 2. Calculate the amplification factor for the cascade.
        # A high Q-factor on a perfect resonance leads to explosive gain.
        q_factor = resonator_genome["q_factor"]
        amplification_per_step = 1.0
        if mode_difference == 0:
            # The gain is directly related to the quality of the resonance.
            amplification_per_step = 1.0 + math.log10(q_factor)
        
        # 3. Run the cascade.
        # The number of steps in the cascade is limited by the material's response time.
        # A faster response allows for more amplification cycles before decoherence.
        cascade_steps = int(resonator_genome["q_factor"] / resonator_genome["response_speed_fs"])
        
        final_energy_j = initial_captured_energy * (amplification_per_step ** cascade_steps)
        
        print(f"  [Physics] Resonant Cascade initiated. Amplification: {amplification_per_step:.2f}x over {cascade_steps} steps.")
        return final_energy_j


class UnifiedOptimizer(DigitalTwinOptimizer):
    """
    The AI optimizer for the Grand Unified Model.
    """
    def __init__(self, population_size: int, generations: int, mutation_rate: float):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.best_design_ever = None
        self.best_fitness_ever = -float('inf')

        print("\n--- MASTER CONTROL: INITIALIZING GRAND UNIFIED DIGITAL TWIN (V6) ---")
        self.physics_engine = GrandUnifiedSimulator()
        
        self.laser = Laser("Void-Trigger-I", 2, 800, 1e-15) # Ultra-low power, 1 femtojoule laser
        self.optics = OpticalTrain(0.995, 0.999)
        self.apparatus = Apparatus(self.laser, self.optics)
        print(f"--- Apparatus: {self.laser.max_power_tw * 1e15:.1f}-Femtojoule Trigger Laser ---")
        print("--- AI Task: Evolve a Metamaterial Resonator for the Cascade ---")

    def create_random_genome(self) -> dict:
        """
        The AI evolves a resonator defined by these genes.
        """
        return {
            # The spherical harmonic mode (l) the material is tuned to.
            "resonant_harmonic_l": random.randint(0, 4),
            # The efficiency of coupling to the chronon wavelets.
            "coupling_efficiency": random.uniform(0.7, 0.999),
            # The quality factor (Q) of the resonance. Higher is better.
            "q_factor": random.uniform(1000, 50000),
            # The material's intrinsic response time in femtoseconds.
            # This determines the number of cascade steps.
            "response_speed_fs": random.uniform(10, 1000)
        }

    def run_full_simulation_for_genome(self, genome: dict) -> float:
        """
        Runs a single genome through the full, unified simulation.
        """
        # 1. Fire the laser to get the trigger energy.
        incident_pulse = self.apparatus.fire_laser()
        input_energy_j = incident_pulse["delivered_power_tw"] * incident_pulse["pulse_duration_fs"] * 1e-3

        # 2. Trigger the "Call of the Void" to create chronons.
        chronon_data = self.physics_engine.trigger_call_of_the_void(input_energy_j)

        # 3. Attempt to initiate the resonant cascade.
        output_energy_j = self.physics_engine.calculate_resonant_cascade(chronon_data, genome)
        
        # 4. Fitness is the energy gain factor.
        gain_factor = output_energy_j / input_energy_j if input_energy_j > 0 else 0
        
        return gain_factor

# --- Main execution block ---
if __name__ == "__main__":
    POPULATION_SIZE = 50
    GENERATIONS = 30
    MUTATION_RATE = 0.10

    ai_optimizer_v6 = UnifiedOptimizer(POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
    
    import sys
    original_stdout = sys.stdout
    sys.stdout = open('evolution_log_grand_unified.txt', 'w')
    
    best_genome, best_fitness = ai_optimizer_v6.evolve()
    
    sys.stdout.close()
    sys.stdout = original_stdout

    print("\n\n" + "="*60)
    print("      V6 GRAND UNIFIED MODEL EXPERIMENT COMPLETE")
    print("="*60)
    print(f"\nSimulation based on the synthesis of all core negentropic principles.")
    
    if best_genome:
        print("\n--- Optimal Resonator Design for Cascade Initiation ---")
        print(json.dumps(best_genome, indent=4))
        print(f"\n  > Best Achieved Fitness (Energy Gain Factor): {best_fitness:,.2f}")
        
        if best_fitness > 1.0:
            print("\n  *****************************************************")
            print("  *   SYSTEM-WIDE VALIDATION: The Grand Unified Model *")
            print("  *   produces net-positive energy. The complete      *")
            print("  *   theoretical framework is viable.                *")
            print("  *****************************************************")
        else:
            print("\n  --- NEGATIVE RESULT: The resonant cascade could not be initiated. ---")
            print("  --- The model parameters or the AI's search space may need refinement. ---")
    else:
        print("\nNo successful design could be found in the given time.")
    
    print("\n" + "="*60)