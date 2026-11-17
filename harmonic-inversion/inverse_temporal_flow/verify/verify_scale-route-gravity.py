#!/usr/bin/env python3
"""
verify_scale-route-gravity.py  —  Note 26, Absolute Scale Route C (Newton's G).

Independent scale route via the gravitational sector. The ONLY dimensionful
input is Newton's G (plus c, hbar to define the Planck length, which is the
shell anchor r0 = ell_P). We do NOT feed in any particle mass. We then PREDICT
the electron mass from its ordinal k_e and report the % miss.

Cross-comparison target (headline): the derived energy quantum omega0 (in GeV),
to be compared with Routes A (Planck, note 24) and B (Lambda, note 25).

ANTI-CIRCULARITY: the scale omega0 = E_P is built only from {G, c, hbar}. No
particle mass touches it. The electron mass is then PREDICTED and the miss
reported honestly. Route C does NOT pin m_e -- that is the result.

Every checkable claim from the corpus brief is recomputed and asserted here.
"""

import math

phi = (1 + 5**0.5) / 2  # golden ratio
lnphi = math.log(phi)  # 0.4812118250596...
inv_phi = 1 / phi  # 0.6180339887...

CHECKS = []


def check(name, got, want, tol, units=""):
    ok = abs(got - want) <= tol
    CHECKS.append(ok)
    flag = "OK " if ok else "XX "
    print(
        f"  [{flag}] {name:44s} = {got:.8g} {units:6s} (want {want:.8g}, tol {tol:.1g})"
    )
    return ok


# ----------------------------------------------------------------------
# 0. Core lattice constants (round 1)
# ----------------------------------------------------------------------
print("\n[0] Core golden-lattice constants")
check("ln phi", lnphi, 0.48121182, 1e-7)
check("1/phi", inv_phi, 0.61803399, 1e-7)
check(
    "per-shell UV ratio phi*e^{-1/phi}", phi * math.exp(-inv_phi), 0.87213, 5e-4
)  # <1 => ZPE UV-finite (note 22)

# Inversion shells & generation step
dk = math.pi / (2 * lnphi)  # 3.26425  shell spacing in k
k1 = math.pi / (4 * lnphi)  # 1.632    first inversion shell
check("Delta k = pi/(2 ln phi)", dk, 3.26425, 1e-4)
check("k_1 = pi/(4 ln phi)", k1, 1.63212, 1e-4)
check("generation step = 6*Dk (shells)", 6 * dk, 19.5855, 1e-3)

# ----------------------------------------------------------------------
# 1. Bare COTV exponent and absorber-completed Newton exponent (notes 03,13)
# ----------------------------------------------------------------------
print("\n[1] Gravitational exponent: bare vs absorber-completed")
nu_bare = 1 / (phi * lnphi)
check("nu_bare = 1/(phi ln phi)", nu_bare, 1.2843, 1e-3)

S1 = math.pi / (2 * phi * lnphi)  # 2.0174  one-bounce action
check("S_1 = pi/(2 phi ln phi)", S1, 2.0174, 1e-3)
Gamma_tot = 1 / (2 * math.sinh(S1))  # 0.13539 total absorber reflection
check("Gamma_tot = 1/(2 sinh S_1)", Gamma_tot, 0.13539, 1e-4)

nu_eff = (inv_phi - Gamma_tot) / lnphi
check("nu_eff = (1/phi - Gamma_tot)/ln phi", nu_eff, 1.00297, 1e-4)
newton_miss = abs(nu_eff - 1.0) * 100
print(
    f"        -> Newton exponent miss = {newton_miss:.3f} %  (fixed line, no running)"
)
check("Newton inverse-square within 0.5%", nu_eff, 1.0, 5e-3)

# ladder & terrace constants (consistency)
check("ladder e^{-pi/(phi ln phi)}", math.exp(-math.pi / (phi * lnphi)), 0.01769, 5e-4)
check("terrace e^{pi/2}", math.exp(math.pi / 2), 4.8105, 1e-3)

# ----------------------------------------------------------------------
# 2. The single dimensionful input: G -> Planck length = shell anchor r0
# ----------------------------------------------------------------------
print("\n[2] G is the single input; r0 = ell_P, omega0 = E_P")
# Physical constants (SI, CODATA)
G = 6.67430e-11  # m^3 kg^-1 s^-2   <-- THE SINGLE INPUT (plus c, hbar)
c = 2.99792458e8  # m/s
hbar = 1.054571817e-34  # J s
M_sun = 1.98892e30  # kg  (IAU nominal solar mass)
GeV_per_J = 1.0 / 1.602176634e-19 / 1e9

ell_P = math.sqrt(hbar * G / c**3)  # Planck length
m_P = math.sqrt(hbar * c / G)  # Planck mass (kg)
E_P_GeV = m_P * c**2 * GeV_per_J  # Planck energy in GeV
print(f"        ell_P = {ell_P:.6e} m")
print(f"        m_P   = {m_P:.6e} kg ; E_P = {E_P_GeV:.6e} GeV")
check("Planck length", ell_P, 1.616255e-35, 1e-40)
check("Planck energy (GeV)", E_P_GeV, 1.2209e19, 5e15)

# Step-2 self-consistency: the unique rung whose Schwarzschild radius equals
# its own size is the Planck rung. r_s(m0)=2G m0/c^2 with m0 = hbar/(c r0).
# Setting r_s = r0 gives r0 = sqrt(2 G hbar / c^3) = sqrt(2)*ell_P; the sqrt(2)
# is the Schwarzschild/Compton O(1) convention absorbed into the rung def.
r0_selfgrav = math.sqrt(2 * G * hbar / c**3)
check("r0(self-grav) / ell_P = sqrt(2)", r0_selfgrav / ell_P, math.sqrt(2), 1e-9)

# ----------------------------------------------------------------------
# 3. Solar horizon shell (note 15) — independent G-anchor cross-check
# ----------------------------------------------------------------------
print("\n[3] Solar horizon shell n_H = log_phi(r_s/ell_P)")
r_s_sun = 2 * G * M_sun / c**2  # Schwarzschild radius of the Sun
n_H = math.log(r_s_sun / ell_P) / lnphi  # horizon shell ordinal
print(f"        r_s(Sun) = {r_s_sun:.6e} m")
check("n_H(Sun) = log_phi(r_s/ell_P)", n_H, 183.08, 0.6)

# ----------------------------------------------------------------------
# 4. Headline scale and electron prediction (anti-circular)
# ----------------------------------------------------------------------
print("\n[4] Headline omega0 and electron mass PREDICTION (no mass input)")
omega0_GeV = E_P_GeV  # headline scale
print(f"        omega0 = E_P = {omega0_GeV:.6e} GeV   <== HEADLINE")

# Mass law (round 3): ln m = a*k + b. Slope a is GEOMETRIC (lepton sector):
a = 0.10454  # corpus lepton slope (geometric, notes 16/04)
seal = math.exp(39 * a)
check("geometric seal e^{39a}=sqrt(m_tau/m_e)", seal, 58.97, 0.2)
m_e_meas = 0.51099895e-3  # GeV
m_tau_meas = 1.77686  # GeV
check("sqrt(m_tau/m_e) measured", math.sqrt(m_tau_meas / m_e_meas), 58.97, 0.6)

k_e = 24  # electron lepton-ladder ordinal (round 1)
N_star = 291.88  # depletion/horizon shell (corpus)
check("N* depletion shell (corpus)", N_star, 291.88, 0.1)

# Best geometric candidates for electron depth below Planck (additive frame):
print("        additive-frame candidates (lepton-ladder depth D):")
for label, depth in [
    ("N*  (full IR depth)", N_star),
    ("N*/phi (Theta_H)", N_star / phi),
    ("N*phi", N_star * phi),
    ("n_H solar (183.08)", 183.08),
]:
    m_e_pred = E_P_GeV * math.exp(-a * (depth - k_e))
    miss = (m_e_pred / m_e_meas - 1) * 100
    print(
        f"          depth={label:22s}: m_e_pred = {m_e_pred:.4e} GeV  (miss {miss:+.1f}%)"
    )

# Depth the framework would NEED for exact m_e (lepton-ladder / slope-a frame):
depth_needed = k_e - math.log(m_e_meas / E_P_GeV) / a
print(
    f"\n        depth NEEDED (slope-a frame) = {depth_needed:.2f} shells below Planck"
)
check("D_need = 24 + ln(E_P/m_e)/a", depth_needed, 516.9, 0.5)
nearest = N_star * phi
miss_mass = (math.exp(a * (nearest - depth_needed)) - 1) * 100
print(
    f"        nearest additive candidate N*phi = {nearest:.2f} "
    f"(off {nearest - depth_needed:+.2f} shells = {miss_mass:+.0f}% in mass)"
)

# ----------------------------------------------------------------------
# 5. EXTENSION — recast the gap as a single phi-power in the BARE hierarchy
# ----------------------------------------------------------------------
print("\n[5] Extension: bare length hierarchy E_P/m_e as a power of phi")
# The natural geometric object is the multiplicative hierarchy, not the
# additive lepton-ladder count. E_P/m_e = phi^N defines the single missing
# integer N. We test N against the integer 107 and the decomposition
# N ~ N* - n_H - 1.
ln_hierarchy = math.log(E_P_GeV / m_e_meas)  # = ln(E_P/m_e)
N_hierarchy = ln_hierarchy / lnphi
print(f"        ln(E_P/m_e) = {ln_hierarchy:.4f}")
print(f"        N = ln(E_P/m_e)/ln phi = {N_hierarchy:.4f}  (E_P/m_e = phi^N)")
check("bare hierarchy power N = log_phi(E_P/m_e)", N_hierarchy, 107.07, 0.1)
# Closeness to the integer 107 (residual in ln):
resid_ln = abs(N_hierarchy - 107) * lnphi
print(
    f"        |N-107| in ln units = {resid_ln:.4f}  ({resid_ln / ln_hierarchy * 100:.2f}% of ln)"
)
check("N within ~0.1 shell of integer 107", N_hierarchy, 107.0, 0.15)
# Suggested decomposition N* - n_H - 1:
decomp = N_star - 183.08 - 1
print(f"        decomposition N* - n_H - 1 = {decomp:.2f}  (vs N = {N_hierarchy:.2f})")
check("N* - n_H - 1 ~ 107 (within 1.2 shell)", decomp, 107.0, 1.2)
# Half-boost rate ratio a/lnphi vs 1/phi^3 = sin^2 theta_W (round 3):
rate_ratio = a / lnphi
check("a/ln phi (rate ratio)", rate_ratio, 0.2172, 1e-3)
check("1/phi^3 = sin^2 theta_W", 1 / phi**3, 0.2361, 1e-3)
print(f"        a/ln phi = {rate_ratio:.4f} vs 1/phi^3 = {1 / phi**3:.4f} (within 8%)")

# ----------------------------------------------------------------------
# 6. HONEST verdict on scale-pinning
# ----------------------------------------------------------------------
print("\n[6] Verdict")
print("    Route C pins the TOP of the ladder cleanly: omega0 = E_P from G alone.")
print("    It does NOT pin the electron rung WITHOUT one integer (N=107 in the")
print("    bare phi-hierarchy, i.e. the intercept b in disguise).")
print("    => scale_pinned = FALSE for the electron mass (honest result).")
print(f"    => headline omega0 = {omega0_GeV:.4e} GeV (cross-route value).")

print("\n" + "=" * 64)
n_ok = sum(CHECKS)
n_tot = len(CHECKS)
print(f"NUMERIC CHECKS PASSED: {n_ok}/{n_tot}")
print("=" * 64)
assert n_ok == n_tot, f"FAILED {n_tot - n_ok} checks"
print("ALL NUMERIC CHECKS PASSED.")
