import numpy as np
import matplotlib.pyplot as plt

# --- Parameters (Copied from numerical_demonstration.py for consistency) ---
R = 10.0
r_eq = 5.0
A = 1.0
B = 0.5
alpha = 0.5
beta = 0.2
distortion_strength = 200.0

# --- Potential and Force Functions ---
def V_void(r, r_eq, A, B, alpha, beta):
    return A * np.exp(-alpha * (r - r_eq)**2) - B * np.exp(-beta * (r - r_eq)**2)

def F_void(r, r_eq, A, B, alpha, beta):
    """ The force, F = -dV/dr """
    term1 = A * alpha * 2 * (r - r_eq) * np.exp(-alpha * (r - r_eq)**2)
    term2 = -B * beta * 2 * (r - r_eq) * np.exp(-beta * (r - r_eq)**2)
    return term1 - term2

# --- Analysis and Plotting ---
print("Generating 1D diagnostic plot for the temporal horizon...")

# Create a high-resolution radial linspace
r_profile = np.linspace(0.1, R, 2000)

# Calculate the force profile
force_profile = F_void(r_profile, r_eq, A, B, alpha, beta)

# The magnitude of the displacement is proportional to the absolute value of the force
# The toroidal field direction is a unit vector, so its magnitude is 1.
delta_r_mag_profile = distortion_strength * np.abs(force_profile)

# The inverse flow magnitude S
# Add a small epsilon to prevent division by zero at r_eq
S_profile = 1.0 / (delta_r_mag_profile + 1e-12)

# --- Create the plot ---
fig, ax1 = plt.subplots(figsize=(12, 7))
color_S = 'crimson'
color_F = 'mediumblue'

# Plot S(r) on the left y-axis
ax1.set_xlabel('Radius (r)')
ax1.set_ylabel('Inverse Flow Magnitude S = 1/|δr|', color=color_S)
ax1.plot(r_profile, S_profile, color=color_S, lw=2, label='S(r) - Inverse Flow')
ax1.tick_params(axis='y', labelcolor=color_S)
ax1.set_yscale('log')
ax1.set_title('1D Analysis of the Temporal Horizon')
ax1.grid(True, which="both", ls="--", alpha=0.5)

# Create a second y-axis for the force F(r)
ax2 = ax1.twinx()
ax2.set_ylabel('Driving Force Magnitude |F(r)|', color=color_F)
ax2.plot(r_profile, np.abs(force_profile), color=color_F, linestyle='--', lw=2, label='|F(r)| - Driving Force')
ax2.tick_params(axis='y', labelcolor=color_F)
ax2.set_yscale('log') # Also log scale to see the zero-crossing clearly

# Highlight the event horizon at r_eq
ax1.axvline(x=r_eq, color='gold', linestyle='-', lw=3, alpha=0.8, label=f'Horizon at r_eq = {r_eq}')

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

fig.tight_layout()
plt.savefig('temporal_horizon_analysis.png')
plt.close(fig)

print("Generated temporal_horizon_analysis.png") 