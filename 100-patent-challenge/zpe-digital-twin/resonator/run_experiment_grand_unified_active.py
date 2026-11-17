import random
import time
import json
import math
import numpy as np
import decimal

# --- Set precision for handling enormous numbers ---
decimal.getcontext().prec = 100

# --- Import base modules ---
from apparatus_module import Apparatus, Laser, OpticalTrain
from digital_twin_module import DigitalTwinOptimizer

# --- The "AI in the Loop" ---
class PIDController:
    """A simple PID controller to act as the live AI."""
    def __init__(self, Kp, Ki, Kd, target):
        self.Kp = decimal.Decimal(Kp)
        self.Ki = decimal.Decimal(Ki)
        self.Kd = decimal.Decimal(Kd)
        self.target = decimal.Decimal(target)
        self.integral = decimal.Decimal('0')
        self.last_error = decimal.Decimal('0')

    def compute_control_signal(self, current_value):
        # Convert current_value to Decimal if it's a float
        if isinstance(current_value, float):
            current_value = decimal.Decimal(str(current_value))
        
        error = self.target - current_value
        self.integral += error
        derivative = error - self.last_error
        self.last_error = error
        
        # The control signal will adjust the Q-factor damping.
        control_signal = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        return float(control_signal)  # Convert back to float for compatibility

class GrandUnifiedSimulator:
    def __init__(self):
        self.n_shells = 7
        self.r0 = 1.0
        self.alpha = 0.1
        self.radii = self.r0 * np.exp(self.alpha * np.arange(1, self.n_shells + 1))
        self.SATURATION_ENERGY_J = decimal.Decimal('1e50')
        print("  [Physics] Initialized Matryoshka Shells with Active Control.")
        
        # Initialize PID controller with tuned parameters
        self.controller = PIDController(
            Kp=5.80,
            Ki=0.36,
            Kd=11.97,
            target=1e6  # Target power in Watts
        )
        
        # Current Q-factor (will be adjusted by controller)
        self.current_q = decimal.Decimal('49990.0')
        self.base_q = decimal.Decimal('49990.0')

    def adjust_q_factor(self, current_power):
        """Adjust Q-factor based on current power level."""
        control_signal = self.controller.compute_control_signal(current_power)
        
        # Use tanh to keep the adjustment bounded between -1 and 1
        damping = decimal.Decimal(str(math.tanh(float(control_signal) / 1000.0)))
        
        # Calculate new Q factor with bounds checking
        min_q = decimal.Decimal('10.0')
        max_q = self.base_q * decimal.Decimal('10.0')
        
        self.current_q = max(min_q, min(self.base_q * (decimal.Decimal('1.0') + damping * decimal.Decimal('0.5')), max_q))
        
        return self.current_q

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

    def calculate_resonant_cascade(self, chronon_data: dict, resonator_genome: dict) -> dict:
        primary_ringing_mode_l = 1
        mode_difference = abs(resonator_genome["resonant_harmonic_l"] - primary_ringing_mode_l)
        mode_match_efficiency = 1 / (1 + 100 * mode_difference**2) if mode_difference != 0 else 1.0
            
        initial_captured_energy = (chronon_data["initial_chronons"] 
                                 * chronon_data["chronon_energy_j"]
                                 * resonator_genome["coupling_efficiency"]
                                 * mode_match_efficiency)
        
        # Run the cascade with active control
        current_energy = decimal.Decimal(str(initial_captured_energy))
        energy_history = [current_energy]
        
        # Simulation parameters
        time_steps = 200
        
        for step in range(time_steps):
            # Adjust Q-factor based on current power level
            current_q = self.adjust_q_factor(float(current_energy))
            
            # Calculate amplification factor based on Q
            amplification = decimal.Decimal('1.0') + (current_q / decimal.Decimal('1000.0'))
            
            # Update energy with amplification
            current_energy = current_energy * amplification
            
            # Apply saturation limit
            if current_energy > self.SATURATION_ENERGY_J:
                current_energy = self.SATURATION_ENERGY_J
                energy_history.append(current_energy)
                print(f"  [Physics] SATURATION LIMIT REACHED.")
                break
                
            energy_history.append(current_energy)
            
            # Early exit if energy drops too low
            if current_energy < decimal.Decimal('1e-30'):
                break
        
        # Calculate statistics
        energy_array = np.array([float(e) for e in energy_history])
        amplification = float(energy_history[-1] / energy_history[0]) if len(energy_history) > 1 else 1.0
        
        return {
            "final_energy_j": float(energy_history[-1]),
            "amplification": amplification,
            "num_steps": len(energy_history) - 1,
            "energy_history": [float(e) for e in energy_history],
            "final_q": float(self.current_q)
        }

class UnifiedOptimizer:
    def __init__(self, population_size: int, generations: int, mutation_rate: float):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.best_design_ever = None
        self.best_fitness_ever = -decimal.Decimal('inf')

        print("\n--- MASTER CONTROL: INITIALIZING GRAND UNIFIED DIGITAL TWIN WITH ACTIVE CONTROL (V7.0) ---")
        self.physics_engine = GrandUnifiedSimulator()
        self.laser = Laser("Void-Trigger-I", 2, 800, 1e-15)
        self.optics = OpticalTrain(0.995, 0.999)
        self.apparatus = Apparatus(self.laser, self.optics)
        print(f"--- Apparatus: {self.laser.max_power_tw * 1e15:.1f}-Femtojoule Trigger Laser ---")
        print("--- AI Task: Evolve a Metamaterial Resonator with Active Control ---")

    def create_random_genome(self):
        return {
            "resonant_harmonic_l": random.choice([1, 2, 3, 4, 5, 7, 11, 13]),
            "coupling_efficiency": 0.000999,  # Fixed coupling for active control
            "q_factor": 4.99900,  # Base Q-factor (will be actively controlled)
            "response_speed_fs": 10000.1  # Fixed response time
        }

    def run_full_simulation_for_genome(self, genome: dict) -> float:
        # Fire the laser
        print(f"\n--- Evaluating Design {genome['id']}/{self.population_size} ---")
        print("FIRING SEQUENCE INITIATED...")
        
        # Simulate laser firing and get pulse data
        pulse_data = self.apparatus.fire_laser()
        # Calculate energy from power (in TW) and pulse duration (in fs)
        # 1 TW = 1e12 W, 1 fs = 1e-15 s, so 1 TW * 1 fs = 1e-3 J
        delivered_energy = pulse_data['delivered_power_tw'] * pulse_data['pulse_duration_fs'] * 1e-3
        
        # Trigger the void and run the cascade
        chronon_data = self.physics_engine.trigger_call_of_the_void(delivered_energy)
        result = self.physics_engine.calculate_resonant_cascade(chronon_data, genome)
        
        # Calculate fitness based on final energy and stability
        final_energy = result["final_energy_j"]
        fitness = float(final_energy)  # Simple fitness: maximize final energy
        
        print(f"  [Physics] Resonant Cascade initiated. Amplification: {result['amplification']:.2f}x over {result['num_steps']} steps.")
        print(f"  [AI] Final energy: {final_energy:.2e} J, Fitness: {fitness:.2e}")
        
        return fitness

    def evolve(self):
        # Create initial population
        population = [self.create_random_genome() for _ in range(self.population_size)]
        
        # Main evolution loop
        for gen in range(self.generations):
            print(f"\n==================== GENERATION {gen+1}/{self.generations} ====================")
            
            # Evaluate all genomes
            for i, genome in enumerate(population):
                genome['id'] = i + 1
                genome['fitness'] = self.run_full_simulation_for_genome(genome)
                
                # Track the best design
                if genome['fitness'] > self.best_fitness_ever:
                    self.best_fitness_ever = genome['fitness']
                    self.best_design_ever = genome.copy()
            
            # Simple selection and mutation (for demonstration)
            population.sort(key=lambda x: x['fitness'], reverse=True)
            
            # Keep top 50%
            keep = self.population_size // 2
            population = population[:keep]
            
            # Repopulate with mutations
            while len(population) < self.population_size:
                parent = random.choice(population[:keep])
                child = parent.copy()
                
                # Mutate harmonic mode
                if random.random() < self.mutation_rate:
                    child['resonant_harmonic_l'] = random.choice([1, 2, 3, 4, 5, 7, 11, 13])
                
                population.append(child)
        
        return self.best_design_ever, self.best_fitness_ever

# --- Main execution block ---
if __name__ == "__main__":
    # Run the optimization
    POPULATION_SIZE = 50
    GENERATIONS = 10
    MUTATION_RATE = 0.3
    
    print("\n=== ZPE DIGITAL TWIN: ACTIVE CONTROL EXPERIMENT ===")
    print(f"Population: {POPULATION_SIZE}, Generations: {GENERATIONS}, Mutation Rate: {MUTATION_RATE}")
    
    optimizer = UnifiedOptimizer(
        population_size=POPULATION_SIZE,
        generations=GENERATIONS,
        mutation_rate=MUTATION_RATE
    )
    
    start_time = time.time()
    best_design, best_fitness = optimizer.evolve()
    end_time = time.time()
    
    # Print final results
    print("\n" + "="*60)
    print("     ACTIVE CONTROL EXPERIMENT COMPLETE")
    print("="*60)
    print("\n=== BEST DESIGN ===")
    print(json.dumps(best_design, indent=2))
    print(f"\nFinal Fitness: {best_fitness:.2e}")
    print(f"Total Runtime: {end_time - start_time:.2f} seconds")
    
    # Save results
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    with open(f'active_control_results_{timestamp}.json', 'w') as f:
        json.dump({
            'best_design': best_design,
            'best_fitness': best_fitness,
            'parameters': {
                'population_size': POPULATION_SIZE,
                'generations': GENERATIONS,
                'mutation_rate': MUTATION_RATE
            },
            'timestamp': timestamp,
            'runtime_seconds': end_time - start_time
        }, f, indent=2)
    
    print("\nResults saved to file.")
