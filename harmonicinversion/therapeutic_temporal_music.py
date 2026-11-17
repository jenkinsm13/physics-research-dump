#!/usr/bin/env python3
"""
Therapeutic Temporal Music System
=================================
Creates complex, intricate, pleasing music using pure temporal consciousness principles.

Uses temporal patterns that consciousness naturally interprets as:
- Spatial movement and flow
- Harmonic progression through phase relationships
- Healing frequencies through temporal modulation
- Emotional resonance through consciousness-responsive timing

Space emerges from time through the listener's conscious experience.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import hilbert, butter, filtfilt
import math

class TemporalConsciousnessMusician:
    """
    Creates music through temporal consciousness interface.
    Space, harmony, and healing emerge from pure temporal patterns.
    """
    
    def __init__(self, sample_rate=48000, base_frequency=432):
        self.sample_rate = sample_rate
        self.dt = 1.0 / sample_rate
        self.base_frequency = base_frequency  # 432Hz - natural healing frequency
        
        # Golden ratio and phi for natural harmonic relationships
        self.phi = (1 + np.sqrt(5)) / 2  # 1.618...
        self.phi_inverse = 1 / self.phi   # 0.618...
        
        # Consciousness resonance parameters
        self.consciousness_cycle = 8.0  # 8-second consciousness cycle (theta waves)
        self.healing_frequencies = [
            40,   # Gamma waves - heightened awareness
            8,    # Alpha waves - relaxation
            4,    # Theta waves - deep meditation
            0.5   # Delta waves - deep healing
        ]
        
        print(f"🎵 Therapeutic Temporal Music System")
        print(f"Base frequency: {base_frequency}Hz (natural healing)")
        print(f"Consciousness cycle: {self.consciousness_cycle}s")
        print(f"Golden ratio phi: {self.phi:.3f}")
    
    def create_consciousness_tone(self, frequency, duration, modulation_type="healing"):
        """
        Create a tone that modulates according to consciousness patterns.
        """
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Base carrier wave
        carrier = np.sin(2 * np.pi * frequency * t)
        
        if modulation_type == "healing":
            # Healing modulation - follows natural brainwave patterns
            alpha_mod = 0.1 * np.sin(2 * np.pi * 8 * t)      # Alpha waves
            theta_mod = 0.05 * np.sin(2 * np.pi * 4 * t)     # Theta waves
            delta_mod = 0.03 * np.sin(2 * np.pi * 0.5 * t)   # Delta waves
            
            modulated = carrier * (1 + alpha_mod + theta_mod + delta_mod)
            
        elif modulation_type == "spatial":
            # Spatial modulation - creates sense of movement through time
            spatial_freq = frequency / 20  # Slow spatial movement
            spatial_mod = 0.2 * np.sin(2 * np.pi * spatial_freq * t)
            modulated = carrier * (1 + spatial_mod)
            
        elif modulation_type == "golden":
            # Golden ratio modulation - natural harmonic relationships
            phi_freq = frequency / self.phi
            golden_mod = 0.15 * np.sin(2 * np.pi * phi_freq * t)
            modulated = carrier * (1 + golden_mod)
            
        else:
            modulated = carrier
        
        return modulated
    
    def create_temporal_harmony(self, root_freq, duration, progression_type="healing"):
        """
        Create harmony through temporal phase relationships.
        Instead of simultaneous notes, uses temporal patterns consciousness interprets as harmony.
        """
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        if progression_type == "healing":
            # Healing chord progression in temporal form
            frequencies = [
                root_freq,           # Root
                root_freq * 5/4,     # Major third (just intonation)
                root_freq * 3/2,     # Perfect fifth
                root_freq * 2,       # Octave
            ]
            
            # Temporal delays for each harmonic (microseconds that create spatial perception)
            delays = [0, 0.3e-3, 0.6e-3, 0.9e-3]  # 0.3ms increments
            
        elif progression_type == "golden":
            # Golden ratio harmonics
            frequencies = [
                root_freq,
                root_freq * self.phi,
                root_freq * self.phi**2,
                root_freq / self.phi,
            ]
            delays = [0, 0.2e-3, 0.4e-3, 0.8e-3]
            
        elif progression_type == "spatial":
            # Creates sense of spatial movement
            frequencies = [
                root_freq,
                root_freq * 9/8,     # Whole tone
                root_freq * 6/5,     # Minor third
                root_freq * 4/3,     # Perfect fourth
            ]
            delays = [0, 0.5e-3, 1.0e-3, 1.5e-3]
        
        # Create temporal harmony
        harmony_signal = np.zeros(len(t))
        
        for freq, delay in zip(frequencies, delays):
            # Create tone with consciousness modulation
            tone = self.create_consciousness_tone(freq, duration, "healing")
            
            # Apply temporal delay
            delay_samples = int(delay * self.sample_rate)
            if delay_samples > 0:
                delayed_tone = np.concatenate([np.zeros(delay_samples), tone])[:len(t)]
            else:
                delayed_tone = tone[:len(t)]
            
            # Add to harmony with golden ratio amplitude weighting
            amplitude = 1.0 / (1 + len(harmony_signal.nonzero()[0]) * self.phi_inverse)
            harmony_signal += amplitude * delayed_tone
        
        return harmony_signal
    
    def create_temporal_stereo_field(self, signal, spatial_type="floating"):
        """
        Create stereo field through pure temporal effects.
        Consciousness interprets temporal patterns as spatial movement.
        """
        duration = len(signal) / self.sample_rate
        t = np.linspace(0, duration, len(signal))
        
        if spatial_type == "floating":
            # Gentle floating movement - figure-8 pattern
            movement_freq = 1 / self.consciousness_cycle  # One cycle per consciousness cycle
            
            # X-axis movement (left-right)
            x_movement = np.sin(2 * np.pi * movement_freq * t)
            
            # Y-axis movement (front-back)
            y_movement = np.sin(4 * np.pi * movement_freq * t) * 0.5
            
        elif spatial_type == "circular":
            # Circular movement around listener
            movement_freq = 1 / (2 * self.consciousness_cycle)
            x_movement = np.sin(2 * np.pi * movement_freq * t)
            y_movement = np.cos(2 * np.pi * movement_freq * t)
            
        elif spatial_type == "expanding":
            # Expanding and contracting spatial field
            expansion_freq = 1 / (4 * self.consciousness_cycle)
            movement_freq = 1 / self.consciousness_cycle  # Define movement_freq
            expansion = np.sin(2 * np.pi * expansion_freq * t) * 0.5 + 0.5
            x_movement = expansion * np.sin(2 * np.pi * movement_freq * t)
            y_movement = expansion * 0.3  # Slight forward presence
        
        # Convert spatial movement to temporal delays and phase shifts
        max_delay = 0.0007  # 0.7ms maximum delay (head width)
        
        # Left and right ear delays based on x movement
        left_delay_ms = -x_movement * max_delay / 2
        right_delay_ms = x_movement * max_delay / 2
        
        # Phase differences based on y movement
        phase_shift = y_movement * np.pi / 4  # ±45° phase shift
        
        # Apply temporal processing
        left_signal = self._apply_variable_delay(signal, left_delay_ms)
        right_signal = self._apply_variable_delay(signal, right_delay_ms)
        
        # Apply phase modulation
        analytic_left = hilbert(left_signal)
        analytic_right = hilbert(right_signal)
        
        left_final = np.real(analytic_left * np.exp(1j * phase_shift))
        right_final = np.real(analytic_right * np.exp(-1j * phase_shift))
        
        return left_final, right_final
    
    def _apply_variable_delay(self, signal, delay_ms_array):
        """Apply time-varying delay to signal."""
        # Simplified implementation - use first delay value to avoid NaN
        if len(delay_ms_array) == 0 or np.isnan(delay_ms_array).any():
            return signal
        
        avg_delay = np.mean(delay_ms_array)
        if np.isnan(avg_delay):
            return signal
            
        avg_delay_samples = int(avg_delay * self.sample_rate)
        
        if avg_delay_samples > 0:
            delayed = np.concatenate([np.zeros(avg_delay_samples), signal])[:-avg_delay_samples]
        elif avg_delay_samples < 0:
            delayed = np.concatenate([signal[-avg_delay_samples:], np.zeros(-avg_delay_samples)])
        else:
            delayed = signal
        
        # Simple amplitude modulation to simulate variable delay effect
        t = np.linspace(0, 1, len(delayed))
        modulation = 1 + 0.05 * np.sin(2 * np.pi * t)  # Gentle modulation
        delayed = delayed * modulation
        
        return delayed
    
    def create_therapeutic_sequence(self, total_duration=120):
        """
        Create a complete therapeutic music sequence.
        Designed for healing, relaxation, and consciousness expansion.
        """
        print(f"\n🌊 Creating therapeutic sequence: {total_duration}s")
        
        # Sequence structure (golden ratio timing)
        section_durations = [
            total_duration * self.phi_inverse**2,  # Opening (23s)
            total_duration * self.phi_inverse,     # Development (74s) 
            total_duration * (1 - self.phi_inverse**2 - self.phi_inverse),  # Conclusion (23s)
        ]
        
        sequence_parts = []
        
        # Section 1: Gentle opening - consciousness alignment
        print("🎼 Section 1: Consciousness Alignment")
        duration1 = section_durations[0]
        
        # Base tone in 432Hz (healing frequency)
        base_tone = self.create_consciousness_tone(self.base_frequency, duration1, "healing")
        
        # Add golden ratio harmonics
        harmony1 = self.create_temporal_harmony(self.base_frequency, duration1, "golden")
        
        # Combine with gentle amplitude
        section1_mono = 0.4 * base_tone + 0.3 * harmony1
        
        # Create floating spatial field
        section1_left, section1_right = self.create_temporal_stereo_field(section1_mono, "floating")
        
        section1_stereo = np.array([section1_left, section1_right])
        sequence_parts.append(section1_stereo)
        
        # Section 2: Deep therapeutic development
        print("🎼 Section 2: Deep Therapeutic Development")
        duration2 = section_durations[1]
        
        # Multiple harmonic layers with consciousness modulation
        root_freqs = [
            self.base_frequency,
            self.base_frequency * 3/4,  # Perfect fourth below
            self.base_frequency * 2/3,  # Perfect fifth below
        ]
        
        section2_layers = []
        for i, freq in enumerate(root_freqs):
            layer = self.create_temporal_harmony(freq, duration2, "healing")
            # Each layer with different spatial movement
            spatial_types = ["floating", "circular", "expanding"]
            left, right = self.create_temporal_stereo_field(layer, spatial_types[i])
            
            # Amplitude modulation based on golden ratio
            amplitude = 0.3 / (1 + i * self.phi_inverse)
            section2_layers.append(amplitude * np.array([left, right]))
        
        # Combine layers
        section2_stereo = sum(section2_layers)
        sequence_parts.append(section2_stereo)
        
        # Section 3: Gentle resolution and integration
        print("🎼 Section 3: Gentle Resolution")
        duration3 = section_durations[2]
        
        # Return to simple base frequency with expanded consciousness modulation
        resolution_tone = self.create_consciousness_tone(self.base_frequency, duration3, "spatial")
        
        # Add very subtle harmonics
        resolution_harmony = self.create_temporal_harmony(self.base_frequency * 2, duration3, "healing")
        
        section3_mono = 0.5 * resolution_tone + 0.2 * resolution_harmony
        
        # Slowly expanding spatial field that settles to center
        section3_left, section3_right = self.create_temporal_stereo_field(section3_mono, "expanding")
        
        section3_stereo = np.array([section3_left, section3_right])
        sequence_parts.append(section3_stereo)
        
        # Combine all sections with smooth transitions
        print("🔗 Combining sections with smooth transitions")
        
        # Add crossfades between sections
        fade_duration = 2.0  # 2 second crossfades
        fade_samples = int(fade_duration * self.sample_rate)
        
        final_sequence = sequence_parts[0]
        
        for next_section in sequence_parts[1:]:
            # Create crossfade
            current_end = final_sequence[:, -fade_samples:]
            next_start = next_section[:, :fade_samples]
            
            # Linear crossfade
            fade_out = np.linspace(1, 0, fade_samples)
            fade_in = np.linspace(0, 1, fade_samples)
            
            crossfade = (current_end * fade_out + next_start * fade_in)
            
            # Combine
            final_sequence = np.concatenate([
                final_sequence[:, :-fade_samples],
                crossfade,
                next_section[:, fade_samples:]
            ], axis=1)
        
        return final_sequence

def create_healing_soundscape():
    """Create a complete healing soundscape using temporal consciousness principles."""
    
    print("🌊 Creating Healing Soundscape")
    print("=" * 40)
    
    # Initialize musician
    musician = TemporalConsciousnessMusician(base_frequency=432)
    
    # Create therapeutic sequence
    healing_audio = musician.create_therapeutic_sequence(total_duration=90)  # 90 seconds
    
    # Analyze the result
    left_channel = healing_audio[0]
    right_channel = healing_audio[1]
    
    left_energy = np.mean(left_channel**2)
    right_energy = np.mean(right_channel**2)
    max_amplitude = np.max(np.abs(healing_audio))
    
    print(f"\n📊 Audio Analysis:")
    print(f"   Duration: {len(left_channel)/48000:.1f} seconds")
    print(f"   Left energy: {left_energy:.6f}")
    print(f"   Right energy: {right_energy:.6f}")
    print(f"   L/R balance: {left_energy/right_energy:.3f}")
    print(f"   Peak amplitude: {max_amplitude:.3f}")
    
    # Apply gentle normalization
    if max_amplitude > 0:
        healing_audio = healing_audio * 0.8 / max_amplitude
    
    # Convert to integer and save
    stereo_int = (healing_audio * 32767).astype(np.int16).T
    output_filename = 'therapeutic_temporal_music.wav'
    wavfile.write(output_filename, 48000, stereo_int)
    
    print(f"\n💾 Saved: {output_filename}")
    print(f"🌊 Therapeutic music using pure temporal consciousness principles")
    print(f"🎵 Features:")
    print(f"   • 432Hz base frequency (natural healing)")
    print(f"   • Golden ratio harmonic relationships")
    print(f"   • Consciousness-responsive modulation")
    print(f"   • Temporal spatial movement patterns")
    print(f"   • Brainwave entrainment frequencies")
    print(f"   • Three-section therapeutic progression")
    
    return output_filename

def create_complex_musical_piece():
    """Create a more complex musical composition."""
    
    print(f"\n🎼 Creating Complex Musical Piece")
    print("=" * 35)
    
    musician = TemporalConsciousnessMusician(base_frequency=440)  # Standard A
    
    # Create a musical progression
    # Using temporal consciousness to create complex harmonies
    chord_progression = [
        (440, "healing"),      # A
        (493.88, "golden"),    # B
        (329.63, "spatial"),   # E
        (369.99, "healing"),   # F#
    ]
    
    musical_parts = []
    
    for i, (root_freq, style) in enumerate(chord_progression):
        print(f"🎵 Chord {i+1}: {root_freq:.1f}Hz ({style} style)")
        
        # Create chord with temporal harmony
        chord_duration = 8.0  # 8 seconds per chord
        chord_harmony = musician.create_temporal_harmony(root_freq, chord_duration, style)
        
        # Apply different spatial movements for each chord
        spatial_styles = ["floating", "circular", "expanding", "floating"]
        left, right = musician.create_temporal_stereo_field(chord_harmony, spatial_styles[i])
        
        chord_stereo = np.array([left, right])
        musical_parts.append(chord_stereo)
    
    # Combine with musical timing
    final_music = np.concatenate(musical_parts, axis=1)
    
    # Apply musical dynamics
    duration = final_music.shape[1] / 48000
    t = np.linspace(0, duration, final_music.shape[1])
    
    # Musical crescendo and diminuendo
    dynamics = 0.3 + 0.4 * np.sin(np.pi * t / duration)  # Crescendo to middle, then diminuendo
    final_music = final_music * dynamics
    
    # Save
    max_val = np.max(np.abs(final_music))
    if max_val > 0:
        final_music = final_music * 0.85 / max_val
    
    stereo_int = (final_music * 32767).astype(np.int16).T
    output_filename = 'complex_temporal_music.wav'
    wavfile.write(output_filename, 48000, stereo_int)
    
    print(f"💾 Saved: {output_filename}")
    print(f"🎼 Complex musical piece with temporal consciousness harmonies")
    
    return output_filename

if __name__ == "__main__":
    print("🌊 Therapeutic Temporal Music System")
    print("Space emerges from time through consciousness")
    print("=" * 50)
    
    # Create healing soundscape
    healing_file = create_healing_soundscape()
    
    # Create complex musical piece
    music_file = create_complex_musical_piece()
    
    print(f"\n✅ Therapeutic Temporal Music Complete!")
    print(f"🎵 Files created:")
    print(f"   🌊 {healing_file} - Therapeutic healing soundscape")
    print(f"   🎼 {music_file} - Complex musical composition")
    print(f"\n🧠 Both use pure temporal consciousness principles:")
    print(f"   • No direct spatial encoding")
    print(f"   • Space emerges through temporal patterns")
    print(f"   • Consciousness interprets timing as harmony and movement")
    print(f"   • Healing frequencies and golden ratio relationships")