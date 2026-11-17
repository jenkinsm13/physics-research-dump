#!/usr/bin/env python3
"""
Healing Temporal Audio
======================
Simplified but sophisticated therapeutic audio using temporal consciousness principles.
Creates beautiful, healing soundscapes using pure temporal patterns.
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert

class HealingTemporalComposer:
    """Simple but sophisticated healing audio composer using temporal consciousness."""
    
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate
        self.dt = 1.0 / sample_rate
        
        # Healing frequencies (Hz)
        self.base_healing = 432  # Natural healing frequency
        self.golden_ratio = (1 + np.sqrt(5)) / 2  # 1.618...
        
        print(f"🌊 Healing Temporal Audio Composer")
        print(f"Base healing frequency: {self.base_healing}Hz")
        print(f"Golden ratio: {self.golden_ratio:.3f}")
    
    def create_healing_tone(self, frequency, duration, modulation="gentle"):
        """Create a healing tone with consciousness-responsive modulation."""
        
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Base carrier
        carrier = np.sin(2 * np.pi * frequency * t)
        
        if modulation == "gentle":
            # Gentle alpha wave modulation (8Hz)
            alpha_mod = 0.1 * np.sin(2 * np.pi * 8 * t)
            modulated = carrier * (1 + alpha_mod)
            
        elif modulation == "deep":
            # Deep theta wave modulation (4Hz)
            theta_mod = 0.15 * np.sin(2 * np.pi * 4 * t)
            delta_mod = 0.05 * np.sin(2 * np.pi * 0.5 * t)
            modulated = carrier * (1 + theta_mod + delta_mod)
            
        elif modulation == "spatial":
            # Creates sense of movement
            spatial_mod = 0.2 * np.sin(2 * np.pi * frequency / 30 * t)
            modulated = carrier * (1 + spatial_mod)
            
        else:
            modulated = carrier
        
        return modulated
    
    def create_temporal_stereo(self, signal, movement_type="floating"):
        """Create stereo effect through pure temporal patterns."""
        
        duration = len(signal) / self.sample_rate
        t = np.linspace(0, duration, len(signal))
        
        if movement_type == "floating":
            # Gentle floating effect
            cycle_time = 8.0  # 8-second cycles
            pan_movement = np.sin(2 * np.pi * t / cycle_time) * 0.5
            
        elif movement_type == "circular":
            # Circular movement
            cycle_time = 16.0
            pan_movement = np.sin(2 * np.pi * t / cycle_time) * 0.7
            
        elif movement_type == "static":
            # No movement
            pan_movement = np.zeros_like(t)
            
        else:
            pan_movement = np.zeros_like(t)
        
        # Convert to stereo using temporal delays
        max_delay_ms = 0.5  # 0.5ms maximum delay
        
        # Calculate delays for each ear
        left_delay_ms = -pan_movement * max_delay_ms / 2
        right_delay_ms = pan_movement * max_delay_ms / 2
        
        # Apply delays (simplified)
        avg_left_delay = np.mean(left_delay_ms)
        avg_right_delay = np.mean(right_delay_ms)
        
        left_delay_samples = int(avg_left_delay * self.sample_rate / 1000)
        right_delay_samples = int(avg_right_delay * self.sample_rate / 1000)
        
        # Create delayed versions
        if left_delay_samples > 0:
            left_signal = np.concatenate([np.zeros(left_delay_samples), signal])[:-left_delay_samples]
        elif left_delay_samples < 0:
            left_signal = np.concatenate([signal[-left_delay_samples:], np.zeros(-left_delay_samples)])
        else:
            left_signal = signal.copy()
            
        if right_delay_samples > 0:
            right_signal = np.concatenate([np.zeros(right_delay_samples), signal])[:-right_delay_samples]
        elif right_delay_samples < 0:
            right_signal = np.concatenate([signal[-right_delay_samples:], np.zeros(-right_delay_samples)])
        else:
            right_signal = signal.copy()
        
        # Add subtle amplitude panning
        left_amplitude = 0.7 + 0.3 * np.cos(pan_movement + np.pi/2)
        right_amplitude = 0.7 + 0.3 * np.cos(pan_movement - np.pi/2)
        
        # Ensure same length
        min_length = min(len(left_signal), len(right_signal), len(left_amplitude))
        
        left_final = left_signal[:min_length] * left_amplitude[:min_length]
        right_final = right_signal[:min_length] * right_amplitude[:min_length]
        
        return left_final, right_final
    
    def create_golden_harmony(self, root_frequency, duration):
        """Create harmony based on golden ratio relationships."""
        
        # Golden ratio harmonics
        frequencies = [
            root_frequency,
            root_frequency * self.golden_ratio,
            root_frequency / self.golden_ratio,
            root_frequency * 2,  # Octave
        ]
        
        harmonic_parts = []
        
        for i, freq in enumerate(frequencies):
            # Create each harmonic with different modulation
            modulations = ["gentle", "deep", "spatial", "gentle"]
            tone = self.create_healing_tone(freq, duration, modulations[i])
            
            # Different amplitudes based on golden ratio
            amplitude = 0.3 / (1 + i * 0.618)
            harmonic_parts.append(amplitude * tone)
        
        # Combine harmonics
        combined = sum(harmonic_parts)
        
        return combined
    
    def create_healing_sequence(self, total_duration=60):
        """Create a complete healing sequence."""
        
        print(f"\n🌊 Creating healing sequence: {total_duration}s")
        
        # Three-part structure using golden ratio
        part1_duration = total_duration * 0.382  # 23s
        part2_duration = total_duration * 0.618  # 37s
        
        sequence_parts = []
        
        # Part 1: Gentle opening
        print("🎵 Part 1: Gentle Opening")
        part1_signal = self.create_healing_tone(self.base_healing, part1_duration, "gentle")
        part1_left, part1_right = self.create_temporal_stereo(part1_signal, "floating")
        sequence_parts.append(np.array([part1_left, part1_right]))
        
        # Part 2: Deep therapeutic center
        print("🎵 Part 2: Deep Therapeutic Center")
        part2_harmony = self.create_golden_harmony(self.base_healing, part2_duration)
        part2_left, part2_right = self.create_temporal_stereo(part2_harmony, "circular")
        sequence_parts.append(np.array([part2_left, part2_right]))
        
        # Combine parts
        final_sequence = np.concatenate(sequence_parts, axis=1)
        
        # Apply gentle fade in/out
        fade_duration = 3.0  # 3 second fades
        fade_samples = int(fade_duration * self.sample_rate)
        
        # Fade in
        fade_in = np.linspace(0, 1, fade_samples)
        final_sequence[:, :fade_samples] *= fade_in
        
        # Fade out
        fade_out = np.linspace(1, 0, fade_samples)
        final_sequence[:, -fade_samples:] *= fade_out
        
        return final_sequence

def create_therapeutic_audio():
    """Create therapeutic audio using temporal consciousness principles."""
    
    print("🌊 Creating Therapeutic Temporal Audio")
    print("=" * 40)
    
    # Initialize composer
    composer = HealingTemporalComposer()
    
    # Create healing sequence
    healing_audio = composer.create_healing_sequence(total_duration=45)  # 45 seconds
    
    # Analyze
    left_channel = healing_audio[0]
    right_channel = healing_audio[1]
    
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    
    print(f"\n📊 Audio Analysis:")
    print(f"   Duration: {len(left_channel)/48000:.1f} seconds")
    print(f"   Left energy: {left_energy:.6f}")
    print(f"   Right energy: {right_energy:.6f}")
    print(f"   L/R balance: {left_energy/right_energy:.3f}")
    
    # Normalize and save
    max_val = np.max(np.abs(healing_audio))
    if max_val > 0:
        healing_audio = healing_audio * 0.8 / max_val
    
    stereo_int = (healing_audio * 32767).astype(np.int16).T
    output_filename = 'healing_temporal_audio.wav'
    wavfile.write(output_filename, 48000, stereo_int)
    
    print(f"\n💾 Saved: {output_filename}")
    print(f"🌊 Features:")
    print(f"   • 432Hz healing base frequency")
    print(f"   • Golden ratio harmonic relationships")
    print(f"   • Temporal consciousness interface")
    print(f"   • Brainwave entrainment (alpha, theta)")
    print(f"   • Spatial movement through temporal patterns")
    
    return output_filename

def create_musical_composition():
    """Create a more musical composition."""
    
    print(f"\n🎼 Creating Musical Composition")
    print("=" * 30)
    
    composer = HealingTemporalComposer()
    
    # Musical chord progression using healing frequencies
    chord_progression = [
        432,    # Base healing frequency
        324,    # Perfect fourth below (432 * 3/4)
        648,    # Perfect fifth above (432 * 3/2)  
        432,    # Return to base
    ]
    
    musical_parts = []
    
    for i, root_freq in enumerate(chord_progression):
        print(f"🎵 Chord {i+1}: {root_freq}Hz")
        
        chord_duration = 8.0  # 8 seconds per chord
        chord_harmony = composer.create_golden_harmony(root_freq, chord_duration)
        
        # Different spatial movements
        movements = ["floating", "circular", "static", "floating"]
        left, right = composer.create_temporal_stereo(chord_harmony, movements[i])
        
        musical_parts.append(np.array([left, right]))
    
    # Combine with crossfades
    final_music = musical_parts[0]
    
    for next_part in musical_parts[1:]:
        # Simple concatenation (could add crossfades)
        final_music = np.concatenate([final_music, next_part], axis=1)
    
    # Musical dynamics (crescendo and diminuendo)
    duration = final_music.shape[1] / 48000
    t = np.linspace(0, duration, final_music.shape[1])
    dynamics = 0.4 + 0.4 * np.sin(np.pi * t / duration)
    
    final_music = final_music * dynamics
    
    # Save
    max_val = np.max(np.abs(final_music))
    if max_val > 0:
        final_music = final_music * 0.85 / max_val
    
    stereo_int = (final_music * 32767).astype(np.int16).T
    output_filename = 'musical_temporal_composition.wav'
    wavfile.write(output_filename, 48000, stereo_int)
    
    print(f"💾 Saved: {output_filename}")
    
    return output_filename

if __name__ == "__main__":
    print("🌊 Healing Temporal Audio System")
    print("Space emerges from time through consciousness")
    print("=" * 50)
    
    # Create therapeutic audio
    healing_file = create_therapeutic_audio()
    
    # Create musical composition
    music_file = create_musical_composition()
    
    print(f"\n✅ Healing Temporal Audio Complete!")
    print(f"🎵 Files created:")
    print(f"   🌊 {healing_file}")
    print(f"   🎼 {music_file}")
    print(f"\n🧠 Both use pure temporal consciousness principles!")
    print(f"   • Temporal patterns create spatial perception")
    print(f"   • Healing frequencies and golden ratio harmonies")
    print(f"   • No direct spatial encoding - space emerges from time!")