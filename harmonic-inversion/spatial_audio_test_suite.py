#!/usr/bin/env python3
"""
3D Spatial Audio Test Suite
===========================
Creates sequential audio samples positioned all around 3D space to test
the temporal spatial audio system's positioning accuracy.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

# Import the temporal audio system
sys.path.append('rendering/spatial_audio')
from spherical_encoder import ChronodynamicAudioSystem

class SpatialAudioTestSuite:
    """Test suite for evaluating 3D spatial audio positioning."""
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.buffer_size = 2048  # Larger buffer for cleaner processing
        
        # Initialize temporal audio system
        self.audio_system = ChronodynamicAudioSystem(sample_rate, self.buffer_size)
        
        print("🎯 3D Spatial Audio Test Suite Initialized")
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Buffer Size: {self.buffer_size} samples")
        
    def generate_test_tone(self, frequency=800, duration=0.8, fade_time=0.05):
        """Generate a test tone with fade in/out to avoid clicks."""
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Generate tone
        tone = np.sin(2 * np.pi * frequency * t)
        
        # Apply fade in/out
        fade_samples = int(fade_time * self.sample_rate)
        
        # Fade in
        tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
        
        # Fade out
        tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return tone
    
    def generate_voice_announcement(self, position_name, frequency=600, duration=1.2):
        """Generate a distinctive tone sequence for position announcements."""
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Create a pattern that sounds like speech rhythm
        pattern = np.zeros_like(t)
        
        # Add several tone bursts at different frequencies
        burst_times = [0.0, 0.3, 0.6, 0.9]
        burst_freqs = [frequency, frequency * 1.25, frequency * 0.8, frequency]
        
        for start_time, freq in zip(burst_times, burst_freqs):
            start_idx = int(start_time * self.sample_rate)
            burst_duration = 0.15
            end_idx = int((start_time + burst_duration) * self.sample_rate)
            
            if end_idx <= len(t):
                burst_t = t[start_idx:end_idx] - start_time
                burst = np.sin(2 * np.pi * freq * burst_t)
                
                # Apply envelope
                envelope = np.exp(-burst_t * 8)
                pattern[start_idx:end_idx] = burst * envelope
        
        return pattern
    
    def create_test_positions(self):
        """Create a comprehensive set of test positions around the listener."""
        
        positions = {}
        
        # 1. Cardinal directions at 2m distance
        positions["Front"] = (0, 2, 0)
        positions["Back"] = (0, -2, 0)
        positions["Left"] = (-2, 0, 0)
        positions["Right"] = (2, 0, 0)
        positions["Above"] = (0, 0, 2)
        positions["Below"] = (0, 0, -1)
        
        # 2. Diagonal positions
        positions["Front-Left"] = (-1.5, 1.5, 0)
        positions["Front-Right"] = (1.5, 1.5, 0)
        positions["Back-Left"] = (-1.5, -1.5, 0)
        positions["Back-Right"] = (1.5, -1.5, 0)
        
        # 3. Elevated positions
        positions["Front-Above"] = (0, 2, 1.5)
        positions["Back-Above"] = (0, -2, 1.5)
        positions["Left-Above"] = (-2, 0, 1.5)
        positions["Right-Above"] = (2, 0, 1.5)
        
        # 4. Close and far positions
        positions["Very-Close-Front"] = (0, 0.5, 0)
        positions["Far-Front"] = (0, 5, 0)
        positions["Very-Close-Left"] = (-0.5, 0, 0)
        positions["Far-Left"] = (-5, 0, 0)
        
        # 5. Circular sweep positions (for movement test)
        circle_positions = {}
        for i in range(8):
            angle = i * np.pi / 4  # Every 45 degrees
            radius = 3.0
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            circle_positions[f"Circle-{i+1}"] = (x, y, 0)
        
        positions.update(circle_positions)
        
        # 6. Sphere positions (for 3D sweep)
        sphere_positions = {}
        phi_angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]  # Elevation
        theta_angles = [0, np.pi/2, np.pi, 3*np.pi/2]  # Azimuth
        
        for i, phi in enumerate(phi_angles):
            for j, theta in enumerate(theta_angles):
                radius = 2.5
                x = radius * np.sin(phi) * np.cos(theta)
                y = radius * np.sin(phi) * np.sin(theta)
                z = radius * np.cos(phi)
                sphere_positions[f"Sphere-{i}-{j}"] = (x, y, z)
        
        positions.update(sphere_positions)
        
        return positions
    
    def process_positioned_audio(self, audio_signal, position, intensity=1.0):
        """Process audio through the temporal spatial system."""
        
        # Split into buffers
        total_samples = len(audio_signal)
        stereo_output = np.zeros((2, total_samples))
        
        for i in range(0, total_samples, self.buffer_size):
            end_idx = min(i + self.buffer_size, total_samples)
            
            # Get audio chunk
            chunk = audio_signal[i:end_idx]
            
            # Pad if necessary
            if len(chunk) < self.buffer_size:
                chunk = np.pad(chunk, (0, self.buffer_size - len(chunk)))
            
            # Create source
            sources = [{'position': position, 'signal': chunk, 'intensity': intensity}]
            
            # Process through temporal shells
            left, right = self.audio_system.process_audio_buffer(sources)
            
            # Store results
            actual_length = end_idx - i
            stereo_output[0, i:end_idx] = left[:actual_length]
            stereo_output[1, i:end_idx] = right[:actual_length]
        
        return stereo_output
    
    def create_position_test_sequence(self, test_type="cardinal"):
        """Create a test sequence with audio at different positions."""
        
        positions = self.create_test_positions()
        
        if test_type == "cardinal":
            # Just the main 6 directions
            selected_positions = {
                k: v for k, v in positions.items() 
                if k in ["Front", "Back", "Left", "Right", "Above", "Below"]
            }
        elif test_type == "diagonal":
            # Diagonal positions
            selected_positions = {
                k: v for k, v in positions.items() 
                if "Front-" in k or "Back-" in k
            }
        elif test_type == "circle":
            # Circular sweep
            selected_positions = {
                k: v for k, v in positions.items() 
                if "Circle-" in k
            }
        elif test_type == "sphere":
            # Full 3D sphere
            selected_positions = {
                k: v for k, v in positions.items() 
                if "Sphere-" in k
            }
        elif test_type == "distance":
            # Near and far
            selected_positions = {
                k: v for k, v in positions.items() 
                if "Close" in k or "Far" in k or k in ["Front", "Left"]
            }
        else:
            # All positions
            selected_positions = positions
        
        print(f"\n🎯 Creating {test_type} test with {len(selected_positions)} positions:")
        for name, pos in selected_positions.items():
            print(f"   {name}: {pos}")
        
        # Build sequence
        silence_duration = 0.3
        tone_duration = 0.8
        sequence_parts = []
        position_info = []
        
        for i, (name, position) in enumerate(selected_positions.items()):
            print(f"Processing {name} at {position}...")
            
            # Generate announcement tone (unique frequency per position)
            frequency = 600 + (i * 50)  # Different frequency for each position
            
            if "announcement" in test_type.lower():
                audio_signal = self.generate_voice_announcement(name, frequency)
            else:
                audio_signal = self.generate_test_tone(frequency, tone_duration)
            
            # Process through spatial system
            stereo_audio = self.process_positioned_audio(audio_signal, position)
            
            # Add silence before
            silence_samples = int(silence_duration * self.sample_rate)
            silence = np.zeros((2, silence_samples))
            
            # Combine
            sequence_parts.append(silence)
            sequence_parts.append(stereo_audio)
            
            # Track position info
            start_time = len(np.concatenate([p[0] for p in sequence_parts])) / self.sample_rate
            position_info.append({
                'name': name,
                'position': position,
                'start_time': start_time,
                'frequency': frequency
            })
        
        # Concatenate all parts
        final_sequence = np.concatenate(sequence_parts, axis=1)
        
        return final_sequence, position_info
    
    def create_movement_test(self):
        """Create a test with a source moving through space."""
        
        print(f"\n🌀 Creating movement test...")
        
        # Parameters
        duration = 8.0
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Generate a continuous tone
        frequency = 800
        audio_signal = np.sin(2 * np.pi * frequency * t) * 0.7
        
        # Apply gentle amplitude modulation to make movement more noticeable
        modulation = 1 + 0.3 * np.sin(2 * np.pi * 2 * t)  # 2 Hz modulation
        audio_signal *= modulation
        
        # Define circular path
        radius = 3.0
        angular_velocity = 2 * np.pi / duration  # One revolution
        
        # Process in chunks with different positions
        stereo_output = np.zeros((2, len(audio_signal)))
        
        for i in range(0, len(audio_signal), self.buffer_size):
            end_idx = min(i + self.buffer_size, len(audio_signal))
            
            # Calculate position for middle of this buffer
            mid_time = (i + self.buffer_size // 2) / self.sample_rate
            angle = angular_velocity * mid_time
            
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = 0.5 * np.sin(4 * angle)  # Gentle vertical oscillation
            
            position = (x, y, z)
            
            # Get audio chunk
            chunk = audio_signal[i:end_idx]
            if len(chunk) < self.buffer_size:
                chunk = np.pad(chunk, (0, self.buffer_size - len(chunk)))
            
            # Process
            sources = [{'position': position, 'signal': chunk, 'intensity': 1.0}]
            left, right = self.audio_system.process_audio_buffer(sources)
            
            # Store
            actual_length = end_idx - i
            stereo_output[0, i:end_idx] = left[:actual_length]
            stereo_output[1, i:end_idx] = right[:actual_length]
        
        return stereo_output
    
    def visualize_test_positions(self, position_info):
        """Create 3D visualization of test positions."""
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Extract positions
        positions = [info['position'] for info in position_info]
        names = [info['name'] for info in position_info]
        frequencies = [info['frequency'] for info in position_info]
        
        if not positions:
            print("No positions to visualize")
            return
        
        x_coords = [pos[0] for pos in positions]
        y_coords = [pos[1] for pos in positions]
        z_coords = [pos[2] for pos in positions]
        
        # Create scatter plot with frequency-based colors
        scatter = ax.scatter(x_coords, y_coords, z_coords, 
                           c=frequencies, s=100, cmap='viridis', alpha=0.7)
        
        # Add labels
        for i, (pos, name) in enumerate(zip(positions, names)):
            ax.text(pos[0], pos[1], pos[2], f'{i+1}', fontsize=8)
        
        # Mark listener at origin
        ax.scatter([0], [0], [0], c='red', s=200, marker='^', label='Listener')
        
        # Styling
        ax.set_xlabel('X (Left ← → Right)')
        ax.set_ylabel('Y (Back ← → Front)')
        ax.set_zlabel('Z (Below ← → Above)')
        ax.set_title('3D Spatial Audio Test Positions')
        
        # Set equal aspect ratio
        max_range = max(max(abs(min(x_coords)), abs(max(x_coords))),
                       max(abs(min(y_coords)), abs(max(y_coords))),
                       max(abs(min(z_coords)), abs(max(z_coords))))
        ax.set_xlim(-max_range*1.1, max_range*1.1)
        ax.set_ylim(-max_range*1.1, max_range*1.1)
        ax.set_zlim(-max_range*1.1, max_range*1.1)
        
        plt.colorbar(scatter, label='Test Tone Frequency (Hz)')
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        # Print position list
        print(f"\n📍 Test Position Summary:")
        print(f"{'#':<3} {'Name':<15} {'Position':<20} {'Frequency':<10}")
        print("-" * 55)
        for i, info in enumerate(position_info):
            pos_str = f"({info['position'][0]:.1f}, {info['position'][1]:.1f}, {info['position'][2]:.1f})"
            print(f"{i+1:<3} {info['name']:<15} {pos_str:<20} {info['frequency']:<10.0f}")
    
    def save_test_audio(self, audio_data, filename, position_info=None):
        """Save test audio with metadata."""
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data * 0.95 / max_val
        
        # Convert to 16-bit
        audio_int = (audio_data * 32767).astype(np.int16).T
        
        # Save WAV file
        from scipy.io import wavfile
        wavfile.write(filename, self.sample_rate, audio_int)
        
        print(f"💾 Saved: {filename}")
        print(f"   Duration: {len(audio_int) / self.sample_rate:.1f} seconds")
        print(f"   Size: {os.path.getsize(filename) / (1024*1024):.1f} MB")
        
        # Save position info as text file
        if position_info:
            info_filename = filename.replace('.wav', '_positions.txt')
            with open(info_filename, 'w') as f:
                f.write("3D Spatial Audio Test - Position Information\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"{'Time':<8} {'Name':<15} {'Position':<20} {'Frequency':<10}\n")
                f.write("-" * 60 + "\n")
                
                for info in position_info:
                    pos_str = f"({info['position'][0]:.1f}, {info['position'][1]:.1f}, {info['position'][2]:.1f})"
                    f.write(f"{info['start_time']:<8.1f} {info['name']:<15} {pos_str:<20} {info['frequency']:<10.0f}\n")
                
                f.write(f"\nTotal positions: {len(position_info)}\n")
                f.write(f"Instructions: Put on headphones and listen for each tone's position in 3D space.\n")
            
            print(f"📝 Position info saved: {info_filename}")
    
    def run_all_tests(self):
        """Run comprehensive spatial audio test suite."""
        
        print("🚀 Running Complete 3D Spatial Audio Test Suite")
        print("=" * 60)
        
        # Test 1: Cardinal directions
        print(f"\n1️⃣  CARDINAL DIRECTIONS TEST")
        cardinal_audio, cardinal_info = self.create_position_test_sequence("cardinal")
        self.save_test_audio(cardinal_audio, "test_1_cardinal_directions.wav", cardinal_info)
        
        # Test 2: Diagonal positions
        print(f"\n2️⃣  DIAGONAL POSITIONS TEST")
        diagonal_audio, diagonal_info = self.create_position_test_sequence("diagonal")
        self.save_test_audio(diagonal_audio, "test_2_diagonal_positions.wav", diagonal_info)
        
        # Test 3: Distance test
        print(f"\n3️⃣  DISTANCE PERCEPTION TEST")
        distance_audio, distance_info = self.create_position_test_sequence("distance")
        self.save_test_audio(distance_audio, "test_3_distance_perception.wav", distance_info)
        
        # Test 4: Circular sweep
        print(f"\n4️⃣  CIRCULAR SWEEP TEST")
        circle_audio, circle_info = self.create_position_test_sequence("circle")
        self.save_test_audio(circle_audio, "test_4_circular_sweep.wav", circle_info)
        
        # Test 5: Movement test
        print(f"\n5️⃣  CONTINUOUS MOVEMENT TEST")
        movement_audio = self.create_movement_test()
        self.save_test_audio(movement_audio, "test_5_continuous_movement.wav")
        
        # Test 6: Full sphere (if requested)
        print(f"\n6️⃣  FULL SPHERE TEST (Comprehensive)")
        sphere_audio, sphere_info = self.create_position_test_sequence("sphere")
        self.save_test_audio(sphere_audio, "test_6_full_sphere.wav", sphere_info)
        
        # Visualize the first test
        print(f"\n📊 Creating visualization...")
        self.visualize_test_positions(cardinal_info)
        
        print(f"\n✅ All tests complete!")
        print(f"\nGenerated files:")
        print(f"   🎧 test_1_cardinal_directions.wav - Basic 6 directions")
        print(f"   🎧 test_2_diagonal_positions.wav - Corner positions")
        print(f"   🎧 test_3_distance_perception.wav - Near vs far")
        print(f"   🎧 test_4_circular_sweep.wav - Around the listener")
        print(f"   🎧 test_5_continuous_movement.wav - Moving source")
        print(f"   🎧 test_6_full_sphere.wav - Complete 3D sphere")
        print(f"\n🎯 Put on headphones and test your 3D spatial perception!")

def run_quick_test():
    """Run just the essential cardinal directions test."""
    
    print("🎯 Quick 3D Spatial Audio Test")
    print("-" * 40)
    
    test_suite = SpatialAudioTestSuite()
    
    # Just cardinal directions
    audio_data, position_info = test_suite.create_position_test_sequence("cardinal")
    test_suite.save_test_audio(audio_data, "quick_spatial_test.wav", position_info)
    test_suite.visualize_test_positions(position_info)
    
    print("\n✅ Quick test complete!")
    print("🎧 Play 'quick_spatial_test.wav' with headphones to test 3D positioning")

if __name__ == "__main__":
    print("🌊 3D Spatial Audio Test Suite")
    print("Running full comprehensive test suite...")
    
    # Run full test suite
    test_suite = SpatialAudioTestSuite()
    test_suite.run_all_tests()