import numpy as np
from scipy.special import sph_harm, genlaguerre, factorial
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SphericalHarmonicAudioEncoder:
   """
   Encodes 3D spatial audio positions into spherical harmonic coefficients
   with temporal evolution based on the modified Schrödinger equation
   """
   
   def __init__(self, sample_rate=48000, max_l=4):
       self.sample_rate = sample_rate
       self.max_l = max_l  # Maximum angular momentum quantum number
       self.dt = 1.0 / sample_rate
       
       # Physical constants (normalized units)
       self.hbar = 1.0
       self.m = 1.0
       
   def cartesian_to_spherical(self, x, y, z):
       """Convert Cartesian to spherical coordinates"""
       r = np.sqrt(x**2 + y**2 + z**2)
       theta = np.arccos(z / r) if r > 0 else 0
       phi = np.arctan2(y, x)
       return r, theta, phi
   
   def compute_spherical_harmonic(self, l, m, theta, phi):
       """Compute spherical harmonic Y_l^m(theta, phi)"""
       return sph_harm(m, l, phi, theta)
   
   def radial_wavefunction(self, n, l, r, a0=1.0):
       """Compute radial part of wavefunction R_nl(r)"""
       rho = 2 * r / (n * a0)
       norm = np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)**3))
       L = genlaguerre(n-l-1, 2*l+1)
       return norm * rho**l * np.exp(-rho/2) * L(rho)
   
   def void_potential(self, r, r1=-1.0, r2=1.0, V1=1.0, V2=0.8, sigma1=0.3, sigma2=0.2):
       """Double Gaussian potential for attraction-repulsion dynamics"""
       attractive = -V1 * np.exp(-(r - r1)**2 / (2 * sigma1**2))
       repulsive = V2 * np.exp(-(r - r2)**2 / (2 * sigma2**2))
       return attractive + repulsive
   
   def encode_spatial_position(self, position, intensity=1.0):
       """
       Encode a 3D position into spherical harmonic coefficients
       Returns: Dictionary of (n,l,m) -> complex coefficient
       """
       x, y, z = position
       r, theta, phi = self.cartesian_to_spherical(x, y, z)
       
       # Limit radius to reasonable range
       r = np.clip(r, 0.1, 10.0)
       
       coefficients = {}
       
       # Decompose into spherical harmonics up to max_l
       for n in range(1, self.max_l + 2):
           for l in range(min(n, self.max_l + 1)):
               for m in range(-l, l + 1):
                   # Compute basis function
                   Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
                   R_nl = self.radial_wavefunction(n, l, r)
                   
                   # Weight by intensity and void potential
                   void_weight = np.exp(self.void_potential(r))
                   coefficient = intensity * R_nl * Y_lm * void_weight
                   
                   coefficients[(n, l, m)] = coefficient
       
       return coefficients
   
   def time_evolve_coefficients(self, coefficients, t):
       """
       Evolve spherical harmonic coefficients in time using 
       modified Schrödinger equation
       """
       evolved = {}
       
       for (n, l, m), c0 in coefficients.items():
           # Energy eigenvalue (including void potential contribution)
           E_n = -13.6 / n**2  # Rydberg energy in eV
           
           # Time evolution operator
           phase = np.exp(-1j * E_n * t / self.hbar)
           
           # Additional phase from magnetic quantum number (rotation)
           rotation_phase = np.exp(-1j * m * t)
           
           evolved[(n, l, m)] = c0 * phase * rotation_phase
           
       return evolved
   
   def coefficients_to_wavefunction(self, coefficients, r_points, theta_points, phi_points):
       """
       Reconstruct wavefunction from spherical harmonic coefficients
       """
       psi = np.zeros((len(r_points), len(theta_points), len(phi_points)), dtype=complex)
       
       for (n, l, m), coeff in coefficients.items():
           for i, r in enumerate(r_points):
               for j, theta in enumerate(theta_points):
                   for k, phi in enumerate(phi_points):
                       Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
                       R_nl = self.radial_wavefunction(n, l, r)
                       psi[i, j, k] += coeff * R_nl * Y_lm
                       
       return psi
   
   def encode_audio_frame(self, source_positions, intensities):
       """
       Encode multiple audio sources for a single time frame
       
       Args:
           source_positions: List of (x, y, z) positions
           intensities: List of source intensities
           
       Returns:
           Combined coefficient dictionary
       """
       combined_coefficients = {}
       
       for pos, intensity in zip(source_positions, intensities):
           source_coeffs = self.encode_spatial_position(pos, intensity)
           
           # Superpose sources
           for key, value in source_coeffs.items():
               if key in combined_coefficients:
                   combined_coefficients[key] += value
               else:
                   combined_coefficients[key] = value
                   
       return combined_coefficients


class TemporalShellProcessor:
   """
   Processes audio through temporal shells based on chronon model
   """
   
   def __init__(self, n_shells=5, base_frequency=1.0):
       self.n_shells = n_shells
       self.base_frequency = base_frequency
       
   def shell_frequency(self, n):
       """Frequency of n-th temporal shell: ω_n = 2π/n²"""
       return 2 * np.pi * self.base_frequency / (n**2)
   
   def process_through_shells(self, signal, sample_rate=48000):
       """
       Process signal through nested temporal shells
       Each shell modulates the signal at its characteristic frequency
       """
       t = np.arange(len(signal)) / sample_rate
       processed = np.zeros_like(signal)
       
       for n in range(1, self.n_shells + 1):
           omega_n = self.shell_frequency(n)
           
           # Temporal modulation for this shell
           modulation = np.cos(omega_n * t)
           
           # Weight decreases with shell number
           weight = 1.0 / n
           
           # Apply modulation
           processed += weight * signal * modulation
           
       # Normalize
       processed /= np.sum([1.0/n for n in range(1, self.n_shells + 1)])
       
       return processed


class ChronodynamicAudioSystem:
   """
   Complete system for encoding/decoding spatial audio using chronodynamic model
   """
   
   def __init__(self, sample_rate=48000, buffer_size=1024):
       self.sample_rate = sample_rate
       self.buffer_size = buffer_size
       
       self.encoder = SphericalHarmonicAudioEncoder(sample_rate)
       self.shell_processor = TemporalShellProcessor()
       
       # State for real-time processing
       self.current_coefficients = {}
       self.time = 0
       
   def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
       """
       Process one buffer of audio
       
       Args:
           audio_sources: List of dicts with 'position', 'signal', 'intensity'
           listener_position: (x, y, z) of listener
           
       Returns:
           Stereo audio buffer (left, right channels)
       """
       left_channel = np.zeros(self.buffer_size)
       right_channel = np.zeros(self.buffer_size)
       
       # Process each source
       for source in audio_sources:
           # Get relative position
           rel_pos = np.array(source['position']) - np.array(listener_position)
           
           # Encode spatial position
           coeffs = self.encoder.encode_spatial_position(
               rel_pos, 
               source['intensity']
           )
           
           # Time evolve coefficients
           evolved_coeffs = self.encoder.time_evolve_coefficients(
               coeffs, 
               self.time
           )
           
           # Decode to spatial distribution
           # Sample at listener's ear positions
           left_ear_pos = (-0.1, 0, 0)  # 10cm to left
           right_ear_pos = (0.1, 0, 0)   # 10cm to right
           
           # Convert to spherical coordinates
           r_l, theta_l, phi_l = self.encoder.cartesian_to_spherical(*left_ear_pos)
           r_r, theta_r, phi_r = self.encoder.cartesian_to_spherical(*right_ear_pos)
           
           # Evaluate wavefunction at ear positions
           psi_left = 0
           psi_right = 0
           
           for (n, l, m), coeff in evolved_coeffs.items():
               # Left ear
               Y_lm_l = self.encoder.compute_spherical_harmonic(l, m, theta_l, phi_l)
               R_nl_l = self.encoder.radial_wavefunction(n, l, r_l)
               psi_left += coeff * R_nl_l * Y_lm_l
               
               # Right ear
               Y_lm_r = self.encoder.compute_spherical_harmonic(l, m, theta_r, phi_r)
               R_nl_r = self.encoder.radial_wavefunction(n, l, r_r)
               psi_right += coeff * R_nl_r * Y_lm_r
           
           # Apply signal with spatial weighting
           weight_left = np.abs(psi_left)**2
           weight_right = np.abs(psi_right)**2
           
           # Process through temporal shells
           processed_signal = self.shell_processor.process_through_shells(
               source['signal'][:self.buffer_size], 
               self.sample_rate
           )
           
           left_channel += weight_left * processed_signal
           right_channel += weight_right * processed_signal
       
       # Update time
       self.time += self.buffer_size / self.sample_rate
       
       return left_channel, right_channel
   
   def visualize_soundfield(self, audio_sources, listener_position=(0, 0, 0)):
       """
       Visualize the 3D soundfield probability distribution
       """
       # Create grid
       x = np.linspace(-3, 3, 30)
       y = np.linspace(-3, 3, 30)
       z = np.linspace(-3, 3, 30)
       
       # Compute coefficients for all sources
       combined_coeffs = {}
       for source in audio_sources:
           rel_pos = np.array(source['position']) - np.array(listener_position)
           coeffs = self.encoder.encode_spatial_position(rel_pos, source['intensity'])
           
           for key, value in coeffs.items():
               if key in combined_coeffs:
                   combined_coeffs[key] += value
               else:
                   combined_coeffs[key] = value
       
       # Evaluate on grid (2D slice at z=0 for visualization)
       psi_grid = np.zeros((len(x), len(y)), dtype=complex)
       z_slice = 0
       
       for i, xi in enumerate(x):
           for j, yi in enumerate(y):
               r, theta, phi = self.encoder.cartesian_to_spherical(xi, yi, z_slice)
               
               for (n, l, m), coeff in combined_coeffs.items():
                   Y_lm = self.encoder.compute_spherical_harmonic(l, m, theta, phi)
                   R_nl = self.encoder.radial_wavefunction(n, l, r)
                   psi_grid[i, j] += coeff * R_nl * Y_lm
       
       # Plot
       fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
       
       # Magnitude
       im1 = ax1.imshow(np.abs(psi_grid)**2, extent=[-3, 3, -3, 3], 
                       origin='lower', cmap='hot')
       ax1.set_title('Sound Field Intensity')
       ax1.set_xlabel('X (meters)')
       ax1.set_ylabel('Y (meters)')
       plt.colorbar(im1, ax=ax1)
       
       # Phase
       im2 = ax2.imshow(np.angle(psi_grid), extent=[-3, 3, -3, 3], 
                       origin='lower', cmap='twilight')
       ax2.set_title('Sound Field Phase')
       ax2.set_xlabel('X (meters)')
       ax2.set_ylabel('Y (meters)')
       plt.colorbar(im2, ax=ax2)
       
       # Mark source positions
       for source in audio_sources:
           ax1.plot(source['position'][0], source['position'][1], 'wo', markersize=10)
           ax2.plot(source['position'][0], source['position'][1], 'wo', markersize=10)
       
       # Mark listener
       ax1.plot(listener_position[0], listener_position[1], 'g^', markersize=12)
       ax2.plot(listener_position[0], listener_position[1], 'g^', markersize=12)
       
       plt.tight_layout()
       plt.show()


# Example usage
if __name__ == "__main__":
   # Create system
   audio_system = ChronodynamicAudioSystem()
   
   # Define audio sources
   test_signal = np.sin(2 * np.pi * 440 * np.arange(1024) / 48000)  # 440 Hz tone
   
   sources = [
       {'position': (2, 0, 0), 'signal': test_signal, 'intensity': 1.0},
       {'position': (-1, 1, 0), 'signal': test_signal * 0.5, 'intensity': 0.8},
       {'position': (0, -2, 1), 'signal': test_signal * 0.7, 'intensity': 0.6}
   ]
   
   # Process audio
   left, right = audio_system.process_audio_buffer(sources)
   
   # Visualize soundfield
   audio_system.visualize_soundfield(sources)
   
   # Plot waveforms
   plt.figure(figsize=(10, 4))
   plt.subplot(1, 2, 1)
   plt.plot(left[:200])
   plt.title('Left Channel')
   plt.xlabel('Sample')
   plt.ylabel('Amplitude')
   
   plt.subplot(1, 2, 2)
   plt.plot(right[:200])
   plt.title('Right Channel')
   plt.xlabel('Sample')
   plt.ylabel('Amplitude')
   
   plt.tight_layout()
   plt.show()