#!/usr/bin/env python3
"""
Corrected Temporal Spatial Audio
===============================
Pure temporal physics with corrected mathematical implementation
for proper spatial separation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.special import sph_harm, genlaguerre, factorial
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class CorrectedTemporalEncoder:
    """Mathematically corrected temporal encoder."""
    
    def __init__(self, sample_rate=48000, max_l=8):
        self.sample_rate = sample_rate
        self.max_l = max_l  # Increase for better angular resolution
        self.dt = 1.0 / sample_rate
        
        # Pure temporal constants
        self.hbar = 1.0
        self.m = 1.0
        
        print(f"🔧 Corrected Temporal Encoder")
        print(f"Higher angular resolution: l_max = {max_l}")
        
    def cartesian_to_spherical(self, x, y, z):
        """Convert to spherical coordinates."""
        r = np.sqrt(x**2 + y**2 + z**2)
        if r < 1e-12:
            return 1e-12, 0, 0
        theta = np.arccos(np.clip(z / r, -1, 1))
        phi = np.arctan2(y, x)
        return r, theta, phi
    
    def compute_spherical_harmonic(self, l, m, theta, phi):
        """Pure spherical harmonic Y_l^m."""
        return sph_harm(m, l, phi, theta)
    
    def radial_wavefunction(self, n, l, r, a0=1.0):
        """Simplified radial function for better numerical stability."""
        if r < 1e-12:
            return 0.0
            
        # Simplified hydrogen-like radial function
        rho = r / (n * a0)
        
        # Simple exponential with power law
        result = (rho**l) * np.exp(-rho/2) / (n**(3/2))
        
        return result
    
    def encode_position_with_focus(self, position, intensity=1.0, focus_factor=5.0):
        """Encode position with enhanced angular focus."""
        
        x, y, z = position
        r, theta, phi = self.cartesian_to_spherical(x, y, z)
        
        print(f"   Encoding {position} -> (r={r:.3f}, θ={theta:.3f}, φ={phi:.3f})")
        
        coefficients = {}
        total_energy = 0
        
        # Enhanced encoding with angular focus
        for n in range(1, 4):  # Fewer radial terms for clarity
            for l in range(0, self.max_l + 1):  # More angular terms
                for m in range(-l, l + 1):
                    
                    # Spherical harmonic
                    Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
                    
                    # Radial component
                    R_nl = self.radial_wavefunction(n, l, r)
                    
                    # Angular focus enhancement
                    angular_weight = (1 + focus_factor * l) if l > 0 else 1.0
                    
                    # Distance scaling
                    distance_weight = np.exp(-r/2)  # Favor closer sources
                    
                    # Combine
                    coefficient = intensity * R_nl * Y_lm * angular_weight * distance_weight
                    
                    if abs(coefficient) > 1e-12:  # Only store significant coefficients
                        coefficients[(n, l, m)] = coefficient
                        total_energy += abs(coefficient)**2
        
        print(f"   Generated {len(coefficients)} significant coefficients")
        print(f"   Total energy: {total_energy:.6f}")
        
        return coefficients
    
    def evaluate_wavefunction_enhanced(self, coefficients, eval_point):
        """Enhanced wavefunction evaluation with proper normalization."""
        
        x, y, z = eval_point
        r, theta, phi = self.cartesian_to_spherical(x, y, z)
        
        psi = 0.0 + 0.0j
        
        for (n, l, m), coeff in coefficients.items():
            Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
            R_nl = self.radial_wavefunction(n, l, r)
            psi += coeff * R_nl * Y_lm
            
        return psi

class CorrectedTemporalAudioSystem:
    """Corrected temporal audio system with proper spatial separation."""
    
    def __init__(self, sample_rate=48000, buffer_size=1024):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Corrected encoder
        self.encoder = CorrectedTemporalEncoder(sample_rate, max_l=8)
        self.shell_processor = TemporalShellProcessor()
        
        self.time = 0
        
        # Optimized observation geometry for your 220mm ear spacing
        ear_separation = 0.22  # Your actual measurement
        
        # Wider observation points for better contrast
        self.observation_points = {
            'left': (-ear_separation/2, 0, 0),
            'right': (ear_separation/2, 0, 0)
        }
        
        print(f"🔧 Corrected Temporal Audio System")
        print(f"Observation separation: {ear_separation*1000:.0f}mm (your measurement)")
        print(f"Enhanced angular resolution for proper spatial separation")
        
    def process_source_corrected(self, source_position, signal, intensity=1.0):
        """Process with corrected temporal physics."""
        
        print(f"\n📍 Processing source at {source_position}")
        
        # Enhanced encoding
        coefficients = self.encoder.encode_position_with_focus(
            source_position, intensity, focus_factor=10.0
        )
        
        # Time evolution
        evolved_coefficients = {}
        for (n, l, m), coeff in coefficients.items():
            # Simple time evolution
            E_n = -1.0 / n**2
            phase = np.exp(-1j * E_n * self.time)
            evolved_coefficients[(n, l, m)] = coeff * phase
        
        # Evaluate at observation points
        left_point = self.observation_points['left']
        right_point = self.observation_points['right']
        
        psi_left = self.encoder.evaluate_wavefunction_enhanced(evolved_coefficients, left_point)
        psi_right = self.encoder.evaluate_wavefunction_enhanced(evolved_coefficients, right_point)
        
        # Calculate probabilities
        prob_left = abs(psi_left)**2
        prob_right = abs(psi_right)**2
        
        # Enhanced separation
        total_prob = prob_left + prob_right
        if total_prob > 1e-12:
            weight_left = prob_left / total_prob
            weight_right = prob_right / total_prob
            
            # Apply separation enhancement
            separation_factor = 2.0
            center_weight = 0.5
            
            # Enhance differences from center
            weight_left = center_weight + separation_factor * (weight_left - center_weight)
            weight_right = center_weight + separation_factor * (weight_right - center_weight)
            
            # Renormalize
            total = weight_left + weight_right
            weight_left /= total
            weight_right /= total
            
            # Ensure valid range
            weight_left = np.clip(weight_left, 0.01, 0.99)
            weight_right = 1.0 - weight_left
            
        else:
            weight_left = 0.5
            weight_right = 0.5
        
        print(f"   ψ_left = {psi_left:.6f}")
        print(f"   ψ_right = {psi_right:.6f}")
        print(f"   P_left = {prob_left:.6f}, P_right = {prob_right:.6f}")
        print(f"   Enhanced weights: L={weight_left:.4f}, R={weight_right:.4f}")
        print(f"   L/R ratio: {weight_left/(weight_right+1e-12):.3f}")
        
        # Apply temporal shell processing
        temporal_signal = self.shell_processor.process_through_shells(signal, self.sample_rate)
        
        # Apply weights
        left_signal = temporal_signal * weight_left
        right_signal = temporal_signal * weight_right
        
        return left_signal, right_signal
    
    def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
        """Process with corrections."""
        
        left_channel = np.zeros(self.buffer_size)
        right_channel = np.zeros(self.buffer_size)
        
        for source in audio_sources:
            rel_pos = np.array(source['position']) - np.array(listener_position)
            signal = source['signal'][:self.buffer_size]
            intensity = source.get('intensity', 1.0)
            
            left_sig, right_sig = self.process_source_corrected(rel_pos, signal, intensity)
            
            left_channel += left_sig[:self.buffer_size]
            right_channel += right_sig[:self.buffer_size]
        
        self.time += self.buffer_size / self.sample_rate
        
        return left_channel, right_channel

def test_corrected_system():
    """Test the corrected system with extreme positions."""
    
    print("🔧 Testing Corrected Temporal Spatial System")
    print("=" * 50)
    
    audio_system = CorrectedTemporalAudioSystem()
    
    # Test parameters
    sample_rate = 48000
    duration = 1.5
    
    # Extreme test positions for clear separation
    test_positions = [
        ("Hard_Left", (-3, 0, 0), 400, "Should be strongly left"),
        ("Center", (0, 2, 0), 500, "Should be centered"),
        ("Hard_Right", (3, 0, 0), 600, "Should be strongly right"),
    ]
    
    sequence_parts = []
    
    for name, position, frequency, expected in test_positions:
        print(f"\n🎯 {name}: {expected}")
        
        # Generate test tone
        t = np.linspace(0, duration, int(duration * sample_rate))
        signal = np.sin(2 * np.pi * frequency * t) * 0.6
        
        # Apply envelope
        fade_samples = int(0.1 * sample_rate)
        signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
        signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        # Process
        sources = [{'position': position, 'signal': signal, 'intensity': 1.0}]
        
        total_samples = len(signal)
        buffer_size = audio_system.buffer_size
        stereo_output = np.zeros((2, total_samples))
        
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
    
    # Analyze final results
    left_channel = final_sequence[0]
    right_channel = final_sequence[1]
    
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    
    print(f"\n📊 Final Analysis:")
    print(f"   Left channel energy: {left_energy:.6f}")
    print(f"   Right channel energy: {right_energy:.6f}")
    print(f"   Overall L/R ratio: {left_energy/(right_energy+1e-12):.3f}")
    
    # Normalize and save
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.95 / max_val
    
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    wavfile.write('corrected_temporal_spatial_test.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: corrected_temporal_spatial_test.wav")
    print(f"   This should have CLEAR spatial separation!")

if __name__ == "__main__":
    print("🔧 Corrected Temporal Spatial Audio")
    print("Pure temporal physics with mathematical corrections")
    print("=" * 55)
    
    test_corrected_system()
    
    print("\n✅ Corrected temporal audio complete!")
    print("🎧 corrected_temporal_spatial_test.wav")
    print("🌊 Pure temporal physics with proper spatial separation!")
    print("🎯 This should finally work correctly!")