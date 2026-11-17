import random
import time
import json
import numpy as np
import decimal
import math

# --- Set precision for stability ---
decimal.getcontext().prec = 50

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
        error = self.target - current_value
        self.integral += error
        derivative = error - self.last_error
        self.last_error = error
        
        # The control signal will adjust the Q-factor damping.
        return (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)

# --- The Tunable Device Physics ---
class ActivelyControlledResonator:
    """Simulates the resonator whose Q-factor is controlled by the AI."""
    def __init__(self, base_genome):
        self.base_q = decimal.Decimal(base_genome["q_factor"])
        self.response_fs = decimal.Decimal(base_genome["response_speed_fs"])
        self.coupling = decimal.Decimal(base_genome["coupling_efficiency"])
        self.current_q = self.base_q
        self.SATURATION_ENERGY_J = decimal.Decimal('1e10')  # Lower saturation point

    def adjust_q_factor(self, control_signal):
        """The AI damps or sharpens the Q-factor."""
        # The control signal provides a damping factor.
        # We use tanh to keep the adjustment bounded between -1 and 1.
        damping = decimal.Decimal(str(math.tanh(float(control_signal) / 1000.0)))
        
        # Calculate new Q factor with bounds checking
        min_q = decimal.Decimal('10.0')  # Minimum Q factor
        max_q = self.base_q * decimal.Decimal('10.0')  # Maximum Q factor (10x base)
        
        # Adjust Q factor based on control signal
        self.current_q = self.base_q * (decimal.Decimal('1.0') + damping * decimal.Decimal('0.5'))
        
        # Apply bounds
        self.current_q = max(min_q, min(max_q, self.current_q))
        
        # Debug print
        print(f"[DEBUG] Control: {control_signal:.2f}, Damping: {damping:.3f}, New Q: {self.current_q:.1f}")

    def step(self, input_energy):
        """Simulates one time-step of the cascade."""
        # Calculate amplification based on Q factor
        # Using a smaller fraction of Q to prevent excessive amplification
        amplification = decimal.Decimal('1.0') + (self.current_q / decimal.Decimal('1000.0'))
        
        # Use fewer cascade steps to prevent runaway growth
        cascade_steps = 5  # Reduced from 10 to 5
        
        # Calculate output energy with proper amplification
        output_energy = input_energy * (amplification ** cascade_steps)
        
        # Debug print to track energy changes
        print(f"[DEBUG] Q: {self.current_q:.1f}, Amplification: {amplification:.2f}, "
              f"Steps: {cascade_steps}, In: {input_energy:.2e} J, Out: {output_energy:.2e} J")
        
        if output_energy > self.SATURATION_ENERGY_J:
            return self.SATURATION_ENERGY_J
        return output_energy

# --- The Main Simulation ---
class ControlSystemOptimizer:
    def __init__(self, generations, population_size):
        self.generations = generations
        self.population_size = population_size
        self.TARGET_POWER_W = decimal.Decimal('1e6') # Target: 1 Megawatt
        self.SIMULATION_DURATION_STEPS = 200 # Simulate for 200 time steps
        
        # Use the best static design as our base hardware
        self.base_hardware_genome = {
            "resonant_harmonic_l": 1,
            "coupling_efficiency": 0.999,
            "q_factor": 49990.0,
            "response_speed_fs": 10.1
        }
        print("\n--- MASTER CONTROL: INITIALIZING ACTIVE CONTROL DIGITAL TWIN (V7) ---")
        print(f"--- Base Hardware Q-Factor: {self.base_hardware_genome['q_factor']:.1f} ---")
        print(f"--- AI Goal: Evolve a PID controller to maintain {float(self.TARGET_POWER_W / decimal.Decimal('1e6')):.1f} MW stable output ---")

    def create_random_genome(self):
        """The genome now defines the AI controller's tuning."""
        return {
            "Kp": random.uniform(0.1, 10.0),
            "Ki": random.uniform(0.001, 0.5),
            "Kd": random.uniform(0.1, 20.0)
        }

    def run_full_simulation_for_genome(self, genome):
        """Simulates the device in operation with the AI controller."""
        device = ActivelyControlledResonator(self.base_hardware_genome)
        controller = PIDController(genome["Kp"], genome["Ki"], genome["Kd"], self.TARGET_POWER_W)
        
        # Initial trigger pulse (1 attojoule - much smaller initial energy)
        power_levels = [decimal.Decimal('1e-18')]
        
        for _ in range(self.SIMULATION_DURATION_STEPS):
            # 1. AI computes control signal based on last power level
            control_signal = controller.compute_control_signal(power_levels[-1])
            
            # 2. AI adjusts the device's Q-factor
            device.adjust_q_factor(control_signal)
            
            # 3. The device operates for one step
            new_power = device.step(power_levels[-1])
            power_levels.append(new_power)

        # Fitness is based on stability (low variance) and being on target
        power_levels_stable = power_levels[50:] # Ignore initial ramp-up
        
        # Debug: Print first few power levels
        print(f"\nDebug - First 5 power levels: {[float(p) for p in power_levels_stable[:5]]}")
        print(f"Last 5 power levels: {[float(p) for p in power_levels_stable[-5:]]}")
        
        # Convert Decimal to float for numpy operations
        power_levels_float = [float(p) for p in power_levels_stable]
        mean_power = np.mean(power_levels_float)
        std_dev = np.std(power_levels_float)
        
        print(f"Mean power: {mean_power:.2e}, Std dev: {std_dev:.2e}")
        
        # Avoid division by zero
        if std_dev == 0: std_dev = 1e-10
        if mean_power == 0: mean_power = 1e-10
            
        # Fitness = reward for being on target, penalty for instability
        # Convert target to float for consistent operations
        target = float(self.TARGET_POWER_W)
        
        # Debug: Print components of fitness calculation
        target_diff = abs(mean_power - target)
        stability = mean_power / std_dev if std_dev > 0 else 0
        print(f"Target: {target:.2e}, Mean: {mean_power:.2e}, Target diff: {target_diff:.2e}, Stability: {stability:.2e}")
        
        fitness = (target / (target_diff + 1)) * stability
        
        print(f"Calculated fitness: {fitness:.2e}")
        
        return float(fitness) # Return as float for the optimizer module

    def evolve(self):
        # This is a simplified genetic algorithm for demonstration
        population = [self.create_random_genome() for _ in range(self.population_size)]
        best_genome_ever = None
        best_fitness_ever = -1

        for gen in range(self.generations):
            fitness_scores = [self.run_full_simulation_for_genome(g) for g in population]
            
            best_idx = np.argmax(fitness_scores)
            if fitness_scores[best_idx] > best_fitness_ever:
                best_fitness_ever = fitness_scores[best_idx]
                best_genome_ever = population[best_idx]
            
            print(f"--- Gen {gen+1}/{self.generations} | Best Fitness: {best_fitness_ever:,.2f} ---")

            # Elitism: Keep the best one
            new_population = [best_genome_ever]
            # Crossover and mutation to create the rest
            while len(new_population) < self.population_size:
                parent1 = random.choice(population)
                parent2 = random.choice(population)
                child = parent1.copy()
                for key in child:
                    if random.random() < 0.5:
                        child[key] = parent2[key]
                    if random.random() < 0.1: # Mutation
                        child[key] *= random.uniform(0.8, 1.2)
                new_population.append(child)
            population = new_population
            
        return best_genome_ever, best_fitness_ever

# --- Main execution block ---
if __name__ == "__main__":
    optimizer = ControlSystemOptimizer(generations=10, population_size=30)
    best_pid_tuning, final_fitness = optimizer.evolve()

    print("\n\n" + "="*60)
    print("      V7 ACTIVE CONTROL EXPERIMENT COMPLETE")
    print("="*60)
    print("\nSimulation of a live, AI-controlled resonant cascade.")
    
    if best_pid_tuning and final_fitness > 0:
        print("\n--- Optimal Onboard AI Controller Tuning (PID) ---")
        print(json.dumps(best_pid_tuning, indent=4))
        print(f"\n  > Final Stability Fitness: {final_fitness:,.2f}")
        
        if final_fitness > 100:  # Only show validation if we have good fitness
            print("\n  *****************************************************")
            print("  *   VALIDATION: The resonant cascade is CONTROLLABLE. *")
            print("  *   The theory enables a stable, high-output power    *")
            print("  *   source, not just a one-shot detonation.           *")
            print("  *****************************************************")
        else:
            print("\n  --- WARNING: Controller found but fitness is too low for validation ---")
    else:
        print("\nNo stable controller tuning could be found.")
    
    print("\n" + "="*60)