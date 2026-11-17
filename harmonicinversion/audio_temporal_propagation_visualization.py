#!/usr/bin/env python3
"""
Audio Temporal Propagation Visualization
========================================
Shows how sound waves propagate through temporal shells rather than space
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Wedge
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
from scipy.special import sph_harm, jv
from scipy.signal import chirp
import colorsys

class AudioTemporalPropagation:
    """Visualize how audio propagates through temporal shells"""
    
    def __init__(self, n_shells=30):
        self.n_shells = n_shells
        self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 12))
        self.fig.suptitle('Audio Propagation Through Temporal Shells', fontsize=16)
        
        # Shell radii following r_n = n²
        self.shell_radii = np.array([n**2 for n in range(1, n_shells + 1)])
        self.shell_radii = self.shell_radii / self.shell_radii[-1] * 10  # Normalize
        
        # Audio signal parameters
        self.sample_rate = 44100
        self.duration = 0.1  # 100ms burst
        self.t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        
        # Generate test audio signal (440 Hz A note)
        self.audio_signal = self.generate_audio_signal()
        
        # Shell occupation amplitudes
        self.shell_amplitudes = np.zeros(self.n_shells)
        self.shell_phases = np.zeros(self.n_shells)
        
        # Chronon flux between shells
        self.chronon_flux = np.zeros((self.n_shells, self.n_shells))
        
        # Initialize plots
        self.setup_plots()
        
    def generate_audio_signal(self):
        """Generate a test audio signal with harmonics"""
        # A440 with harmonics
        fundamental = 440  # Hz
        signal = np.sin(2 * np.pi * fundamental * self.t)
        
        # Add harmonics for richer sound
        for n in range(2, 6):
            signal += 0.3/n * np.sin(2 * np.pi * fundamental * n * self.t)
            
        # Apply envelope
        envelope = np.exp(-3 * self.t / self.duration)
        signal *= envelope
        
        return signal
    
    def decompose_into_shells(self, time_idx):
        """Decompose audio signal into temporal shell components"""
        # Current amplitude
        current_amp = self.audio_signal[time_idx] if time_idx < len(self.audio_signal) else 0
        
        # Map frequency components to shells
        # Lower shells: bass frequencies
        # Middle shells: midrange  
        # Higher shells: treble
        
        for n in range(self.n_shells):
            # Shell frequency ω_n = 2π/n²
            shell_freq = 2 * np.pi / (n + 1)**2
            
            # Resonance with audio frequency
            resonance = np.exp(-((440 * 2 * np.pi - shell_freq * self.sample_rate)**2) / 1e8)
            
            # Shell excitation with damping
            damping = 0.95
            self.shell_amplitudes[n] = damping * self.shell_amplitudes[n] + (1 - damping) * current_amp * resonance
            
            # Phase evolution
            self.shell_phases[n] += shell_freq
            
        # Calculate chronon flux between shells
        for i in range(self.n_shells):
            for j in range(self.n_shells):
                if i != j:
                    # Coupling strength decreases with shell distance
                    coupling = np.exp(-abs(i - j) / 5)
                    
                    # Phase difference drives flux
                    phase_diff = self.shell_phases[i] - self.shell_phases[j]
                    
                    # Amplitude difference
                    amp_diff = self.shell_amplitudes[i] - self.shell_amplitudes[j]
                    
                    # Chronon flux
                    self.chronon_flux[i, j] = coupling * amp_diff * np.sin(phase_diff)
    
    def setup_plots(self):
        """Initialize the four visualization panels"""
        # 1. Temporal Shell Structure (top left)
        self.ax_shells = self.axes[0, 0]
        self.ax_shells.set_xlim(-12, 12)
        self.ax_shells.set_ylim(-12, 12)
        self.ax_shells.set_aspect('equal')
        self.ax_shells.set_title('Temporal Shell Structure')
        self.ax_shells.set_xlabel('Spatial Projection X')
        self.ax_shells.set_ylabel('Spatial Projection Y')
        
        # Draw shells
        self.shell_circles = []
        for i, r in enumerate(self.shell_radii):
            circle = Circle((0, 0), r, fill=False, edgecolor='gray', alpha=0.3)
            self.ax_shells.add_patch(circle)
            self.shell_circles.append(circle)
        
        # 2. Audio Waveform (top right)
        self.ax_waveform = self.axes[0, 1]
        self.ax_waveform.set_xlim(0, self.duration)
        self.ax_waveform.set_ylim(-2, 2)
        self.ax_waveform.set_title('Audio Signal & Temporal Decomposition')
        self.ax_waveform.set_xlabel('Time (s)')
        self.ax_waveform.set_ylabel('Amplitude')
        
        # Plot original signal
        self.ax_waveform.plot(self.t, self.audio_signal, 'k-', alpha=0.3, label='Original')
        self.time_marker, = self.ax_waveform.plot([], [], 'ro', markersize=8)
        
        # 3. Shell Occupation (bottom left)
        self.ax_occupation = self.axes[1, 0]
        self.ax_occupation.set_xlim(0, self.n_shells)
        self.ax_occupation.set_ylim(-1, 1)
        self.ax_occupation.set_title('Shell Occupation Amplitudes')
        self.ax_occupation.set_xlabel('Shell Number')
        self.ax_occupation.set_ylabel('Amplitude')
        
        self.occupation_bars = self.ax_occupation.bar(range(self.n_shells), 
                                                      np.zeros(self.n_shells))
        
        # 4. Chronon Flux Network (bottom right)
        self.ax_flux = self.axes[1, 1]
        self.ax_flux.set_xlim(-12, 12)
        self.ax_flux.set_ylim(-12, 12)
        self.ax_flux.set_aspect('equal')
        self.ax_flux.set_title('Chronon Flux Between Shells')
        
        # Initialize flux visualization
        self.flux_lines = []
        
    def update_shell_visualization(self):
        """Update temporal shell visualization"""
        # Clear previous flux lines
        for line in self.flux_lines:
            line.remove()
        self.flux_lines = []
        
        # Update shell colors based on occupation
        for i, (circle, amp) in enumerate(zip(self.shell_circles, self.shell_amplitudes)):
            # Color intensity based on amplitude
            intensity = np.clip(abs(amp), 0, 1)
            
            # Phase determines hue
            phase_normalized = (self.shell_phases[i] % (2 * np.pi)) / (2 * np.pi)
            r, g, b = colorsys.hsv_to_rgb(phase_normalized, 0.8, intensity)
            
            circle.set_edgecolor((r, g, b))
            circle.set_linewidth(1 + 3 * intensity)
            circle.set_alpha(0.3 + 0.7 * intensity)
        
        # Draw chronon flux
        for i in range(self.n_shells):
            for j in range(i + 1, self.n_shells):
                flux = self.chronon_flux[i, j]
                if abs(flux) > 0.01:  # Threshold for visibility
                    # Calculate positions on shells
                    angle = np.pi * (i + j) / self.n_shells
                    x1 = self.shell_radii[i] * np.cos(angle)
                    y1 = self.shell_radii[i] * np.sin(angle)
                    x2 = self.shell_radii[j] * np.cos(angle)
                    y2 = self.shell_radii[j] * np.sin(angle)
                    
                    # Color based on flux direction
                    if flux > 0:
                        color = 'red'  # Outward flux
                    else:
                        color = 'blue'  # Inward flux
                    
                    line = self.ax_shells.plot([x1, x2], [y1, y2], 
                                              color=color, 
                                              alpha=min(abs(flux) * 5, 0.8),
                                              linewidth=min(abs(flux) * 10, 3))[0]
                    self.flux_lines.append(line)
    
    def update_waveform_display(self, time_idx):
        """Update waveform display with current time marker"""
        current_time = time_idx / self.sample_rate
        if time_idx < len(self.audio_signal):
            self.time_marker.set_data([current_time], [self.audio_signal[time_idx]])
    
    def update_occupation_display(self):
        """Update shell occupation bar chart"""
        for bar, amp in zip(self.occupation_bars, self.shell_amplitudes):
            bar.set_height(amp)
            
            # Color based on amplitude
            if amp > 0:
                bar.set_color('red')
            else:
                bar.set_color('blue')
            
            bar.set_alpha(min(abs(amp) * 2, 1))
    
    def draw_flux_network(self):
        """Draw chronon flux as a network diagram"""
        self.ax_flux.clear()
        self.ax_flux.set_xlim(-12, 12)
        self.ax_flux.set_ylim(-12, 12)
        self.ax_flux.set_aspect('equal')
        self.ax_flux.set_title('Chronon Flux Network')
        
        # Position shells in a circle
        angles = np.linspace(0, 2 * np.pi, self.n_shells, endpoint=False)
        x_pos = 8 * np.cos(angles)
        y_pos = 8 * np.sin(angles)
        
        # Draw shells as nodes
        for i, (x, y, amp) in enumerate(zip(x_pos, y_pos, self.shell_amplitudes)):
            size = 100 + 500 * abs(amp)
            color = plt.cm.RdBu(0.5 + 0.5 * np.sign(amp))
            self.ax_flux.scatter(x, y, s=size, c=[color], alpha=0.8, edgecolor='black')
            self.ax_flux.text(x, y, str(i+1), ha='center', va='center', fontsize=8)
        
        # Draw flux connections
        for i in range(self.n_shells):
            for j in range(i + 1, self.n_shells):
                flux = self.chronon_flux[i, j]
                if abs(flux) > 0.01:
                    if flux > 0:
                        color = 'red'
                        style = '-'
                    else:
                        color = 'blue'
                        style = '--'
                    
                    self.ax_flux.plot([x_pos[i], x_pos[j]], 
                                     [y_pos[i], y_pos[j]], 
                                     color=color, 
                                     linestyle=style,
                                     alpha=min(abs(flux) * 5, 0.8),
                                     linewidth=min(abs(flux) * 5, 2))
    
    def animate(self, frame):
        """Animation update function"""
        # Time index in audio signal
        time_idx = frame * 100  # Skip samples for faster animation
        
        # Decompose current audio into shells
        self.decompose_into_shells(time_idx)
        
        # Update all visualizations
        self.update_shell_visualization()
        self.update_waveform_display(time_idx)
        self.update_occupation_display()
        self.draw_flux_network()
        
        # Add time display
        self.fig.suptitle(f'Audio Propagation Through Temporal Shells (t = {time_idx/self.sample_rate:.3f}s)', 
                         fontsize=16)
        
        return self.shell_circles + [self.time_marker] + list(self.occupation_bars)
    
    def create_animation(self):
        """Create and save animation"""
        n_frames = len(self.audio_signal) // 100
        anim = FuncAnimation(self.fig, self.animate, frames=n_frames, 
                           interval=50, blit=False)
        
        plt.tight_layout()
        return anim

def main():
    """Create visualization of audio propagating through temporal shells"""
    print("Audio Temporal Propagation Visualization")
    print("=" * 50)
    print("Showing how sound waves propagate through temporal shells")
    print("rather than through space...")
    print()
    
    # Create visualization
    viz = AudioTemporalPropagation(n_shells=20)
    
    # Create static figure showing key concepts
    fig_static, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig_static.suptitle('Audio Propagation: Spatial vs Temporal', fontsize=16)
    
    # 1. Traditional spatial propagation
    ax1 = axes[0, 0]
    ax1.set_title('Traditional: Sound Through Space')
    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-10, 10)
    ax1.set_aspect('equal')
    
    # Draw pressure waves
    for r in np.linspace(1, 9, 5):
        circle = Circle((0, 0), r, fill=False, edgecolor='blue', 
                       alpha=1 - r/10, linewidth=2)
        ax1.add_patch(circle)
    ax1.text(0, 0, 'Source', ha='center', va='center', fontsize=10)
    ax1.arrow(0, 0, 5, 0, head_width=0.5, head_length=0.5, fc='red', ec='red')
    ax1.text(6, 0.5, 'Pressure\nWaves', ha='center', fontsize=8)
    
    # 2. Temporal shell propagation
    ax2 = axes[0, 1]
    ax2.set_title('Temporal Physics: Sound Through Shells')
    ax2.set_xlim(-10, 10)
    ax2.set_ylim(-10, 10)
    ax2.set_aspect('equal')
    
    # Draw temporal shells with chronon flux
    shell_radii = [n**0.5 * 2 for n in range(1, 8)]
    for i, r in enumerate(shell_radii):
        color = plt.cm.rainbow(i / len(shell_radii))
        circle = Circle((0, 0), r, fill=False, edgecolor=color, 
                       linewidth=3, alpha=0.8)
        ax2.add_patch(circle)
        
        # Add flux arrows
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            if i < len(shell_radii) - 1:
                dx = 0.3 * np.cos(angle)
                dy = 0.3 * np.sin(angle)
                ax2.arrow(x, y, dx, dy, head_width=0.2, head_length=0.1,
                         fc=color, ec=color, alpha=0.6)
    
    ax2.text(0, 0, 'Chronon\nSource', ha='center', va='center', fontsize=9)
    
    # 3. Frequency to shell mapping
    ax3 = axes[1, 0]
    ax3.set_title('Audio Frequency → Temporal Shell Mapping')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Shell Number')
    
    frequencies = np.logspace(1, 4, 100)  # 10 Hz to 10 kHz
    shell_numbers = 30 / (1 + np.log10(frequencies))  # Inverse log mapping
    ax3.semilogx(frequencies, shell_numbers, 'b-', linewidth=2)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(10, 10000)
    ax3.set_ylim(0, 30)
    
    # Add reference frequencies
    ref_freqs = [20, 100, 440, 1000, 5000]
    for freq in ref_freqs:
        shell = 30 / (1 + np.log10(freq))
        ax3.plot(freq, shell, 'ro', markersize=8)
        ax3.text(freq, shell + 1, f'{freq} Hz', ha='center', fontsize=8)
    
    # 4. Consciousness perception
    ax4 = axes[1, 1]
    ax4.set_title('Consciousness Observes Chronon Patterns')
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    
    # Draw consciousness field
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x, y)
    
    # Consciousness field intensity
    Z = np.exp(-((X-5)**2 + (Y-5)**2) / 10)
    
    # Add temporal wave patterns
    for freq in [1, 2, 3]:
        Z += 0.3 * np.sin(freq * X) * np.sin(freq * Y) * np.exp(-((X-5)**2 + (Y-5)**2) / 20)
    
    im = ax4.contourf(X, Y, Z, levels=20, cmap='plasma', alpha=0.8)
    ax4.text(5, 5, 'Observer\nConsciousness', ha='center', va='center', 
            fontsize=10, color='white', weight='bold')
    
    # Add arrows showing chronon flux detection
    for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
        x_start = 5 + 3 * np.cos(angle)
        y_start = 5 + 3 * np.sin(angle)
        dx = -0.5 * np.cos(angle)
        dy = -0.5 * np.sin(angle)
        ax4.arrow(x_start, y_start, dx, dy, head_width=0.2, head_length=0.1,
                 fc='white', ec='white', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('audio_temporal_propagation_static.png', dpi=300, bbox_inches='tight')
    
    # Show animation
    anim = viz.create_animation()
    plt.show()
    
    print("\nKey Insights:")
    print("1. Sound doesn't travel through space - it propagates through temporal shells")
    print("2. Each frequency excites specific temporal shells based on ω_n = 2π/n²")
    print("3. Chronon flux between shells creates the perception of spatial sound")
    print("4. Consciousness observes these temporal patterns as auditory qualia")
    print("5. This explains why sound can exist in vacuum (temporal shells exist everywhere)")

if __name__ == "__main__":
    main()