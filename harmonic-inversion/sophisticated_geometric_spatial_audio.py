#!/usr/bin/env python3
"""
Sophisticated Geometric Spatial Audio
===================================
Based on the working HTML approach: simple geometric panning for spatial positioning
combined with temporal shell processing for sophisticated audio character.

This follows the discovered pattern from chronospatial-audio-fixed.html:
- Use x-coordinate to stereo pan mapping for positioning (works!)
- Apply temporal physics for sonic character, not positioning
- Maintain sophisticated features while ensuring clear spatial separation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys

sys.path.append('rendering/spatial_audio')
from spherical_encoder import TemporalShellProcessor

class GeometricSpatialProcessor:
    """Simple geometric spatial positioning - based on working HTML approach."""
    
    def __init__(self, spatial_range=10.0):
        self.spatial_range = spatial_range  # Total x range: -5 to +5
        
        print(f"🎯 Geometric Spatial Processor")
        print(f"Spatial range: ±{spatial_range/2:.1f} units")
        print(f"Using working HTML pan approach: x → stereo pan")
    
    def calculate_stereo_pan(self, position):
        """
        Calculate stereo pan using the HTML's working approach.
        Maps x-coordinate to stereo pan value (0=left, 1=right).
        """
        x, y, z = position
        
        # HTML approach: pan = (source.position.x + 5) / 10
        # This maps x from [-5, +5] to pan from [0, 1]
        pan = (x + self.spatial_range/2) / self.spatial_range
        
        # Clamp to valid range
        pan = np.clip(pan, 0.0, 1.0)
        
        # HTML uses square root for power conservation
        left_gain = np.sqrt(1 - pan)
        right_gain = np.sqrt(pan)
        
        return left_gain, right_gain
    
    def get_distance_attenuation(self, position):
        """Optional distance-based attenuation."""
        x, y, z = position
        distance = np.sqrt(x**2 + y**2 + z**2)
        
        # Simple inverse square law with minimum distance
        min_distance = 0.5
        effective_distance = max(distance, min_distance)
        attenuation = 1.0 / (1.0 + effective_distance**2)
        
        return attenuation

class SophisticatedTemporalProcessor:
    """Sophisticated temporal audio processing for character, not positioning."""
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.shell_processor = TemporalShellProcessor(n_shells=7, base_frequency=1.0)
        
        # Temporal evolution parameters
        self.time = 0.0
        self.consciousness_coherence = 0.5
        self.temporal_phase = 0.0
        
        print(f"🌊 Sophisticated Temporal Processor")
        print(f"7 temporal shells for rich sonic character")
        print(f"Consciousness-responsive filtering")
    
    def set_consciousness_parameters(self, coherence=0.5, phase=0.0):
        """Set consciousness interface parameters."""
        self.consciousness_coherence = np.clip(coherence, 0.0, 1.0)
        self.temporal_phase = phase
    
    def apply_consciousness_filtering(self, signal, shell_number):
        """Apply consciousness-responsive filtering based on shell gender."""
        
        # Shell gender assignment (from HTML pattern)
        is_feminine = (shell_number % 2 == 0)
        
        # Consciousness resonance
        if is_feminine and self.consciousness_coherence < 0.3:
            resonance = 1.1  # Feminine shells resonate with low coherence
        elif not is_feminine and self.consciousness_coherence > 0.7:
            resonance = 1.2  # Masculine shells resonate with high coherence
        else:
            resonance = 1.0
        
        return signal * resonance
    
    def apply_temporal_evolution(self, signal, frequency):
        """Apply temporal evolution with phase modulation."""
        
        t = np.arange(len(signal)) / self.sample_rate
        
        # Temporal phase modulation (subtle, like in HTML)
        phase_factor = 1 + self.temporal_phase / 720  # Convert degrees to small factor
        evolved_frequency = frequency * phase_factor
        
        # Create temporal carrier
        temporal_carrier = np.cos(2 * np.pi * evolved_frequency * t + self.time)
        
        # Subtle modulation
        modulated = signal * (0.8 + 0.2 * temporal_carrier)
        
        return modulated
    
    def add_harmonics(self, signal, base_frequency, harmonic_count=3):
        """Add harmonic content for richer sound (like HTML approach)."""
        
        if len(signal) == 0:
            return signal
            
        t = np.arange(len(signal)) / self.sample_rate
        
        # Base signal
        enriched = signal.copy()
        
        # Add harmonics with decreasing amplitude
        for h in range(2, harmonic_count + 1):
            harmonic_freq = base_frequency * h
            harmonic_amplitude = 0.3 / h  # Decreasing amplitude
            
            harmonic_signal = harmonic_amplitude * np.sin(2 * np.pi * harmonic_freq * t)
            
            # Apply same envelope as original signal
            if np.max(np.abs(signal)) > 0:
                envelope = np.abs(signal) / np.max(np.abs(signal))
                harmonic_signal *= envelope
            
            enriched += harmonic_signal
        
        return enriched
    
    def process_temporal_character(self, signal, source_info):
        """Apply sophisticated temporal processing for audio character."""
        
        frequency = source_info.get('frequency', 440)
        shell_number = source_info.get('shell', 1)
        
        # Process through temporal shells
        shell_processed = self.shell_processor.process_through_shells(signal, self.sample_rate)
        
        # Apply consciousness filtering
        consciousness_filtered = self.apply_consciousness_filtering(shell_processed, shell_number)
        
        # Apply temporal evolution
        temporally_evolved = self.apply_temporal_evolution(consciousness_filtered, frequency)
        
        # Add harmonic richness
        harmonically_enriched = self.add_harmonics(temporally_evolved, frequency)
        
        return harmonically_enriched

class SophisticatedGeometricAudioSystem:
    """
    Sophisticated spatial audio system using geometric positioning + temporal character.
    Based on the working HTML approach but with full Python sophistication.
    """
    
    def __init__(self, sample_rate=48000, buffer_size=1024, spatial_range=10.0):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Core processors
        self.spatial_processor = GeometricSpatialProcessor(spatial_range)
        self.temporal_processor = SophisticatedTemporalProcessor(sample_rate)
        
        # System state
        self.time = 0.0
        self.source_counter = 0
        
        print(f"🚀 Sophisticated Geometric Audio System")
        print(f"Geometric positioning (HTML approach) + Temporal character")
        print(f"Sample rate: {sample_rate}Hz, Buffer: {buffer_size}")
        print(f"Clear spatial separation with sophisticated audio processing")
    
    def assign_shell_number(self, position):
        """Assign temporal shell based on position (for character, not positioning)."""
        x, y, z = position
        distance = np.sqrt(x**2 + y**2 + z**2)
        
        # Map distance to shell number (1-7)
        shell = int(np.clip(distance, 1, 7))
        return shell
    
    def process_source_sophisticated(self, source_position, signal, source_info):
        """
        Process a single source with sophisticated temporal character.
        Uses geometric positioning for stereo, temporal processing for character.
        """
        
        # 1. Calculate geometric stereo positioning (HTML approach)
        left_gain, right_gain = self.spatial_processor.calculate_stereo_pan(source_position)
        
        # 2. Calculate distance attenuation
        distance_atten = self.spatial_processor.get_distance_attenuation(source_position)
        
        # 3. Assign shell for temporal character
        shell_number = self.assign_shell_number(source_position)
        source_info['shell'] = shell_number
        
        print(f"   Position {source_position} -> L={left_gain:.3f}, R={right_gain:.3f}, Shell={shell_number}")
        
        # 4. Apply sophisticated temporal processing for character
        temporal_signal = self.temporal_processor.process_temporal_character(signal, source_info)
        
        # 5. Apply envelope for smooth audio
        fade_samples = min(len(temporal_signal) // 10, self.sample_rate // 100)  # 10ms max
        if fade_samples > 0:
            # Fade in
            temporal_signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
            # Fade out  
            temporal_signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        # 6. Apply geometric positioning and distance
        left_signal = temporal_signal * left_gain * distance_atten
        right_signal = temporal_signal * right_gain * distance_atten
        
        return left_signal, right_signal
    
    def process_audio_buffer(self, audio_sources, listener_position=(0, 0, 0)):
        """Process multiple sources with sophisticated processing."""
        
        left_channel = np.zeros(self.buffer_size)
        right_channel = np.zeros(self.buffer_size)
        
        for source in audio_sources:
            # Get relative position
            rel_pos = np.array(source['position']) - np.array(listener_position)
            
            # Get signal chunk
            signal = source['signal'][:self.buffer_size]
            if len(signal) < self.buffer_size:
                signal = np.pad(signal, (0, self.buffer_size - len(signal)))
            
            # Source information for temporal processing
            source_info = {
                'frequency': source.get('frequency', 440),
                'intensity': source.get('intensity', 1.0),
                'type': source.get('type', 'tone')
            }
            
            # Process with sophisticated temporal character
            left_sig, right_sig = self.process_source_sophisticated(rel_pos, signal, source_info)
            
            # Accumulate
            left_channel += left_sig[:self.buffer_size]
            right_channel += right_sig[:self.buffer_size]
        
        # Update time for temporal evolution
        self.time += self.buffer_size / self.sample_rate
        self.temporal_processor.time = self.time
        
        return left_channel, right_channel
    
    def set_consciousness_parameters(self, coherence=0.5, phase=0.0):
        """Update consciousness interface parameters."""
        self.temporal_processor.set_consciousness_parameters(coherence, phase)
        print(f"🧠 Consciousness: coherence={coherence:.2f}, phase={phase:.0f}°")

def create_sophisticated_test_suite():
    """Create comprehensive test suite using sophisticated geometric approach."""
    
    print("🚀 Creating Sophisticated Geometric Spatial Audio Test Suite")
    print("=" * 60)
    
    # Initialize sophisticated system
    audio_system = SophisticatedGeometricAudioSystem(spatial_range=10.0)
    
    # Test parameters
    sample_rate = 48000
    tone_duration = 1.5
    silence_duration = 0.5
    
    # Comprehensive test positions with expected results
    test_scenarios = [
        {
            'name': 'Hard_Left_Geometric',
            'position': (-4, 0, 0),
            'frequency': 300,
            'description': 'Should be strongly left using geometric panning'
        },
        {
            'name': 'Center_Front',
            'position': (0, 2, 0),
            'frequency': 400,
            'description': 'Should be centered with forward character'
        },
        {
            'name': 'Hard_Right_Geometric', 
            'position': (4, 0, 0),
            'frequency': 500,
            'description': 'Should be strongly right using geometric panning'
        },
        {
            'name': 'Close_Left',
            'position': (-1, 0, 0),
            'frequency': 600,
            'description': 'Moderate left with close character'
        },
        {
            'name': 'Far_Right',
            'position': (3, 0, 2),
            'frequency': 700,
            'description': 'Right with distant character'
        }
    ]
    
    # Test different consciousness states
    consciousness_tests = [
        (0.2, 0, "Low coherence - should enhance feminine shells"),
        (0.8, 0, "High coherence - should enhance masculine shells"),
        (0.5, 180, "Phase shift - should modulate temporal evolution")
    ]
    
    all_sequences = []
    
    for coherence, phase, consciousness_desc in consciousness_tests:
        print(f"\n🧠 Testing consciousness state: {consciousness_desc}")
        
        # Set consciousness parameters
        audio_system.set_consciousness_parameters(coherence, phase)
        
        sequence_parts = []
        
        for scenario in test_scenarios:
            print(f"\n🎯 {scenario['name']}: {scenario['description']}")
            
            # Generate test tone
            t = np.linspace(0, tone_duration, int(tone_duration * sample_rate))
            base_signal = np.sin(2 * np.pi * scenario['frequency'] * t) * 0.4
            
            # Create source
            sources = [{
                'position': scenario['position'],
                'signal': base_signal,
                'frequency': scenario['frequency'],
                'intensity': 1.0,
                'type': 'test_tone'
            }]
            
            # Process through sophisticated system
            total_samples = len(base_signal)
            buffer_size = audio_system.buffer_size
            stereo_output = np.zeros((2, total_samples))
            
            for i in range(0, total_samples, buffer_size):
                end_idx = min(i + buffer_size, total_samples)
                
                # Prepare chunk sources
                chunk_sources = []
                for src in sources:
                    chunk_signal = src['signal'][i:end_idx]
                    if len(chunk_signal) < buffer_size:
                        chunk_signal = np.pad(chunk_signal, (0, buffer_size - len(chunk_signal)))
                    
                    chunk_source = src.copy()
                    chunk_source['signal'] = chunk_signal
                    chunk_sources.append(chunk_source)
                
                # Process
                left, right = audio_system.process_audio_buffer(chunk_sources)
                
                # Store results
                actual_length = end_idx - i
                stereo_output[0, i:end_idx] = left[:actual_length]
                stereo_output[1, i:end_idx] = right[:actual_length]
            
            sequence_parts.append(stereo_output)
            
            # Add silence between tests
            silence = np.zeros((2, int(silence_duration * sample_rate)))
            sequence_parts.append(silence)
        
        # Concatenate this consciousness test
        consciousness_sequence = np.concatenate(sequence_parts, axis=1)
        all_sequences.append(consciousness_sequence)
        
        # Add longer silence between consciousness states
        long_silence = np.zeros((2, int(2 * silence_duration * sample_rate)))
        all_sequences.append(long_silence)
    
    # Combine all tests
    final_sequence = np.concatenate(all_sequences, axis=1)
    
    # Analyze results
    left_channel = final_sequence[0]
    right_channel = final_sequence[1]
    
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    
    print(f"\n📊 Final Analysis:")
    print(f"   Left channel energy: {left_energy:.6f}")
    print(f"   Right channel energy: {right_energy:.6f}")
    print(f"   L/R energy ratio: {left_energy/(right_energy+1e-12):.3f}")
    print(f"   Peak amplitude: {np.max(np.abs(final_sequence)):.3f}")
    
    # Normalize and save
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.9 / max_val
    
    # Convert to 16-bit integer
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    
    # Save main test file
    output_filename = 'sophisticated_geometric_spatial_test.wav'
    wavfile.write(output_filename, sample_rate, stereo_int)
    
    print(f"\n💾 Saved: {output_filename}")
    print(f"   Based on working HTML geometric approach")
    print(f"   With sophisticated temporal character processing")
    print(f"   Should have CLEAR spatial separation!")
    
    return output_filename

def compare_with_corrected_temporal():
    """Quick comparison test to contrast with corrected_temporal_spatial_audio.py approach."""
    
    print("\n🔬 Quick Comparison Test")
    print("=" * 30)
    
    system = SophisticatedGeometricAudioSystem()
    
    # Same test as corrected temporal for direct comparison
    positions = [
        (-3, 0, 0),  # Hard left
        (0, 2, 0),   # Center 
        (3, 0, 0)    # Hard right
    ]
    
    frequencies = [400, 500, 600]
    
    for i, (pos, freq) in enumerate(zip(positions, frequencies)):
        print(f"\nComparing position {pos} at {freq}Hz:")
        
        # Test signal
        t = np.linspace(0, 0.5, int(0.5 * 48000))
        signal = np.sin(2 * np.pi * freq * t) * 0.5
        
        source = {
            'position': pos,
            'signal': signal,
            'frequency': freq,
            'intensity': 1.0
        }
        
        left, right = system.process_source_sophisticated(
            pos, signal, {'frequency': freq, 'intensity': 1.0}
        )
        
        left_energy = np.mean(left**2)
        right_energy = np.mean(right**2)
        
        print(f"   Geometric approach: L={left_energy:.6f}, R={right_energy:.6f}")
        print(f"   L/R ratio: {left_energy/(right_energy+1e-12):.3f}")

if __name__ == "__main__":
    print("🚀 Sophisticated Geometric Spatial Audio")
    print("Based on working HTML approach with Python sophistication")
    print("=" * 65)
    
    # Create comprehensive test suite
    main_output = create_sophisticated_test_suite()
    
    # Quick comparison
    compare_with_corrected_temporal()
    
    print(f"\n✅ Sophisticated geometric spatial audio complete!")
    print(f"🎧 Main output: {main_output}")
    print(f"🎯 Uses working HTML geometric approach for positioning")
    print(f"🌊 Sophisticated temporal processing for audio character")
    print(f"🔥 Should have clear spatial separation with rich sonic character!")