import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# --- Parameters ---
R = 10.0
n_shells = 40 # Increased for better resolution
Ngrid = 500

# --- Call-of-the-Void Potential Parameters ---
# These parameters define the double-well potential from the documentation.
# We will place the equilibrium point in the middle of the shells.
r_eq = 5.0
A = 1.0
B = 0.5
alpha = 0.5
beta = 0.2
# The distortion strength now scales the force derived from the potential.
distortion_strength = 200.0

# --- Potential and Force Functions ---
def V_void(r, r_eq, A, B, alpha, beta):
    return A * np.exp(-alpha * (r - r_eq)**2) - B * np.exp(-beta * (r - r_eq)**2)

def F_void(r, r_eq, A, B, alpha, beta):
    """ The force, F = -dV/dr """
    term1 = A * alpha * 2 * (r - r_eq) * np.exp(-alpha * (r - r_eq)**2)
    term2 = -B * beta * 2 * (r - r_eq) * np.exp(-beta * (r - r_eq)**2)
    return term1 - term2

# --- 1. Undistorted Shells & Force Visualization ---
fig, (ax1, ax_force) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [3, 1]})
ax1.set_aspect('equal')
radii = np.linspace(0.1, R, n_shells)
for r in radii:
    circle = plt.Circle((0, 0), radius=r, fill=False, edgecolor='blue', linewidth=1)
    ax1.add_patch(circle)
ax1.set_xlim(-R * 1.2, R * 1.2)
ax1.set_ylim(-R * 1.2, R * 1.2)
ax1.grid(True)
ax1.set_title('Undistorted Temporal Shells')
# Plot the force profile
r_plot = np.linspace(0.1, R, 500)
force_plot = F_void(r_plot, r_eq, A, B, alpha, beta)
ax_force.plot(r_plot, force_plot, 'k-')
ax_force.axhline(0, color='gray', linestyle='--')
ax_force.axvline(r_eq, color='red', linestyle='--', label=f'r_eq = {r_eq}')
ax_force.set_title('Driving Force Profile F(r) = -dV/dr')
ax_force.set_xlabel('Radius (r)')
ax_force.set_ylabel('Force')
ax_force.legend()
ax_force.grid(True)
plt.tight_layout()
plt.savefig('undistorted_shells_with_force.png')
plt.close(fig)
print("Generated undistorted_shells_with_force.png")

# --- 2. Distorted Shells (V_void driven Toroidal Field) ---
print("\n--- Recalculating with V_void driven Toroidal Field ---")
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.set_aspect('equal')

theta = np.linspace(0, 2 * np.pi, 300)

for i, r_orig in enumerate(radii):
    # The scalar magnitude of the distortion is now the force from the potential
    force_magnitude = F_void(r_orig, r_eq, A, B, alpha, beta)
    
    # Define the pole separation for the toroidal field
    pole_separation = R * 0.4 
    p1 = np.array([0, pole_separation])
    p2 = np.array([0, -pole_separation])
    
    x_orig = r_orig * np.cos(theta)
    y_orig = r_orig * np.sin(theta)
    
    v1_x, v1_y = x_orig - p1[0], y_orig - p1[1]
    r1_sq = v1_x**2 + v1_y**2 + 1e-9
    v2_x, v2_y = x_orig - p2[0], y_orig - p2[1]
    r2_sq = v2_x**2 + v2_y**2 + 1e-9
    
    field_x = (-v1_y / r1_sq) + (v2_y / r2_sq)
    field_y = (v1_x / r1_sq) - (v2_x / r2_sq)
    
    field_mag = np.sqrt(field_x**2 + field_y**2) + 1e-9
    
    # The displacement vector delta_r has magnitude from F_void and direction from the toroidal field
    dx = distortion_strength * force_magnitude * (field_x / field_mag)
    dy = distortion_strength * force_magnitude * (field_y / field_mag)
    
    x_new = x_orig + dx
    y_new = y_orig + dy
    
    ax2.plot(x_new, y_new, 'r-')

ax2.plot(0, 0, 'ko', markersize=8, label='Mass Center')
ax2.axhline(pole_separation, color='cyan', linestyle=':', lw=1, label='Toroidal Pole')
ax2.axhline(-pole_separation, color='cyan', linestyle=':', lw=1)
ax2.set_xlim(-R * 1.2, R * 1.2)
ax2.set_ylim(-R * 1.2, R * 1.2)
ax2.grid(True)
ax2.set_title('V_void-Driven Toroidal Distortion')
ax2.legend()
plt.savefig('distorted_shells.png')
plt.close(fig2)
print("Generated distorted_shells.png")

# --- 3. Inverse Temporal Flow Field (from V_void driven Toroidal Field) ---
x_grid = np.linspace(-R, R, Ngrid)
y_grid = np.linspace(-R, R, Ngrid)
X, Y = np.meshgrid(x_grid, y_grid)

# Calculate force magnitude at each point in the grid
dist_to_center = np.sqrt(X**2 + Y**2) + 1e-9
force_field_magnitude = F_void(dist_to_center, r_eq, A, B, alpha, beta)

# Calculate toroidal field direction at each point in the grid
v1_x, v1_y = X - p1[0], Y - p1[1]
r1_sq = v1_x**2 + v1_y**2 + 1e-9
v2_x, v2_y = X - p2[0], Y - p2[1]
r2_sq = v2_x**2 + v2_y**2 + 1e-9
field_x = (-v1_y / r1_sq) + (v2_y / r2_sq)
field_y = (v1_x / r1_sq) - (v2_x / r2_sq)
field_mag = np.sqrt(field_x**2 + field_y**2) + 1e-9
unit_field_x = field_x / field_mag
unit_field_y = field_y / field_mag

# The total displacement vector field delta_r
total_dx = distortion_strength * force_field_magnitude * unit_field_x
total_dy = distortion_strength * force_field_magnitude * unit_field_y

# The magnitude of the total displacement vector field
delta_r_mag = np.sqrt(total_dx**2 + total_dy**2) + 1e-9

# The user wants S(x,y) = 1 / |delta_r(x,y)|
S_field = 1.0 / delta_r_mag

fig3, ax3 = plt.subplots(figsize=(9, 8))
ax3.set_aspect('equal')
im = ax3.pcolormesh(X, Y, S_field, cmap='inferno', norm=LogNorm(), shading='auto')
fig3.colorbar(im, ax=ax3, label='Inverse Flow Magnitude S = 1/|δr| (Log Scale)')
ax3.set_xlim(-R, R)
ax3.set_ylim(-R, R)
ax3.set_title('Inverse Temporal Flow Field (V_void Driven)')
plt.savefig('inverse_flow_field.png')
plt.close(fig3)
print("Generated inverse_flow_field.png") 