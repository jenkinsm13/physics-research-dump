#!/usr/bin/env python3
"""
Practical Guide to Using the Temporal Spatial Audio System
=========================================================
This script shows how to actually generate, process, and output 
audible audio using the temporal framework.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import resample
import os
import sys

# Import the spatial audio system
sys.path.append('rendering/spatial_audio')
from spherical_encoder import ChronodynamicAudioSystem, SphericalHarmonicAudioEncoder, TemporalShellProcessor

class PracticalTemporalAudio:
    """Practical interface for generating audible temporal audio."""
    
    def __init__(self, sample_rate=48000, buffer_size=4096):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Initialize the temporal audio system
        self.audio_system = ChronodynamicAudioSystem(sample_rate, buffer_size)
        
        print("🎵 Temporal Audio System Initialized")
        print(f"Sample Rate: {sample_rate} Hz")
        print(f"Buffer Size: {buffer_size} samples")
        print(f"Duration per buffer: {buffer_size/sample_rate:.3f} seconds")
    
    def generate_test_signals(self, duration=2.0):
        """Generate various test signals for spatial audio."""
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        signals = {
            'sine_440': np.sin(2 * np.pi * 440 * t),  # A4 note
            'sine_880': np.sin(2 * np.pi * 880 * t),  # A5 note (octave)
            'chirp': np.sin(2 * np.pi * (100 + 400 * t) * t),  # Frequency sweep
            'noise': np.random.normal(0, 0.1, len(t)),  # White noise
            'piano_chord': (np.sin(2 * np.pi * 261.63 * t) +   # C4
                           np.sin(2 * np.pi * 329.63 * t) +   # E4
                           np.sin(2 * np.pi * 392.00 * t)),   # G4
            'pulse_train': np.where(t % 0.5 < 0.05, 1.0, 0.0),  # Pulse every 0.5s
        }
        
        # Normalize all signals
        for name, signal in signals.items():
            signals[name] = signal / (np.max(np.abs(signal)) + 1e-8)
        
        return signals
    
    def create_3d_audio_scene(self, signals, duration=2.0):
        """Create a 3D audio scene with multiple positioned sources."""
        
        # Define source positions in 3D space (x, y, z in meters)
        source_configs = [
            {'position': (2, 0, 0), 'signal_name': 'sine_440', 'intensity': 1.0},      # Right side
            {'position': (-2, 0, 0), 'signal_name': 'sine_880', 'intensity': 0.8},     # Left side  
            {'position': (0, 2, 0), 'signal_name': 'chirp', 'intensity': 0.6},         # Front
            {'position': (0, -2, 0), 'signal_name': 'noise', 'intensity': 0.3},        # Behind
            {'position': (0, 0, 2), 'signal_name': 'piano_chord', 'intensity': 0.7},   # Above
            {'position': (1, 1, 1), 'signal_name': 'pulse_train', 'intensity': 0.5},   # Diagonal
        ]
        
        # Process the entire scene in chunks
        total_samples = int(duration * self.sample_rate)
        num_buffers = (total_samples + self.buffer_size - 1) // self.buffer_size
        
        stereo_output = np.zeros((2, total_samples))  # [left, right channels]
        
        print(f"\n🎛️  Processing {num_buffers} buffers for {duration:.1f}s audio scene...")
        
        for buffer_idx in range(num_buffers):
            start_sample = buffer_idx * self.buffer_size
            end_sample = min(start_sample + self.buffer_size, total_samples)
            buffer_length = end_sample - start_sample
            
            # Prepare sources for this buffer
            buffer_sources = []
            for config in source_configs:
                signal = signals[config['signal_name']]
                
                # Extract buffer portion
                buffer_signal = signal[start_sample:end_sample]
                
                # Pad if necessary
                if len(buffer_signal) < self.buffer_size:
                    buffer_signal = np.pad(buffer_signal, 
                                         (0, self.buffer_size - len(buffer_signal)), 
                                         'constant')
                
                buffer_sources.append({
                    'position': config['position'],
                    'signal': buffer_signal,
                    'intensity': config['intensity']
                })
            
            # Process through temporal audio system
            left_channel, right_channel = self.audio_system.process_audio_buffer(buffer_sources)
            
            # Store in output
            stereo_output[0, start_sample:end_sample] = left_channel[:buffer_length]
            stereo_output[1, start_sample:end_sample] = right_channel[:buffer_length]
            
            if buffer_idx % 10 == 0:
                print(f"  Buffer {buffer_idx+1}/{num_buffers} processed")
        
        return stereo_output
    
    def save_audio(self, stereo_data, filename, normalize=True):
        """Save stereo audio data to WAV file."""
        
        if normalize:
            # Normalize to prevent clipping
            max_val = np.max(np.abs(stereo_data))
            if max_val > 0:
                stereo_data = stereo_data * 0.95 / max_val
        
        # Convert to 16-bit integer format
        audio_data = (stereo_data * 32767).astype(np.int16).T  # Shape: (samples, channels)
        
        # Save to file
        wavfile.write(filename, self.sample_rate, audio_data)
        print(f"💾 Audio saved to: {filename}")
        
        # Print file info
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        duration = len(audio_data) / self.sample_rate
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   File size: {file_size:.2f} MB")
        print(f"   Sample rate: {self.sample_rate} Hz")
        print(f"   Channels: {audio_data.shape[1]}")
    
    def analyze_output(self, stereo_data):
        """Analyze the spatial audio output."""
        left_channel = stereo_data[0]
        right_channel = stereo_data[1]
        
        print(f"\n📊 Audio Analysis:")
        print(f"   Left channel peak: {np.max(np.abs(left_channel)):.3f}")
        print(f"   Right channel peak: {np.max(np.abs(right_channel)):.3f}")
        print(f"   Stereo correlation: {np.corrcoef(left_channel, right_channel)[0,1]:.3f}")
        
        # RMS levels
        left_rms = np.sqrt(np.mean(left_channel**2))
        right_rms = np.sqrt(np.mean(right_channel**2))
        print(f"   Left RMS: {left_rms:.3f}")
        print(f"   Right RMS: {right_rms:.3f}")
        
        # Dynamic range
        left_dr = 20 * np.log10(np.max(np.abs(left_channel)) / (left_rms + 1e-8))
        right_dr = 20 * np.log10(np.max(np.abs(right_channel)) / (right_rms + 1e-8))
        print(f"   Left dynamic range: {left_dr:.1f} dB")
        print(f"   Right dynamic range: {right_dr:.1f} dB")
    
    def visualize_audio(self, stereo_data, signals_info=None):
        """Create visualizations of the temporal audio output."""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Time domain plots
        time_axis = np.linspace(0, len(stereo_data[0]) / self.sample_rate, len(stereo_data[0]))
        
        # Left channel waveform
        axes[0, 0].plot(time_axis, stereo_data[0], 'b-', alpha=0.7, linewidth=0.5)
        axes[0, 0].set_title('Left Channel Waveform')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Right channel waveform  
        axes[0, 1].plot(time_axis, stereo_data[1], 'r-', alpha=0.7, linewidth=0.5)
        axes[0, 1].set_title('Right Channel Waveform')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Amplitude')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Frequency domain analysis
        left_fft = np.abs(np.fft.fft(stereo_data[0]))
        right_fft = np.abs(np.fft.fft(stereo_data[1]))
        freq_axis = np.fft.fftfreq(len(stereo_data[0]), 1/self.sample_rate)
        
        # Only plot positive frequencies up to Nyquist
        nyquist_idx = len(freq_axis) // 2
        freq_axis = freq_axis[:nyquist_idx]
        left_fft = left_fft[:nyquist_idx]
        right_fft = right_fft[:nyquist_idx]
        
        axes[1, 0].semilogy(freq_axis, left_fft, 'b-', alpha=0.7, label='Left')
        axes[1, 0].semilogy(freq_axis, right_fft, 'r-', alpha=0.7, label='Right')
        axes[1, 0].set_title('Frequency Spectrum')
        axes[1, 0].set_xlabel('Frequency (Hz)')
        axes[1, 0].set_ylabel('Magnitude')
        axes[1, 0].set_xlim(0, min(5000, self.sample_rate//2))  # Show up to 5kHz
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Stereo field visualization
        axes[1, 1].scatter(stereo_data[0][::100], stereo_data[1][::100], 
                          alpha=0.6, s=1, c=time_axis[::100], cmap='viridis')
        axes[1, 1].set_title('Stereo Field (L vs R)')
        axes[1, 1].set_xlabel('Left Channel')
        axes[1, 1].set_ylabel('Right Channel')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Temporal Spatial Audio Analysis', fontsize=16)
        plt.tight_layout()
        plt.show()
    
    def demonstrate_temporal_effects(self):
        """Demonstrate unique temporal audio effects."""
        
        print(f"\n🌀 Demonstrating Temporal Audio Effects...")
        
        # Generate test signal
        duration = 3.0
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        base_signal = np.sin(2 * np.pi * 440 * t) * np.exp(-t/2)  # Decaying sine
        
        # Create moving source
        positions = []
        for i, time in enumerate(t[::self.buffer_size]):
            # Circular motion
            angle = 2 * np.pi * time / duration
            radius = 2.0
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = 0.5 * np.sin(4 * angle)  # Vertical oscillation
            positions.append((x, y, z))
        
        # Process moving source
        output_data = np.zeros((2, len(t)))
        
        for i, pos in enumerate(positions):
            start_idx = i * self.buffer_size
            end_idx = min(start_idx + self.buffer_size, len(t))
            
            if start_idx >= len(t):
                break
                
            buffer_signal = base_signal[start_idx:end_idx]
            if len(buffer_signal) < self.buffer_size:
                buffer_signal = np.pad(buffer_signal, (0, self.buffer_size - len(buffer_signal)))
            
            sources = [{'position': pos, 'signal': buffer_signal, 'intensity': 1.0}]
            left, right = self.audio_system.process_audio_buffer(sources)
            
            actual_length = end_idx - start_idx
            output_data[0, start_idx:end_idx] = left[:actual_length]
            output_data[1, start_idx:end_idx] = right[:actual_length]
        
        return output_data
    
    def run_full_demo(self):
        """Run complete demonstration of temporal spatial audio."""
        
        print("🚀 Starting Complete Temporal Audio Demonstration")
        print("=" * 60)
        
        # 1. Generate test signals
        print("\n1️⃣  Generating test signals...")
        signals = self.generate_test_signals(duration=4.0)
        print(f"   Generated {len(signals)} test signals")
        
        # 2. Create 3D audio scene
        print("\n2️⃣  Creating 3D audio scene...")
        stereo_output = self.create_3d_audio_scene(signals, duration=4.0)
        
        # 3. Analyze output
        self.analyze_output(stereo_output)
        
        # 4. Save to file
        print("\n3️⃣  Saving audio files...")
        self.save_audio(stereo_output, 'temporal_spatial_audio_demo.wav')
        
        # 5. Demonstrate temporal effects
        print("\n4️⃣  Demonstrating temporal effects...")
        moving_audio = self.demonstrate_temporal_effects()
        self.save_audio(moving_audio, 'temporal_moving_source.wav')
        
        # 6. Visualize results
        print("\n5️⃣  Creating visualizations...")
        self.visualize_audio(stereo_output)
        
        # 7. Show soundfield visualization
        print("\n6️⃣  Visualizing sound field...")
        # Create simple test sources for visualization
        test_sources = [
            {'position': (2, 0, 0), 'intensity': 1.0},
            {'position': (-1, 1, 0), 'intensity': 0.8},
            {'position': (0, -2, 1), 'intensity': 0.6}
        ]
        self.audio_system.visualize_soundfield(test_sources)
        
        print("\n✅ Demo complete! Check the generated WAV files:")
        print("   - temporal_spatial_audio_demo.wav (3D positioned sources)")
        print("   - temporal_moving_source.wav (moving source demo)")
        print("\n🎧 Play these files in any audio player to hear temporal spatial audio!")

def simple_usage_example():
    """Simple example showing basic usage."""
    print("🎵 Simple Temporal Audio Example")
    print("-" * 40)
    
    # Create audio system
    temporal_audio = PracticalTemporalAudio(sample_rate=44100, buffer_size=1024)
    
    # Generate a simple stereo test
    duration = 2.0
    t = np.linspace(0, duration, int(duration * 44100))
    
    # Create two different tones for left and right positioning
    tone_left = np.sin(2 * np.pi * 400 * t)  # 400 Hz
    tone_right = np.sin(2 * np.pi * 600 * t)  # 600 Hz
    
    # Position sources in space
    sources = [
        {'position': (-2, 0, 0), 'signal': tone_left, 'intensity': 1.0},   # Left
        {'position': (2, 0, 0), 'signal': tone_right, 'intensity': 1.0},   # Right
    ]
    
    # Process (note: need to chunk for the system)
    stereo_out = np.zeros((2, len(t)))
    buffer_size = 1024
    
    for i in range(0, len(t), buffer_size):
        end_idx = min(i + buffer_size, len(t))
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
        
        left, right = temporal_audio.audio_system.process_audio_buffer(chunk_sources)
        actual_length = end_idx - i
        stereo_out[0, i:end_idx] = left[:actual_length]
        stereo_out[1, i:end_idx] = right[:actual_length]
    
    # Save result
    temporal_audio.save_audio(stereo_out, 'simple_temporal_test.wav')
    print("✅ Simple test saved as 'simple_temporal_test.wav'")

if __name__ == "__main__":
    print("🌊 Temporal Spatial Audio System")
    print("Running simple demonstration...")
    
    # Run simple example by default for non-interactive environment
    simple_usage_example()