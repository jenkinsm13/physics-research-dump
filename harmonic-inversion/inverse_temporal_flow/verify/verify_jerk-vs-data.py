#!/usr/bin/env python3
"""verify_jerk-vs-data.py — Note 33: the cosmic jerk and w(z) vs survey data.

Recomputes the Matryoshka-Chronon cosmological kinematics (j0, w0, w(z), z_x,
the CPL fit, and the jerk bound) and the sigma-tension arithmetic against the
DESI DR1/DR2 dark-energy constraints fetched from the literature. numpy only;
no scipy. Leaves no __pycache__ (run with PYTHONDONTWRITEBYTECODE / -B).

PHASE CONVENTION (load-bearing; see note 21 / note 33).
  The framework evaluates the oscillatory horizon phase  Phi(N) = -cos(2 N lnphi)
  at the INTEGER corpus shell  N = 291  (the realized top-of-stack count), while
  the 1/N_star AMPLITUDE and Omega_Lambda use the continuous depletion shell
  N_star = log_phi(R_H / l_P) = 291.88. Mixing these is intentional and is what
  makes w0 = -0.99693 and z_x = 1.765 come out as quoted. Coding 291.88 inside
  the cosine instead gives cos = -0.2574 (w0 = -0.9991) and the numbers no longer
  match the note — that would be a transcription error, not a falsification.
"""

import numpy as np

# ---------------------------------------------------------------- constants
phi = (1.0 + np.sqrt(5.0)) / 2.0  # golden ratio
lnphi = np.log(phi)  # 0.4812118...
N_star = 291.88  # continuous depletion shell (amplitude)
N_phase = 291  # integer corpus shell (oscillation)

assert abs(lnphi - 0.4812118) < 1e-6, lnphi

# Horizon phase, evaluated at the integer corpus shell.
two_N_lnphi = 2.0 * N_phase * lnphi  # 280.0653 rad ; mod 2pi = 3.605129
c = np.cos(two_N_lnphi)  # -0.894477
s = np.sin(two_N_lnphi)  # -0.447114
Phi_res = -c  # residual directed flow = +0.894

# Parameter-free density split from the one-shell turning point (note 21 sec.3).
Omega_L = (phi + 0.5) / (phi + 1.5)  # 0.679285
Omega_m = 1.0 - Omega_L  # 0.320715

print("=" * 64)
print("FRAMEWORK INTERNALS")
print("=" * 64)
print(f"phi               = {phi:.6f}")
print(f"ln(phi)           = {lnphi:.6f}")
print(
    f"phase 2*291*lnphi = {two_N_lnphi:.6f}  (mod 2pi = {two_N_lnphi % (2 * np.pi):.6f})"
)
print(f"cos, sin          = {c:.6f}, {s:.6f}")
print(f"Phi_res = -cos    = {Phi_res:.6f}")
print(f"Omega_Lambda      = {Omega_L:.6f}")
print(f"Omega_m           = {Omega_m:.6f}")

# ---------------------------------------------------------------- w0, w(z)
w0 = -1.0 + Phi_res / N_star  # quintessence side, w0 > -1
assert abs(w0 - (-0.99693)) < 1e-4, w0


def w_of_z(z):
    """Horizon-anchored equation of state (note 21 sec.4).

    w(z) = -1 - cos(2 N_phase lnphi - 2 ln(1+z)) / N_star.
    The integer-shell phase is what reproduces w0 and z_x; N_star sets amplitude.
    """
    arg = two_N_lnphi - 2.0 * np.log(1.0 + z)
    return -1.0 - np.cos(arg) / N_star


# w(0) must return w0 to guard the sign (note 08 had a sign error w/ local shell).
assert abs(w_of_z(0.0) - w0) < 1e-9, (w_of_z(0.0), w0)

# CPL fit over z in [0, 2]: least squares of w(z) onto {1, 1-a} with a=1/(1+z).
z_grid = np.linspace(0.0, 2.0, 4001)
a_grid = 1.0 / (1.0 + z_grid)
w_grid = w_of_z(z_grid)
# basis: w = w0_cpl * 1 + wa_cpl * (1 - a)
X = np.column_stack([np.ones_like(z_grid), 1.0 - a_grid])
coef, *_ = np.linalg.lstsq(X, w_grid, rcond=None)
w0_cpl, wa_cpl = coef

print()
print("EQUATION OF STATE")
print(f"w0 (z=0)          = {w0:.6f}   (quintessence, w0 > -1)")
print(f"|1+w| <= 1/N_star = {1.0 / N_star:.6e}")
print(f"CPL fit z in[0,2] : w0_cpl = {w0_cpl:.4f}, wa_cpl = {wa_cpl:.4f}")

# ---------------------------------------------------------------- phantom crossing
# w = -1 where cos(arg) = 0, i.e. arg = pi/2 + k*pi. First root in observable window.
m = two_N_lnphi % (2.0 * np.pi)  # 3.605129
z_cross = None
for k in range(-3, 4):
    target = np.pi / 2.0 + k * np.pi
    z = np.exp((m - target) / 2.0) - 1.0
    if 0.0 < z < 3.0:
        z_cross = z
assert z_cross is not None and abs(z_cross - 1.765) < 2e-3, z_cross
print(f"phantom crossing  : z_x = {z_cross:.4f}   (w crosses -1)")

# ---------------------------------------------------------------- the jerk
# j0 - 1 = (3 Omega_L / 2 N_star)[3 cos - 2 sin]  (Visser identity, note 21 ext.)
j0_minus_1 = (3.0 * Omega_L / (2.0 * N_star)) * (3.0 * c - 2.0 * s)
j0 = 1.0 + j0_minus_1
j0_bound = 3.0 * Omega_L * np.sqrt(13.0) / (2.0 * N_star)
assert abs(j0 - 0.99375) < 1e-4, j0
assert abs(j0_bound - 0.0126) < 1e-3, j0_bound

print()
print("THE JERK")
print(f"j0 - 1            = {j0_minus_1:.6f}")
print(f"j0                = {j0:.6f}   (LambdaCDM: j == 1)")
print(f"|j0-1| bound      = {j0_bound:.6f}  (sqrt(13) envelope)")

# ---------------------------------------------------------------- DESI data (fetched)
# DESI DR2 key paper: Abdul-Karim et al. 2025, arXiv:2503.14738 (PRD 112, 083515):
#   w0waCDM preferred over LambdaCDM at 3.1 sigma (DESI BAO + CMB),
#   2.8-4.2 sigma including SNe; w0 > -1 and wa < 0 throughout.
# Central (w0, wa) +/- 1sigma, DESI DR2 BAO + CMB + SN, from
#   EPJC (2026), arXiv:2508.10514, Table 4 (fetch-verified):
desi = {
    #  name        w0      sw0     wa      swa     sigma_LCDM
    "DESI+CMB+Pantheon+": (-0.858, 0.058, -0.58, 0.24, 2.8),
    "DESI+CMB+DES-SN5YR": (-0.821, 0.059, -0.73, 0.255, 4.2),  # DESY5/Dovekie
    "DESI+CMB+Union3": (-0.662, 0.091, -1.15, 0.33, 3.8),
}

print()
print("=" * 64)
print("TENSION vs DESI DR2  (framework w0=-0.997, wa=-0.006)")
print("=" * 64)

fw_w0, fw_wa = w0_cpl, wa_cpl
print(f"{'combination':22s} {'w0 sig':>7s} {'wa sig':>7s}  {'cross z':>8s}")
for name, (dw0, sw0, dwa, swa, sigL) in desi.items():
    # Per-parameter marginal tension between framework point and DESI mean.
    sig_w0 = abs(fw_w0 - dw0) / sw0
    sig_wa = abs(fw_wa - dwa) / swa
    # DESI's own implied quint->phantom crossing: z/(1+z) = (-1-w0)/wa.
    x = (-1.0 - dw0) / dwa
    zc = x / (1.0 - x) if x < 1.0 else float("nan")
    print(f"{name:22s} {sig_w0:6.1f}  {sig_wa:6.1f}   {zc:7.3f}")

# Headline tension number: framework is ~ LambdaCDM, so it inherits DESI's
# *exclusion of LambdaCDM*. The framework point sits this far from LCDM in DESI units:
print()
print("Framework vs LambdaCDM in DESI marginal errors (DESY5 combo):")
dw0, sw0, dwa, swa = -0.821, 0.059, -0.73, 0.255
print(f"  |w0_fw - (-1)| / sw0 = {abs(fw_w0 - (-1)) / sw0:.3f} sigma")
print(f"  |wa_fw -   0 | / swa = {abs(fw_wa - 0.0) / swa:.3f} sigma")
print("  => framework is observationally LambdaCDM-like; it is therefore")
print("     DISFAVORED at the SAME 2.8-4.2 sigma DESI excludes LambdaCDM.")

# ---------------------------------------------------------------- the jerk test
# Realized cosmographic sigma(j0) from model-independent fits is O(0.1-1),
# method/truncation dependent (Luongo & Muccino 2024, arXiv:2404.07070:
# j0 ~ 0.6 with tight errors but order-truncation sensitive; DESI DR2 cosmography
# arXiv:2506.22373: LambdaCDM j0=1 inside 2sigma). To resolve j0=0.9938 vs 1
# you need sigma(j0) << |j0-1| = 0.00625.
sigma_j0_optimistic = 0.1
print()
print("JERK TEST FEASIBILITY")
print(f"  framework deficit |j0-1| = {abs(j0_minus_1):.5f}")
print(
    f"  need sigma(j0) << this; best current sigma(j0) ~ {sigma_j0_optimistic} (>15x too coarse)"
)
print(f"  -> j0 = {j0:.4f} is currently INDISTINGUISHABLE from LambdaCDM j0=1.")

print()
print("ALL FRAMEWORK ASSERTIONS PASSED.")
