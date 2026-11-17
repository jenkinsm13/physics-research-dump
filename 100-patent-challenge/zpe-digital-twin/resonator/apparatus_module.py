import time
import random

# --- Layer 3: The Apparatus Simulator ---
# This module simulates the physical hardware that generates and delivers the
# energy pulse. It models the laser and the optical train (lenses, mirrors).
# Its sole purpose is to produce a highly controlled, simulated energy pulse
# that will serve as the input for our next module, the Metamaterial.

class Laser:
    """
    Represents a high-power, ultra-fast laser source.
    """
    def __init__(self, name: str, pulse_duration_fs: int, wavelength_nm: int, max_power_tw: float):
        """
        Initializes the Laser source.

        Args:
            name (str): The model name of the laser, e.g., "Titan-Sapphire Pulse".
            pulse_duration_fs (int): The duration of the laser pulse in femtoseconds (1 fs = 10^-15 s).
            wavelength_nm (int): The laser's wavelength in nanometers.
            max_power_tw (float): The maximum theoretical power in Terawatts (1 TW = 10^12 W).
        """
        self.name = name
        self.pulse_duration_fs = pulse_duration_fs
        self.wavelength_nm = wavelength_nm
        self.max_power_tw = max_power_tw
        print(f"  [+] Laser '{self.name}' configured: {self.pulse_duration_fs} fs pulse, {self.max_power_tw} TW peak power.")

class OpticalTrain:
    """
    Simulates the series of mirrors, lenses, and beam shapers that guide
    and focus the laser pulse onto the target.
    """
    def __init__(self, focus_efficiency: float, stability: float):
        """
        Initializes the optical train.

        Args:
            focus_efficiency (float): The overall efficiency of the optical path (0.0 to 1.0).
                                      Accounts for losses from mirrors and lenses.
            stability (float): The stability of the focus (0.9 to 1.0). A lower number
                               introduces more random fluctuation in delivered power.
        """
        if not (0.0 <= focus_efficiency <= 1.0):
            raise ValueError("Focus efficiency must be between 0.0 and 1.0")
        if not (0.9 <= stability <= 1.0):
            raise ValueError("Stability must be between 0.9 (noisy) and 1.0 (perfect).")
            
        self.focus_efficiency = focus_efficiency
        self.stability = stability
        print(f"  [+] Optical Train configured: {self.focus_efficiency*100:.1f}% efficiency, {self.stability*100:.1f}% stability.")

class Apparatus:
    """
    The main class for the physical apparatus. It integrates the laser and optics
    to deliver a precise energy pulse.
    """
    def __init__(self, laser: Laser, optics: OpticalTrain):
        """
        Initializes the complete apparatus.
        """
        print("\n--- Initializing Digital Twin: Apparatus Layer ---")
        self.laser = laser
        self.optics = optics
        print("--- Apparatus Ready ---\n")

    def fire_laser(self) -> dict:
        """
        Simulates firing the laser and delivering the pulse to the target.
        This is the primary method of this module.

        Returns:
            dict: A dictionary describing the properties of the energy pulse
                  as it arrives at the metamaterial target.
        """
        print(f"FIRING SEQUENCE INITIATED...")
        time.sleep(0.5)
        
        # 1. Simulate power stability fluctuations
        # A stability of 1.0 means no fluctuation. Lower values introduce randomness.
        stability_fluctuation = random.uniform(self.optics.stability, 1.0)
        
        # 2. Calculate power at the source
        source_power = self.laser.max_power_tw * stability_fluctuation
        print(f"  [1] Laser power at source: {source_power:.4f} TW (includes stability fluctuation).")
        time.sleep(0.5)

        # 3. Simulate propagation and focusing losses through the optical train
        delivered_power = source_power * self.optics.focus_efficiency
        print(f"  [2] Simulating beam propagation through optics...")
        print(f"  [3] Delivered power at target: {delivered_power:.4f} TW (after {self.optics.focus_efficiency*100:.1f}% efficiency loss).")
        time.sleep(0.5)

        # 4. Package the final pulse characteristics into a dictionary
        # This data structure is the official output of this module.
        final_pulse = {
            "delivered_power_tw": delivered_power,
            "pulse_duration_fs": self.laser.pulse_duration_fs,
            "wavelength_nm": self.laser.wavelength_nm,
            "status": "SUCCESS"
        }
        
        print("\nFIRING COMPLETE. Pulse delivered to target.")
        return final_pulse

# --- Main execution block ---
# This allows us to run this file directly to test the Apparatus module.
if __name__ == "__main__":
    # 1. Define the components of our virtual apparatus
    # We are choosing parameters for a state-of-the-art petawatt-class laser system.
    main_laser = Laser(
        name="L4-Aton",
        pulse_duration_fs=150,
        wavelength_nm=800, # Typical for Ti:Sapphire lasers
        max_power_tw=1.0   # 1 Petawatt = 1000 Terawatts. We'll simulate a 1 TW system for now.
    )
    
    main_optics = OpticalTrain(
        focus_efficiency=0.85, # 85% is a realistic efficiency for a complex optical path
        stability=0.99         # 99% stability is very good
    )

    # 2. Assemble the apparatus
    the_machine = Apparatus(laser=main_laser, optics=main_optics)

    # 3. Run the simulation
    delivered_pulse_data = the_machine.fire_laser()

    # 4. Display the final results
    print("\n--- Simulation Output: Delivered Pulse Characteristics ---")
    for key, value in delivered_pulse_data.items():
        print(f"  {key}: {value}")
    print("---------------------------------------------------------")
    print("\nThis data packet is now ready to be passed to the Metamaterial module.")