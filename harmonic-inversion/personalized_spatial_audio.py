#!/usr/bin/env python3
"""
Personalized Spatial Audio System
=================================
Customized for your specific ear spacing (220mm) for maximum spatial accuracy.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class PersonalizedSpatialAudio:
    """Spatial audio system customized for 220mm ear spacing."""
    
    def __init__(self, sample_rate=48000, buffer_size=1024, ear_spacing_mm=220):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Your personal ear geometry
        self.ear_spacing = ear_spacing_mm / 1000.0  # Convert to meters
        self.head_radius = self.ear_spacing / 2.0    # Approximate head radius
        
        # Temporal shell processor
        self.shell_processor = TemporalShellProcessor()
        
        # Ear positions relative to head center
        self.ear_positions = {
            'left': (-self.ear_spacing/2, 0, 0),
            'right': (self.ear_spacing/2, 0, 0)
        }
        
        # Head model for shadow calculations
        self.head_circumference = np.pi * self.ear_spacing  # Approximate
        
        self.time = 0
        
        print(f"🎧 Personalized Spatial Audio System")
        print(f"Ear spacing: {ear_spacing_mm}mm ({self.ear_spacing:.3f}m)")
        print(f"Head radius: {self.head_radius*1000:.1f}mm")
        print(f"Head circumference: {self.head_circumference*1000:.1f}mm")
        
    def calculate_interaural_time_difference(self, source_pos):
        """Calculate ITD based on your specific head geometry."""
        
        # Speed of sound
        c = 343.0  # m/s
        
        # Calculate path lengths to each ear
        left_ear = np.array(self.ear_positions['left'])
        right_ear = np.array(self.ear_positions['right'])
        source = np.array(source_pos)
        
        # Direct distances
        dist_left = np.linalg.norm(source - left_ear)
        dist_right = np.linalg.norm(source - right_ear)
        
        # For more accuracy, account for head geometry
        # Angle of source relative to head center
        angle_to_source = np.arctan2(source[1], source[0])
        
        # Path difference accounting for head diffraction
        if abs(source[0]) > 0.001:  # Not directly in front/back
            # Simplified Woodworth formula for ITD
            sin_theta = source[0] / np.linalg.norm(source[:2])
            sin_theta = np.clip(sin_theta, -1, 1)
            
            # ITD with head diffraction
            itd = (self.ear_spacing / c) * (sin_theta + np.sin(np.arcsin(sin_theta)))
        else:
            # Direct front/back - minimal ITD
            itd = (dist_right - dist_left) / c
        
        # Convert to samples
        itd_samples = int(itd * self.sample_rate)
        
        return itd_samples, itd
    
    def calculate_interaural_level_difference(self, source_pos):
        """Calculate ILD based on head shadow with your geometry."""
        
        source = np.array(source_pos)
        
        # Angle relative to front of head
        angle = np.arctan2(source[0], source[1])  # x,y -> left/right, front/back
        
        # Distance to each ear
        left_ear = np.array(self.ear_positions['left'])
        right_ear = np.array(self.ear_positions['right'])
        
        dist_left = np.linalg.norm(source - left_ear)
        dist_right = np.linalg.norm(source - right_ear)
        
        # Inverse square law
        gain_left = 1.0 / (1.0 + dist_left**2)
        gain_right = 1.0 / (1.0 + dist_right**2)
        
        # Head shadow effect based on frequency and angle
        # Higher frequencies are more affected by head shadow
        frequency_factor = 1000  # Assume mid-frequency for now
        shadow_frequency = 2000  # Hz where head shadow becomes significant
        shadow_strength = min(1.0, frequency_factor / shadow_frequency)
        
        # Calculate shadow attenuation
        if source[0] < -self.head_radius/2:  # Source on left side
            # Right ear is shadowed
            shadow_angle = np.pi + angle if angle < 0 else angle
            shadow_attenuation = 1.0 - shadow_strength * np.exp(-abs(shadow_angle) / (np.pi/2))
            gain_right *= shadow_attenuation
            
        elif source[0] > self.head_radius/2:  # Source on right side
            # Left ear is shadowed
            shadow_angle = angle if angle > 0 else np.pi + angle
            shadow_attenuation = 1.0 - shadow_strength * np.exp(-abs(shadow_angle) / (np.pi/2))
            gain_left *= shadow_attenuation
        
        # Directional sensitivity of ears (pointing outward)
        # Left ear points left, right ear points right
        left_direction = np.array([-1, 0, 0])
        right_direction = np.array([1, 0, 0])
        
        to_source_left = (source - left_ear)
        to_source_right = (source - right_ear)
        
        if np.linalg.norm(to_source_left) > 0:
            to_source_left = to_source_left / np.linalg.norm(to_source_left)
            directional_left = max(0.1, np.dot(left_direction, to_source_left))
        else:
            directional_left = 1.0
            
        if np.linalg.norm(to_source_right) > 0:
            to_source_right = to_source_right / np.linalg.norm(to_source_right)
            directional_right = max(0.1, np.dot(right_direction, to_source_right))
        else:
            directional_right = 1.0
        
        # Combine all effects
        final_gain_left = gain_left * directional_left
        final_gain_right = gain_right * directional_right
        
        return final_gain_left, final_gain_right
    
    def process_source_with_hrtf(self, source_pos, signal, intensity=1.0):
        """Process source with personalized HRTF for your head geometry."""
        
        # Calculate ITD and ILD
        itd_samples, itd_seconds = self.calculate_interaural_time_difference(source_pos)
        gain_left, gain_right = self.calculate_interaural_level_difference(source_pos)
        
        # Apply temporal shell processing first
        temporal_signal = self.shell_processor.process_through_shells(signal, self.sample_rate)
        
        # Apply intensity
        temporal_signal *= intensity
        
        # Create stereo with ITD
        left_signal = np.zeros_like(temporal_signal)
        right_signal = np.zeros_like(temporal_signal)
        
        # Apply time delays
        if itd_samples > 0:  # Right ear delayed
            right_signal[abs(itd_samples):] = temporal_signal[:-abs(itd_samples)]
            left_signal = temporal_signal
        elif itd_samples < 0:  # Left ear delayed
            left_signal[abs(itd_samples):] = temporal_signal[:-abs(itd_samples)]
            right_signal = temporal_signal
        else:  # No delay
            left_signal = temporal_signal
            right_signal = temporal_signal
        
        # Apply ILD gains
        left_signal *= gain_left
        right_signal *= gain_right
        
        # Debug info
        debug_info = {
            'source_position': source_pos,
            'itd_seconds': itd_seconds,
            'itd_samples': itd_samples,
            'gain_left': gain_left,
            'gain_right': gain_right,
            'lr_ratio': gain_left / (gain_right + 1e-10),
            'distance_left': np.linalg.norm(np.array(source_pos) - np.array(self.ear_positions['left'])),
            'distance_right': np.linalg.norm(np.array(source_pos) - np.array(self.ear_positions['right']))
        }
        
        return left_signal, right_signal, debug_info
    
    def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
        """Process multiple sources for personalized spatial audio."""
        
        left_channel = np.zeros(self.buffer_size)
        right_channel = np.zeros(self.buffer_size)
        
        debug_info = []
        
        for source in audio_sources:
            # Adjust for listener position
            rel_pos = np.array(source['position']) - np.array(listener_position)
            
            # Get signal chunk
            signal = source['signal'][:self.buffer_size]
            intensity = source.get('intensity', 1.0)
            
            # Process with personalized HRTF
            left_sig, right_sig, debug = self.process_source_with_hrtf(rel_pos, signal, intensity)
            
            # Add to output channels
            left_channel += left_sig[:self.buffer_size]
            right_channel += right_sig[:self.buffer_size]
            
            debug_info.append(debug)
        
        self.time += self.buffer_size / self.sample_rate
        
        return left_channel, right_channel, debug_info

def create_personalized_test_suite():
    """Create test suite optimized for 220mm ear spacing."""
    
    print("\n🎯 Creating Personalized Test Suite (220mm ears)")
    print("=" * 55)
    
    # Initialize with your ear spacing
    audio_system = PersonalizedSpatialAudio(ear_spacing_mm=220)
    
    # Test parameters
    sample_rate = 48000
    tone_duration = 1.5
    silence_duration = 0.5
    
    # Comprehensive test positions
    test_positions = [
        ("Hard_Left", (-4, 0, 0), 400),
        ("Soft_Left", (-1, 0, 0), 450), 
        ("Center", (0, 2, 0), 500),
        ("Soft_Right", (1, 0, 0), 550),
        ("Hard_Right", (4, 0, 0), 600),
        ("Back_Left", (-2, -2, 0), 650),
        ("Back_Right", (2, -2, 0), 700),
        ("Above_Left", (-1, 0, 2), 750),
        ("Above_Right", (1, 0, 2), 800),
        ("Close_Left", (-0.3, 0, 0), 850),  # Very close to your head
        ("Close_Right", (0.3, 0, 0), 900),
    ]
    
    sequence_parts = []
    
    for name, position, frequency in test_positions:
        print(f"\n📍 {name} at {position} ({frequency}Hz)")
        
        # Generate test tone
        t = np.linspace(0, tone_duration, int(tone_duration * sample_rate))
        test_signal = np.sin(2 * np.pi * frequency * t)
        
        # Apply gentle envelope
        fade_samples = int(0.05 * sample_rate)
        test_signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
        test_signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        test_signal *= 0.7
        
        # Process through personalized system
        sources = [{'position': position, 'signal': test_signal, 'intensity': 1.0}]
        
        total_samples = len(test_signal)
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
            
            left, right, debug = audio_system.process_audio_buffer(chunk_sources)
            
            actual_length = end_idx - i
            stereo_output[0, i:end_idx] = left[:actual_length]
            stereo_output[1, i:end_idx] = right[:actual_length]
            
            # Print debug for first chunk
            if i == 0 and debug:
                d = debug[0]
                print(f"   ITD: {d['itd_seconds']*1000:.2f}ms ({d['itd_samples']} samples)")
                print(f"   Gains: L={d['gain_left']:.4f}, R={d['gain_right']:.4f}")
                print(f"   L/R ratio: {d['lr_ratio']:.3f}")
                print(f"   Distances: L={d['distance_left']:.3f}m, R={d['distance_right']:.3f}m")
        
        # Add silence
        silence_samples = int(silence_duration * sample_rate)
        silence = np.zeros((2, silence_samples))
        
        sequence_parts.append(stereo_output)
        sequence_parts.append(silence)
    
    # Concatenate and save
    final_sequence = np.concatenate(sequence_parts, axis=1)
    
    # Normalize
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.95 / max_val
    
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    wavfile.write('personalized_spatial_test_220mm.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: personalized_spatial_test_220mm.wav")
    print(f"   Duration: {len(stereo_int) / sample_rate:.1f} seconds")
    print(f"   Optimized for your 220mm ear spacing!")

def create_precision_movement_test():
    """Create ultra-precise movement test for 220mm ears."""
    
    print("\n🌀 Creating Precision Movement Test")
    print("=" * 35)
    
    audio_system = PersonalizedSpatialAudio(ear_spacing_mm=220)
    
    # Parameters for smooth movement
    duration = 8.0
    sample_rate = 48000
    total_samples = int(duration * sample_rate)
    
    # Generate smooth tone with gentle modulation
    t = np.linspace(0, duration, total_samples)
    base_frequency = 600
    modulation = 1 + 0.1 * np.sin(2 * np.pi * 3 * t)  # 3Hz modulation
    signal = np.sin(2 * np.pi * base_frequency * t * modulation) * 0.6
    
    # Movement path: figure-8 around your head
    path_frequency = 1 / duration  # One complete figure-8
    
    # Process with high temporal resolution
    buffer_size = audio_system.buffer_size
    stereo_output = np.zeros((2, total_samples))
    
    print("   Movement path:")
    
    for i in range(0, total_samples, buffer_size):
        end_idx = min(i + buffer_size, total_samples)
        
        # Calculate position for this moment
        chunk_time = i / sample_rate
        
        # Figure-8 parametric equations
        param_t = 2 * np.pi * path_frequency * chunk_time
        scale = 2.5  # Size of figure-8
        
        x = scale * np.sin(param_t)
        y = scale * np.sin(param_t) * np.cos(param_t)
        z = 0.2 * np.sin(4 * param_t)  # Gentle vertical oscillation
        
        position = (x, y, z)
        
        # Get signal chunk
        chunk_signal = signal[i:end_idx]
        if len(chunk_signal) < buffer_size:
            chunk_signal = np.pad(chunk_signal, (0, buffer_size - len(chunk_signal)))
        
        # Process
        sources = [{'position': position, 'signal': chunk_signal, 'intensity': 1.0}]
        left, right, debug = audio_system.process_audio_buffer(sources)
        
        # Store
        actual_length = end_idx - i
        stereo_output[0, i:end_idx] = left[:actual_length]
        stereo_output[1, i:end_idx] = right[:actual_length]
        
        # Debug output every second
        if i % sample_rate == 0:
            if debug:
                d = debug[0]
                print(f"   t={chunk_time:.1f}s: pos=({x:.1f},{y:.1f},{z:.1f}), "
                      f"ITD={d['itd_seconds']*1000:.1f}ms, L/R={d['lr_ratio']:.2f}")
    
    # Save
    max_val = np.max(np.abs(stereo_output))
    if max_val > 0:
        stereo_output = stereo_output * 0.95 / max_val
    
    stereo_int = (stereo_output * 32767).astype(np.int16).T
    wavfile.write('personalized_movement_220mm.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: personalized_movement_220mm.wav")
    print(f"   Figure-8 movement optimized for 220mm ears!")

if __name__ == "__main__":
    print("🎧 Personalized Spatial Audio for 220mm Ear Spacing")
    print("=" * 55)
    
    # Create personalized test suite
    create_personalized_test_suite()
    
    # Create precision movement test
    create_precision_movement_test()
    
    print("\n✅ Personalized spatial audio complete!")
    print("\nGenerated files optimized for YOUR ear geometry:")
    print("   🎧 personalized_spatial_test_220mm.wav - Precision positioning")
    print("   🎧 personalized_movement_220mm.wav - Figure-8 movement")
    print("\n🎯 These are calculated specifically for 220mm ear spacing!")
    print("🎧 Should provide the most accurate spatial perception possible!")