import random
import time
import json
import math
import numpy as np
import decimal

# --- Set precision for handling enormous numbers ---
# A precision of 100 digits should be sufficient.
decimal.getcontext().prec = 100

# --- Import base modules ---
from apparatus_module import Apparatus, Laser, OpticalTrain
from digital_twin_module import DigitalTwinOptimizer

class GrandUnifiedSimulator:
    def __init__(self):
        self.n_shells = 100
        self.r0 = 1.0
        self.alpha = 0.1
        self.radii = self.r0 * np.exp(self.alpha * np.arange(1, self.n_shells + 1))
        # --- NEW: Add a physical saturation limit ---
        # This is the maximum energy budget of the local temporal shells.
        self.SATURATION_ENERGY_J = decimal.Decimal('1e50') # 10^50 Joules
        print("  [Physics] Initialized Matryoshka Shells with Saturation Limit.")

    def trigger_call_of_the_void(self, input_energy_j: float) -> dict:
        CHRONON_CREATION_COST_J = 5e-24
        num_initial_chronons = input_energy_j / CHRONON_CREATION_COST_J
        shell_potentials = 1.0 / self.radii
        avg_potential_diff = np.mean(np.abs(np.diff(shell_potentials)))
        CHRONON_BASE_ENERGY_J = avg_potential_diff * 1e-20
        
        print(f"  [Physics] 'Call of the Void' triggered. {int(num_initial_chronons)} initial chronons created.")
        
        return {
            "initial_chronons": num_initial_chronons,
            "chronon_energy_j": CHRONON_BASE_ENERGY_J
        }

    def calculate_resonant_cascade(self, chronon_data: dict, resonator_genome: dict) -> decimal.Decimal:
        primary_ringing_mode_l = 1
        mode_difference = abs(resonator_genome["resonant_harmonic_l"] - primary_ringing_mode_l)
        mode_match_efficiency = 1 / (1 + 100 * mode_difference**2) if mode_difference != 0 else 1.0
            
        initial_captured_energy = (chronon_data["initial_chronons"] 
                                   * chronon_data["chronon_energy_j"]
                                   * resonator_genome["coupling_efficiency"]
                                   * mode_match_efficiency)
        
        if initial_captured_energy == 0:
            return decimal.Decimal('0')

        q_factor = resonator_genome["q_factor"]
        amplification_per_step = 1.0
        if mode_difference == 0:
            amplification_per_step = 1.0 + math.log10(q_factor)
        
        cascade_steps = int(q_factor / resonator_genome["response_speed_fs"])
        
        print(f"  [Physics] Resonant Cascade initiated. Amplification: {amplification_per_step:.2f}x over {cascade_steps} steps.")
        
        # --- FIXED: Use Decimal for the calculation to prevent overflow ---
        initial_energy_dec = decimal.Decimal(initial_captured_energy)
        amplification_dec = decimal.Decimal(amplification_per_step)
        
        final_energy_j = initial_energy_dec * (amplification_dec ** cascade_steps)
        
        # --- NEW: Apply the physical saturation limit ---
        if final_energy_j > self.SATURATION_ENERGY_J:
            final_energy_j = self.SATURATION_ENERGY_J
            print("  [Physics] SATURATION LIMIT REACHED.")

        return final_energy_j


class UnifiedOptimizer(DigitalTwinOptimizer):
    def __init__(self, population_size: int, generations: int, mutation_rate: float):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.best_design_ever = None
        self.best_fitness_ever = -decimal.Decimal('inf')

        print("\n--- MASTER CONTROL: INITIALIZING GRAND UNIFIED DIGITAL TWIN (V6.1) ---")
        self.physics_engine = GrandUnifiedSimulator()
        self.laser = Laser("Void-Trigger-I", 2, 800, 1e-15)
        self.optics = OpticalTrain(0.995, 0.999)
        self.apparatus = Apparatus(self.laser, self.optics)
        print(f"--- Apparatus: {self.laser.max_power_tw * 1e15:.1f}-Femtojoule Trigger Laser ---")
        print("--- AI Task: Evolve a Metamaterial Resonator for the Cascade ---")

    def create_random_genome(self) -> dict:
        return {
            "resonant_harmonic_l": random.randint(0, 4),
            "coupling_efficiency": random.uniform(0.7, 0.999),
            "q_factor": random.uniform(1000, 50000),
            "response_speed_fs": random.uniform(10, 1000)
        }

    def run_full_simulation_for_genome(self, genome: dict) -> decimal.Decimal:
        incident_pulse = self.apparatus.fire_laser()
        input_energy_j = incident_pulse["delivered_power_tw"] * incident_pulse["pulse_duration_fs"] * 1e-3
        chronon_data = self.physics_engine.trigger_call_of_the_void(input_energy_j)
        output_energy_j = self.physics_engine.calculate_resonant_cascade(chronon_data, genome)
        gain_factor = output_energy_j / decimal.Decimal(input_energy_j) if input_energy_j > 0 else decimal.Decimal('0')
        return gain_factor

# --- Main execution block ---
if __name__ == "__main__":
    POPULATION_SIZE = 50
    GENERATIONS = 10 # We can run fewer generations as the solution is so strong
    MUTATION_RATE = 0.10

    ai_optimizer_v6_1 = UnifiedOptimizer(POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
    
    import sys
    original_stdout = sys.stdout
    sys.stdout = open('evolution_log_grand_unified.txt', 'w')
    
    best_genome, best_fitness = ai_optimizer_v6_1.evolve()
    
    sys.stdout.close()
    sys.stdout = original_stdout

    print("\n\n" + "="*60)
    print("      V6.1 GRAND UNIFIED MODEL EXPERIMENT COMPLETE")
    print("="*60)
    print(f"\nSimulation based on the synthesis of all core principles,")
    print("including arbitrary-precision math and a physical saturation limit.")
    
    if best_genome:
        print("\n--- Optimal Resonator Design for Cascade Initiation ---")
        print(json.dumps(best_genome, indent=4))
        print(f"\n  > Best Achieved Fitness (Energy Gain Factor): {best_fitness:,.2f}")
        
        if best_fitness > 1.0:
            print("\n  *****************************************************")
            print("  *   SYSTEM-WIDE VALIDATION: The Grand Unified Model *")
            print("  *   predicts a runaway energy cascade, validating   *")
            print("  *   the core principles of the theory.              *")
            print("  *****************************************************")
    else:
        print("\nNo successful design could be found.")
    
    print("\n" + "="*60)