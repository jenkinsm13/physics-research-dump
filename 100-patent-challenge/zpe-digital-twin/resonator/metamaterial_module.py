import time
import math

# --- Layer 2: The Metamaterial Modeler ---
# This module simulates the heart of our device: the engineered metamaterial.
# Its primary job is to take the energy pulse from the Apparatus as input
# and determine if the material can withstand the energy and, if so, how it
# transforms that energy into a rapidly changing boundary condition—the
# solid-state equivalent of a collapsing bubble.

class Metamaterial:
    """
    Represents a specific design of a metamaterial, defined by a 'genome' of properties.
    """
    def __init__(self, design_name: str, genome: dict):
        """
        Initializes a metamaterial based on a design genome.

        Args:
            design_name (str): A human-readable name for this material design.
            genome (dict): A dictionary of physical properties that define the material.
        """
        self.design_name = design_name
        # --- Key Material Properties ---
        # How well the material absorbs the laser's energy.
        self.coupling_efficiency = genome.get("coupling_efficiency", 0.5)
        # How fast the material's refractive index can change (in picoseconds). Lower is better.
        self.response_speed_ps = genome.get("response_speed_ps", 10.0)
        # The maximum power the material can handle before being destroyed (in Terawatts).
        self.damage_threshold_tw = genome.get("damage_threshold_tw", 1.0)
        # The quality of the engineered nanocavity. Higher is better.
        self.void_quality_factor = genome.get("void_quality_factor", 0.9)
        
        print(f"\n--- Initializing Digital Twin: Metamaterial Layer ---")
        print(f"  Material Design: '{self.design_name}'")
        print(f"  Properties: Coupling={self.coupling_efficiency*100}%, Speed={self.response_speed_ps}ps, Threshold={self.damage_threshold_tw}TW, QF={self.void_quality_factor}")
        print("--- Metamaterial Ready ---")

    def calculate_response(self, incident_pulse: dict) -> dict:
        """
        Simulates the material's physical response to an incoming laser pulse.
        This is the primary method of this module.

        Args:
            incident_pulse (dict): The output dictionary from the Apparatus module.

        Returns:
            dict: A dictionary describing the resulting boundary condition, or a failure state.
        """
        print(f"\nMETAMATERIAL '{self.design_name}' INTERACTION SEQUENCE...")
        time.sleep(0.5)

        # 1. Calculate absorbed power
        delivered_power = incident_pulse["delivered_power_tw"]
        absorbed_power = delivered_power * self.coupling_efficiency
        print(f"  [1] Incident Pulse Power: {delivered_power:.4f} TW.")
        print(f"  [2] Absorbed Power: {absorbed_power:.4f} TW ({self.coupling_efficiency*100}% coupling).")
        time.sleep(0.5)

        # 2. Check for material damage
        print(f"  [3] Checking against Damage Threshold ({self.damage_threshold_tw:.4f} TW)...")
        if absorbed_power >= self.damage_threshold_tw:
            print("  [X] CRITICAL FAILURE: Absorbed power exceeds damage threshold.")
            return {
                "status": "FAILURE",
                "reason": "Material damage threshold exceeded.",
                "absorbed_power": absorbed_power,
                "damage_threshold": self.damage_threshold_tw
            }
        print("  [+] Material integrity maintained.")
        time.sleep(0.5)

        # 3. Calculate the resulting boundary condition properties
        # This is the core of the simulation: translating laser power into a "moving mirror".
        # The effective velocity is the key parameter for the Dynamic Casimir Effect.
        # This simplified formula models that faster response times and higher (but non-damaging)
        # power result in a faster effective boundary velocity.
        
        # The velocity is proportional to how close we are to the damage limit.
        power_ratio = absorbed_power / self.damage_threshold_tw
        
        # The velocity is inversely proportional to the material's response time.
        # The constant 0.1 is a scaling factor for this simulation to keep velocity < 1.0c.
        effective_velocity_c = 0.1 * math.sqrt(power_ratio) / self.response_speed_ps

        # The duration of the event is limited by the material's response speed.
        event_duration_fs = self.response_speed_ps * 1000 # Convert ps to fs
        
        print("  [4] Generating effective boundary condition...")
        print(f"  [+] Effective Boundary Velocity: {effective_velocity_c:.5f} c (fraction of light speed).")
        print(f"  [+] Event Duration: {event_duration_fs:.0f} fs.")
        
        # 4. Package the results for the next layer (Quantum Core)
        boundary_condition = {
            "status": "SUCCESS",
            "design_name": self.design_name,
            "boundary_velocity_c": effective_velocity_c,
            "event_duration_fs": event_duration_fs,
            "quality_factor": self.void_quality_factor
        }
        
        print("\nINTERACTION COMPLETE. Boundary condition data generated.")
        return boundary_condition

# --- Main execution block ---
# This allows us to run this file directly to test different material designs.
if __name__ == "__main__":
    # 1. Define a sample incoming pulse (simulating the output from apparatus_module.py)
    # This is a powerful, clean pulse from a well-tuned apparatus.
    sample_pulse_from_apparatus = {
        "delivered_power_tw": 0.8500,
        "pulse_duration_fs": 150,
        "wavelength_nm": 800,
        "status": "SUCCESS"
    }

    # 2. Define several competing metamaterial designs (genomes)
    genome_A = { # A well-balanced, robust design
        "coupling_efficiency": 0.9,
        "response_speed_ps": 1.0,
        "damage_threshold_tw": 1.0,
        "void_quality_factor": 0.95
    }
    
    genome_B = { # A fragile design that can't handle the power
        "coupling_efficiency": 0.95, # Couples very well, but...
        "response_speed_ps": 0.8,
        "damage_threshold_tw": 0.7, # ...has a low damage threshold.
        "void_quality_factor": 0.98
    }

    genome_C = { # A slow, inefficient design
        "coupling_efficiency": 0.4, # Poor coupling
        "response_speed_ps": 25.0,  # Very slow response
        "damage_threshold_tw": 5.0, # Very tough, but unresponsive
        "void_quality_factor": 0.8
    }
    
    designs_to_test = [
        Metamaterial("Project Chimera", genome_A),
        Metamaterial("Project Icarus", genome_B),
        Metamaterial("Project Tortoise", genome_C)
    ]

    # 3. Run the simulation for each design
    print("\n\n--- Starting Metamaterial Design Competition ---")
    results = []
    for material_design in designs_to_test:
        result = material_design.calculate_response(sample_pulse_from_apparatus)
        results.append(result)
        print("-" * 50)

    # 4. Display the final results
    print("\n\n--- Simulation Output: Boundary Condition Results ---")
    for res in results:
        print(f"\n  Design: {res.get('design_name', 'FAILURE')}")
        print(f"  Status: {res['status']}")
        if res['status'] == 'SUCCESS':
            print(f"    -> Boundary Velocity: {res['boundary_velocity_c']:.6f} c")
            print(f"    -> Quality Factor: {res['quality_factor']}")
        else:
            print(f"    -> Reason: {res['reason']}")
    print("---------------------------------------------------")
    print("\nThis data packet is now ready to be passed to the Quantum Core module.")