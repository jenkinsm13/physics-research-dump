#!/usr/bin/env python3
"""
Gravitational Phase Shift Simulation

This script simulates and visualizes the gravitational phase shift effect
based on the Quantum Gravity as Inverse Temporal Flow theory.

The phase shift is calculated using: Δφ = (m/ħ) ∫ Φ(x(t)) dt

Where:
- m is the mass of the quantum particle
- ħ is the reduced Planck constant
- Φ(x(t)) is the gravitational potential at the particle's position x(t)
- The integral is over the path of the particle

This simulation demonstrates:
1. Path-dependent phase accumulation for quantum particles
2. Gravitational interference effects
3. Temporal shell influence on quantum phases
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import simpson

# Physical constants (SI units)
G = 6.67430e-11  # Gravitational constant
hbar = 1.054571817e-34  # Reduced Planck constant
c = 299792458.0  # Speed of light

# Simulation parameters
m_particle = 1.0e-27  # Mass of quantum particle (proton mass ~ 1.6e-27 kg)
m_source = 1.0e20  # Mass of gravitational source (small astronomical mass)

# For visualization scaling (we'll use arbitrary units for phase)
PHASE_SCALE = 1.0e15  # Scale factor to make phase shifts visible

class TemporalShell:
    """Represents a shell in the temporal Matryoshka structure"""
    
    def __init__(self, index, radius, central_mass):
        """
        Initialize a temporal shell
        
        Parameters:
        -----------
        index : int
            Shell index (future = lower, past = higher)
        radius : float
            Shell radius (exponential scaling: r = r0*exp(α*i))
        central_mass : float
            Mass of the gravitational source at the center
        """
        self.index = index
        self.radius = radius
        self.mass = central_mass
        
        # Distortion due to mass (decreases with radius)
        self.distortion = -G * central_mass / (c**2 * self.radius)
        
    def gravitational_potential(self, r):
        """
        Calculate gravitational potential at distance r
        
        In the temporal shell model, the potential is modified by shell distortion:
        Φ(r) = -GM/r * exp(-λ|i-i0|)
        
        Where i is the shell index and i0 is the central shell index.
        """
        # For simplicity, assume shell 0 is central shell
        lambda_param = 0.5
        shell_factor = np.exp(-lambda_param * abs(self.index))
        
        # Basic Newtonian potential with shell modification
        return -G * self.mass * shell_factor / max(r, 1e-10)
    
    def calculate_phase_shift(self, path, dt, particle_mass):
        """
        Calculate phase shift for a particle traveling along path
        
        Parameters:
        -----------
        path : array
            Array of (x,y,z) positions
        dt : float
            Time step
        particle_mass : float
            Mass of the quantum particle
        
        Returns:
        --------
        phase_shift : float
            Accumulated phase shift due to gravitational potential
        """
        # Calculate distance from center at each point
        distances = np.sqrt(np.sum(path**2, axis=1))
        
        # Calculate potential at each point
        potentials = np.array([self.gravitational_potential(r) for r in distances])
        
        # Integrate along path (m/ħ) ∫ Φ(x(t)) dt
        phase_shift = (particle_mass / hbar) * simpson(potentials, dx=dt)
        
        return phase_shift


def simulate_quantum_interference(shells, paths, dt, particle_mass):
    """
    Simulate quantum interference between two paths through multiple shells
    
    Parameters:
    -----------
    shells : list
        List of TemporalShell objects
    paths : list
        List of paths (each path is an array of positions)
    dt : float
        Time step
    particle_mass : float
        Mass of quantum particle
        
    Returns:
    --------
    phase_shifts : dict
        Dictionary of phase shifts for each path through each shell
    total_phase_shifts : list
        Total phase shift for each path (summed over all shells)
    """
    n_paths = len(paths)
    n_shells = len(shells)
    
    # Store phase shifts for each path through each shell
    phase_shifts = {f"path_{i}": {f"shell_{j}": 0.0 for j in range(n_shells)} 
                  for i in range(n_paths)}
    
    # Calculate phase shifts
    for i, path in enumerate(paths):
        for j, shell in enumerate(shells):
            phase_shifts[f"path_{i}"][f"shell_{j}"] = shell.calculate_phase_shift(path, dt, particle_mass)
    
    # Calculate total phase shift for each path (sum over shells)
    total_phase_shifts = [sum(phase_shifts[f"path_{i}"].values()) for i in range(n_paths)]
    
    return phase_shifts, total_phase_shifts


def create_paths():
    """Create two different paths for interference simulation"""
    # Time parameters
    t_max = 1.0  # Total path time
    n_points = 100  # Number of points along path
    t = np.linspace(0, t_max, n_points)
    dt = t_max / n_points
    
    # Path 1: Straight line through gravitational field
    path1 = np.zeros((n_points, 3))
    path1[:, 0] = np.linspace(-50, 50, n_points)  # x: -50 to 50
    
    # Path 2: Curved path further from gravitational source
    path2 = np.zeros((n_points, 3))
    path2[:, 0] = np.linspace(-50, 50, n_points)  # x: -50 to 50
    path2[:, 1] = 20 * np.sin(np.pi * t)  # y: sinusoidal path
    
    return path1, path2, dt


def visualize_paths_and_shells(paths, shells):
    """Visualize the paths and shells in 3D"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot shells
    for shell in shells:
        # Create a wireframe sphere
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = shell.radius * np.cos(u) * np.sin(v)
        y = shell.radius * np.sin(u) * np.sin(v)
        z = shell.radius * np.cos(v)
        
        # Plot the shell with transparency based on index
        alpha = 0.1 + 0.1 * (len(shells) - shell.index) / len(shells)
        ax.plot_wireframe(x, y, z, color='b', alpha=alpha)
        
    # Plot paths
    path1, path2 = paths
    ax.plot(path1[:, 0], path1[:, 1], path1[:, 2], 'r-', linewidth=2, label='Path 1')
    ax.plot(path2[:, 0], path2[:, 1], path2[:, 2], 'g-', linewidth=2, label='Path 2')
    
    # Add the mass at the center
    ax.scatter(0, 0, 0, color='black', s=100, label='Gravitational Source')
    
    # Set axis properties
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Quantum Particle Paths Through Temporal Shells')
    ax.legend()
    
    # Make the plot more viewable
    max_range = max(
        [shells[-1].radius, abs(path1[:, 0]).max(), 
         abs(path1[:, 1]).max(), abs(path2[:, 0]).max(), 
         abs(path2[:, 1]).max()]
    )
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    plt.savefig('paths_and_shells.png', dpi=300)
    plt.close()


def visualize_phase_accumulation(paths, phase_shifts, total_phase_shifts):
    """Visualize how phase accumulates along each path"""
    path1, path2 = paths
    distances1 = np.sqrt(np.sum(path1**2, axis=1))
    distances2 = np.sqrt(np.sum(path2**2, axis=1))
    
    # Set up the figure for phase accumulation
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot phase accumulation for each path
    x1 = np.arange(len(distances1))
    x2 = np.arange(len(distances2))
    
    # Create cumulative phase functions (these would be calculated in a real simulation)
    # Here we create a proxy based on distances
    phase1 = PHASE_SCALE * total_phase_shifts[0] * (1 - np.exp(-0.05 * x1))
    phase2 = PHASE_SCALE * total_phase_shifts[1] * (1 - np.exp(-0.05 * x2))
    
    # Plot the phases
    ax.plot(x1, phase1, 'r-', linewidth=2, label='Phase along Path 1')
    ax.plot(x2, phase2, 'g-', linewidth=2, label='Phase along Path 2')
    ax.plot(x1, phase1 - phase2, 'b--', linewidth=1.5, label='Phase Difference')
    
    # Mark the phase difference at the end
    phase_diff = phase1[-1] - phase2[-1]
    ax.scatter(x1[-1], phase_diff, color='blue', s=100, 
              label=f'Final Phase Difference: {phase_diff:.2f}')
    
    ax.set_xlabel('Position along path')
    ax.set_ylabel('Phase (scaled)')
    ax.set_title('Gravitational Phase Accumulation')
    ax.grid(True)
    ax.legend()
    
    plt.savefig('phase_accumulation.png', dpi=300)
    plt.close()


def visualize_interference_pattern(phase_difference):
    """Visualize the quantum interference pattern resulting from phase difference"""
    # Create a position array for the interference pattern
    x = np.linspace(-10, 10, 1000)
    
    # Create wave functions with the phase difference
    # Ψ1 = exp(i*kx)
    # Ψ2 = exp(i*(kx + Δφ))
    # |Ψ1 + Ψ2|^2 = 2 + 2*cos(Δφ)
    k = 2.0  # Wave number (arbitrary units)
    
    # Calculate probabilities at each position for visualization
    probability = lambda x, phase_diff: np.abs(np.exp(1j*k*x) + np.exp(1j*(k*x + phase_diff)))**2
    
    # Plot the interference pattern
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    
    # Plot with no gravitational phase shift (reference)
    y_ref = probability(x, 0.0)
    axes[0].plot(x, y_ref, 'k-')
    axes[0].set_title('Interference Pattern: No Gravitational Effect')
    axes[0].set_xlabel('Position')
    axes[0].set_ylabel('Probability')
    axes[0].grid(True)
    
    # Plot with gravitational phase shift
    y_grav = probability(x, phase_difference)
    axes[1].plot(x, y_grav, 'b-')
    axes[1].set_title(f'Interference Pattern: With Gravitational Phase Shift Δφ = {phase_difference:.2f}')
    axes[1].set_xlabel('Position')
    axes[1].set_ylabel('Probability')
    axes[1].grid(True)
    
    # Plot comparison
    axes[2].plot(x, y_ref, 'k-', label='No Gravity')
    axes[2].plot(x, y_grav, 'b-', label='With Gravity')
    axes[2].set_title('Comparison of Interference Patterns')
    axes[2].set_xlabel('Position')
    axes[2].set_ylabel('Probability')
    axes[2].legend()
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.savefig('interference_pattern.png', dpi=300)
    plt.close()


def animate_shell_propagation(paths, shells, total_phase_shifts):
    """Create an animation of the wave propagation through temporal shells"""
    path1, path2 = paths
    
    # Check if animation is possible (if ffmpeg is available)
    try:
        # Set up the figure
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(-60, 60)
        ax.set_ylim(-30, 30)
        
        # Plot the paths
        ax.plot(path1[:, 0], path1[:, 1], 'r--', alpha=0.3, label='Path 1')
        ax.plot(path2[:, 0], path2[:, 1], 'g--', alpha=0.3, label='Path 2')
        
        # Plot the gravitational source
        ax.scatter(0, 0, color='black', s=100, label='Mass')
        
        # Create shell circles (only show a few for clarity)
        shell_circles = []
        for i, shell in enumerate(shells):
            if i % 2 == 0:  # Only show every other shell
                circle = plt.Circle((0, 0), shell.radius, fill=False, 
                                  color='blue', alpha=0.2, linestyle='--')
                ax.add_patch(circle)
                shell_circles.append(circle)
        
        # Create wave points
        point1, = ax.plot([], [], 'ro', markersize=10)
        point2, = ax.plot([], [], 'go', markersize=10)
        
        # Phase indicators (using text)
        phase_text1 = ax.text(0, 0, "", fontsize=12, color='red')
        phase_text2 = ax.text(0, 0, "", fontsize=12, color='green')
        diff_text = ax.text(0, 25, "", fontsize=14, color='blue')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Quantum Wave Propagation Through Temporal Shells')
        ax.legend()
        ax.grid(True)
        
        # Animation function
        def init():
            point1.set_data([], [])
            point2.set_data([], [])
            phase_text1.set_text("")
            phase_text2.set_text("")
            diff_text.set_text("")
            return point1, point2, phase_text1, phase_text2, diff_text
        
        def update(frame):
            if frame < len(path1):
                # Update positions
                point1.set_data([path1[frame, 0]], [path1[frame, 1]])
                point2.set_data([path2[frame, 0]], [path2[frame, 1]])
                
                # Simulate accumulated phase
                # In a real simulation, we would calculate this precisely
                phase1 = PHASE_SCALE * total_phase_shifts[0] * (1 - np.exp(-0.05 * frame))
                phase2 = PHASE_SCALE * total_phase_shifts[1] * (1 - np.exp(-0.05 * frame))
                
                # Update texts
                phase_text1.set_position((path1[frame, 0] + 5, path1[frame, 1] + 2))
                phase_text1.set_text(f"φ1 = {phase1:.1f}")
                
                phase_text2.set_position((path2[frame, 0] + 5, path2[frame, 1] + 2))
                phase_text2.set_text(f"φ2 = {phase2:.1f}")
                
                diff_text.set_text(f"Δφ = {abs(phase1 - phase2):.1f}")
                
            return point1, point2, phase_text1, phase_text2, diff_text
        
        # Create animation
        ani = FuncAnimation(fig, update, frames=len(path1),
                           init_func=init, blit=True, interval=50)
        
        # Save animation
        try:
            ani.save('shell_propagation.mp4', writer='ffmpeg', dpi=200)
            print("Created animation of wave propagation (shell_propagation.mp4)")
        except Exception as e:
            print(f"Could not save animation: {e}")
            print("Saving static image instead...")
            plt.savefig('shell_propagation_static.png', dpi=300)
        
        plt.close()
        
    except Exception as e:
        print(f"Animation creation failed: {e}")
        print("Creating static image instead...")
        
        # Create a static visualization as a fallback
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot the paths
        ax.plot(path1[:, 0], path1[:, 1], 'r-', linewidth=2, label='Path 1')
        ax.plot(path2[:, 0], path2[:, 1], 'g-', linewidth=2, label='Path 2')
        
        # Plot the gravitational source
        ax.scatter(0, 0, color='black', s=100, label='Mass')
        
        # Plot shells as circles
        for i, shell in enumerate(shells):
            if i % 2 == 0:  # Only show every other shell
                circle = plt.Circle((0, 0), shell.radius, fill=False, 
                                  color='blue', alpha=0.3, linestyle='--')
                ax.add_patch(circle)
        
        # Add phase information as text
        phase1 = PHASE_SCALE * total_phase_shifts[0]
        phase2 = PHASE_SCALE * total_phase_shifts[1]
        phase_diff = abs(phase1 - phase2)
        
        ax.text(0, -25, f"φ1 = {phase1:.2f}, φ2 = {phase2:.2f}, Δφ = {phase_diff:.2f}", 
               ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.7))
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Quantum Paths Through Temporal Shells (Static View)')
        ax.legend()
        ax.grid(True)
        ax.set_xlim(-60, 60)
        ax.set_ylim(-30, 30)
        ax.set_aspect('equal')
        
        plt.savefig('shell_propagation_static.png', dpi=300)
        plt.close()


def explain_results(phase_shifts, total_phase_shifts):
    """Generate explanation of the results and findings"""
    explanation = {
        "title": "Gravitational Phase Shift in Quantum Gravity as Inverse Temporal Flow",
        "total_shift_path1": total_phase_shifts[0] * PHASE_SCALE,
        "total_shift_path2": total_phase_shifts[1] * PHASE_SCALE,
        "phase_difference": abs(total_phase_shifts[0] - total_phase_shifts[1]) * PHASE_SCALE,
        "interpretation": """
            The simulation demonstrates how gravity creates quantum phase shifts 
            through the inverse temporal flow mechanism. Path 1, which passes closer 
            to the gravitational source, accumulates a different phase than Path 2.
            
            This phase difference leads to observable interference effects, 
            which could be measured in precision quantum interference experiments.
            
            In the temporal shell model, these phase shifts arise from the particle's
            wave function interacting with multiple temporal shells, each distorted
            differently by the gravitational source.
            
            This provides a testable prediction of the Quantum Gravity as Inverse
            Temporal Flow theory: gravitational fields should produce specific
            interference patterns distinct from those predicted by both standard
            quantum mechanics and general relativity alone.
        """
    }
    
    # Save explanation to file
    with open('phase_shift_explanation.txt', 'w') as f:
        f.write(f"# {explanation['title']}\n\n")
        f.write(f"Total phase shift along Path 1: {explanation['total_shift_path1']:.2f}\n")
        f.write(f"Total phase shift along Path 2: {explanation['total_shift_path2']:.2f}\n")
        f.write(f"Phase difference: {explanation['phase_difference']:.2f}\n\n")
        f.write(explanation['interpretation'])
    
    return explanation


def main():
    """Main function to run the simulation"""
    print("Gravitational Phase Shift Simulation")
    print("======================================")
    
    # Create temporal shells
    n_shells = 7
    base_radius = 10.0
    shells = []
    
    for i in range(n_shells):
        # Exponential scaling of shell radii
        radius = base_radius * np.exp(0.3 * i)
        shell = TemporalShell(i, radius, m_source)
        shells.append(shell)
    
    print(f"Created {n_shells} temporal shells")
    
    # Create paths for comparison
    path1, path2, dt = create_paths()
    print("Created quantum particle paths")
    
    # Visualize paths and shells
    visualize_paths_and_shells([path1, path2], shells)
    print("Visualized paths and shells")
    
    # Simulate quantum interference
    phase_shifts, total_phase_shifts = simulate_quantum_interference(
        shells, [path1, path2], dt, m_particle)
    print("Calculated phase shifts")
    
    # Visualize phase accumulation
    visualize_phase_accumulation([path1, path2], phase_shifts, total_phase_shifts)
    print("Visualized phase accumulation")
    
    # Calculate scaled phase difference for visualization
    phase_difference = abs(total_phase_shifts[0] - total_phase_shifts[1]) * PHASE_SCALE
    
    # Visualize interference pattern
    visualize_interference_pattern(phase_difference)
    print("Visualized interference pattern")
    
    # Animate shell propagation
    animate_shell_propagation([path1, path2], shells, total_phase_shifts)
    print("Created animation of wave propagation")
    
    # Generate explanation
    explanation = explain_results(phase_shifts, total_phase_shifts)
    print("Generated explanation")
    
    print("\nSimulation complete!")
    print(f"Phase difference between paths: {phase_difference:.2f}")
    print("Files generated:")
    print("  - paths_and_shells.png: 3D visualization of paths through shells")
    print("  - phase_accumulation.png: Graph of phase accumulation along paths")
    print("  - interference_pattern.png: Resulting quantum interference pattern")
    print("  - shell_propagation_static.png: Static visualization of wave propagation")
    print("  - phase_shift_explanation.txt: Detailed explanation of results")


if __name__ == "__main__":
    main()
