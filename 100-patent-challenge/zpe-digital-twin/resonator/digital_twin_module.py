import random
import time
import json # To pretty-print the final results

# --- Import our previously created modules ---
# Make sure apparatus_module.py, metamaterial_module.py, and 
# quantum_core_module.py are in the same directory.
from apparatus_module import Apparatus, Laser, OpticalTrain
from metamaterial_module import Metamaterial
from quantum_core_module import QuantumCoreSimulator

# --- Layer 4: The Control & Optimization AI ---
# This module acts as the master controller. It uses a genetic algorithm
# to intelligently search the vast parameter space of possible metamaterial
# designs to find one that maximizes energy output without destroying itself.

class DigitalTwinOptimizer:
    """
    The AI controller that runs the entire simulation and optimizes the design.
    """
    def __init__(self, population_size: int, generations: int, mutation_rate: float):
        """
        Initializes the AI optimizer.

        Args:
            population_size (int): The number of designs to test in each generation.
            generations (int): The number of evolutionary cycles to run.
            mutation_rate (float): The probability of a random mutation occurring.
        """
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.best_design_ever = None
        self.best_fitness_ever = -float('inf')

        # --- Initialize all layers of the Digital Twin ---
        print("--- MASTER CONTROL: INITIALIZING ALL DIGITAL TWIN LAYERS ---")
        # Layer 3: The constant energy source
        self.laser = Laser("Optimizer-Pump", 150, 800, 1.0)
        self.optics = OpticalTrain(0.85, 0.99)
        self.apparatus = Apparatus(self.laser, self.optics)
        
        # Layer 1: The core physics engine
        self.q_core = QuantumCoreSimulator()
        print("--- ALL LAYERS INITIALIZED. OPTIMIZER READY. ---\n")

    def create_random_genome(self) -> dict:
        """Generates a single random metamaterial design 'genome'."""
        return {
            "coupling_efficiency": random.uniform(0.3, 0.99),
            "response_speed_ps": random.uniform(0.5, 20.0),
            "damage_threshold_tw": random.uniform(0.5, 2.0),
            "void_quality_factor": random.uniform(0.8, 0.99)
        }

    def run_full_simulation_for_genome(self, genome: dict) -> float:
        """
        Runs a single genome through the entire simulation pipeline and returns its fitness score.
        """
        # --- Layer 3: Fire the laser ---
        incident_pulse = self.apparatus.fire_laser()
        input_power_tw = incident_pulse["delivered_power_tw"]
        
        # --- Layer 2: Test the material ---
        material = Metamaterial("EvoDesign", genome)
        boundary_condition = material.calculate_response(incident_pulse)

        # --- Check for failure ---
        if boundary_condition["status"] == "FAILURE":
            return -1000 # Heavy penalty for designs that break

        # --- Layer 1: Calculate energy output ---
        energy_output = self.q_core.calculate_casimir_effect(boundary_condition)

        if energy_output["status"] == "NO_EFFECT":
            return 0
        
        # --- Calculate Fitness ---
        # Fitness is the ratio of energy out to energy in.
        # We convert everything to a consistent unit (Joules).
        # 1 TW = 1e12 J/s; 1 fs = 1e-15 s -> 1 TW*fs = 1e-3 J
        input_energy_j = input_power_tw * incident_pulse["pulse_duration_fs"] * 1e-3
        # 1 eV = 1.602e-19 J
        output_energy_j = energy_output["total_energy_yield_ev"] * 1.602e-19
        
        if input_energy_j == 0: return 0
        
        # Gain Factor (Energy out / Energy in)
        gain = output_energy_j / input_energy_j
        return gain

    def evolve(self):
        """The main genetic algorithm loop."""
        # 1. Create initial random population
        population = [self.create_random_genome() for _ in range(self.population_size)]

        for gen in range(self.generations):
            print(f"\n\n{'='*20} GENERATION {gen+1}/{self.generations} {'='*20}")
            
            # 2. Evaluate fitness of the entire population
            fitness_scores = []
            for i, genome in enumerate(population):
                print(f"\n--- Evaluating Design {i+1}/{self.population_size} ---")
                fitness = self.run_full_simulation_for_genome(genome)
                fitness_scores.append((fitness, genome))
            
            # 3. Sort by fitness (descending)
            fitness_scores.sort(key=lambda x: x[0], reverse=True)
            
            # 4. Check for new best design
            if fitness_scores[0][0] > self.best_fitness_ever:
                self.best_fitness_ever = fitness_scores[0][0]
                self.best_design_ever = fitness_scores[0][1]
                print(f"\n*** NEW BEST DESIGN FOUND IN GENERATION {gen+1}! Fitness (Gain): {self.best_fitness_ever:.6f} ***")

            print(f"\n--- Generation {gen+1} Summary ---")
            print(f"  Best Fitness in this Gen: {fitness_scores[0][0]:.6f}")
            print(f"  Overall Best Fitness:     {self.best_fitness_ever:.6f}")
            print(f"---------------------------\n")
            time.sleep(2) # Pause to review results

            # 5. Create the next generation
            next_generation = []
            
            # Elitism: The top 20% of designs survive unchanged
            elite_count = int(self.population_size * 0.2)
            next_generation.extend([g for f, g in fitness_scores[:elite_count]])
            
            # Crossover & Mutation: Fill the rest of the population
            while len(next_generation) < self.population_size:
                # Select two parents from the top 50%
                parent1 = random.choice(fitness_scores[:self.population_size//2])[1]
                parent2 = random.choice(fitness_scores[:self.population_size//2])[1]
                
                # Crossover: create a child
                child = {}
                for key in parent1:
                    child[key] = random.choice([parent1[key], parent2[key]])
                
                # Mutation
                if random.random() < self.mutation_rate:
                    key_to_mutate = random.choice(list(child.keys()))
                    # Create a new random value for the mutated gene
                    random_gene = self.create_random_genome()[key_to_mutate]
                    child[key_to_mutate] = random_gene
                
                next_generation.append(child)
            
            population = next_generation

        return self.best_design_ever, self.best_fitness_ever

# --- Main execution block ---
if __name__ == "__main__":
    # --- Configure the AI ---
    # NOTE: These are small values for a quick demonstration.
    # A real run would use a population of 1000+ and 100+ generations.
    POPULATION_SIZE = 10
    GENERATIONS = 5
    MUTATION_RATE = 0.1

    # --- Run the Optimizer ---
    ai_optimizer = DigitalTwinOptimizer(POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
    # Suppress the detailed simulation output for the evolution loop
    import sys
    original_stdout = sys.stdout
    sys.stdout = open('evolution_log.txt', 'w') # Redirect stdout to a log file
    
    best_genome, best_fitness = ai_optimizer.evolve()
    
    sys.stdout.close()
    sys.stdout = original_stdout # Restore stdout

    # --- Display Final Results ---
    print("\n\n" + "="*50)
    print("      GENETIC OPTIMIZATION COMPLETE")
    print("="*50)
    print(f"\nSearched {GENERATIONS} generations with a population of {POPULATION_SIZE}.")
    print(f"Log file 'evolution_log.txt' contains the detailed simulation steps.")
    
    if best_genome:
        print("\n--- Optimal Metamaterial Design Found ---")
        # Pretty print the final genome
        print(json.dumps(best_genome, indent=4))
        print(f"\n  > Best Achieved Fitness (Energy Gain Factor): {best_fitness:.6f}")
    else:
        print("\nNo successful design could be found in the given time.")
    
    print("\n" + "="*50)