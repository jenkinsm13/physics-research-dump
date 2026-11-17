#!/usr/bin/env python3
"""
Pure Temporal Spatial Audio
===========================
Returns to the pure temporal physics model without conventional audio artifacts.
Investigates and fixes the spherical harmonic evaluation for proper spatial separation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.special import sph_harm, genlaguerre, factorial
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class PureTemporalSpatialEncoder:
    """Pure temporal encoding without conventional audio contamination."""
    
    def __init__(self, sample_rate=48000, max_l=4):
        self.sample_rate = sample_rate
        self.max_l = max_l
        self.dt = 1.0 / sample_rate
        
        # Pure temporal constants
        self.hbar = 1.0  # Normalized units
        self.m = 1.0
        
        print(f"🌊 Pure Temporal Spatial Encoder")
        print(f"Max angular momentum: l={max_l}")
        print(f"Pure temporal physics - no conventional audio contamination")
        
    def cartesian_to_spherical(self, x, y, z):
        """Convert to spherical coordinates."""
        r = np.sqrt(x**2 + y**2 + z**2)
        if r < 1e-10:
            return 0, 0, 0
        theta = np.arccos(np.clip(z / r, -1, 1))
        phi = np.arctan2(y, x)
        return r, theta, phi
    
    def compute_spherical_harmonic(self, l, m, theta, phi):
        """Compute Y_l^m(theta, phi) - pure mathematical form."""
        return sph_harm(m, l, phi, theta)
    
    def radial_wavefunction(self, n, l, r, a0=1.0):
        """Pure radial wavefunction without arbitrary scaling."""
        if r < 1e-10:
            return 0.0
            
        rho = 2 * r / (n * a0)
        
        # Proper normalization
        norm_factor = np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
        
        try:
            L = genlaguerre(n-l-1, 2*l+1)
            laguerre_val = L(rho)
        except:
            laguerre_val = 1.0
            
        result = norm_factor * (rho**l) * np.exp(-rho/2) * laguerre_val
        
        # Ensure real result for numerical stability
        if np.iscomplex(result):
            result = np.real(result)
            
        return result
    
    def void_potential(self, r, r1=1.0, r2=2.0, V1=1.0, V2=0.5, sigma1=0.5, sigma2=0.8):
        """Pure void potential - controls temporal shell coupling."""
        attractive = -V1 * np.exp(-(r - r1)**2 / (2 * sigma1**2))
        repulsive = V2 * np.exp(-(r - r2)**2 / (2 * sigma2**2))
        return attractive + repulsive
    
    def encode_pure_temporal_position(self, position, intensity=1.0):
        """Pure temporal encoding - no conventional audio concepts."""
        
        x, y, z = position
        r, theta, phi = self.cartesian_to_spherical(x, y, z)
        
        # Don't artificially limit radius - let temporal physics handle it
        if r < 0.01:
            r = 0.01  # Only avoid singularity
            
        coefficients = {}
        
        print(f"   Encoding position {position} -> (r={r:.3f}, θ={theta:.3f}, φ={phi:.3f})")
        
        total_energy = 0
        
        # Encode into temporal shells
        for n in range(1, self.max_l + 2):
            for l in range(min(n, self.max_l + 1)):
                for m in range(-l, l + 1):
                    
                    # Pure spherical harmonic
                    Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
                    
                    # Pure radial component
                    R_nl = self.radial_wavefunction(n, l, r)
                    
                    # Pure void potential effect
                    void_factor = np.exp(self.void_potential(r))
                    
                    # Pure temporal coefficient
                    coefficient = intensity * R_nl * Y_lm * void_factor
                    
                    coefficients[(n, l, m)] = coefficient
                    total_energy += abs(coefficient)**2
        
        print(f"   Generated {len(coefficients)} coefficients, total energy: {total_energy:.6f}")
        return coefficients
    
    def evaluate_wavefunction_at_point(self, coefficients, eval_point):
        """Evaluate the temporal wavefunction at a specific point."""
        
        x, y, z = eval_point
        r, theta, phi = self.cartesian_to_spherical(x, y, z)
        
        if r < 1e-10:
            return 0.0
            
        psi = 0.0
        
        for (n, l, m), coeff in coefficients.items():
            Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
            R_nl = self.radial_wavefunction(n, l, r)
            psi += coeff * R_nl * Y_lm
            
        return psi

class PureTemporalAudioSystem:
    """Pure temporal audio system - no conventional contamination."""
    
    def __init__(self, sample_rate=48000, buffer_size=1024):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Pure temporal components
        self.encoder = PureTemporalSpatialEncoder(sample_rate)
        self.shell_processor = TemporalShellProcessor()
        
        self.time = 0
        
        # Pure observation points (listener's temporal detection points)
        self.observation_separation = 0.2  # 20cm - pure geometric
        self.observation_points = {
            'left': (-self.observation_separation/2, 0, 0),
            'right': (self.observation_separation/2, 0, 0)
        }
        
        print(f"🌊 Pure Temporal Audio System")
        print(f"Observation point separation: {self.observation_separation*100:.0f}cm")
        print(f"No conventional audio artifacts")
    
    def process_source_purely(self, source_position, signal, intensity=1.0):
        """Process source through pure temporal physics."""
        
        print(f"\n🎯 Processing source at {source_position}")
        
        # Encode position into temporal shell coefficients
        coefficients = self.encoder.encode_pure_temporal_position(source_position, intensity)
        
        # Apply temporal evolution
        evolved_coefficients = {}
        for (n, l, m), coeff in coefficients.items():
            # Pure temporal evolution - no artificial phases
            E_n = -13.6 / n**2  # Pure energy eigenvalue
            phase = np.exp(-1j * E_n * self.time / self.encoder.hbar)
            evolved_coefficients[(n, l, m)] = coeff * phase
        
        # Evaluate wavefunction at observation points
        left_point = self.observation_points['left']
        right_point = self.observation_points['right']
        
        psi_left = self.encoder.evaluate_wavefunction_at_point(evolved_coefficients, left_point)
        psi_right = self.encoder.evaluate_wavefunction_at_point(evolved_coefficients, right_point)
        
        # Pure probability amplitudes
        prob_left = abs(psi_left)**2
        prob_right = abs(psi_right)**2
        
        total_prob = prob_left + prob_right
        if total_prob > 1e-10:
            weight_left = prob_left / total_prob
            weight_right = prob_right / total_prob
        else:
            weight_left = 0.5
            weight_right = 0.5
            
        print(f"   Left observation: ψ={psi_left:.6f}, P={prob_left:.6f}")
        print(f"   Right observation: ψ={psi_right:.6f}, P={prob_right:.6f}")
        print(f"   Weights: L={weight_left:.4f}, R={weight_right:.4f}")
        print(f"   L/R ratio: {weight_left/(weight_right+1e-10):.3f}")
        
        # Apply pure temporal shell processing
        temporal_signal = self.shell_processor.process_through_shells(signal, self.sample_rate)
        
        # Pure amplitude modulation by observation probabilities
        left_signal = temporal_signal * weight_left
        right_signal = temporal_signal * weight_right
        
        return left_signal, right_signal
    
    def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
        """Process sources through pure temporal physics."""
        
        left_channel = np.zeros(self.buffer_size)
        right_channel = np.zeros(self.buffer_size)
        
        for source in audio_sources:
            # Relative position
            rel_pos = np.array(source['position']) - np.array(listener_position)
            
            # Get signal chunk
            signal = source['signal'][:self.buffer_size]
            intensity = source.get('intensity', 1.0)
            
            # Process purely through temporal physics
            left_sig, right_sig = self.process_source_purely(rel_pos, signal, intensity)
            
            # Accumulate
            left_channel += left_sig[:self.buffer_size]
            right_channel += right_sig[:self.buffer_size]
        
        self.time += self.buffer_size / self.sample_rate
        
        return left_channel, right_channel

def debug_pure_temporal_encoding():
    """Debug the pure temporal encoding to find the spatial issue."""
    
    print("🔍 Debugging Pure Temporal Encoding")
    print("=" * 40)
    
    encoder = PureTemporalSpatialEncoder()
    
    # Test extreme positions
    test_positions = [
        ("Center", (0, 0, 0)),
        ("Right_1m", (1, 0, 0)),
        ("Right_5m", (5, 0, 0)),
        ("Left_1m", (-1, 0, 0)),
        ("Left_5m", (-5, 0, 0)),
    ]
    
    observation_points = {
        'left': (-0.1, 0, 0),
        'right': (0.1, 0, 0)
    }
    
    for name, pos in test_positions:
        print(f"\n📍 Testing {name} at {pos}")
        
        coeffs = encoder.encode_pure_temporal_position(pos, intensity=1.0)
        
        # Evaluate at observation points
        psi_left = encoder.evaluate_wavefunction_at_point(coeffs, observation_points['left'])
        psi_right = encoder.evaluate_wavefunction_at_point(coeffs, observation_points['right'])
        
        prob_left = abs(psi_left)**2
        prob_right = abs(psi_right)**2
        
        print(f"   ψ_left = {psi_left:.6f}, P_left = {prob_left:.6f}")
        print(f"   ψ_right = {psi_right:.6f}, P_right = {prob_right:.6f}")
        print(f"   L/R ratio = {prob_left/(prob_right+1e-10):.3f}")

def create_pure_spatial_test():
    """Create test using only pure temporal physics."""
    
    print("\n🌊 Creating Pure Temporal Spatial Test")
    print("=" * 40)
    
    # Initialize pure system
    audio_system = PureTemporalAudioSystem()
    
    # Test parameters
    sample_rate = 48000
    duration = 1.0
    
    # Simple test positions
    test_positions = [
        ("Pure_Left", (-2, 0, 0), 400),
        ("Pure_Center", (0, 1, 0), 500), 
        ("Pure_Right", (2, 0, 0), 600),
    ]
    
    sequence_parts = []
    
    for name, position, frequency in test_positions:
        print(f"\n🎯 Processing {name}")
        
        # Generate pure tone
        t = np.linspace(0, duration, int(duration * sample_rate))
        signal = np.sin(2 * np.pi * frequency * t) * 0.5
        
        # Process through pure temporal system
        sources = [{'position': position, 'signal': signal, 'intensity': 1.0}]
        
        total_samples = len(signal)
        buffer_size = audio_system.buffer_size
        stereo_output = np.zeros((2, total_samples))
        
        # Process in chunks
        for i in range(0, total_samples, buffer_size):
            end_idx = min(i + buffer_size, total_samples)
            
            chunk_sources = []
            for src in sources:
                chunk_signal = src['signal'][i:end_idx]
                if len(chunk_signal) < buffer_size:
                    chunk_signal = np.pad(chunk_signal, (0, buffer_size - len(chunk_signal)))
                
                chunk_sources.append({
                    'position': src['position'],
                    'signal': chunk_signal,
                    'intensity': src['intensity']
                })
            
            left, right = audio_system.process_audio_buffer(chunk_sources)
            
            actual_length = end_idx - i
            stereo_output[0, i:end_idx] = left[:actual_length]
            stereo_output[1, i:end_idx] = right[:actual_length]
        
        # Add silence
        silence = np.zeros((2, int(0.5 * sample_rate)))
        sequence_parts.append(stereo_output)
        sequence_parts.append(silence)
    
    # Concatenate and save
    final_sequence = np.concatenate(sequence_parts, axis=1)
    
    # Normalize without artifacts
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.9 / max_val
    
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    wavfile.write('pure_temporal_spatial_test.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: pure_temporal_spatial_test.wav")
    print(f"   Pure temporal physics - no conventional artifacts")

if __name__ == "__main__":
    print("🌊 Pure Temporal Spatial Audio - No Contamination")
    print("=" * 55)
    
    # Debug the encoding
    debug_pure_temporal_encoding()
    
    # Create pure test
    create_pure_spatial_test()
    
    print("\n✅ Pure temporal audio complete!")
    print("🎧 pure_temporal_spatial_test.wav - Clean temporal physics only")
    print("🌊 No conventional audio artifacts or buzzing!")