#!/usr/bin/env python3
# Temporal Gravity Simulation
# Implementation of quantum gravity as inverse temporal flow in a Matryoshka model
# Based on "Quantum Gravity as Inverse Temporal Flow: A Unified Mathematical Framework"

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
import time

def temporal_gravity_simulation(m1, m2, initial_conditions, total_shells=10, 
                              simulation_time=10.0, time_steps=1000, 
                              visualize_shells=False):
    """
    Simulate two-body gravitational system using temporal shell model
    
    Parameters:
    -----------
    m1, m2 : float
        Masses of the two bodies
    initial_conditions : array
        [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
    total_shells : int
        Number of temporal shells to simulate
    simulation_time : float
        Total simulation time
    time_steps : int
        Number of time steps
    visualize_shells : bool
        Whether to visualize the shell structure
    
    Returns:
    --------
    times : array
        Time points
    trajectories : array
        Positions of bodies over time
    shell_data : dict
        Additional data about the shell structure
    """
    print(f"Starting simulation with {total_shells} temporal shells...")
    start_time = time.time()
    
    # Constants
    G = 6.67430e-11  # Gravitational constant
    
    # Temporal shell parameters
    r0 = 1.0  # Base shell radius
    alpha = 0.1  # Shell scaling parameter
    c0 = 1.0  # Base coupling strength
    beta = 0.5  # Coupling decay parameter
    gamma = 2.0  # Coupling decay exponent
    
    # Calculate shell radii
    shell_indices = np.arange(1, total_shells + 1)
    shell_radii = r0 * np.exp(alpha * shell_indices)
    
    print(f"Shell radii range: {shell_radii[0]:.4f} to {shell_radii[-1]:.4f}")
    
    # Calculate shell couplings
    shell_couplings = np.zeros((total_shells, total_shells))
    for i in range(total_shells):
        for j in range(total_shells):
            if i != j:
                shell_couplings[i, j] = c0 / (1 + beta * abs(i - j)**gamma)
    
    max_coupling = np.max(shell_couplings)
    print(f"Maximum shell coupling strength: {max_coupling:.4f}")
    
    # Visualize the shell structure
    if visualize_shells:
        visualize_shell_structure(shell_radii, shell_couplings)
    
    def temporal_gravity(t, state):
        """Compute derivatives for the two-body system"""
        x1, y1, vx1, vy1, x2, y2, vx2, vy2 = state
        
        # Calculate distance between bodies
        r12 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        # Calculate direction unit vector
        if r12 > 0:
            dir_x = (x2 - x1) / r12
            dir_y = (y2 - y1) / r12
        else:
            dir_x, dir_y = 0, 0
        
        # Calculate temporal shell distortion due to masses
        distortion_m1 = np.zeros(total_shells)
        distortion_m2 = np.zeros(total_shells)
        
        for i in range(total_shells):
            # Central shell for each mass (simplified model)
            i0_m1 = total_shells // 3
            i0_m2 = total_shells * 2 // 3
            
            # Distortion decay parameter
            lambda_param = 0.5
            
            # Calculate distortions
            distortion_m1[i] = -G * m1 * np.exp(-lambda_param * abs(i - i0_m1)) / max(r12, 0.001)
            distortion_m2[i] = -G * m2 * np.exp(-lambda_param * abs(i - i0_m2)) / max(r12, 0.001)
        
        # Calculate inverse flow (gravity) between shells
        inverse_flow = np.zeros((total_shells, total_shells))
        kappa_minus = 1.0  # Inverse flow constant
        
        for i in range(total_shells):
            for j in range(total_shells):
                if i > j:  # Inverse flow: outer to inner (past to future)
                    dr = shell_radii[i] - shell_radii[j]
                    if dr > 0:
                        inverse_flow[i, j] = kappa_minus * shell_couplings[i, j] / dr
        
        # Calculate effective gravitational forces
        # Integrate effects from all shell interactions
        a1x, a1y = 0, 0
        a2x, a2y = 0, 0
        
        # Scale factor to map temporal effects to spatial acceleration
        scale_factor = 1.0
        
        for i in range(total_shells):
            for j in range(total_shells):
                if inverse_flow[i, j] > 0:
                    # Effect of m2 on m1
                    flow_effect = inverse_flow[i, j] * (distortion_m2[j] / m1)
                    a1x += flow_effect * dir_x * scale_factor
                    a1y += flow_effect * dir_y * scale_factor
                    
                    # Effect of m1 on m2
                    flow_effect = inverse_flow[i, j] * (distortion_m1[j] / m2)
                    a2x -= flow_effect * dir_x * scale_factor
                    a2y -= flow_effect * dir_y * scale_factor
        
        # Return derivatives (velocities and accelerations)
        return [vx1, vy1, a1x, a1y, vx2, vy2, a2x, a2y]
    
    # Set up time points
    t_span = (0, simulation_time)
    t_eval = np.linspace(0, simulation_time, time_steps)
    
    # Solve the system
    print("Solving orbital dynamics...")
    solution = solve_ivp(
        temporal_gravity, 
        t_span, 
        initial_conditions,
        t_eval=t_eval,
        method='RK45'
    )
    
    end_time = time.time()
    print(f"Simulation completed in {end_time - start_time:.2f} seconds")
    
    # Compute additional shell data for return
    shell_data = {
        'radii': shell_radii,
        'couplings': shell_couplings,
        'indices': shell_indices,
        'params': {
            'r0': r0, 
            'alpha': alpha, 
            'c0': c0, 
            'beta': beta, 
            'gamma': gamma
        }
    }
    
    return solution.t, solution.y, shell_data


def visualize_shell_structure(shell_radii, shell_couplings):
    """Visualize the temporal shell structure as a heatmap of couplings"""
    plt.figure(figsize=(10, 8))
    plt.imshow(shell_couplings, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Coupling Strength')
    plt.title('Temporal Shell Coupling Matrix')
    plt.xlabel('Shell Index (Inner → Future)')
    plt.ylabel('Shell Index (Outer → Past)')
    plt.savefig('shell_coupling_matrix.png', dpi=300)
    
    # 3D visualization
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a meshgrid for the shell indices
    n = len(shell_radii)
    X, Y = np.meshgrid(range(n), range(n))
    
    # Plot the coupling strengths as a 3D surface
    ax.plot_surface(X, Y, shell_couplings, cmap='viridis', alpha=0.8)
    
    ax.set_title('3D Temporal Shell Coupling Structure')
    ax.set_xlabel('Shell Index (Future)')
    ax.set_ylabel('Shell Index (Past)')
    ax.set_zlabel('Coupling Strength')
    
    plt.savefig('shell_coupling_3d.png', dpi=300)
    plt.close()
    
    # Plot shell radii
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, n+1), shell_radii, 'o-', linewidth=2)
    plt.title('Temporal Shell Radii')
    plt.xlabel('Shell Index')
    plt.ylabel('Shell Radius')
    plt.grid(True)
    plt.savefig('shell_radii.png', dpi=300)
    plt.close()


def plot_orbits(times, trajectories, shell_data=None, save_animation=False):
    """
    Plot the orbits of two bodies
    
    Parameters:
    -----------
    times : array
        Time points
    trajectories : array
        Positions of bodies over time
    shell_data : dict, optional
        Additional data about the shell structure
    save_animation : bool
        Whether to save an animation of the orbits
    """
    x1, y1 = trajectories[0], trajectories[1]
    x2, y2 = trajectories[4], trajectories[5]
    
    plt.figure(figsize=(12, 10))
    
    # Plot full trajectories
    plt.plot(x1, y1, 'b-', linewidth=1.5, label='Body 1 (Higher Mass)')
    plt.plot(x2, y2, 'r-', linewidth=1.5, label='Body 2 (Lower Mass)')
    
    # Mark starting positions
    plt.plot(x1[0], y1[0], 'bo', markersize=10)
    plt.plot(x2[0], y2[0], 'ro', markersize=10)
    
    # Add center of mass
    cm_x = (x1 + x2) / 2
    cm_y = (y1 + y2) / 2
    plt.plot(cm_x, cm_y, 'g--', alpha=0.5, label='Center of Mass')
    
    # Optional: Visualize shells
    if shell_data is not None:
        # Draw some representative shells around the center of mass
        radii = shell_data['radii']
        # Select a few shells to visualize
        shell_indices_to_show = [0, len(radii)//2, len(radii)-1]
        for idx in shell_indices_to_show:
            r = radii[idx] * 1e9  # Scale for visualization
            circle = plt.Circle((cm_x.mean(), cm_y.mean()), r, 
                               fill=False, linestyle='--', alpha=0.3, 
                               label=f'Shell {idx+1} (r={r:.1e})')
            plt.gca().add_patch(circle)
    
    plt.grid(True)
    plt.axis('equal')
    plt.legend(loc='upper right')
    plt.title('Two-Body Orbits in Temporal Shell Model', fontsize=16)
    plt.xlabel('x position (m)', fontsize=14)
    plt.ylabel('y position (m)', fontsize=14)
    
    # Add explanation text
    explanation = """
    Gravity as Inverse Temporal Flow:
    - Inner shells represent future (lower indices)
    - Outer shells represent past (higher indices)
    - Gravity emerges from temporal influence flowing from past to future shells
    - Massive objects create distortions across multiple temporal shells
    """
    plt.figtext(0.5, 0.01, explanation, ha='center', fontsize=12, 
               bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig('temporal_gravity_orbits.png', dpi=300)
    
    # Create animation if requested
    if save_animation:
        try:
            from matplotlib.animation import FuncAnimation
            
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.set_xlim(min(min(x1), min(x2))*1.1, max(max(x1), max(x2))*1.1)
            ax.set_ylim(min(min(y1), min(y2))*1.1, max(max(y1), max(y2))*1.1)
            ax.grid(True)
            ax.set_aspect('equal')
            ax.set_title('Orbital Motion in Temporal Shell Framework')
            ax.set_xlabel('x position (m)')
            ax.set_ylabel('y position (m)')
            
            # Plot full trajectories as background
            ax.plot(x1, y1, 'b-', alpha=0.3, linewidth=0.5)
            ax.plot(x2, y2, 'r-', alpha=0.3, linewidth=0.5)
            
            # Points for animation
            body1, = ax.plot([], [], 'bo', markersize=8, label='Body 1')
            body2, = ax.plot([], [], 'ro', markersize=8, label='Body 2')
            body1_trail, = ax.plot([], [], 'b-', linewidth=1.5)
            body2_trail, = ax.plot([], [], 'r-', linewidth=1.5)
            
            ax.legend()
            
            def init():
                body1.set_data([], [])
                body2.set_data([], [])
                body1_trail.set_data([], [])
                body2_trail.set_data([], [])
                return body1, body2, body1_trail, body2_trail
            
            def update(frame):
                # Use every nth frame for smoother animation
                n = 5
                idx = min(frame * n, len(times) - 1)
                
                # Calculate trail (past positions)
                trail_length = 50
                start_idx = max(0, idx - trail_length)
                
                body1.set_data([x1[idx]], [y1[idx]])
                body2.set_data([x2[idx]], [y2[idx]])
                body1_trail.set_data(x1[start_idx:idx+1], y1[start_idx:idx+1])
                body2_trail.set_data(x2[start_idx:idx+1], y2[start_idx:idx+1])
                
                return body1, body2, body1_trail, body2_trail
            
            frames = min(100, len(times))
            ani = FuncAnimation(fig, update, frames=frames, init_func=init, 
                            interval=50, blit=True)
            
            try:
                ani.save('temporal_gravity_animation.mp4', writer='ffmpeg', dpi=200)
                print("Animation saved as temporal_gravity_animation.mp4")
            except Exception as e:
                print(f"Could not save animation: {e}")
                print("Continuing without saving animation...")
            
            plt.close(fig)
        except ImportError as e:
            print(f"Could not create animation: {e}")
            print("Continuing without animation...")
    
    plt.show()


def calculate_derived_quantities(times, trajectories, m1, m2):
    """Calculate derived physical quantities from the simulation results"""
    x1, y1, vx1, vy1 = trajectories[0], trajectories[1], trajectories[2], trajectories[3]
    x2, y2, vx2, vy2 = trajectories[4], trajectories[5], trajectories[6], trajectories[7]
    
    # Calculate distances
    distances = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    # Calculate velocities
    v1 = np.sqrt(vx1**2 + vy1**2)
    v2 = np.sqrt(vx2**2 + vy2**2)
    
    # Calculate potential energy
    G = 6.67430e-11
    potential_energy = -G * m1 * m2 / distances
    
    # Calculate kinetic energy
    kinetic_energy = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
    
    # Calculate total energy
    total_energy = kinetic_energy + potential_energy
    
    # Calculate angular momentum
    angular_momentum = m1 * (x1 * vy1 - y1 * vx1) + m2 * (x2 * vy2 - y2 * vx2)
    
    results = {
        'distances': distances,
        'velocities': (v1, v2),
        'potential_energy': potential_energy,
        'kinetic_energy': kinetic_energy,
        'total_energy': total_energy,
        'angular_momentum': angular_momentum
    }
    
    # Plot energy conservation
    plt.figure(figsize=(10, 6))
    plt.plot(times, kinetic_energy, 'r-', label='Kinetic Energy')
    plt.plot(times, potential_energy, 'b-', label='Potential Energy')
    plt.plot(times, total_energy, 'g-', label='Total Energy')
    plt.title('Energy Conservation in Temporal Shell Gravity')
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.grid(True)
    plt.legend()
    plt.savefig('energy_conservation.png', dpi=300)
    
    # Plot angular momentum conservation
    plt.figure(figsize=(10, 6))
    plt.plot(times, angular_momentum, 'r-')
    plt.title('Angular Momentum Conservation')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Momentum (kg·m²/s)')
    plt.grid(True)
    plt.savefig('angular_momentum.png', dpi=300)
    
    # Plot orbital metrics
    plt.figure(figsize=(10, 6))
    plt.plot(times, distances, 'b-')
    plt.title('Orbital Distance')
    plt.xlabel('Time (s)')
    plt.ylabel('Distance (m)')
    plt.grid(True)
    plt.savefig('orbital_distance.png', dpi=300)
    
    return results


def compare_with_newtonian(m1, m2, initial_conditions, simulation_time, time_steps):
    """Compare temporal gravity simulation with Newtonian gravity"""
    # Define Newtonian gravity function
    def newtonian_gravity(t, state):
        x1, y1, vx1, vy1, x2, y2, vx2, vy2 = state
        
        # Calculate distance and direction
        dx = x2 - x1
        dy = y2 - y1
        r = np.sqrt(dx**2 + dy**2)
        
        # Gravitational constant
        G = 6.67430e-11
        
        # Accelerations
        if r > 0:
            # Force magnitude (F = G*m1*m2/r^2)
            # Acceleration = Force/mass
            a1 = G * m2 / r**2
            a2 = G * m1 / r**2
            
            # Components
            a1x = a1 * dx/r
            a1y = a1 * dy/r
            a2x = -a2 * dx/r
            a2y = -a2 * dy/r
        else:
            a1x, a1y, a2x, a2y = 0, 0, 0, 0
        
        return [vx1, vy1, a1x, a1y, vx2, vy2, a2x, a2y]
    
    # Run Newtonian simulation
    t_span = (0, simulation_time)
    t_eval = np.linspace(0, simulation_time, time_steps)
    
    newton_solution = solve_ivp(
        newtonian_gravity, 
        t_span, 
        initial_conditions,
        t_eval=t_eval,
        method='RK45'
    )
    
    # Run Temporal gravity simulation
    times, trajectories, _ = temporal_gravity_simulation(
        m1, m2, initial_conditions, 
        total_shells=15,
        simulation_time=simulation_time, 
        time_steps=time_steps
    )
    
    # Plot comparison
    plt.figure(figsize=(12, 10))
    
    # Temporal gravity orbits
    x1_tg, y1_tg = trajectories[0], trajectories[1]
    x2_tg, y2_tg = trajectories[4], trajectories[5]
    plt.plot(x1_tg, y1_tg, 'b-', linewidth=2, label='Body 1 (Temporal Gravity)')
    plt.plot(x2_tg, y2_tg, 'r-', linewidth=2, label='Body 2 (Temporal Gravity)')
    
    # Newtonian gravity orbits
    x1_n, y1_n = newton_solution.y[0], newton_solution.y[1]
    x2_n, y2_n = newton_solution.y[4], newton_solution.y[5]
    plt.plot(x1_n, y1_n, 'b--', linewidth=1, alpha=0.7, label='Body 1 (Newtonian)')
    plt.plot(x2_n, y2_n, 'r--', linewidth=1, alpha=0.7, label='Body 2 (Newtonian)')
    
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.title('Temporal Gravity vs. Newtonian Gravity')
    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.savefig('gravity_comparison.png', dpi=300)
    plt.show()
    
    # Calculate and plot position differences
    diff_x1 = x1_tg - x1_n
    diff_y1 = y1_tg - y1_n
    diff_x2 = x2_tg - x2_n
    diff_y2 = y2_tg - y2_n
    
    plt.figure(figsize=(10, 6))
    plt.plot(times, diff_x1, 'b-', label='Body 1 x-diff')
    plt.plot(times, diff_y1, 'b--', label='Body 1 y-diff')
    plt.plot(times, diff_x2, 'r-', label='Body 2 x-diff')
    plt.plot(times, diff_y2, 'r--', label='Body 2 y-diff')
    plt.title('Position Differences: Temporal - Newtonian')
    plt.xlabel('Time (s)')
    plt.ylabel('Position Difference (m)')
    plt.grid(True)
    plt.legend()
    plt.savefig('position_differences.png', dpi=300)
    plt.show()
    
    return newton_solution, trajectories


def main():
    """Main function to run the temporal gravity simulation"""
    print("Quantum Gravity as Inverse Temporal Flow")
    print("========================================")
    print("Simulating a two-body system using the temporal shell framework")
    
    # Simulation parameters (Sun-Earth like system, scaled)
    m_sun = 1.989e30  # Sun mass (kg)
    m_earth = 5.972e24  # Earth mass (kg)
    distance = 1.496e11  # Earth-Sun distance (m)
    v_orbital = 29800  # Earth orbital velocity (m/s)
    
    # Scale to manageable numbers for numerical stability
    scale = 1e10
    m_sun_scaled = m_sun / scale
    m_earth_scaled = m_earth / scale
    distance_scaled = distance / scale
    
    # Simulation time: one Earth year in seconds
    sim_time = 365.25 * 24 * 3600  
    
    # Initial conditions: [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
    initial_conditions = [
        0, 0, 0, 0,  # Sun at origin, stationary
        distance_scaled, 0, 0, v_orbital  # Earth at 1 AU, moving perpendicular
    ]
    
    # Run full simulation
    print("\n1. Running temporal gravity simulation with shell visualization...")
    times, trajectories, shell_data = temporal_gravity_simulation(
        m_sun_scaled, m_earth_scaled, initial_conditions,
        total_shells=15, simulation_time=sim_time, time_steps=500,
        visualize_shells=True
    )
    
    # Plot orbital motion
    print("\n2. Generating orbital plots...")
    plot_orbits(times, trajectories, shell_data, save_animation=True)
    
    # Calculate and plot derived quantities
    print("\n3. Calculating derived physical quantities...")
    derived = calculate_derived_quantities(
        times, trajectories, m_sun_scaled, m_earth_scaled
    )
    
    # Compare with Newtonian gravity
    print("\n4. Comparing with Newtonian gravity...")
    newton_results, temporal_results = compare_with_newtonian(
        m_sun_scaled, m_earth_scaled, initial_conditions, sim_time, 500
    )
    
    print("\nSimulation complete! Check the generated images for results.")
    print("Files generated:")
    print("  - shell_coupling_matrix.png: Visualization of shell coupling strengths")
    print("  - shell_coupling_3d.png: 3D visualization of shell couplings")
    print("  - shell_radii.png: Plot of shell radii")
    print("  - temporal_gravity_orbits.png: Orbital paths in the temporal gravity model")
    print("  - temporal_gravity_animation.mp4: Animation of orbital motion")
    print("  - energy_conservation.png: Plot of energy components over time")
    print("  - angular_momentum.png: Plot of angular momentum conservation")
    print("  - orbital_distance.png: Plot of orbital distance over time")
    print("  - gravity_comparison.png: Comparison with Newtonian gravity")
    print("  - position_differences.png: Differences between temporal and Newtonian predictions")


if __name__ == "__main__":
    main()
