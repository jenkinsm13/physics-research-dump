import numpy as np
import matplotlib.pyplot as plt

def generate_inverse_flow_field():
    """
    Generates and plots the inverse flow field of the V_void potential.

    This script implements the angle-dependent V_void potential as described
    in the "Architecture of Reality" framework. It visualizes the restorative
    force (nabla V), revealing the toroidal structure and dynamically
    generated event horizon that are key consequences of the theory.
    """
    print("Generating inverse flow field for the V_void potential...")

    # --- Grid Setup ---
    # We model a 2D cross-section in (z, rho) cylindrical coordinates.
    # z is the axis of symmetry (plotted as x-axis).
    # rho is the radial distance from the z-axis (plotted as y-axis).
    z_range = np.linspace(-12, 12, 60)
    rho_range = np.linspace(0.1, 12, 60) # Start from 0.1 to avoid division by zero at r=0
    Z, RHO = np.meshgrid(z_range, rho_range)

    # --- Potential Parameters ---
    # These parameters are chosen to clearly illustrate the double-well
    # and toroidal structure described in the textbook.
    A0 = 10.0  # Amplitude of the repulsive term
    B0 = 10.5  # Amplitude of the attractive term
    alpha = 0.4 # Range of the repulsive term (larger alpha = shorter range)
    beta = 0.3  # Range of the attractive term (smaller beta = longer range)
    r_eq = 6.0  # Equilibrium radius, the center of the potential wells

    # --- Angle-Dependent V_void Potential ---
    # Convert grid coordinates to polar coordinates (r, theta)
    r = np.sqrt(Z**2 + RHO**2)
    theta = np.arctan2(RHO, Z)

    # The potential's asymmetry is encoded in the angular dependence of the
    # attractive term. This term is stronger at the poles (theta=0, pi),
    # causing the structure to "fold in" and form a torus.
    B_theta = B0 * (1 + 0.5 * np.cos(theta)**2)
    
    # The V_void potential equation
    V_void = A0 * np.exp(-alpha * (r - r_eq)**2) - B_theta * np.exp(-beta * (r - r_eq)**2)

    # --- Calculate the Restorative Force Field ---
    # The restorative force is the gradient of the potential, nabla(V).
    # We calculate it numerically.
    dvdz, dvdrho = np.gradient(V_void, z_range[1]-z_range[0], rho_range[1]-rho_range[0])
    
    # For visualization, we mirror the rho result for the negative half-plane
    Z_full = np.vstack((Z, Z))
    RHO_full = np.vstack((RHO, -RHO))
    dvdz_full = np.vstack((dvdz, dvdz))
    dvdrho_full = np.vstack((dvdrho, -dvdrho))

    # Normalize vectors for clearer visualization of direction
    magnitude = np.sqrt(dvdz_full**2 + dvdrho_full**2)
    # Avoid division by zero in regions of zero force (the horizon)
    magnitude[magnitude == 0] = 1.0 
    
    # --- Plotting ---
    print("Plotting the vector field...")
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot the vector field (quiver plot)
    ax.quiver(Z_full, RHO_full, dvdz_full/magnitude, dvdrho_full/magnitude, 
              magnitude, cmap='viridis', headwidth=4, headlength=6, pivot='mid')

    # --- Highlighting the Event Horizon ---
    # The "event horizon" is the unstable equilibrium point where nabla(V) ~ 0.
    # We can visualize this by plotting a contour where the potential is at its
    # local maximum, which is slightly inside r_eq.
    horizon_radius = 5.2
    horizon_circle = plt.Circle((0, 0), horizon_radius, color='red', fill=False, 
                                linestyle='--', linewidth=2, label='Event Horizon (Unstable Equilibrium)')
    ax.add_artist(horizon_circle)
    
    # --- Aesthetics ---
    ax.set_title(r'Inverse Flow Field of the $V_{\mathrm{void}}$ Potential', fontsize=18)
    ax.set_xlabel('z (Axis of Symmetry)', fontsize=12)
    ax.set_ylabel(r'$\rho$ (Radial Distance)', fontsize=12)
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.grid(True, linestyle='--', alpha=0.2)
    
    plt.legend(handles=[horizon_circle], loc='upper right', facecolor='darkgrey')
    
    # --- Save and Show ---
    output_filename = 'inverse_flow_field.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor='black')
    print(f"Successfully generated '{output_filename}'")
    # plt.show()

if __name__ == '__main__':
    generate_inverse_flow_field() 