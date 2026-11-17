#!/usr/bin/env python3
"""
Temporal Atmos Player
====================
A complete playback system for Temporal Atmos encoded files.
Decodes temporal coefficient patterns back to audible spatial audio.

This demonstrates the full codec pipeline:
1. Encode spatial scene → Temporal coefficients (storage format)
2. Decode temporal coefficients → Binaural audio (playback format)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import json
import pickle
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class TemporalAtmosFileFormat:
    """
    File format for storing Temporal Atmos encoded content.
    
    Format:
    - .tma files: Temporal coefficient data (JSON/pickle)
    - .wav files: Decoded binaural audio for standard playback
    """
    
    @staticmethod
    def save_temporal_stream(temporal_stream, metadata, filename):
        """Save temporal stream to .tma format."""
        
        # Convert complex temporal data to serializable format
        serializable_stream = {}
        for shell_n, pattern in temporal_stream.items():
            serializable_stream[str(shell_n)] = {
                'real': pattern.real.tolist(),
                'imag': pattern.imag.tolist(),
                'length': len(pattern)
            }
        
        # Create file package
        tma_data = {
            'format_version': '1.0',
            'metadata': metadata,
            'temporal_stream': serializable_stream,
            'codec_info': {
                'n_shells': len(temporal_stream),
                'temporal_resolution': len(list(temporal_stream.values())[0]),
                'encoding': 'temporal_coefficient_patterns'
            }
        }
        
        # Save as JSON for readability and cross-platform compatibility
        with open(filename, 'w') as f:
            json.dump(tma_data, f, indent=2)
        
        print(f"💾 Saved Temporal Atmos file: {filename}")
        print(f"   Format: TMA v{tma_data['format_version']}")
        print(f"   Shells: {tma_data['codec_info']['n_shells']}")
        print(f"   Resolution: {tma_data['codec_info']['temporal_resolution']} samples")
    
    @staticmethod
    def load_temporal_stream(filename):
        """Load temporal stream from .tma format."""
        
        with open(filename, 'r') as f:
            tma_data = json.load(f)
        
        # Reconstruct complex temporal patterns
        temporal_stream = {}
        for shell_str, pattern_data in tma_data['temporal_stream'].items():
            shell_n = int(shell_str)
            real_part = np.array(pattern_data['real'])
            imag_part = np.array(pattern_data['imag'])
            temporal_stream[shell_n] = real_part + 1j * imag_part
        
        metadata = tma_data['metadata']
        
        print(f"📂 Loaded Temporal Atmos file: {filename}")
        print(f"   Format: TMA v{tma_data['format_version']}")
        print(f"   Title: {metadata.get('title', 'Untitled')}")
        print(f"   Objects: {len(metadata.get('objects', []))}")
        
        return temporal_stream, metadata

class TemporalAtmosDecoder:
    """Real-time decoder for Temporal Atmos streams."""
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.shell_processor = TemporalShellProcessor()
        
        print(f"🎧 Temporal Atmos Decoder initialized")
        print(f"   Sample rate: {sample_rate}Hz")
    
    def decode_temporal_stream_to_binaural(self, temporal_stream, 
                                         listener_position=(0, 0, 0),
                                         head_rotation=0,
                                         ear_separation=0.22):
        """
        Decode temporal stream to binaural audio for standard playback.
        
        Args:
            temporal_stream: Dict of shell -> temporal patterns
            listener_position: (x, y, z) listener position
            head_rotation: Head rotation in radians
            ear_separation: Distance between ears in meters
            
        Returns:
            (left_channel, right_channel) as numpy arrays
        """
        
        print(f"🎧 Decoding to binaural audio")
        print(f"   Listener at: {listener_position}")
        print(f"   Head rotation: {head_rotation:.2f} rad ({np.degrees(head_rotation):.1f}°)")
        print(f"   Ear separation: {ear_separation*1000:.0f}mm")
        
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
        
        # Decode at each ear position
        left_signal = self._decode_at_position(temporal_stream, left_ear)
        right_signal = self._decode_at_position(temporal_stream, right_ear)
        
        # Apply temporal shell processing for character
        left_processed = self.shell_processor.process_through_shells(left_signal, self.sample_rate)
        right_processed = self.shell_processor.process_through_shells(right_signal, self.sample_rate)
        
        print(f"   Left peak: {np.max(np.abs(left_processed)):.3f}")
        print(f"   Right peak: {np.max(np.abs(right_processed)):.3f}")
        
        return left_processed, right_processed
    
    def _decode_at_position(self, temporal_stream, position):
        """Decode temporal stream at specific spatial position."""
        
        x, y, z = position
        
        # Convert to spherical coordinates  
        r = np.sqrt(x**2 + y**2 + z**2)
        if r < 1e-10:
            # At origin, return average of all shells
            signal_length = len(list(temporal_stream.values())[0])
            return np.zeros(signal_length)
            
        theta = np.arccos(np.clip(z / r, -1, 1))
        phi = np.arctan2(y, x)
        
        # Reconstruct signal by evaluating all temporal shells
        reconstructed = None
        
        for shell_n, shell_pattern in temporal_stream.items():
            # Calculate spatial weight for this shell at this position
            spatial_weight = self._calculate_spatial_weight(shell_n, r, theta, phi)
            
            # Weight the temporal pattern
            weighted_pattern = spatial_weight * shell_pattern
            
            if reconstructed is None:
                reconstructed = weighted_pattern.copy()
            else:
                reconstructed += weighted_pattern
        
        # Convert to real signal (take real part of complex temporal evolution)
        if reconstructed is not None:
            real_signal = np.real(reconstructed)
        else:
            real_signal = np.zeros(len(list(temporal_stream.values())[0]))
        
        return real_signal
    
    def _calculate_spatial_weight(self, shell_n, r, theta, phi):
        """Calculate how much each temporal shell contributes at this position."""
        
        # Distance-based shell contribution
        shell_radius = shell_n  # Each shell has characteristic radius
        distance_factor = np.exp(-abs(r - shell_radius) / shell_radius)
        
        # Angular contribution (simplified spherical harmonics)
        angular_factor = 1.0 + 0.5 * np.cos(shell_n * theta) * np.cos(shell_n * phi)
        
        # Overall weight
        weight = distance_factor * angular_factor / shell_n
        
        return weight
    
    def decode_to_surround(self, temporal_stream, speaker_positions):
        """Decode to arbitrary surround speaker configuration."""
        
        print(f"🔊 Decoding to {len(speaker_positions)} speaker surround")
        
        speaker_signals = []
        for i, speaker_pos in enumerate(speaker_positions):
            signal = self._decode_at_position(temporal_stream, speaker_pos)
            processed = self.shell_processor.process_through_shells(signal, self.sample_rate)
            speaker_signals.append(processed)
            
            print(f"   Speaker {i+1} at {speaker_pos}: peak={np.max(np.abs(processed)):.3f}")
        
        return speaker_signals

class TemporalAtmosPlayer:
    """Complete player system for Temporal Atmos content."""
    
    def __init__(self, sample_rate=48000):
        self.decoder = TemporalAtmosDecoder(sample_rate)
        self.sample_rate = sample_rate
        
        print(f"🎵 Temporal Atmos Player initialized")
    
    def play_tma_file(self, tma_filename, output_wav=None, 
                     listener_position=(0, 0, 0), 
                     head_rotation=0):
        """
        Load and decode a .tma file to playable binaural audio.
        
        Args:
            tma_filename: Path to .tma file
            output_wav: Optional output .wav filename
            listener_position: Where listener is positioned
            head_rotation: Head rotation in degrees
            
        Returns:
            (left, right) binaural audio channels
        """
        
        print(f"\n🎵 Playing Temporal Atmos file: {tma_filename}")
        
        # Load temporal stream
        temporal_stream, metadata = TemporalAtmosFileFormat.load_temporal_stream(tma_filename)
        
        # Convert head rotation to radians
        head_rotation_rad = np.radians(head_rotation)
        
        # Decode to binaural
        left_channel, right_channel = self.decoder.decode_temporal_stream_to_binaural(
            temporal_stream, 
            listener_position, 
            head_rotation_rad
        )
        
        # Save decoded audio if requested
        if output_wav:
            self._save_binaural_audio(left_channel, right_channel, output_wav)
        
        return left_channel, right_channel
    
    def _save_binaural_audio(self, left, right, filename):
        """Save binaural audio to standard WAV file."""
        
        # Combine channels
        stereo_audio = np.array([left, right])
        
        # Normalize
        max_val = np.max(np.abs(stereo_audio))
        if max_val > 0:
            stereo_audio = stereo_audio * 0.9 / max_val
        
        # Convert to 16-bit integer
        stereo_int = (stereo_audio * 32767).astype(np.int16).T
        
        # Save
        wavfile.write(filename, self.sample_rate, stereo_int)
        
        print(f"💾 Decoded audio saved: {filename}")
        print(f"   Standard WAV format - playable on any device!")

def create_sample_tma_file():
    """Create a sample .tma file to demonstrate the format."""
    
    print("🎬 Creating sample Temporal Atmos content")
    
    # Import our encoder
    from temporal_atmos_codec import TemporalAtmosCodec
    
    # Create sample spatial scene
    sample_rate = 48000
    duration = 2.0
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    spatial_scene = [
        {
            'name': 'Left_Bell',
            'position': (-2, 0, 0),
            'signal': np.sin(2 * np.pi * 400 * t) * np.exp(-t/2) * 0.6,  # Decaying bell
            'metadata': {'type': 'bell', 'frequency': 400, 'decay': 2.0}
        },
        {
            'name': 'Center_Drone',
            'position': (0, 1, 0),
            'signal': np.sin(2 * np.pi * 200 * t) * 0.4,  # Steady drone
            'metadata': {'type': 'drone', 'frequency': 200}
        },
        {
            'name': 'Right_Chirp',
            'position': (2, 0, 0),
            'signal': np.sin(2 * np.pi * (600 + 200 * t) * t) * 0.5,  # Rising chirp
            'metadata': {'type': 'chirp', 'start_freq': 600, 'end_freq': 800}
        },
        {
            'name': 'Overhead_Rain',
            'position': (0, 0, 3),
            'signal': np.random.normal(0, 0.1, len(t)) * np.sin(2 * np.pi * 1000 * t) * 0.3,  # Filtered noise
            'metadata': {'type': 'rain', 'center_freq': 1000}
        }
    ]
    
    # Initialize codec and encode
    codec = TemporalAtmosCodec(temporal_resolution=4096)  # Higher resolution for quality
    temporal_stream = codec.encode_scene(spatial_scene)
    
    # Create metadata
    metadata = {
        'title': 'Sample Temporal Atmos Scene',
        'description': 'Demonstration of spatial audio encoded as temporal patterns',
        'duration': duration,
        'sample_rate': sample_rate,
        'creation_date': '2025-06-03',
        'objects': [obj['metadata'] for obj in spatial_scene],
        'original_positions': [obj['position'] for obj in spatial_scene]
    }
    
    # Save as .tma file
    tma_filename = 'sample_temporal_atmos.tma'
    TemporalAtmosFileFormat.save_temporal_stream(temporal_stream, metadata, tma_filename)
    
    return tma_filename

def demonstrate_temporal_atmos_player():
    """Demonstrate the complete Temporal Atmos playback system."""
    
    print("🌊 Temporal Atmos Player Demonstration")
    print("=" * 50)
    
    # Create sample .tma file
    tma_file = create_sample_tma_file()
    
    # Initialize player
    player = TemporalAtmosPlayer()
    
    # Test different listening positions and orientations
    test_scenarios = [
        {
            'name': 'Center_Listener',
            'position': (0, 0, 0),
            'rotation': 0,
            'output': 'decoded_center_listener.wav'
        },
        {
            'name': 'Left_Position',
            'position': (-1, 0, 0),
            'rotation': 0,
            'output': 'decoded_left_position.wav'
        },
        {
            'name': 'Rotated_Head',
            'position': (0, 0, 0),
            'rotation': 45,  # 45 degrees
            'output': 'decoded_rotated_head.wav'
        }
    ]
    
    all_outputs = []
    
    for scenario in test_scenarios:
        print(f"\n🎧 Scenario: {scenario['name']}")
        
        # Decode TMA file to binaural audio
        left, right = player.play_tma_file(
            tma_file,
            output_wav=scenario['output'],
            listener_position=scenario['position'],
            head_rotation=scenario['rotation']
        )
        
        # Analyze the decoded audio
        left_energy = np.mean(left**2)
        right_energy = np.mean(right**2)
        lr_ratio = left_energy / (right_energy + 1e-12)
        
        print(f"   Decoded L/R energy ratio: {lr_ratio:.3f}")
        
        all_outputs.append(scenario['output'])
    
    print(f"\n✅ Temporal Atmos Player demonstration complete!")
    print(f"📂 Created files:")
    print(f"   📄 {tma_file} - Temporal Atmos encoded format")
    for output in all_outputs:
        print(f"   🎵 {output} - Decoded binaural audio (playable)")
    
    print(f"\n🎯 Key insight: The .tma file contains pure temporal patterns.")
    print(f"   The .wav files contain decoded spatial audio for normal playback.")
    print(f"   Space emerges during the decoding process!")
    
    return tma_file, all_outputs

if __name__ == "__main__":
    print("🌊 Temporal Atmos Player System")
    print("Complete codec pipeline: Encode → Store → Decode → Play")
    print("=" * 60)
    
    # Demonstrate the complete system
    tma_file, wav_outputs = demonstrate_temporal_atmos_player()
    
    print(f"\n🎵 Try playing the decoded .wav files:")
    for wav_file in wav_outputs:
        print(f"   🔊 {wav_file}")
    
    print(f"\n🌊 The {tma_file} contains the pure temporal encoding.")
    print(f"   This is the 'storage format' where space emerges from time!")