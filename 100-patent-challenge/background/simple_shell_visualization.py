#!/usr/bin/env python3
"""
Simple Temporal Shell Visualization

This script creates an intuitive visualization of the temporal shell structure
with future shells at the top, past shells at the bottom, a mass in the middle,
and quantum particles traveling through the structure.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.collections import PatchCollection

def create_simplified_shell_visualization():
    """Create a simplified visualization of temporal shells with quantum paths"""
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 12))
    
    # Set up the axis
    ax.set_xlim(-5, 5)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide the axes for cleaner visualization
    
    # Create temporal shells (ellipses that are wider at the bottom)
    shells = []
    labels = []
    
    # Define shell parameters
    num_shells = 7
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, num_shells))
    
    # Create shells
    for i in range(num_shells):
        # Calculate position and size
        # Future shells (top) are smaller, past shells (bottom) are larger
        y_pos = 3 - i  # Start at top (future)
        
        # Ellipse parameters - wider at bottom (past)
        width = 3 + 0.5 * i
        height = 1 + 0.2 * i
        
        # Create elliptical shell
        shell = plt.matplotlib.patches.Ellipse((0, y_pos), width, height, 
                                             fill=False, edgecolor=colors[i], 
                                             linewidth=2, alpha=0.7)
        shells.append(shell)
        
        # Add shell label
        if i == 0:
            labels.append(ax.text(3.5, y_pos, "Distant Future (Shell 6)", 
                              fontsize=12, ha='left', va='center'))
        elif i == num_shells - 1:
            labels.append(ax.text(3.5, y_pos, "Distant Past (Shell 0)", 
                              fontsize=12, ha='left', va='center'))
        elif i == num_shells // 2:
            labels.append(ax.text(3.5, y_pos, "Present Moment (Shell 3)", 
                              fontsize=12, ha='left', va='center', 
                              bbox=dict(facecolor='white', alpha=0.7)))
    
    # Add shells to plot
    for shell in shells:
        ax.add_patch(shell)
    
    # Create mass in the middle (slightly above center to be near present)
    mass_y = 0  # Near the present moment
    mass = plt.Circle((0, mass_y), 0.5, color='black', zorder=10)
    ax.add_patch(mass)
    ax.text(0, mass_y, "M", color='white', ha='center', va='center', 
           fontsize=14, fontweight='bold', zorder=11)
    
    # Add mass label
    ax.text(0, mass_y - 0.8, "Massive Object", ha='center', va='top', 
           fontsize=12, bbox=dict(facecolor='white', alpha=0.7))
    
    # Create shell distortion (using partially transparent patches)
    distortion_patches = []
    
    # Parameters for distortion
    dist_colors = plt.cm.Oranges(np.linspace(0.3, 0.7, 3))
    
    # Create distortion zones
    for i, (radius, alpha) in enumerate(zip([2.0, 1.3, 0.8], [0.2, 0.3, 0.4])):
        distortion = plt.Circle((0, mass_y), radius, color=dist_colors[i], 
                              alpha=alpha, zorder=2)
        distortion_patches.append(distortion)
    
    # Add distortion to plot
    for patch in distortion_patches:
        ax.add_patch(patch)
    
    # Add distortion label
    ax.text(1.7, mass_y + 0.3, "Shell Distortion\nfrom Mass", ha='center', va='center', 
           fontsize=10, bbox=dict(facecolor='white', alpha=0.7), zorder=12)
    
    # Create quantum particle paths
    # Path 1: Close to mass
    x1 = np.linspace(-4, 4, 100)
    y1 = np.zeros_like(x1) + 0.8  # Just above the mass
    
    # Path 2: Far from mass
    x2 = np.linspace(-4, 4, 100)
    y2 = np.zeros_like(x2) - 2.0  # Below the mass, avoiding strong distortion
    
    # Plot paths
    ax.plot(x1, y1, 'r-', linewidth=2, zorder=5, label="Path 1 (Close to Mass)")
    ax.plot(x2, y2, 'g-', linewidth=2, zorder=5, label="Path 2 (Far from Mass)")
    
    # Add arrows to show direction
    arrow_props = dict(arrowstyle='->', linewidth=2, shrinkA=0, shrinkB=0, zorder=6)
    
    # Add arrows along the paths
    for x, y, color in zip([x1, x2], [y1, y2], ['r', 'g']):
        indices = [25, 50, 75]  # Positions for arrows
        for idx in indices:
            # Calculate direction for the arrow
            dx = 0.001 * (x[idx+1] - x[idx-1])
            dy = 0.001 * (y[idx+1] - y[idx-1])
            arrow = FancyArrowPatch((x[idx]-dx, y[idx]-dy), (x[idx]+dx, y[idx]+dy), 
                                  color=color, **arrow_props)
            ax.add_patch(arrow)
    
    # Add particle labels
    ax.text(3.8, y1[0], "Quantum\nParticle 1", color='red', ha='left', va='center', 
           fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
    ax.text(3.8, y2[0], "Quantum\nParticle 2", color='green', ha='left', va='center', 
           fontsize=10, bbox=dict(facecolor='white', alpha=0.7))
    
    # Add major temporal flow arrow (future to past)
    time_arrow = FancyArrowPatch((-4.5, 4), (-4.5, -4), color='blue', 
                               arrowstyle='-|>', linewidth=3, 
                               mutation_scale=20)
    ax.add_patch(time_arrow)
    ax.text(-4.5, 4.3, "Forward Time Flow\n(Future → Past)", 
           color='blue', ha='center', va='bottom', fontsize=12)
    
    # Add inverse flow arrow (past to future, gravity)
    gravity_arrow = FancyArrowPatch((-4.0, -4), (-4.0, 4), color='purple', 
                                 arrowstyle='-|>', linewidth=3, 
                                 linestyle='--', mutation_scale=20)
    ax.add_patch(gravity_arrow)
    ax.text(-4.0, -4.3, "Inverse Flow\n(Gravity)", 
           color='purple', ha='center', va='top', fontsize=12)
    
    # Add phase information
    ax.text(-3, 5, "Quantum Phase Accumulation:", fontsize=14, fontweight='bold')
    ax.text(-3, 4.5, "• Path 1 (close to mass): Large phase shift", color='red', fontsize=12)
    ax.text(-3, 4.0, "• Path 2 (far from mass): Small phase shift", color='green', fontsize=12)
    ax.text(-3, 3.5, "• Measurable Difference: Interference pattern shift", fontsize=12)
    
    # Add title
    plt.suptitle("Temporal Shell Structure with Quantum Particles", fontsize=16, fontweight='bold', y=0.98)
    plt.title("Future at Top, Past at Bottom, Mass Creates Shell Distortion", fontsize=14, y=1.01)
    
    # Add explanation
    explanation = (
        "This diagram shows how mass distorts temporal shells, creating gravitational effects.\n"
        "Quantum particles traveling on different paths accumulate different phase shifts.\n"
        "This phase difference leads to observable interference patterns that reveal gravity's\n"
        "true nature as the inverse flow of time from past (bottom) to future (top)."
    )
    plt.figtext(0.5, 0.02, explanation, ha='center', fontsize=12, 
               bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7))
    
    # Save high resolution image
    plt.savefig('simple_temporal_shells.png', dpi=300, bbox_inches='tight')
    plt.savefig('simple_temporal_shells.pdf', bbox_inches='tight')
    
    print("Created simplified visualization of temporal shells with quantum paths")
    print("Saved as 'simple_temporal_shells.png' and 'simple_temporal_shells.pdf'")

if __name__ == "__main__":
    create_simplified_shell_visualization()
