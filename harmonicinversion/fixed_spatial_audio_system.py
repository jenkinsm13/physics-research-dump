#!/usr/bin/env python3
"""
Fixed Spatial Audio System
==========================
Creates proper stereo separation using direct geometric calculations
combined with temporal processing.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class FixedSpatialAudioSystem:
    """Fixed spatial audio system with proper stereo separation."""
    
    def __init__(self, sample_rate=48000, buffer_size=1024):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Temporal shell processor for the unique temporal characteristics
        self.shell_processor = TemporalShellProcessor()
        
        # Listener/ear geometry
        self.head_width = 0.18  # 18cm between ears
        self.ear_positions = {
            'left': (-self.head_width/2, 0, 0),
            'right': (self.head_width/2, 0, 0)
        }
        
        self.time = 0
        
        print("🔧 Fixed Spatial Audio System Initialized")
        print(f"Head width: {self.head_width*100:.0f}cm")
        
    def calculate_distance_attenuation(self, source_pos, ear_pos):
        """Calculate distance-based attenuation."""
        distance = np.linalg.norm(np.array(source_pos) - np.array(ear_pos))
        
        # Avoid division by zero
        distance = max(distance, 0.01)
        
        # Inverse square law with minimum distance
        attenuation = 1.0 / (1.0 + distance**2)
        
        return attenuation, distance
    
    def calculate_directional_gain(self, source_pos, ear_pos):
        """Calculate directional gain based on angle."""
        
        # Vector from ear to source
        to_source = np.array(source_pos) - np.array(ear_pos)
        distance = np.linalg.norm(to_source)
        
        if distance < 0.001:
            return 1.0
        
        # Normalize
        to_source = to_source / distance
        
        # Ear direction (pointing outward from head)
        if ear_pos[0] < 0:  # Left ear
            ear_direction = np.array([-1, 0, 0])
        else:  # Right ear
            ear_direction = np.array([1, 0, 0])
        
        # Cosine of angle between ear direction and source
        cos_angle = np.dot(ear_direction, to_source)
        
        # Convert to gain (0.1 to 1.0 range)
        gain = 0.1 + 0.9 * max(0, cos_angle)
        
        return gain
    
    def calculate_time_delay(self, source_pos, ear_pos):
        """Calculate time delay between ears (ITD - Interaural Time Difference)."""
        
        distance = np.linalg.norm(np.array(source_pos) - np.array(ear_pos))
        
        # Speed of sound (in temporal units)
        c_sound = 343.0  # m/s
        
        delay_seconds = distance / c_sound
        delay_samples = int(delay_seconds * self.sample_rate)
        
        return delay_samples
    
    def apply_head_shadow(self, source_pos, ear_pos):
        """Apply head shadow effect (ILD - Interaural Level Difference)."""
        
        # Vector from center of head to source
        head_center = (0, 0, 0)
        to_source = np.array(source_pos) - np.array(head_center)
        to_ear = np.array(ear_pos) - np.array(head_center)
        
        # Check if source is on opposite side of head from ear
        source_side = np.sign(to_source[0])  # Left (-) or right (+)
        ear_side = np.sign(to_ear[0])
        
        if source_side != ear_side:
            # Source is on opposite side - apply head shadow
            shadow_factor = 0.3  # 70% attenuation
        else:
            # Source is on same side
            shadow_factor = 1.0
        
        return shadow_factor
    
    def process_source_for_ear(self, source, ear_name, ear_pos):
        """Process a single source for one ear."""
        
        source_pos = source['position']
        signal = source['signal']
        intensity = source['intensity']
        
        # Calculate spatial effects
        attenuation, distance = self.calculate_distance_attenuation(source_pos, ear_pos)
        directional_gain = self.calculate_directional_gain(source_pos, ear_pos)
        head_shadow = self.apply_head_shadow(source_pos, ear_pos)
        time_delay = self.calculate_time_delay(source_pos, ear_pos)
        
        # Combine all effects
        total_gain = intensity * attenuation * directional_gain * head_shadow
        
        # Apply time delay
        delayed_signal = np.zeros_like(signal)
        if time_delay > 0 and time_delay < len(signal):
            delayed_signal[time_delay:] = signal[:-time_delay]
        else:
            delayed_signal = signal
        
        # Apply gain
        processed_signal = delayed_signal * total_gain
        
        # Process through temporal shells for unique character
        temporal_processed = self.shell_processor.process_through_shells(
            processed_signal, self.sample_rate
        )
        
        # Debug info
        debug_info = {
            'ear': ear_name,
            'distance': distance,
            'attenuation': attenuation,
            'directional_gain': directional_gain,
            'head_shadow': head_shadow,
            'time_delay_samples': time_delay,
            'total_gain': total_gain
        }
        
        return temporal_processed, debug_info
    
    def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
        """Process audio sources into stereo output."""
        
        left_channel = np.zeros(self.buffer_size)
        right_channel = np.zeros(self.buffer_size)
        
        debug_info = []
        
        for source in audio_sources:
            # Adjust source position relative to listener
            rel_pos = np.array(source['position']) - np.array(listener_position)
            source_adjusted = {
                'position': rel_pos,
                'signal': source['signal'][:self.buffer_size],
                'intensity': source['intensity']
            }
            
            # Process for left ear
            left_ear_pos = self.ear_positions['left']
            left_signal, left_debug = self.process_source_for_ear(
                source_adjusted, 'left', left_ear_pos
            )
            
            # Process for right ear
            right_ear_pos = self.ear_positions['right']
            right_signal, right_debug = self.process_source_for_ear(
                source_adjusted, 'right', right_ear_pos
            )
            
            # Add to channels
            left_channel += left_signal[:self.buffer_size]
            right_channel += right_signal[:self.buffer_size]
            
            debug_info.append({
                'source_position': source['position'],
                'left': left_debug,
                'right': right_debug
            })
        
        self.time += self.buffer_size / self.sample_rate
        
        return left_channel, right_channel, debug_info

def create_fixed_test_suite():
    """Create test suite with the fixed spatial audio system."""
    
    print("\n🚀 Creating Fixed Spatial Audio Test Suite")
    print("=" * 50)
    
    # Initialize fixed system
    fixed_system = FixedSpatialAudioSystem()
    
    # Test parameters
    sample_rate = 48000
    tone_duration = 1.0
    silence_duration = 0.5
    
    # Test positions with expected results
    test_positions = [
        ("Hard_Left", (-3, 0, 0), "Should be strongly left"),
        ("Hard_Right", (3, 0, 0), "Should be strongly right"),
        ("Front", (0, 2, 0), "Should be centered"),
        ("Back", (0, -2, 0), "Should be centered"),
        ("Close_Left", (-0.5, 0, 0), "Should be slightly left"),
        ("Far_Left", (-10, 0, 0), "Should be left but quieter"),
    ]
    
    # Build test sequence
    sequence_parts = []
    
    for name, position, description in test_positions:
        print(f"\n📍 Processing {name} at {position}")
        print(f"   Expected: {description}")
        
        # Generate test tone
        t = np.linspace(0, tone_duration, int(tone_duration * sample_rate))
        frequency = 600 + hash(name) % 400  # Unique frequency per position
        test_signal = np.sin(2 * np.pi * frequency * t) * 0.7
        
        # Create source
        sources = [{
            'position': position,
            'signal': test_signal,
            'intensity': 1.0
        }]
        
        # Process through fixed system
        total_samples = len(test_signal)
        buffer_size = fixed_system.buffer_size
        stereo_output = np.zeros((2, total_samples))
        
        for i in range(0, total_samples, buffer_size):
            end_idx = min(i + buffer_size, total_samples)
            
            # Prepare chunk
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
            
            # Process
            left, right, debug = fixed_system.process_audio_buffer(chunk_sources)
            
            # Store results
            actual_length = end_idx - i
            stereo_output[0, i:end_idx] = left[:actual_length]
            stereo_output[1, i:end_idx] = right[:actual_length]
            
            # Print debug for first chunk
            if i == 0 and debug:
                d = debug[0]
                print(f"   Left gain: {d['left']['total_gain']:.4f}")
                print(f"   Right gain: {d['right']['total_gain']:.4f}")
                print(f"   L/R ratio: {d['left']['total_gain']/(d['right']['total_gain']+1e-10):.3f}")
        
        # Add silence
        silence_samples = int(silence_duration * sample_rate)
        silence = np.zeros((2, silence_samples))
        
        # Add to sequence
        sequence_parts.append(stereo_output)
        sequence_parts.append(silence)
    
    # Concatenate all parts
    final_sequence = np.concatenate(sequence_parts, axis=1)
    
    # Normalize and save
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.95 / max_val
    
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    wavfile.write('fixed_spatial_test.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: fixed_spatial_test.wav")
    print(f"   Duration: {len(stereo_int) / sample_rate:.1f} seconds")
    print(f"   This should have CLEAR spatial separation!")

def create_moving_source_test():
    """Create a test with a source moving around the listener."""
    
    print("\n🌀 Creating Moving Source Test")
    print("=" * 30)
    
    fixed_system = FixedSpatialAudioSystem()
    
    # Parameters
    duration = 6.0
    sample_rate = 48000
    total_samples = int(duration * sample_rate)
    
    # Generate continuous tone
    t = np.linspace(0, duration, total_samples)
    frequency = 800
    signal = np.sin(2 * np.pi * frequency * t) * 0.6
    
    # Circular motion parameters
    radius = 2.0
    angular_velocity = 2 * np.pi / duration  # One revolution
    
    # Process in chunks
    buffer_size = fixed_system.buffer_size
    stereo_output = np.zeros((2, total_samples))
    
    for i in range(0, total_samples, buffer_size):
        end_idx = min(i + buffer_size, total_samples)
        
        # Calculate position for this chunk
        chunk_time = i / sample_rate
        angle = angular_velocity * chunk_time
        
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.3 * np.sin(4 * angle)  # Gentle vertical motion
        
        position = (x, y, z)
        
        # Get signal chunk
        chunk_signal = signal[i:end_idx]
        if len(chunk_signal) < buffer_size:
            chunk_signal = np.pad(chunk_signal, (0, buffer_size - len(chunk_signal)))
        
        # Create source
        sources = [{
            'position': position,
            'signal': chunk_signal,
            'intensity': 1.0
        }]
        
        # Process
        left, right, debug = fixed_system.process_audio_buffer(sources)
        
        # Store
        actual_length = end_idx - i
        stereo_output[0, i:end_idx] = left[:actual_length]
        stereo_output[1, i:end_idx] = right[:actual_length]
        
        # Debug every 2 seconds
        if i % (2 * sample_rate) == 0:
            if debug:
                d = debug[0]
                print(f"   t={chunk_time:.1f}s: pos=({x:.1f},{y:.1f},{z:.1f}), "
                      f"L/R={d['left']['total_gain']/(d['right']['total_gain']+1e-10):.2f}")
    
    # Save
    max_val = np.max(np.abs(stereo_output))
    if max_val > 0:
        stereo_output = stereo_output * 0.95 / max_val
    
    stereo_int = (stereo_output * 32767).astype(np.int16).T
    wavfile.write('fixed_moving_source.wav', sample_rate, stereo_int)
    
    print(f"\n💾 Saved: fixed_moving_source.wav")
    print(f"   Source moves in circle around you!")

if __name__ == "__main__":
    print("🔧 Fixed Spatial Audio System")
    print("=" * 40)
    
    # Create test suite
    create_fixed_test_suite()
    
    # Create moving source test
    create_moving_source_test()
    
    print("\n✅ Fixed spatial audio tests complete!")
    print("\nGenerated files:")
    print("   🎧 fixed_spatial_test.wav - Multiple positioned sources")
    print("   🎧 fixed_moving_source.wav - Source moving in circle")
    print("\n🎯 These should have OBVIOUS stereo separation!")
    print("🎧 Put on headphones and test immediately!")