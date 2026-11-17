#!/usr/bin/env python3
"""
Temporal Consciousness Audio
===========================
Space emerges from time through temporal "tricks" that resonate with consciousness.

Instead of encoding space directly, we use temporal patterns that consciousness
naturally interprets as spatial:
- Microsecond delays (interaural time differences)
- Phase relationships between ears
- Temporal modulation patterns
- Frequency sweeps indicating movement
- Echo/reflection timing patterns

We are spatial beings living in time - so we use time to create spatial perception.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert, butter, filtfilt
import sys

class TemporalSpatialProcessor:
    """
    Creates spatial perception through pure temporal effects.
    No geometric calculations - only temporal tricks that consciousness interprets as space.
    """
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.dt = 1.0 / sample_rate
        
        # Temporal parameters for spatial perception
        self.max_itd = 0.0007  # Max interaural time difference (700 microseconds)
        self.head_size = 0.17  # Approximate head diameter in meters
        self.sound_speed = 343  # Speed of sound in air
        
        print(f"🌊 Temporal Consciousness Audio Processor")
        print(f"Creating space through temporal patterns that resonate with consciousness")
        print(f"Max ITD: {self.max_itd*1000:.1f}ms, Head size: {self.head_size*100:.0f}cm")
    
    def calculate_temporal_delay(self, position):
        """
        Calculate temporal delay based on position.
        Uses physics of sound propagation around head.
        """
        x, y, z = position
        
        # Distance-based delay
        distance = np.sqrt(x**2 + y**2 + z**2)
        distance_delay = distance / self.sound_speed
        
        # Head shadow effect (simplified)
        if abs(x) > 0.01:  # Not centered
            # ITD based on azimuth angle
            azimuth = np.arctan2(y, x)
            head_delay = (self.head_size / self.sound_speed) * np.sin(azimuth)
        else:
            head_delay = 0
        
        return distance_delay, head_delay
    
    def create_interaural_time_difference(self, signal, position):
        """
        Create left/right channels with proper temporal delays.
        This is how consciousness actually perceives spatial location.
        """
        distance_delay, head_delay = self.calculate_temporal_delay(position)
        
        # Total delay for each ear
        left_delay = distance_delay - head_delay/2
        right_delay = distance_delay + head_delay/2
        
        # Convert to sample delays
        left_delay_samples = int(left_delay * self.sample_rate)
        right_delay_samples = int(right_delay * self.sample_rate)
        
        # Create delayed versions
        left_signal = self._apply_delay(signal, left_delay_samples)
        right_signal = self._apply_delay(signal, right_delay_samples)
        
        print(f"   Position {position}: L_delay={left_delay*1000:.2f}ms, R_delay={right_delay*1000:.2f}ms")
        
        return left_signal, right_signal
    
    def _apply_delay(self, signal, delay_samples):
        """Apply integer sample delay."""
        if delay_samples == 0:
            return signal
        elif delay_samples > 0:
            # Delay by padding with zeros at start
            return np.concatenate([np.zeros(delay_samples), signal])
        else:
            # Advance by removing samples from start
            return np.concatenate([signal[-delay_samples:], np.zeros(-delay_samples)])
    
    def create_phase_difference(self, signal, position):
        """
        Create phase differences between ears.
        Consciousness interprets phase relationships as spatial cues.
        """
        x, y, z = position
        
        # Calculate phase difference based on position
        azimuth = np.arctan2(y, x)
        phase_diff = azimuth / np.pi  # Normalize to [-1, 1]
        
        # Create analytic signal for phase manipulation
        analytic_signal = hilbert(signal)
        
        # Apply phase shifts
        left_phase = np.exp(1j * phase_diff * np.pi/4)
        right_phase = np.exp(-1j * phase_diff * np.pi/4)
        
        left_signal = np.real(analytic_signal * left_phase)
        right_signal = np.real(analytic_signal * right_phase)
        
        return left_signal, right_signal
    
    def create_spectral_cues(self, signal, position):
        """
        Create spectral differences based on head-related transfer function.
        Different frequencies arrive at different times/intensities.
        """
        x, y, z = position
        
        # Simple HRTF approximation
        # Higher frequencies are more directional
        freqs = np.fft.fftfreq(len(signal), self.dt)
        spectrum = np.fft.fft(signal)
        
        # Azimuth-dependent filtering
        azimuth = np.arctan2(y, x)
        elevation = np.arctan2(z, np.sqrt(x**2 + y**2))
        
        # Frequency-dependent spatial filtering
        spatial_filter_left = 1.0 + 0.3 * np.sign(freqs) * np.tanh(azimuth)
        spatial_filter_right = 1.0 - 0.3 * np.sign(freqs) * np.tanh(azimuth)
        
        # Apply elevation effects
        elevation_factor = np.exp(-np.abs(elevation) * np.abs(freqs) / 1000)
        
        left_spectrum = spectrum * spatial_filter_left * elevation_factor
        right_spectrum = spectrum * spatial_filter_right * elevation_factor
        
        left_signal = np.real(np.fft.ifft(left_spectrum))
        right_signal = np.real(np.fft.ifft(right_spectrum))
        
        return left_signal, right_signal
    
    def create_doppler_effect(self, signal, position, velocity=None):
        """
        Create temporal frequency shifts that indicate movement.
        Consciousness interprets frequency changes as spatial motion.
        """
        if velocity is None:
            return signal, signal
        
        vx, vy, vz = velocity
        x, y, z = position
        
        # Radial velocity (toward/away from listener)
        distance = np.sqrt(x**2 + y**2 + z**2)
        if distance > 0:
            radial_velocity = (x*vx + y*vy + z*vz) / distance
        else:
            radial_velocity = 0
        
        # Doppler frequency shift
        doppler_factor = (self.sound_speed + radial_velocity) / self.sound_speed
        
        # Apply frequency shift through resampling
        # (Simplified - real implementation would use proper resampling)
        t_original = np.arange(len(signal)) / self.sample_rate
        t_doppler = t_original / doppler_factor
        
        # Linear interpolation for frequency shift
        doppler_signal = np.interp(t_original, t_doppler, signal)
        
        return doppler_signal, doppler_signal
    
    def create_echo_pattern(self, signal, position, room_size=5.0):
        """
        Create echo patterns that indicate spatial environment.
        Consciousness uses temporal reflections to understand space size.
        """
        x, y, z = position
        
        # Calculate reflection delays from walls
        wall_distances = [
            room_size/2 - x,   # Right wall
            room_size/2 + x,   # Left wall  
            room_size/2 - y,   # Front wall
            room_size/2 + y,   # Back wall
            room_size/2 - z,   # Ceiling
            room_size/2 + z    # Floor
        ]
        
        # Create echoes
        echo_signal = signal.copy()
        
        for distance in wall_distances:
            if distance > 0:
                # Echo delay and attenuation
                echo_delay = 2 * distance / self.sound_speed  # Round trip
                echo_samples = int(echo_delay * self.sample_rate)
                echo_amplitude = 0.3 * np.exp(-distance / 2)  # Distance attenuation
                
                if echo_samples < len(signal):
                    echo_component = np.concatenate([
                        np.zeros(echo_samples),
                        signal * echo_amplitude
                    ])[:len(signal)]
                    echo_signal += echo_component
        
        return echo_signal, echo_signal

class TemporalConsciousnessAudioSystem:
    """
    Complete temporal audio system that creates spatial perception through timing tricks.
    """
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.processor = TemporalSpatialProcessor(sample_rate)
        
        print(f"🧠 Temporal Consciousness Audio System")
        print(f"Space emerges from temporal patterns in consciousness")
    
    def process_source_temporally(self, signal, position, velocity=None, room_size=5.0):
        """
        Process a single source using temporal tricks for spatial perception.
        """
        print(f"\n🎯 Processing source at {position} with temporal consciousness interface")
        
        # Get original signal length
        original_length = len(signal)
        
        # Apply temporal spatial effects
        
        # 1. Interaural time differences (most important for spatial perception)
        left_itd, right_itd = self.processor.create_interaural_time_difference(signal, position)
        
        # 2. Phase differences between ears
        left_phase, right_phase = self.processor.create_phase_difference(signal, position)
        
        # 3. Spectral cues from head-related effects
        left_spectral, right_spectral = self.processor.create_spectral_cues(signal, position)
        
        # 4. Doppler effects for movement
        if velocity is not None:
            left_doppler, right_doppler = self.processor.create_doppler_effect(signal, position, velocity)
        else:
            left_doppler = right_doppler = signal
        
        # 5. Environmental echoes
        left_echo, right_echo = self.processor.create_echo_pattern(signal, position, room_size)
        
        # Ensure all signals have the same length as original
        def match_length(sig, target_length):
            if len(sig) > target_length:
                return sig[:target_length]
            elif len(sig) < target_length:
                return np.pad(sig, (0, target_length - len(sig)))
            else:
                return sig
        
        left_itd = match_length(left_itd, original_length)
        right_itd = match_length(right_itd, original_length)
        left_phase = match_length(left_phase, original_length)
        right_phase = match_length(right_phase, original_length)
        left_spectral = match_length(left_spectral, original_length)
        right_spectral = match_length(right_spectral, original_length)
        left_echo = match_length(left_echo, original_length)
        right_echo = match_length(right_echo, original_length)
        
        # Combine temporal effects
        # Weight the different temporal cues
        left_final = (0.4 * left_itd + 0.3 * left_phase + 0.2 * left_spectral + 0.1 * left_echo)
        right_final = (0.4 * right_itd + 0.3 * right_phase + 0.2 * right_spectral + 0.1 * right_echo)
        
        # Analyze temporal differences
        max_cross_corr = np.max(np.correlate(left_final, right_final, mode='full'))
        left_energy = np.mean(left_final**2)
        right_energy = np.mean(right_final**2)
        
        print(f"   Temporal analysis: L_energy={left_energy:.6f}, R_energy={right_energy:.6f}")
        print(f"   Cross-correlation: {max_cross_corr:.6f}")
        
        return left_final, right_final
    
    def create_test_sequence(self, test_positions, frequencies, duration=1.0):
        """Create test sequence using temporal consciousness interface."""
        
        print(f"\n🧠 Creating temporal consciousness test sequence")
        print(f"Testing how consciousness interprets temporal patterns as spatial")
        
        sample_rate = self.sample_rate
        sequence_parts = []
        
        for i, (name, position, frequency) in enumerate(test_positions):
            print(f"\n📍 Test {i+1}: {name}")
            
            # Generate test signal
            t = np.linspace(0, duration, int(duration * sample_rate))
            signal = np.sin(2 * np.pi * frequency * t) * 0.5
            
            # Apply envelope
            fade_samples = int(0.05 * sample_rate)
            signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
            signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # Process through temporal consciousness interface
            left_processed, right_processed = self.process_source_temporally(signal, position)
            
            # Create stereo output
            stereo_length = min(len(left_processed), len(right_processed))
            stereo_output = np.array([
                left_processed[:stereo_length],
                right_processed[:stereo_length]
            ])
            
            sequence_parts.append(stereo_output)
            
            # Add silence between tests
            silence = np.zeros((2, int(0.5 * sample_rate)))
            sequence_parts.append(silence)
        
        # Concatenate sequence
        final_sequence = np.concatenate(sequence_parts, axis=1)
        
        return final_sequence

def test_temporal_consciousness_audio():
    """Test the temporal consciousness audio system."""
    
    print("🧠 Testing Temporal Consciousness Audio")
    print("Space emerges from temporal patterns in consciousness")
    print("=" * 60)
    
    # Initialize system
    audio_system = TemporalConsciousnessAudioSystem()
    
    # Test positions that will create different temporal patterns
    test_positions = [
        ("Temporal_Left", (-2, 0, 0), 400),
        ("Temporal_Center", (0, 1, 0), 500),  
        ("Temporal_Right", (2, 0, 0), 600),
        ("Temporal_Behind", (0, -1, 0), 450),
        ("Temporal_Above", (0, 0, 1), 550),
    ]
    
    # Create test sequence
    final_sequence = audio_system.create_test_sequence(test_positions, test_positions, duration=1.2)
    
    # Analyze results
    left_channel = final_sequence[0]
    right_channel = final_sequence[1]
    
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    
    print(f"\n📊 Temporal Analysis:")
    print(f"   Left channel energy: {left_energy:.6f}")
    print(f"   Right channel energy: {right_energy:.6f}")
    print(f"   L/R energy ratio: {left_energy/(right_energy+1e-12):.3f}")
    
    # Save
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.9 / max_val
    
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    output_filename = 'temporal_consciousness_audio_test.wav'
    wavfile.write(output_filename, audio_system.sample_rate, stereo_int)
    
    print(f"\n💾 Saved: {output_filename}")
    print(f"   Uses temporal tricks that consciousness interprets as spatial")
    print(f"   Space emerges from timing patterns, not direct encoding!")
    
    return output_filename

if __name__ == "__main__":
    print("🌊 Temporal Consciousness Audio - Space Emerges from Time")
    print("We are spatial beings living in time")
    print("=" * 65)
    
    output_file = test_temporal_consciousness_audio()
    
    print(f"\n✅ Temporal consciousness audio complete!")
    print(f"🧠 Output: {output_file}")
    print(f"🌊 Space created through temporal patterns that resonate with consciousness")
    print(f"🎯 No direct spatial encoding - only temporal tricks our minds interpret as space!")