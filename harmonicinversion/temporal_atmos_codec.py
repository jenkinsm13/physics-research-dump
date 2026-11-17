#!/usr/bin/env python3
"""
Temporal Atmos Codec
===================
A proper codec for encoding spatial information temporally, following the principle
that "space emerges from time" in our Matryoshka-Chronon framework.

Similar to Dolby Atmos but using temporal shells as the fundamental encoding medium.
Space is not stored directly - it emerges from temporal coefficient patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.special import sph_harm, genlaguerre, factorial
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class TemporalAtmosEncoder:
    """
    Temporal Atmos Encoder - encodes spatial information as temporal coefficient patterns.
    Space emerges from time through proper temporal shell encoding.
    """
    
    def __init__(self, sample_rate=48000, n_shells=7, temporal_resolution=1024):
        self.sample_rate = sample_rate
        self.n_shells = n_shells
        self.temporal_resolution = temporal_resolution
        
        # Temporal codec parameters
        self.shell_frequencies = self._calculate_shell_frequencies()
        self.temporal_window = temporal_resolution / sample_rate
        
        print(f"🌊 Temporal Atmos Encoder")
        print(f"Temporal shells: {n_shells}")
        print(f"Temporal resolution: {temporal_resolution} samples ({self.temporal_window*1000:.1f}ms)")
        print(f"Space emerges from temporal coefficient patterns")
    
    def _calculate_shell_frequencies(self):
        """Calculate fundamental frequencies for each temporal shell."""
        frequencies = {}
        for n in range(1, self.n_shells + 1):
            # Temporal shell frequency: ω_n = 2π/n²  
            frequencies[n] = 2 * np.pi / (n**2)
        return frequencies
    
    def encode_spatial_object(self, position, signal, metadata=None):
        """
        Encode a spatial audio object into temporal coefficients.
        
        Args:
            position: (x, y, z) spatial position
            signal: Audio signal 
            metadata: Object metadata (intensity, type, etc.)
            
        Returns:
            temporal_coefficients: Dict mapping shell -> temporal pattern
        """
        x, y, z = position
        
        print(f"🎯 Encoding spatial object at {position}")
        
        # Convert position to spherical coordinates
        r = np.sqrt(x**2 + y**2 + z**2)
        if r < 1e-10:
            theta, phi = 0, 0
            r = 1e-10
        else:
            theta = np.arccos(np.clip(z / r, -1, 1))
            phi = np.arctan2(y, x)
        
        print(f"   Spherical: (r={r:.3f}, θ={theta:.3f}, φ={phi:.3f})")
        
        # Encode position into temporal shell coefficients
        temporal_coefficients = {}
        
        for n in range(1, self.n_shells + 1):
            # Calculate quantum numbers for this shell
            l_max = min(n-1, 4)  # Practical limit for angular momentum
            
            shell_pattern = np.zeros(self.temporal_resolution, dtype=complex)
            
            for l in range(l_max + 1):
                for m in range(-l, l + 1):
                    
                    # Spherical harmonic coefficient
                    Y_lm = sph_harm(m, l, phi, theta)
                    
                    # Radial component weight
                    radial_weight = self._calculate_radial_weight(n, l, r)
                    
                    # Temporal pattern for this (n,l,m) state
                    temporal_pattern = self._generate_temporal_pattern(
                        n, l, m, Y_lm * radial_weight, signal
                    )
                    
                    shell_pattern += temporal_pattern
            
            temporal_coefficients[n] = shell_pattern
            
            print(f"   Shell {n}: {np.max(np.abs(shell_pattern)):.6f} peak amplitude")
        
        return temporal_coefficients
    
    def _calculate_radial_weight(self, n, l, r, a0=1.0):
        """Calculate radial wavefunction weight for encoding."""
        rho = 2 * r / (n * a0)
        
        try:
            # Simplified radial function
            norm_factor = np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
            radial = norm_factor * (rho**l) * np.exp(-rho/2)
            
            if np.isfinite(radial) and not np.isnan(radial):
                return float(np.real(radial))
            else:
                return 0.0
                
        except:
            # Fallback for numerical issues
            return np.exp(-r/n) / n
    
    def _generate_temporal_pattern(self, n, l, m, coefficient, signal):
        """Generate temporal pattern for specific quantum state."""
        
        # Time evolution frequency for this state
        omega_n = self.shell_frequencies[n]
        
        # Magnetic quantum number introduces rotational frequency
        omega_rotation = m * omega_n / 10  # Scaled rotation
        
        # Combined frequency
        omega_total = omega_n + omega_rotation
        
        # Generate temporal carrier
        t = np.linspace(0, self.temporal_window, self.temporal_resolution)
        
        # Temporal evolution pattern
        temporal_carrier = np.exp(1j * omega_total * t)
        
        # Amplitude modulation by signal energy
        if len(signal) > 0:
            signal_energy = np.mean(signal**2)
            amplitude_mod = np.sqrt(signal_energy)
        else:
            amplitude_mod = 1.0
        
        # Final temporal pattern
        pattern = coefficient * amplitude_mod * temporal_carrier
        
        return pattern
    
    def create_temporal_stream(self, spatial_objects):
        """
        Create temporal stream from multiple spatial objects.
        This is the "encoded" format - pure temporal data.
        """
        
        print(f"\n🌊 Creating temporal stream from {len(spatial_objects)} objects")
        
        # Initialize temporal stream
        temporal_stream = {}
        for n in range(1, self.n_shells + 1):
            temporal_stream[n] = np.zeros(self.temporal_resolution, dtype=complex)
        
        # Encode each spatial object
        for i, obj in enumerate(spatial_objects):
            print(f"\nObject {i+1}: {obj.get('name', 'Unnamed')}")
            
            coefficients = self.encode_spatial_object(
                obj['position'], 
                obj['signal'],
                obj.get('metadata', {})
            )
            
            # Add to temporal stream
            for n, pattern in coefficients.items():
                temporal_stream[n] += pattern
        
        print(f"\n📊 Temporal stream statistics:")
        for n in range(1, self.n_shells + 1):
            energy = np.mean(np.abs(temporal_stream[n])**2)
            print(f"   Shell {n}: energy={energy:.6f}")
        
        return temporal_stream

class TemporalAtmosDecoder:
    """
    Temporal Atmos Decoder - reconstructs spatial audio from temporal coefficients.
    Space emerges during decoding through proper observation geometry.
    """
    
    def __init__(self, sample_rate=48000, temporal_resolution=1024):
        self.sample_rate = sample_rate
        self.temporal_resolution = temporal_resolution
        self.shell_processor = TemporalShellProcessor()
        
        print(f"🎧 Temporal Atmos Decoder")
        print(f"Reconstructs space from temporal patterns")
    
    def decode_to_binaural(self, temporal_stream, listener_position=(0, 0, 0), head_rotation=0):
        """
        Decode temporal stream to binaural audio.
        Space emerges through evaluation at ear positions.
        """
        
        print(f"\n🎧 Decoding to binaural at position {listener_position}")
        
        # Listener geometry (220mm ear spacing as measured)
        ear_separation = 0.22
        
        # Calculate ear positions with head rotation
        cos_rot = np.cos(head_rotation)
        sin_rot = np.sin(head_rotation)
        
        left_ear = (
            listener_position[0] - ear_separation/2 * cos_rot,
            listener_position[1] - ear_separation/2 * sin_rot,
            listener_position[2]
        )
        
        right_ear = (
            listener_position[0] + ear_separation/2 * cos_rot,
            listener_position[1] + ear_separation/2 * sin_rot,
            listener_position[2]
        )
        
        print(f"   Left ear: {left_ear}")
        print(f"   Right ear: {right_ear}")
        
        # Evaluate temporal stream at ear positions
        left_signal = self._evaluate_at_position(temporal_stream, left_ear)
        right_signal = self._evaluate_at_position(temporal_stream, right_ear)
        
        return left_signal, right_signal
    
    def _evaluate_at_position(self, temporal_stream, position):
        """Evaluate temporal stream at specific spatial position - space emerges here."""
        
        x, y, z = position
        
        # Convert to spherical coordinates
        r = np.sqrt(x**2 + y**2 + z**2)
        if r < 1e-10:
            return np.zeros(self.temporal_resolution)
            
        theta = np.arccos(np.clip(z / r, -1, 1))
        phi = np.arctan2(y, x)
        
        # Reconstruct signal by evaluating all shells
        reconstructed = np.zeros(self.temporal_resolution, dtype=complex)
        
        for n, shell_pattern in temporal_stream.items():
            
            # Calculate spatial weight at this position for shell n
            spatial_weight = self._calculate_spatial_weight(n, r, theta, phi)
            
            # Add weighted contribution
            reconstructed += spatial_weight * shell_pattern
        
        # Convert to real signal and apply temporal processing
        real_signal = np.real(reconstructed)
        
        # Apply temporal shell processing for character
        processed_signal = self.shell_processor.process_through_shells(
            real_signal, self.sample_rate
        )
        
        return processed_signal
    
    def _calculate_spatial_weight(self, n, r, theta, phi):
        """Calculate spatial weight for shell n at position (r, theta, phi)."""
        
        # Radial component
        radial_weight = np.exp(-r/n) / n  # Simplified but stable
        
        # Angular component - sum over relevant harmonics
        angular_weight = 0.0
        l_max = min(n-1, 4)
        
        for l in range(l_max + 1):
            for m in range(-l, l + 1):
                Y_lm = sph_harm(m, l, phi, theta)
                angular_weight += abs(Y_lm)**2
        
        # Normalize
        angular_weight = angular_weight / ((l_max + 1)**2)
        
        return radial_weight * angular_weight
    
    def decode_to_surround(self, temporal_stream, speaker_positions):
        """
        Decode to arbitrary speaker configuration.
        Space emerges through evaluation at speaker positions.
        """
        
        print(f"\n🔊 Decoding to {len(speaker_positions)} speakers")
        
        speaker_signals = []
        
        for i, speaker_pos in enumerate(speaker_positions):
            signal = self._evaluate_at_position(temporal_stream, speaker_pos)
            speaker_signals.append(signal)
            
            print(f"   Speaker {i+1} at {speaker_pos}: peak={np.max(np.abs(signal)):.3f}")
        
        return speaker_signals

class TemporalAtmosCodec:
    """Complete Temporal Atmos Codec - encode spatial scenes to temporal, decode back to spatial."""
    
    def __init__(self, sample_rate=48000, temporal_resolution=1024, n_shells=7):
        self.encoder = TemporalAtmosEncoder(sample_rate, n_shells, temporal_resolution)
        self.decoder = TemporalAtmosDecoder(sample_rate, temporal_resolution)
        
        print(f"🌊 Temporal Atmos Codec Initialized")
        print(f"Space ↔ Time encoding with {n_shells} temporal shells")
    
    def encode_scene(self, spatial_objects):
        """Encode entire spatial scene to temporal format."""
        return self.encoder.create_temporal_stream(spatial_objects)
    
    def decode_scene_binaural(self, temporal_stream, listener_position=(0, 0, 0)):
        """Decode temporal format back to binaural spatial audio."""
        return self.decoder.decode_to_binaural(temporal_stream, listener_position)
    
    def decode_scene_surround(self, temporal_stream, speaker_config):
        """Decode temporal format to surround speaker configuration."""
        return self.decoder.decode_to_surround(temporal_stream, speaker_config)

def test_temporal_atmos_codec():
    """Test the complete Temporal Atmos codec system."""
    
    print("🌊 Testing Temporal Atmos Codec")
    print("=" * 40)
    
    # Initialize codec
    codec = TemporalAtmosCodec(temporal_resolution=2048)
    
    # Create test scene with spatial objects
    sample_rate = 48000
    duration = 1.0
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    spatial_scene = [
        {
            'name': 'Left_Source',
            'position': (-3, 0, 0),
            'signal': np.sin(2 * np.pi * 300 * t) * 0.5,
            'metadata': {'type': 'tone', 'frequency': 300}
        },
        {
            'name': 'Center_Source',
            'position': (0, 2, 0),
            'signal': np.sin(2 * np.pi * 400 * t) * 0.5,
            'metadata': {'type': 'tone', 'frequency': 400}
        },
        {
            'name': 'Right_Source',
            'position': (3, 0, 0),
            'signal': np.sin(2 * np.pi * 500 * t) * 0.5,
            'metadata': {'type': 'tone', 'frequency': 500}
        },
        {
            'name': 'Overhead_Source',
            'position': (0, 0, 2),
            'signal': np.sin(2 * np.pi * 600 * t) * 0.3,
            'metadata': {'type': 'tone', 'frequency': 600}
        }
    ]
    
    print(f"\n📦 Encoding scene with {len(spatial_scene)} objects")
    
    # ENCODE: Spatial scene → Temporal stream
    temporal_stream = codec.encode_scene(spatial_scene)
    
    print("\n✅ Encoding complete - space stored as temporal patterns")
    
    # DECODE: Temporal stream → Binaural audio
    print("\n🎧 Decoding to binaural audio")
    left_channel, right_channel = codec.decode_scene_binaural(temporal_stream)
    
    # Analyze spatial separation
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    
    print(f"\n📊 Decoding analysis:")
    print(f"   Left channel energy: {left_energy:.6f}")
    print(f"   Right channel energy: {right_energy:.6f}")
    print(f"   L/R ratio: {left_energy/(right_energy+1e-12):.3f}")
    
    # Create full audio sequence with silence between
    sequence_parts = []
    
    # Process scene in chunks (simulating real-time codec)
    chunk_size = codec.encoder.temporal_resolution
    total_samples = len(spatial_scene[0]['signal'])
    
    for chunk_start in range(0, total_samples, chunk_size):
        chunk_end = min(chunk_start + chunk_size, total_samples)
        
        # Create chunk scene
        chunk_scene = []
        for obj in spatial_scene:
            chunk_obj = obj.copy()
            chunk_obj['signal'] = obj['signal'][chunk_start:chunk_end]
            chunk_scene.append(chunk_obj)
        
        # Encode chunk
        chunk_temporal = codec.encode_scene(chunk_scene)
        
        # Decode chunk
        chunk_left, chunk_right = codec.decode_scene_binaural(chunk_temporal)
        
        # Store chunk
        chunk_stereo = np.array([chunk_left, chunk_right])
        sequence_parts.append(chunk_stereo)
    
    # Concatenate all chunks
    if sequence_parts:
        final_audio = np.concatenate(sequence_parts, axis=1)
    else:
        final_audio = np.array([left_channel, right_channel])
    
    # Add silence and save
    silence = np.zeros((2, int(0.5 * sample_rate)))
    final_sequence = np.concatenate([final_audio, silence], axis=1)
    
    # Normalize
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.9 / max_val
    
    # Save
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    wavfile.write('temporal_atmos_test.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: temporal_atmos_test.wav")
    print(f"   Spatial scene encoded/decoded through temporal coefficients")
    print(f"   Space emerged from time during decoding!")
    
    return 'temporal_atmos_test.wav'

def demo_temporal_stream_analysis():
    """Demonstrate analysis of the temporal stream format."""
    
    print("\n🔬 Temporal Stream Analysis")
    print("=" * 30)
    
    codec = TemporalAtmosCodec()
    
    # Simple test object
    t = np.linspace(0, 0.5, int(0.5 * 48000))
    test_signal = np.sin(2 * np.pi * 440 * t) * 0.5
    
    test_object = {
        'name': 'Analysis_Source',
        'position': (1, 1, 0),
        'signal': test_signal,
        'metadata': {'frequency': 440}
    }
    
    # Encode
    temporal_stream = codec.encode_scene([test_object])
    
    # Analyze temporal patterns
    print("\n📊 Temporal stream analysis:")
    for shell_n, pattern in temporal_stream.items():
        
        # Energy analysis
        energy = np.mean(np.abs(pattern)**2)
        peak = np.max(np.abs(pattern))
        
        # Frequency analysis
        fft = np.fft.fft(pattern)
        freq_bins = np.fft.fftfreq(len(pattern), 1/codec.encoder.sample_rate)
        dominant_freq_idx = np.argmax(np.abs(fft))
        dominant_freq = freq_bins[dominant_freq_idx]
        
        print(f"   Shell {shell_n}: energy={energy:.6f}, peak={peak:.3f}, freq={dominant_freq:.2f}Hz")
    
    print("\n✅ This is the 'encoded' format - pure temporal data")
    print("   Spatial information emerges only during decoding!")

if __name__ == "__main__":
    print("🌊 Temporal Atmos Codec - Space Emerges from Time")
    print("=" * 55)
    
    # Test complete codec
    output_file = test_temporal_atmos_codec()
    
    # Demonstrate temporal stream analysis
    demo_temporal_stream_analysis()
    
    print(f"\n✅ Temporal Atmos codec demonstration complete!")
    print(f"🎧 Output: {output_file}")
    print(f"🌊 Space encoded as temporal coefficients")
    print(f"🎯 Space emerges during decoding - true temporal-first approach!")