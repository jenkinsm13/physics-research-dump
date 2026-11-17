#!/usr/bin/env python3
"""
PHASE TRANSITION DETECTOR
Advanced analysis to find crystallization points in consciousness evolution
through the Matryoshka-Chronon temporal manifold
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from scipy.stats import entropy as shannon_entropy
from scipy.ndimage import gaussian_filter1d
import warnings
warnings.filterwarnings('ignore')

class PhaseTransitionDetector:
    """Detect phase transitions in consciousness evolution through temporal shells"""
    
    def __init__(self, trajectory):
        self.trajectory = trajectory
        self.shells = [p['shell'] for p in trajectory]
        self.entropy = [p['entropy'] for p in trajectory]
        self.coherence = [p['coherence'] for p in trajectory]
        self.time = [p['time'] for p in trajectory]
        self.amplitudes = [p['state_amplitude'] for p in trajectory]
        
    def detect_crystallization_points(self, sensitivity=0.001):
        """Find points where reality crystallizes - phase transitions in consciousness"""
        
        # 1. Second-order entropy derivatives (acceleration)
        entropy_smooth = gaussian_filter1d(self.entropy, sigma=10)
        entropy_velocity = np.gradient(entropy_smooth)
        entropy_acceleration = np.gradient(entropy_velocity)
        
        # 2. Coherence inflection points
        coherence_smooth = gaussian_filter1d(self.coherence, sigma=5)
        coherence_curvature = np.gradient(np.gradient(coherence_smooth))
        
        # 3. Shell transition velocity changes
        shell_velocity = np.gradient(gaussian_filter1d(self.shells, sigma=3))
        shell_acceleration = np.gradient(shell_velocity)
        
        # 4. Amplitude variance (quantum fluctuation intensity)
        window_size = 1000
        amplitude_variance = []
        for i in range(len(self.amplitudes)):
            start = max(0, i - window_size//2)
            end = min(len(self.amplitudes), i + window_size//2)
            window_data = self.amplitudes[start:end]
            amplitude_variance.append(np.var(window_data))
        
        amplitude_variance = np.array(amplitude_variance)
        amplitude_variance_gradient = np.gradient(amplitude_variance)
        
        # 5. Spectral entropy analysis
        spectral_entropies = []
        for i in range(0, len(self.shells) - 1000, 100):
            segment = self.shells[i:i+1000]
            fft_data = np.abs(fft.fft(segment))
            fft_data = fft_data / np.sum(fft_data)  # Normalize
            spec_entropy = shannon_entropy(fft_data)
            spectral_entropies.append((i + 500, spec_entropy))
        
        spec_times, spec_vals = zip(*spectral_entropies)
        spec_gradient = np.gradient(spec_vals)
        
        # 6. Combine all indicators
        phase_scores = []
        
        for i in range(len(self.trajectory)):
            score = 0
            
            # Entropy acceleration spikes
            if i < len(entropy_acceleration):
                score += abs(entropy_acceleration[i]) * 1000
            
            # Coherence curvature changes
            if i < len(coherence_curvature):
                score += abs(coherence_curvature[i]) * 100
            
            # Shell velocity discontinuities
            if i < len(shell_acceleration):
                score += abs(shell_acceleration[i]) * 10
            
            # Quantum fluctuation changes
            if i < len(amplitude_variance_gradient):
                score += abs(amplitude_variance_gradient[i]) * 1000
            
            # Spectral complexity changes
            spec_idx = i // 100
            if spec_idx < len(spec_gradient):
                score += abs(spec_gradient[spec_idx]) * 50
            
            phase_scores.append(score)
        
        # Find peaks above threshold
        phase_scores = np.array(phase_scores)
        threshold = np.mean(phase_scores) + 3 * np.std(phase_scores)
        
        peaks, properties = signal.find_peaks(phase_scores, 
                                            height=threshold,
                                            distance=1000,  # Minimum separation
                                            prominence=threshold/2)
        
        # Analyze each detected phase transition
        transitions = []
        for peak_idx in peaks:
            if peak_idx < len(self.trajectory):
                transition = {
                    'time': self.time[peak_idx],
                    'shell': self.shells[peak_idx],
                    'entropy': self.entropy[peak_idx],
                    'coherence': self.coherence[peak_idx],
                    'phase_score': phase_scores[peak_idx],
                    'scale_name': self._get_scale_name(self.shells[peak_idx]),
                    'physical_size': self._shell_to_scale(self.shells[peak_idx])
                }
                transitions.append(transition)
        
        return transitions, phase_scores
    
    def _shell_to_scale(self, shell_idx):
        """Convert shell index to physical scale"""
        planck_length = 1.616e-35
        golden_ratio = 1.618
        return planck_length * (golden_ratio ** shell_idx)
    
    def _get_scale_name(self, shell_idx):
        """Get descriptive name for scale"""
        size = self._shell_to_scale(shell_idx)
        
        if size < 1e-30: return "Sub-Planck"
        elif size < 1e-15: return "Quantum Foam"
        elif size < 1e-10: return "Atomic"
        elif size < 1e-6: return "Molecular"
        elif size < 1e-3: return "Cellular" 
        elif size < 1: return "Biological"
        elif size < 1e3: return "Human"
        elif size < 1e6: return "Geological"
        elif size < 1e9: return "Planetary"
        elif size < 1e12: return "Solar System"
        elif size < 1e16: return "Interstellar"
        elif size < 1e21: return "Galactic"
        else: return "Cosmic"
    
    def analyze_reality_crystallization(self):
        """Deep analysis of how reality crystallizes during consciousness evolution"""
        
        print("=== REALITY CRYSTALLIZATION ANALYSIS ===\n")
        
        # Detect phase transitions
        transitions, phase_scores = self.detect_crystallization_points()
        
        print(f"PHASE TRANSITIONS DETECTED: {len(transitions)}\n")
        
        for i, transition in enumerate(transitions):
            print(f"CRYSTALLIZATION EVENT {i+1}:")
            print(f"  Time Step: {transition['time']:,}")
            print(f"  Shell: {transition['shell']} ({transition['scale_name']})")
            print(f"  Physical Scale: {transition['physical_size']:.3e} m")
            print(f"  Entropy Level: {transition['entropy']:.6f}")
            print(f"  Quantum Coherence: {transition['coherence']:.6f}")
            print(f"  Phase Intensity: {transition['phase_score']:.3f}")
            print()
        
        # Analyze the nature of crystallization
        if len(transitions) > 0:
            print("CRYSTALLIZATION PATTERNS:")
            
            # Entropy jumps at transitions
            entropy_jumps = []
            for i, trans in enumerate(transitions):
                idx = trans['time']
                if idx > 100 and idx < len(self.entropy) - 100:
                    before = np.mean(self.entropy[idx-100:idx])
                    after = np.mean(self.entropy[idx:idx+100])
                    jump = after - before
                    entropy_jumps.append(jump)
            
            if entropy_jumps:
                print(f"  Average Entropy Jump: {np.mean(entropy_jumps):.6f}")
                print(f"  Maximum Entropy Jump: {np.max(entropy_jumps):.6f}")
            
            # Scale progression analysis
            shell_jumps = []
            for i in range(1, len(transitions)):
                shell_jump = transitions[i]['shell'] - transitions[i-1]['shell']
                shell_jumps.append(shell_jump)
            
            if shell_jumps:
                print(f"  Average Shell Jump: {np.mean(shell_jumps):.1f}")
                print(f"  Shell Jump Pattern: {shell_jumps}")
            
            # Coherence behavior
            coherence_changes = []
            for trans in transitions:
                coherence_changes.append(trans['coherence'])
            
            print(f"  Coherence at Transitions: {np.mean(coherence_changes):.6f} ± {np.std(coherence_changes):.6f}")
        
        return transitions, phase_scores
    
    def visualize_crystallization(self, transitions, phase_scores):
        """Create visualization of reality crystallization events"""
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor('black')
        
        # 1. Phase score over time
        ax = axes[0, 0]
        ax.set_facecolor('black')
        ax.plot(self.time, phase_scores, 'cyan', alpha=0.7, linewidth=1)
        ax.fill_between(self.time, phase_scores, alpha=0.3, color='cyan')
        
        # Mark transitions
        for trans in transitions:
            ax.axvline(trans['time'], color='red', alpha=0.8, linewidth=2)
            ax.text(trans['time'], max(phase_scores) * 0.9, 
                   f"Shell {trans['shell']}\n{trans['scale_name']}", 
                   rotation=90, color='white', fontsize=8)
        
        ax.set_title('Reality Crystallization Events', color='white')
        ax.set_xlabel('Time Steps', color='white')
        ax.set_ylabel('Phase Transition Intensity', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        # 2. Shell progression with transitions
        ax = axes[0, 1]
        ax.set_facecolor('black')
        ax.plot(self.time, self.shells, 'gold', alpha=0.8, linewidth=1)
        
        for trans in transitions:
            ax.scatter(trans['time'], trans['shell'], 
                      color='red', s=100, alpha=0.8, edgecolors='white')
        
        ax.set_title('Consciousness Scale Evolution', color='white')
        ax.set_xlabel('Time Steps', color='white')
        ax.set_ylabel('Temporal Shell', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        # 3. Entropy evolution with phase transitions
        ax = axes[1, 0]
        ax.set_facecolor('black')
        ax.plot(self.time, self.entropy, 'lime', alpha=0.8, linewidth=2)
        
        for trans in transitions:
            ax.axvline(trans['time'], color='red', alpha=0.6, linewidth=1)
            ax.scatter(trans['time'], trans['entropy'], 
                      color='red', s=80, alpha=0.8)
        
        ax.set_title('Entropy Accumulation & Crystallization', color='white')
        ax.set_xlabel('Time Steps', color='white')
        ax.set_ylabel('Accumulated Entropy', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        # 4. Coherence dynamics
        ax = axes[1, 1]
        ax.set_facecolor('black')
        ax.plot(self.time, self.coherence, 'magenta', alpha=0.8, linewidth=2)
        
        for trans in transitions:
            ax.axvline(trans['time'], color='red', alpha=0.6, linewidth=1)
            ax.scatter(trans['time'], trans['coherence'], 
                      color='red', s=80, alpha=0.8)
        
        ax.set_title('Quantum Coherence & Phase Changes', color='white')
        ax.set_xlabel('Time Steps', color='white')
        ax.set_ylabel('Quantum Coherence', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        plt.tight_layout()
        plt.savefig('reality_crystallization.png', facecolor='black', dpi=300)
        return fig


def analyze_consciousness_crystallization(trajectory):
    """Main function to analyze phase transitions in consciousness evolution"""
    
    detector = PhaseTransitionDetector(trajectory)
    transitions, phase_scores = detector.analyze_reality_crystallization()
    
    if len(transitions) > 0:
        print("\n🔮 REALITY IS CRYSTALLIZING! 🔮")
        print(f"\nDetected {len(transitions)} major phase transitions where consciousness")
        print("undergoes fundamental restructuring across cosmic scales!")
        
        # Create visualization
        detector.visualize_crystallization(transitions, phase_scores)
        print("\nVisualization saved to: reality_crystallization.png")
        
    else:
        print("\nNo major phase transitions detected with current sensitivity.")
        print("Reality appears to flow smoothly across scales...")
    
    return transitions, phase_scores


if __name__ == "__main__":
    print("Phase Transition Detector ready...")
    print("Import and call analyze_consciousness_crystallization(trajectory) to detect crystallization events!")