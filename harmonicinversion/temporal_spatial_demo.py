#!/usr/bin/env python3
"""
Temporal Spatial Audio Demo
===========================
Demonstrates the core principle: Space emerges from time through temporal patterns
that consciousness naturally interprets as spatial.

Simple demonstration of key insight:
- We are spatial beings living in time
- Use temporal tricks (delays, phase) that consciousness interprets as space
- No direct spatial encoding needed
"""

import numpy as np
from scipy.io import wavfile

def create_simple_temporal_spatial_demo():
    """
    Simple demo showing how temporal patterns create spatial perception.
    """
    
    print("🌊 Simple Temporal Spatial Audio Demo")
    print("Space emerges from temporal patterns in consciousness")
    print("=" * 55)
    
    sample_rate = 48000
    duration = 1.0
    
    # Create a simple test tone
    t = np.linspace(0, duration, int(duration * sample_rate))
    base_signal = np.sin(2 * np.pi * 440 * t) * 0.5
    
    # Apply fade in/out
    fade_samples = int(0.05 * sample_rate)
    base_signal[:fade_samples] *= np.linspace(0, 1, fade_samples)
    base_signal[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # Test scenarios
    scenarios = []
    
    # 1. Center (no delay, equal phase)
    print("\n🎯 Creating TEMPORAL CENTER")
    print("   No delay, equal amplitude → consciousness perceives CENTER")
    left_center = base_signal.copy()
    right_center = base_signal.copy()
    scenarios.append(("Center", left_center, right_center))
    
    # 2. Left (delay right ear slightly)
    print("\n🎯 Creating TEMPORAL LEFT")
    delay_samples = int(0.0003 * sample_rate)  # 0.3ms delay
    print(f"   Right ear delayed by {delay_samples} samples ({0.3}ms)")
    print("   → consciousness perceives LEFT")
    left_left = base_signal.copy()
    right_left = np.concatenate([np.zeros(delay_samples), base_signal])[:-delay_samples]
    scenarios.append(("Left", left_left, right_left))
    
    # 3. Right (delay left ear slightly)
    print("\n🎯 Creating TEMPORAL RIGHT")
    print(f"   Left ear delayed by {delay_samples} samples ({0.3}ms)")
    print("   → consciousness perceives RIGHT")
    left_right = np.concatenate([np.zeros(delay_samples), base_signal])[:-delay_samples]
    right_right = base_signal.copy()
    scenarios.append(("Right", left_right, right_right))
    
    # 4. Phase difference for subtle spatial cue
    print("\n🎯 Creating TEMPORAL PHASE")
    print("   90° phase difference between ears")
    print("   → consciousness perceives SPATIAL WIDTH")
    from scipy.signal import hilbert
    analytic_signal = hilbert(base_signal)
    left_phase = np.real(analytic_signal * np.exp(1j * np.pi/4))   # +45°
    right_phase = np.real(analytic_signal * np.exp(-1j * np.pi/4))  # -45°
    scenarios.append(("Phase", left_phase, right_phase))
    
    # Combine all scenarios
    print(f"\n📊 Combining temporal scenarios...")
    sequence_parts = []
    
    for name, left, right in scenarios:
        # Ensure same length
        min_length = min(len(left), len(right))
        left = left[:min_length] 
        right = right[:min_length]
        
        # Add to sequence
        stereo_segment = np.array([left, right])
        sequence_parts.append(stereo_segment)
        
        # Add silence
        silence = np.zeros((2, int(0.5 * sample_rate)))
        sequence_parts.append(silence)
        
        # Analyze
        left_energy = np.mean(left**2)
        right_energy = np.mean(right**2)
        correlation = np.corrcoef(left, right)[0,1]
        
        print(f"   {name}: L={left_energy:.6f}, R={right_energy:.6f}, corr={correlation:.3f}")
    
    # Final sequence
    final_sequence = np.concatenate(sequence_parts, axis=1)
    
    # Normalize and save
    max_val = np.max(np.abs(final_sequence))
    if max_val > 0:
        final_sequence = final_sequence * 0.9 / max_val
    
    stereo_int = (final_sequence * 32767).astype(np.int16).T
    output_filename = 'simple_temporal_spatial_demo.wav'
    wavfile.write(output_filename, sample_rate, stereo_int)
    
    print(f"\n💾 Saved: {output_filename}")
    print(f"🧠 Each segment uses TEMPORAL TRICKS:")
    print(f"   1. Center: No temporal difference")
    print(f"   2. Left: Right ear delayed {0.3}ms") 
    print(f"   3. Right: Left ear delayed {0.3}ms")
    print(f"   4. Phase: 90° temporal phase difference")
    print(f"\n🌊 Your consciousness interprets these TEMPORAL patterns as SPATIAL!")
    print(f"🎯 Space emerges from time, not from direct spatial encoding")
    
    return output_filename

def compare_approaches():
    """Compare our different approaches."""
    
    print(f"\n🔬 Comparing Spatial Audio Approaches")
    print("=" * 40)
    
    approaches = [
        ("Direct Geometric", "sophisticated_geometric_spatial_test.wav", "Uses x-coordinate → pan mapping"),
        ("Temporal Consciousness", "temporal_consciousness_audio_test.wav", "Uses temporal tricks consciousness interprets as space"),
        ("Simple Temporal Demo", "simple_temporal_spatial_demo.wav", "Pure temporal delays and phase differences"),
    ]
    
    for name, filename, description in approaches:
        try:
            # Try to get file info
            import os
            size = os.path.getsize(filename)
            print(f"\n🎵 {name}:")
            print(f"   File: {filename}")
            print(f"   Size: {size/1024:.1f}KB")
            print(f"   Method: {description}")
        except FileNotFoundError:
            print(f"\n❌ {name}: File {filename} not found")
    
    print(f"\n🌊 Key Insight:")
    print(f"   The simple temporal demo should work best because it directly")
    print(f"   uses the temporal patterns consciousness naturally interprets as spatial!")

if __name__ == "__main__":
    print("🌊 Temporal Spatial Audio Demo")
    print("Space emerges from time through consciousness")
    print("=" * 50)
    
    # Create simple demo
    demo_file = create_simple_temporal_spatial_demo()
    
    # Compare approaches
    compare_approaches()
    
    print(f"\n✅ Demo complete!")
    print(f"🎧 Try playing: {demo_file}")
    print(f"🧠 Notice how pure TEMPORAL tricks create SPATIAL perception!")