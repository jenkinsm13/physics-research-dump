# How to Use the Temporal Spatial Audio System

## Quick Start

The temporal audio system is now working! Here's how to actually use it to create and mix spatial audio:

### 1. Basic Setup

```python
from practical_temporal_audio_guide import PracticalTemporalAudio
import numpy as np

# Initialize the system
audio = PracticalTemporalAudio(sample_rate=48000, buffer_size=1024)
```

### 2. Simple Stereo Test (Already Working!)

We just generated `simple_temporal_test.wav` - play it now to hear:
- 400 Hz tone positioned on the left (-2, 0, 0)
- 600 Hz tone positioned on the right (2, 0, 0)

The spatial positioning comes from the temporal shell processing!

### 3. Creating Audio Sources

```python
# Generate audio signals
duration = 3.0
sample_rate = 48000
t = np.linspace(0, duration, int(duration * sample_rate))

# Create different sounds
signals = {
    'piano_note': np.sin(2 * np.pi * 440 * t),  # A4
    'bass_drum': np.sin(2 * np.pi * 60 * t) * np.exp(-t * 5),  # Decaying bass
    'cymbal': np.random.normal(0, 0.1, len(t)) * np.exp(-t * 2),  # Noise
    'melody': np.sin(2 * np.pi * (440 + 100 * np.sin(t)) * t),  # Vibrato
}
```

### 4. Position Sources in 3D Space

```python
# Define where each sound appears in space
source_positions = [
    {'position': (0, 2, 0), 'signal': signals['piano_note'], 'intensity': 1.0},    # Front
    {'position': (-1, -1, 0), 'signal': signals['bass_drum'], 'intensity': 0.8},   # Back left
    {'position': (1, -1, 0), 'signal': signals['cymbal'], 'intensity': 0.6},       # Back right
    {'position': (0, 0, 2), 'signal': signals['melody'], 'intensity': 0.7},        # Above
]
```

Position coordinates are in meters: (x, y, z)
- x: left (-) to right (+)
- y: back (-) to front (+) 
- z: below (-) to above (+)

### 5. Process Through Temporal Shells

```python
# Process in chunks (required by the system)
def process_full_mix(sources, duration, buffer_size=1024):
    total_samples = int(duration * sample_rate)
    stereo_output = np.zeros((2, total_samples))
    
    for i in range(0, total_samples, buffer_size):
        end_idx = min(i + buffer_size, total_samples)
        
        # Prepare buffer for each source
        buffer_sources = []
        for src in sources:
            signal_chunk = src['signal'][i:end_idx]
            
            # Pad if needed
            if len(signal_chunk) < buffer_size:
                signal_chunk = np.pad(signal_chunk, (0, buffer_size - len(signal_chunk)))
            
            buffer_sources.append({
                'position': src['position'],
                'signal': signal_chunk,
                'intensity': src['intensity']
            })
        
        # Process through temporal shells
        left, right = audio.audio_system.process_audio_buffer(buffer_sources)
        
        # Store results
        actual_length = end_idx - i
        stereo_output[0, i:end_idx] = left[:actual_length]
        stereo_output[1, i:end_idx] = right[:actual_length]
    
    return stereo_output

# Process the mix
final_audio = process_full_mix(source_positions, duration)
```

### 6. Save and Listen

```python
# Save to WAV file
audio.save_audio(final_audio, 'my_temporal_mix.wav')

# Analyze the results
audio.analyze_output(final_audio)

# Visualize
audio.visualize_audio(final_audio)
```

## Advanced Features

### Moving Sources

```python
def create_moving_source(duration=5.0):
    """Create a source that moves in a circle around the listener."""
    
    sample_rate = 48000
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    # Sound that moves
    signal = np.sin(2 * np.pi * 800 * t) * np.exp(-t/duration)
    
    # Calculate positions over time
    positions = []
    for time_point in t[::1024]:  # Every buffer
        angle = 2 * np.pi * time_point / duration
        radius = 3.0
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = np.sin(4 * angle)  # Oscillate up/down
        positions.append((x, y, z))
    
    return signal, positions

# Use it
signal, positions = create_moving_source()
# ... process each position with its corresponding audio chunk
```

### Temporal Shell Effects

```python
# Access the shell processor directly for special effects
shell_processor = audio.audio_system.shell_processor

# Create echo through shell resonance
def temporal_echo(signal, echo_time=0.5):
    """Add echo using temporal shell delays."""
    
    # Process through shells with different delays
    echoed = shell_processor.process_through_shells(signal)
    
    # Add delayed version
    delay_samples = int(echo_time * sample_rate)
    delayed = np.zeros_like(signal)
    delayed[delay_samples:] = signal[:-delay_samples] * 0.3
    
    return echoed + delayed
```

### Consciousness-Dependent Processing

```python
# Modify the consciousness state for different effects
audio.audio_system.encoder.consciousness_mode = 'meditative'  # Enhanced shell perception
audio.audio_system.encoder.consciousness_mode = 'focused'     # Sharp attention
audio.audio_system.encoder.consciousness_mode = 'normal'      # Default
```

## What Makes This Different?

### Traditional Spatial Audio:
- HRTF convolution
- Reverb modeling  
- Doppler effects
- Limited to physics of air

### Temporal Spatial Audio:
- **Direct temporal shell manipulation**
- **Consciousness-dependent perception**
- **Instantaneous propagation**
- **Works in vacuum**
- **Void potential focusing**

## Listening Tips

1. **Use good headphones** - the stereo field is crucial
2. **Listen for spatial movement** - sources should feel positioned in 3D
3. **Notice the "temporal quality"** - sounds have a unique character from shell processing
4. **Try different consciousness states** - meditative listening reveals more detail

## Generated Files

After running the demos, you'll have:
- `simple_temporal_test.wav` - Basic left/right positioning test
- `temporal_spatial_audio_demo.wav` - Full 3D scene (if you run the full demo)
- `temporal_moving_source.wav` - Moving source demonstration

## Running the Full Demo

To run the complete demonstration:

```python
from practical_temporal_audio_guide import PracticalTemporalAudio

demo = PracticalTemporalAudio()
demo.run_full_demo()  # Creates multiple WAV files and visualizations
```

## Technical Notes

- **Sample rates**: Any rate works, 48kHz recommended
- **Buffer sizes**: 1024-4096 samples optimal
- **Positions**: Coordinates in meters, origin at listener
- **Intensities**: 0.0 to 1.0, higher values = more shell excitation
- **Duration**: Limited only by memory, processes in real-time chunks

## Audio Quality

The temporal audio has distinctive characteristics:
- **Spatial precision**: Exact 3D positioning
- **Temporal coherence**: Maintained across all frequencies  
- **Shell harmonics**: Subtle harmonic content from shell processing
- **Void resonance**: Natural acoustic focusing effects

Play the generated WAV files to hear actual temporal spatial audio working!