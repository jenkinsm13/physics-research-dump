#!/usr/bin/env python3
"""verify_scale-route-vacuum.py  — Thread 25, Absolute Scale Route B (Regulated Vacuum / Lambda).

Pins omega0 (and r0) from the MEASURED cosmological constant Lambda plus the framework's
own per-shell dispersion omega0 = c/r0, then predicts the electron mass-energy from its
ordinal k_e=24 as the shell quantum hbar*omega0*phi^24 and reports the miss in orders of
magnitude.  Anti-circularity: the ONLY empirical input that sets the scale is Lambda; no
particle mass is fed in to pin omega0.  The electron is then a genuine post-diction.

Run:  python3 verify_scale-route-vacuum.py
Every printed number is reproduced in note 25-scale-route-vacuum.md.
"""

import math

# ---------------------------------------------------------------- constants
phi = (1 + math.sqrt(5)) / 2
lnphi = math.log(phi)
inv_phi = 1 / phi

c = 2.99792458e8  # m/s   (exact, SI)
hbar = 1.054571817e-34  # J*s   (CODATA)
G = 6.67430e-11  # m^3 kg^-1 s^-2 (CODATA)
eV = 1.602176634e-19  # J     (exact)
MeV = 1e6 * eV

Lambda = 1.1e-52  # m^-2  measured cosmological constant (corpus note 08)
mec2 = (
    0.51099895e6 * eV
)  # electron rest energy (J) -- used ONLY for the final comparison

print("phi=%.10f  1/phi=%.10f  lnphi=%.10f" % (phi, inv_phi, lnphi))


# ---------------------------------------------------------------- (1) regulated vacuum sum E0
# note 22 sec 3:  E0 = sum_n phi^n osc(n) e^{-n/phi}  in units of (1/2) hbar omega0.
# Compute in LOG SPACE: phi^n * e^{-n/phi} = e^{n*lnphi - n/phi}.  (phi**n alone overflows.)
def osc(k):
    return 1.0 / (1.0 + math.cos(2 * k * lnphi) ** 2)


E0 = sum(osc(n) * math.exp(n * lnphi - n * inv_phi) for n in range(0, 2001))
ratio = phi * math.exp(-inv_phi)
assert abs(E0 - 5.41196) < 1e-3, E0
assert ratio < 1.0
print(
    "\n[1] E0 = %.6f (1/2 hbar w0)   per-shell ratio phi e^{-1/phi} = %.6f < 1  margin=%.6f"
    % (E0, ratio, inv_phi - lnphi)
)

# ---------------------------------------------------------------- (2) rho_Lambda (energy density)
# Lambda*c^2/(8 pi G) carries units kg/m^3 (a MASS density). Energy density = (that)*c^2.
rho_L_mass = Lambda * c**2 / (8 * math.pi * G)  # kg/m^3
rho_L = rho_L_mass * c**2  # J/m^3
print("[2] rho_Lambda = %.4e kg/m^3 = %.4e J/m^3" % (rho_L_mass, rho_L))
assert 4e-10 < rho_L < 7e-10, rho_L  # standard dark-energy density ~5-6e-10 J/m^3

# ---------------------------------------------------------------- (3) ROUTE B2: pin r0, omega0
# Vacuum energy per stack = E0*(1/2 hbar w0).  Stack volume ~ r0^3 (seed shell).
# Dispersion (the ONE framework assumption): w0 = c/r0.
# rho_vac = E0*(1/2) hbar (c/r0) / r0^3 = (E0/2) hbar c / r0^4.
# Set rho_vac = rho_Lambda  ->  r0^4 = (E0/2) hbar c / rho_Lambda.
hbar_c = hbar * c
r0_4 = (E0 / 2.0) * hbar_c / rho_L
r0 = r0_4**0.25
w0 = c / r0
print("\n[3] ROUTE B2 (input: Lambda; assumption: w0=c/r0, vol~r0^3)")
print("    (E0/2)*hbar*c = %.4e J*m ;  r0^4 = %.4e m^4" % ((E0 / 2.0) * hbar_c, r0_4))
print("    r0  = %.6e m   (~%.3f mm)" % (r0, r0 * 1e3))
print("    w0  = c/r0 = %.6e rad/s  (~%.3f THz)" % (w0, w0 / (2 * math.pi) / 1e12))
print("    hbar*w0 = %.6e J = %.6e eV" % (hbar * w0, hbar * w0 / eV))

# ---------------------------------------------------------------- (4) ELECTRON TEST (post-diction)
# electron = k_e=24 shell quantum, energy hbar*omega_k = hbar*w0*phi^24.  NO lepton-fit intercept.
ke = 24
phi24 = phi**ke
E_e = hbar * w0 * phi24
print("\n[4] ELECTRON TEST  (k_e=24, E = hbar w0 phi^24;  phi^24 = %.5e)" % phi24)
print("    E_e_pred       = %.6e J = %.4f eV = %.4e MeV" % (E_e, E_e / eV, E_e / MeV))
print("    m_e c^2        = %.6e MeV" % (mec2 / MeV))
r = E_e / mec2
print(
    "    E_pred/m_e c^2 = %.4e   ->  log10 = %.3f  (%.0fx too LIGHT)"
    % (r, math.log10(r), 1 / r)
)

# ordinal the electron would need at this w0
k_need = math.log(mec2 / (hbar * w0)) / lnphi
print(
    "    ordinal needed for 511 keV at this w0: k = %.2f  (corpus uses 24; short by %.1f shells)"
    % (k_need, k_need - ke)
)

# ---------------------------------------------------------------- (5) cross-check vs electron-anchored w0
w0_A = mec2 / (hbar * phi24)
print(
    "\n[5] electron-demanded w0_A = %.4e rad/s ;  w0_B2/w0_A = %.4e (log10=%.2f)"
    % (w0_A, w0 / w0_A, math.log10(w0 / w0_A))
)
assert (
    abs(math.log10(w0 / w0_A) - math.log10(r)) < 1e-9
)  # E proportional to w0: same factor

# ---------------------------------------------------------------- (6) reject B1 (Planck anchor)
lP = math.sqrt(hbar * G / c**3)
wP = c / lP
rho_P = (E0 / 2.0) * hbar * wP / lP**3
print(
    "\n[6] B1 Planck anchor (REJECTED, circular): rho_vac/rho_Lambda = 10^%.1f  (the ~122-orders gap)"
    % math.log10(rho_P / rho_L)
)

# ---------------------------------------------------------------- (7) sensitivity to volume power d
print(
    "\n[7] sensitivity (vol ~ r0^d):  E_e ~ rho_Lambda^{1/(d+1)} -> weak; never reaches 511 keV"
)
for d in (1, 2, 3, 4):
    r0d = ((E0 / 2.0) * hbar_c / rho_L) ** (1.0 / (d + 1))
    w0d = c / r0d
    print(
        "    d=%d: r0=%.3e m  E_e=%.3e MeV  log10(E_e/me)=%+.2f"
        % (d, r0d, w0d * hbar * phi24 / MeV, math.log10(w0d * hbar * phi24 / mec2))
    )

# ---------------------------------------------------------------- (8) EXTENSION: gap in inversion-shell units
# The shortfall in shells, k_need - k_e, measured in units of the inversion-shell spacing Dk.
# FLAGGED as a near-integer COINCIDENCE (~1% in shell count), NOT an established structure: there is
# no a-priori reason the offset should be 5 (checked: generation step ~12 Dk, comb shells 1.63/4.90/8.16
# select nothing here). Reported honestly as a postdiction for follow-up, riding on a clean negative.
Dk = math.pi / (2 * lnphi)  # inversion comb spacing = 3.26425
offset_shells = k_need - ke  # ~16.5
offset_in_Dk = offset_shells / Dk  # ~5.06  -> NEAR 5, not exactly
print(
    "\n[8] EXTENSION: gap in inversion-shell units (flagged near-integer coincidence)"
)
print(
    "    Dk = pi/(2 lnphi) = %.5f ;  (k_need - k_e) = %.3f shells = %.4f * Dk  (NEAR 5, 1.1%% off)"
    % (Dk, offset_shells, offset_in_Dk)
)
# IF the offset were exactly 5 inversion shells: w0_A ?= w0_B2 * phi^(5 Dk)
w0A_from_offset = w0 * phi ** (5 * Dk)
print(
    "    5*Dk = %.3f shells ;  phi^(5 Dk) = %.3e ;  w0_B2*phi^(5Dk) = %.3e rad/s"
    % (5 * Dk, phi ** (5 * Dk), w0A_from_offset)
)
print(
    "    vs electron-demanded w0_A = %.3e  ->  within %.1f%% (residual = %.3f Dk non-integer part)"
    % (w0_A, 100 * abs(w0A_from_offset / w0_A - 1), offset_in_Dk - 5)
)
print(
    "    NO independent confirmation, NO derivation of '5' -> coincidence, not structure. Negative stands."
)

print(
    "\nHEADLINE: w0 = %.3e rad/s (r0 ~ %.2f mm);  E_e_pred = %.1f eV vs 511 keV"
    " -> %.1f orders of magnitude short." % (w0, r0 * 1e3, E_e / eV, -math.log10(r))
)
print(
    "RESULT: Route B does NOT pin a scale consistent with the lepton ladder. Honest negative."
)
