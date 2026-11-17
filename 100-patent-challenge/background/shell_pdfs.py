import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Constants (SI units, from paper)
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
r_0 = 1.616e-35  # Planck length (m), base radius
c_0 = r_0**3     # Base coupling strength (m^3)
alpha = 1.0      # Shell growth rate (dimensionless)
lambda_ord = 0.118  # Ordinal decay rate (dimensionless)
rho_dm = 2.5e-27  # Dark matter density (kg/m^3)
c = 3e8          # Speed of light (m/s)
H_0 = 2.27e-18   # Hubble constant (s^-1)
m_P = 2.18e-8    # Planck mass (kg)
beta = (rho_dm * (c / H_0)**3 / m_P) * 0.1894  # Derived coupling coefficient (dimensionless)
gamma = 1.0      # Power-law exponent (dimensionless)
kappa_minus = G * m_P / c**2  # Inverse flow constant (m/kg, from distortion scaling)
lambda_dist = 0.1  # Shell distortion decay (arbitrary, for illustration)

# Compute S and collect data
def compute_S(alpha, lambda_ord, beta, gamma, tolerance=1e-100, max_k=100):
    k = np.arange(1, max_k + 1)
    exp_alpha_k = np.exp(alpha * k) - 1
    exp_lambda_k = np.exp(-lambda_ord * k)
    denom = (1 + beta * k**gamma) * exp_alpha_k**3
    terms = exp_lambda_k / denom
    cumulative_S = np.cumsum(terms)
    k_converge = np.where(terms < tolerance)[0][0] + 1 if np.any(terms < tolerance) else max_k
    S = cumulative_S[k_converge - 1]
    print(f"Converged at k = {k_converge}, S = {S:.2e}")
    return S, k[:k_converge], terms[:k_converge], cumulative_S[:k_converge]

# Compute Lambda and data
def compute_lambda(G, r_0, c_0, alpha, lambda_ord, beta, gamma):
    inner_sum = 1 / (np.exp(3 * alpha) - 1)
    S, k, terms, cumulative_S = compute_S(alpha, lambda_ord, beta, gamma)
    lambda_result = (c_0 / (8 * np.pi * G * r_0**3)) * inner_sum * S
    return lambda_result, k, terms, cumulative_S

# Calculate
lambda_calc, k, terms, cumulative_S = compute_lambda(G, r_0, c_0, alpha, lambda_ord, beta, gamma)
lambda_observed = 1.1e-52  # Observed cosmological constant (m^-2)

# Plot 1: Shell Radii Evolution with Distortion
plt.figure(figsize=(10, 6))
i = np.arange(0, 50)
radii = r_0 * np.exp(alpha * i)
# Mass-induced distortion (Definition 4.1), assume m = m_P at i_m = 25, x = 1e-30 m
delta_r_i = -(G * m_P / c**2) * (1 / 1e-30) * np.exp(-lambda_dist * np.abs(i - 25))
radii_distorted = radii + delta_r_i
plt.plot(i, radii, 'b-', lw=2, label=r'$r_i = r_0 e^{\alpha i}$')
plt.plot(i, radii_distorted, 'g--', lw=2, label=r'$r_i + \Delta r_i$ (with mass $m_P$)')
plt.axhline(y=c/H_0, color='r', linestyle='--', label=r'Hubble Length $c/H_0$')
plt.axhline(y=r_0, color='k', linestyle='--', label=r'Planck Length $r_0$')
plt.yscale('log')
plt.xlabel(r'Ordinal Index $i$', fontsize=14)
plt.ylabel(r'Shell Radius $r_i$ (m)', fontsize=14)
plt.title(r'Temporal Shell Radii: Planck to Cosmic Scales', fontsize=16)
plt.text(25, 1e-20, rf'$\alpha = {alpha}, \lambda = {lambda_dist}$', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()
plt.savefig('shell_radii_distorted.pdf')
plt.show()

# Plot 2: Coupling and Inverse Flow
plt.figure(figsize=(12, 7))
k_plot = k
c_ij = c_0 * np.exp(-lambda_ord * k_plot) / (1 + beta * k_plot)
r_diff = r_0 * (np.exp(alpha * k_plot) - 1)
inverse_flow = kappa_minus * m_P * c_ij / r_diff  # F^-_{i->j} with mass scaling (kg m^2)
force_scaling = -G * m_P**2 / (r_diff**2)  # Newtonian approximation (N)
plt.plot(k_plot, c_ij, 'b-', lw=2, label=r'$c_{ij} = \frac{c_0 e^{-\lambda_{\text{ord}} k}}{1 + \beta k}$')
plt.plot(k_plot, inverse_flow, 'r-', lw=2, label=r'$\mathcal{F}^-_{i \to j} = \kappa^- m_P \frac{c_{ij}}{r_i - r_j}$')
plt.plot(k_plot, np.abs(force_scaling), 'g--', lw=2, label=r'$|\vec{F}| = G \frac{m_P^2}{(r_i - r_j)^2}$')
plt.yscale('log')
plt.xlabel(r'Ordinal Separation $k = |i - j|$', fontsize=14)
plt.ylabel(r'Amplitude (m$^3$, kg m$^2$, N)', fontsize=14)
plt.title(r'Shell Coupling and Inverse Temporal Flow (Gravity Emergence)', fontsize=16)
plt.text(15, 1e-80, f'$\\lambda_{{\\text{{ord}}}} = {lambda_ord:.3f}, \\beta = {beta:.2e}$', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.tight_layout()
plt.savefig('coupling_flow_gravity.pdf')
plt.show()

# Plot 3: Cumulative Lambda Convergence
plt.figure(figsize=(12, 7))
lambda_partial = (c_0 / (8 * np.pi * G * r_0**3)) * (1 / (np.exp(3 * alpha) - 1)) * cumulative_S
plt.plot(k, lambda_partial, 'b-', lw=2, label=r'$\Lambda(k)$ (Cumulative)')
plt.plot(k, terms * (c_0 / (8 * np.pi * G * r_0**3)) * (1 / (np.exp(3 * alpha) - 1)), 'g--', lw=1, label=r'Individual Terms $\frac{c_{ij}}{(r_i - r_j)^3}$')
plt.axhline(y=lambda_observed, color='r', linestyle='--', label=r'$\Lambda_{\text{obs}} = 1.1 \times 10^{-52}$ m$^{-2}$')
plt.yscale('log')
plt.xlabel(r'Ordinal Separation $k$', fontsize=14)
plt.ylabel(r'Contribution to $\Lambda$ (m$^{-2}$)', fontsize=14)
plt.title(r'Convergence of $\Lambda$ from Shell Interactions', fontsize=16)
plt.text(15, 1e-50, f'$\\lambda_{{\\text{{ord}}}} = {lambda_ord:.3f}, \\beta = {beta:.2e}$', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.tight_layout()
plt.savefig('lambda_convergence_detailed.pdf')
plt.show()

# Output results
print(f"Derived beta: {beta:.2e}")
print(f"Calculated Lambda: {lambda_calc:.2e} m^-2")
print(f"Observed Lambda: {lambda_observed:.2e} m^-2")
print(f"Ratio (Calculated / Observed): {lambda_calc / lambda_observed:.2f}")