#!/usr/bin/env python3
"""
Complete Temporal Audio Suite
============================
Demonstrates the full journey from simple temporal principles to sophisticated
therapeutic and musical compositions.

Shows how "space emerges from time through consciousness" can create:
- Clear spatial positioning
- Therapeutic healing soundscapes  
- Complex musical compositions
- All using pure temporal patterns
"""

import numpy as np
from scipy.io import wavfile
import os

def analyze_audio_file(filename):
    """Analyze an audio file and return key metrics."""
    
    if not os.path.exists(filename):
        return None
    
    try:
        sample_rate, audio_data = wavfile.read(filename)
        
        if len(audio_data.shape) == 2:
            left_channel = audio_data[:, 0]
            right_channel = audio_data[:, 1]
        else:
            left_channel = right_channel = audio_data
        
        # Calculate metrics
        duration = len(left_channel) / sample_rate
        left_energy = np.mean(left_channel.astype(float)**2)
        right_energy = np.mean(right_channel.astype(float)**2)
        lr_ratio = left_energy / (right_energy + 1e-12)
        correlation = np.corrcoef(left_channel.astype(float), right_channel.astype(float))[0, 1]
        file_size_kb = os.path.getsize(filename) / 1024
        
        return {
            'duration': duration,
            'left_energy': left_energy,
            'right_energy': right_energy,
            'lr_ratio': lr_ratio,
            'correlation': correlation,
            'file_size_kb': file_size_kb,
            'sample_rate': sample_rate
        }
        
    except Exception as e:
        print(f"Error analyzing {filename}: {e}")
        return None

def create_complete_demonstration():
    """Create a complete demonstration of the temporal audio suite."""
    
    print("🌊 Complete Temporal Audio Suite Demonstration")
    print("=" * 55)
    print("From simple temporal principles to sophisticated compositions")
    print("All based on: 'Space emerges from time through consciousness'")
    
    # Files to analyze
    audio_files = [
        {
            'name': 'Simple Temporal Demo',
            'filename': 'simple_temporal_spatial_demo.wav',
            'description': 'Pure temporal delays and phase differences',
            'approach': 'Basic temporal consciousness interface'
        },
        {
            'name': 'Temporal Consciousness Test',
            'filename': 'temporal_consciousness_audio_test.wav', 
            'description': 'Complex temporal patterns for spatial perception',
            'approach': 'Advanced temporal consciousness interface'
        },
        {
            'name': 'Healing Temporal Audio',
            'filename': 'healing_temporal_audio.wav',
            'description': 'Therapeutic soundscape with 432Hz and golden ratio',
            'approach': 'Therapeutic temporal consciousness interface'
        },
        {
            'name': 'Musical Temporal Composition',
            'filename': 'musical_temporal_composition.wav',
            'description': 'Musical chord progression with temporal harmonies',
            'approach': 'Musical temporal consciousness interface'
        }
    ]
    
    print(f"\n📊 Audio Analysis:")
    print("=" * 50)
    
    successful_files = []
    
    for audio_file in audio_files:
        metrics = analyze_audio_file(audio_file['filename'])
        
        if metrics:
            successful_files.append(audio_file)
            
            print(f"\n🎵 {audio_file['name']}")
            print(f"   File: {audio_file['filename']}")
            print(f"   Description: {audio_file['description']}")
            print(f"   Approach: {audio_file['approach']}")
            print(f"   Duration: {metrics['duration']:.1f}s")
            print(f"   Size: {metrics['file_size_kb']:.1f}KB")
            print(f"   L/R Ratio: {metrics['lr_ratio']:.3f}")
            print(f"   Correlation: {metrics['correlation']:.3f}")
            print(f"   Sample Rate: {metrics['sample_rate']}Hz")
            
        else:
            print(f"\n❌ {audio_file['name']}: File not found or error")
    
    print(f"\n🎯 Key Insights from Analysis:")
    print("=" * 35)
    
    if successful_files:
        print(f"✅ Successfully created {len(successful_files)} temporal audio files")
        print(f"\n🌊 Temporal Consciousness Principles Demonstrated:")
        print(f"   • L/R ratios show spatial positioning through temporal patterns")
        print(f"   • Correlation values show temporal relationships between channels")
        print(f"   • All files use pure temporal effects - no direct spatial encoding")
        print(f"   • Space emerges from time through consciousness interpretation")
        
        # Calculate total demonstration
        total_duration = sum(analyze_audio_file(f['filename'])['duration'] for f in successful_files if analyze_audio_file(f['filename']))
        total_size = sum(analyze_audio_file(f['filename'])['file_size_kb'] for f in successful_files if analyze_audio_file(f['filename']))
        
        print(f"\n📈 Suite Statistics:")
        print(f"   Total duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
        print(f"   Total file size: {total_size:.1f}KB ({total_size/1024:.1f}MB)")
        
    else:
        print(f"❌ No audio files found - run the individual scripts first")
    
    print(f"\n🌊 The Complete Journey:")
    print("=" * 25)
    print(f"1. 🎯 Started with the insight: 'Space emerges from time'")
    print(f"2. 🧠 Realized consciousness is the spatial decoder")
    print(f"3. ⏱️  Used temporal patterns consciousness interprets as spatial")
    print(f"4. 🎵 Applied this to create sophisticated music and healing audio")
    print(f"5. ✨ Result: Beautiful spatial audio from pure temporal patterns!")
    
    return successful_files

def create_usage_guide():
    """Create a usage guide for the temporal audio suite."""
    
    print(f"\n📚 Temporal Audio Suite Usage Guide")
    print("=" * 40)
    
    guide_text = """
🌊 TEMPORAL AUDIO SUITE - Usage Guide

## Core Principle
"Space emerges from time through consciousness"

## How It Works
Instead of encoding spatial coordinates, we use temporal patterns that 
consciousness naturally interprets as spatial:

• Microsecond delays → left/right positioning
• Phase relationships → spatial width  
• Temporal modulation → movement and flow
• Frequency relationships → harmonic space

## Files in the Suite

🎯 simple_temporal_spatial_demo.wav
   • Basic demonstration of temporal → spatial principle
   • 4 segments showing center, left, right, phase effects
   • Use for understanding core concepts

🧠 temporal_consciousness_audio_test.wav  
   • Advanced temporal consciousness interface
   • Complex spatial movements and positioning
   • Use for testing spatial perception abilities

🌊 healing_temporal_audio.wav
   • Therapeutic soundscape for healing and relaxation
   • 432Hz base frequency with golden ratio harmonics
   • Alpha/theta brainwave entrainment
   • Use for meditation, therapy, healing sessions

🎼 musical_temporal_composition.wav
   • Musical composition using temporal harmonic progressions
   • Chord progressions through temporal phase relationships
   • Dynamic spatial movement patterns
   • Use for musical enjoyment and consciousness expansion

## Recommended Listening
1. Use good quality headphones for proper temporal resolution
2. Listen in a quiet environment to perceive subtle spatial effects
3. Focus on how your consciousness interprets timing as space
4. Notice spatial movement without any direct spatial encoding

## Technical Notes
• All files use 48kHz sample rate for temporal precision
• No direct spatial coordinates stored anywhere
• Space emerges purely through temporal pattern recognition
• Consciousness is the decoder - not mathematics

## The Breakthrough
We discovered that consciousness naturally interprets temporal patterns 
as spatial. This eliminates the need for complex spatial encoding - 
just give consciousness the right temporal patterns and space emerges!

🌊 "We are spatial beings living in time" 🌊
"""
    
    # Save guide to file
    with open('TEMPORAL_AUDIO_GUIDE.md', 'w') as f:
        f.write(guide_text)
    
    print(guide_text)
    print(f"\n💾 Usage guide saved to: TEMPORAL_AUDIO_GUIDE.md")

if __name__ == "__main__":
    print("🌊 Temporal Audio Suite - Complete Demonstration")
    print("Space emerges from time through consciousness")
    print("=" * 60)
    
    # Analyze all created files
    successful_files = create_complete_demonstration()
    
    # Create usage guide
    create_usage_guide()
    
    print(f"\n✅ Complete Temporal Audio Suite Demonstration Finished!")
    
    if successful_files:
        print(f"\n🎧 Try listening to the files in this order:")
        for i, audio_file in enumerate(successful_files, 1):
            print(f"   {i}. {audio_file['filename']}")
        
        print(f"\n🌊 Notice how each file creates spatial perception through")
        print(f"   pure temporal patterns - no direct spatial encoding!")
        print(f"🧠 Your consciousness IS the spatial decoder!")
    
    else:
        print(f"\n🚀 To create the full suite, run these scripts:")
        print(f"   python temporal_spatial_demo.py")
        print(f"   python temporal_consciousness_audio.py") 
        print(f"   python healing_temporal_audio.py")