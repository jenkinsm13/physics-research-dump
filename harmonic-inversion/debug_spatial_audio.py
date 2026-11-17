#!/usr/bin/env python3
"""
Debug Spatial Audio System
==========================
Investigates why the spatial audio isn't creating proper stereo separation
and fixes the positioning algorithm.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import SphericalHarmonicAudioEncoder, ChronodynamicAudioSystem

def debug_spherical_harmonics():
    """Debug spherical harmonic calculations."""
    
    encoder = SphericalHarmonicAudioEncoder()
    
    print("🔍 Debugging Spherical Harmonic Calculations")
    print("=" * 50)
    
    # Test positions
    test_positions = [
        ("Center", (0, 0, 0)),
        ("Right", (2, 0, 0)),
        ("Left", (-2, 0, 0)),
        ("Front", (0, 2, 0)),
        ("Back", (0, -2, 0)),
    ]
    
    # Ear positions
    left_ear = (-0.1, 0, 0)
    right_ear = (0.1, 0, 0)
    
    for name, pos in test_positions:
        print(f"\n📍 Testing position: {name} at {pos}")
        
        # Get spherical coordinates
        r, theta, phi = encoder.cartesian_to_spherical(*pos)
        print(f"   Spherical: r={r:.3f}, θ={theta:.3f}, φ={phi:.3f}")
        
        # Encode position
        coeffs = encoder.encode_spatial_position(pos, intensity=1.0)
        print(f"   Generated {len(coeffs)} coefficients")
        
        # Sample at ears
        r_l, theta_l, phi_l = encoder.cartesian_to_spherical(*left_ear)
        r_r, theta_r, phi_r = encoder.cartesian_to_spherical(*right_ear)
        
        psi_left = 0
        psi_right = 0
        
        for (n, l, m), coeff in coeffs.items():
            # Left ear
            Y_lm_l = encoder.compute_spherical_harmonic(l, m, theta_l, phi_l)
            R_nl_l = encoder.radial_wavefunction(n, l, r_l)
            psi_left += coeff * R_nl_l * Y_lm_l
            
            # Right ear
            Y_lm_r = encoder.compute_spherical_harmonic(l, m, theta_r, phi_r)
            R_nl_r = encoder.radial_wavefunction(n, l, r_r)
            psi_right += coeff * R_nl_r * Y_lm_r
        
        weight_left = abs(psi_left)**2
        weight_right = abs(psi_right)**2
        
        print(f"   Left ear weight: {weight_left:.6f}")
        print(f"   Right ear weight: {weight_right:.6f}")
        print(f"   L/R ratio: {weight_left/(weight_right+1e-10):.3f}")
        print(f"   Total: {weight_left + weight_right:.6f}")

def create_simple_stereo_test():
    """Create a simple test that should definitely work."""
    
    print("\n🎯 Creating Simple Stereo Test")
    print("=" * 40)
    
    sample_rate = 48000
    duration = 1.0
    
    # Generate test signal
    t = np.linspace(0, duration, int(duration * sample_rate))
    test_signal = np.sin(2 * np.pi * 440 * t) * 0.5
    
    # Create manual stereo panning for comparison
    manual_left = np.copy(test_signal)
    manual_right = np.zeros_like(test_signal)
    manual_stereo = np.vstack([manual_left, manual_right])
    
    # Save manual test
    manual_int = (manual_stereo * 32767).astype(np.int16).T
    wavfile.write('manual_left_test.wav', sample_rate, manual_int)
    print("💾 Saved manual_left_test.wav (should be hard left)")
    
    # Now try with spatial encoder
    encoder = SphericalHarmonicAudioEncoder(sample_rate)
    
    # Test extreme left position
    left_position = (-5, 0, 0)
    coeffs = encoder.encode_spatial_position(left_position, intensity=1.0)
    
    print(f"Encoding position {left_position}")
    print(f"Generated {len(coeffs)} coefficients")
    
    # Sample at ears with wider separation
    left_ear = (-0.5, 0, 0)   # Much wider separation
    right_ear = (0.5, 0, 0)
    
    r_l, theta_l, phi_l = encoder.cartesian_to_spherical(*left_ear)
    r_r, theta_r, phi_r = encoder.cartesian_to_spherical(*right_ear)
    
    psi_left = 0
    psi_right = 0
    
    for (n, l, m), coeff in coeffs.items():
        Y_lm_l = encoder.compute_spherical_harmonic(l, m, theta_l, phi_l)
        R_nl_l = encoder.radial_wavefunction(n, l, r_l)
        psi_left += coeff * R_nl_l * Y_lm_l
        
        Y_lm_r = encoder.compute_spherical_harmonic(l, m, theta_r, phi_r)
        R_nl_r = encoder.radial_wavefunction(n, l, r_r)
        psi_right += coeff * R_nl_r * Y_lm_r
    
    weight_left = abs(psi_left)**2
    weight_right = abs(psi_right)**2
    
    print(f"Left weight: {weight_left:.6f}")
    print(f"Right weight: {weight_right:.6f}")
    print(f"L/R ratio: {weight_left/(weight_right+1e-10):.3f}")
    
    # Create spatial audio
    spatial_left = test_signal * weight_left
    spatial_right = test_signal * weight_right
    spatial_stereo = np.vstack([spatial_left, spatial_right])
    
    # Normalize
    max_val = np.max(np.abs(spatial_stereo))
    if max_val > 0:
        spatial_stereo = spatial_stereo * 0.95 / max_val
    
    spatial_int = (spatial_stereo * 32767).astype(np.int16).T
    wavfile.write('spatial_left_test.wav', sample_rate, spatial_int)
    print("💾 Saved spatial_left_test.wav (temporal spatial)")

def create_enhanced_spatial_system():
    """Create an enhanced spatial audio system with stronger separation."""
    
    class EnhancedSpatialEncoder(SphericalHarmonicAudioEncoder):
        """Enhanced encoder with stronger spatial separation."""
        
        def __init__(self, sample_rate=48000, max_l=6):
            super().__init__(sample_rate, max_l)
            # Increase max_l for more spatial resolution
            
        def encode_spatial_position(self, position, intensity=1.0):
            """Enhanced spatial encoding with stronger contrast."""
            x, y, z = position
            r, theta, phi = self.cartesian_to_spherical(x, y, z)
            
            # Limit radius to reasonable range but don't clip too aggressively
            r = np.clip(r, 0.01, 20.0)
            
            coefficients = {}
            
            # Use more terms for better spatial resolution
            for n in range(1, self.max_l + 3):
                for l in range(min(n, self.max_l + 1)):
                    for m in range(-l, l + 1):
                        # Compute basis function
                        Y_lm = self.compute_spherical_harmonic(l, m, theta, phi)
                        R_nl = self.radial_wavefunction(n, l, r)
                        
                        # Enhanced void potential
                        void_weight = np.exp(self.void_potential(r) * 2.0)  # Stronger effect
                        
                        # Weight higher order terms more for spatial precision
                        spatial_weight = 1.0 + l * 0.5
                        
                        coefficient = intensity * R_nl * Y_lm * void_weight * spatial_weight
                        coefficients[(n, l, m)] = coefficient
            
            return coefficients
    
    class EnhancedChronodynamicSystem:
        """Enhanced system with better binaural processing."""
        
        def __init__(self, sample_rate=48000, buffer_size=1024):
            self.sample_rate = sample_rate
            self.buffer_size = buffer_size
            self.encoder = EnhancedSpatialEncoder(sample_rate)
            self.time = 0
            
        def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
            """Enhanced processing with stronger binaural separation."""
            
            left_channel = np.zeros(self.buffer_size)
            right_channel = np.zeros(self.buffer_size)
            
            for source in audio_sources:
                # Get relative position
                rel_pos = np.array(source['position']) - np.array(listener_position)
                
                # Encode with enhanced encoder
                coeffs = self.encoder.encode_spatial_position(rel_pos, source['intensity'])
                
                # Time evolution
                evolved_coeffs = self.encoder.time_evolve_coefficients(coeffs, self.time)
                
                # Enhanced ear positions (wider separation + slight offset)
                left_ear_pos = (-0.3, 0.05, 0)   # 30cm apart, slightly offset
                right_ear_pos = (0.3, -0.05, 0)
                
                # Convert to spherical
                r_l, theta_l, phi_l = self.encoder.cartesian_to_spherical(*left_ear_pos)
                r_r, theta_r, phi_r = self.encoder.cartesian_to_spherical(*right_ear_pos)
                
                # Evaluate wavefunction
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
                
                # Enhanced spatial weighting
                weight_left = abs(psi_left)**2
                weight_right = abs(psi_right)**2
                
                # Enhance separation by boosting differences
                total_weight = weight_left + weight_right + 1e-10
                weight_left = weight_left / total_weight
                weight_right = weight_right / total_weight
                
                # Apply power law to enhance differences
                power = 1.5
                weight_left = weight_left ** power
                weight_right = weight_right ** power
                
                # Renormalize
                total_weight = weight_left + weight_right + 1e-10
                weight_left = weight_left / total_weight
                weight_right = weight_right / total_weight
                
                # Apply to signal
                signal = source['signal'][:self.buffer_size]
                left_channel += weight_left * signal
                right_channel += weight_right * signal
            
            self.time += self.buffer_size / self.sample_rate
            return left_channel, right_channel
    
    return EnhancedChronodynamicSystem

def test_enhanced_system():
    """Test the enhanced spatial audio system."""
    
    print("\n🚀 Testing Enhanced Spatial Audio System")
    print("=" * 50)
    
    # Create enhanced system
    Enhanced = create_enhanced_spatial_system()
    audio_system = Enhanced()
    
    # Test parameters
    sample_rate = 48000
    duration = 2.0
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    # Create test signals
    test_signal = np.sin(2 * np.pi * 440 * t) * 0.7
    
    # Test extreme positions
    test_sources = [
        {'position': (-3, 0, 0), 'signal': test_signal, 'intensity': 1.0},  # Hard left
    ]
    
    # Process in chunks
    total_samples = len(test_signal)
    buffer_size = audio_system.buffer_size
    stereo_output = np.zeros((2, total_samples))
    
    for i in range(0, total_samples, buffer_size):
        end_idx = min(i + buffer_size, total_samples)
        
        # Prepare chunk
        chunk_sources = []
        for src in test_sources:
            chunk_signal = src['signal'][i:end_idx]
            if len(chunk_signal) < buffer_size:
                chunk_signal = np.pad(chunk_signal, (0, buffer_size - len(chunk_signal)))
            
            chunk_sources.append({
                'position': src['position'],
                'signal': chunk_signal,
                'intensity': src['intensity']
            })
        
        # Process
        left, right = audio_system.process_audio_buffer(chunk_sources)
        
        actual_length = end_idx - i
        stereo_output[0, i:end_idx] = left[:actual_length]
        stereo_output[1, i:end_idx] = right[:actual_length]
    
    # Analyze results
    left_channel = stereo_output[0]
    right_channel = stereo_output[1]
    
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    total_energy = left_energy + right_energy
    
    print(f"Left energy: {left_energy:.6f} ({left_energy/total_energy*100:.1f}%)")
    print(f"Right energy: {right_energy:.6f} ({right_energy/total_energy*100:.1f}%)")
    print(f"L/R ratio: {left_energy/(right_energy+1e-10):.3f}")
    
    # Save enhanced test
    max_val = np.max(np.abs(stereo_output))
    if max_val > 0:
        stereo_output = stereo_output * 0.95 / max_val
    
    stereo_int = (stereo_output * 32767).astype(np.int16).T
    wavfile.write('enhanced_spatial_test.wav', sample_rate, stereo_int)
    print("💾 Saved enhanced_spatial_test.wav")

def create_extreme_separation_test():
    """Create test with maximum possible separation."""
    
    print("\n💥 Creating Extreme Separation Test")
    print("=" * 40)
    
    sample_rate = 48000
    duration = 1.0
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    # Different frequencies for left and right
    left_freq = 400
    right_freq = 800
    
    left_signal = np.sin(2 * np.pi * left_freq * t) * 0.7
    right_signal = np.sin(2 * np.pi * right_freq * t) * 0.7
    
    # Manual extreme separation
    extreme_stereo = np.vstack([left_signal, right_signal])
    
    # Save
    extreme_int = (extreme_stereo * 32767).astype(np.int16).T
    wavfile.write('extreme_separation_test.wav', sample_rate, extreme_int)
    print("💾 Saved extreme_separation_test.wav (400Hz left, 800Hz right)")
    print("   This should have OBVIOUS left/right separation")

if __name__ == "__main__":
    print("🔧 Spatial Audio Debug Session")
    print("=" * 60)
    
    # Debug spherical harmonics
    debug_spherical_harmonics()
    
    # Create simple tests
    create_simple_stereo_test()
    
    # Test enhanced system
    test_enhanced_system()
    
    # Create extreme test for comparison
    create_extreme_separation_test()
    
    print("\n✅ Debug session complete!")
    print("\nGenerated test files:")
    print("   🎧 manual_left_test.wav - Manual hard left (should work)")
    print("   🎧 spatial_left_test.wav - Basic spatial left")
    print("   🎧 enhanced_spatial_test.wav - Enhanced spatial")
    print("   🎧 extreme_separation_test.wav - Extreme L/R test")
    print("\n🎯 Test these files to diagnose the spatial issue!")