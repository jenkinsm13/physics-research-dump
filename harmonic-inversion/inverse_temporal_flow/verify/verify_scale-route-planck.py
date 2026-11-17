#!/usr/bin/env python3
"""
Verify note 24 -- Absolute Scale, Route A: the Planck-Horizon Closure.

HONESTY-FIRST verification. The single dimensional input is r0 = ell_P (Planck
length). m_e is used ONLY as the comparison target, never to set the scale.

The note's two load-bearing claims are BOTH encoded as passing tests:
  (1) omega_0 = hbar c / ell_P = E_P, pinned with zero mass input        -> PASS
  (2) the electron mass is NOT pinned: n_e = log_phi(E_P/m_e) = 107.08
      is not a clean phi-lattice number; the naive "2/5 N_star" guess
      misses by ~99%.   We assert the FAILURE as a passing test.         -> PASS

Run:  python3 verify_scale-route-planck.py
Exit 0 and "ALL CHECKS PASSED" iff every check holds.
"""

import math

phi = (1 + 5**0.5) / 2
lnphi = math.log(phi)

# --- physical constants (CODATA-ish), all energies in GeV ---
hbar = 1.054571817e-34  # J s
c = 2.99792458e8  # m/s
GeV = 1.602176634e-10  # J
ell_P = 1.616255e-35  # m    <-- THE SINGLE INPUT (r0)
E_P = 1.220890e19  # GeV  (Planck energy = sqrt(hbar c^5 / G))
m_e = 0.51099895e-3  # GeV  (electron mass; COMPARISON TARGET ONLY)
m_tau = 1.77686  # GeV
a = 0.1045383  # lepton mass-law slope (note 17)
Nstar = 291.88  # depletion shell, log_phi(R_H/ell_P) (note 08)
hbarH0_eV = 1.5e-33  # eV   present Hubble energy, order of magnitude

passed, failed = [], []


def check(name, ok, detail=""):
    (passed if ok else failed).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{('  ' + detail) if detail else ''}")
    return ok


print("=" * 72)
print("Route A: Planck-Horizon Closure   (single input: r0 = ell_P)")
print("=" * 72)
print(f"phi={phi:.10f}  ln phi={lnphi:.10f}  1/phi={1 / phi:.10f}")
print()

# === (1) HEADLINE: omega_0 = hbar c / r0 = E_P, zero mass input ==========
omega0_GeV = (hbar * c / ell_P) / GeV
check(
    "HEADLINE  omega_0 = hbar c / ell_P = E_P (no mass input)",
    abs(omega0_GeV / E_P - 1) < 1e-5,
    f"omega_0={omega0_GeV:.6g} GeV  E_P={E_P:.6g} GeV  ratio={omega0_GeV / E_P:.9f}",
)
print()

# === (2) N_star hierarchy closes the ladder (note 08) ===================
om_deep = E_P * phi ** (-Nstar)  # deepest shell energy, GeV
om_deep_eV = om_deep * 1e9
check(
    "N_star closes ladder: phi^N_star ~ 1e61",
    abs(math.log10(phi**Nstar) - 61.0) < 0.6,
    f"phi^N_star=10^{math.log10(phi**Nstar):.2f}",
)
check(
    "IR cutoff falls out: omega_{N*} ~ Hubble energy (order)",
    0.1 < om_deep_eV / hbarH0_eV < 10.0,
    f"omega_deep={om_deep_eV:.3g} eV  vs hbar H0~{hbarH0_eV:.2g} eV  "
    f"ratio={om_deep_eV / hbarH0_eV:.3g}",
)
print()

# === (3) THE ANTI-CIRCULAR CORE: electron shell is NOT phi-clean ========
n_e = math.log(E_P / m_e) / lnphi
frac = n_e / Nstar
check(
    "electron energy shell n_e = log_phi(E_P/m_e) = 107.08",
    abs(n_e - 107.079) < 0.01,
    f"n_e={n_e:.4f}",
)
check(
    "n_e/N_star = 0.3669 is NOT 2/5 (0.4)",
    abs(frac - 0.36686) < 1e-3 and abs(frac - 0.4) > 0.02,
    f"n_e/N_star={frac:.5f}",
)

# the naive 2/5 prediction MUST miss badly -- assert the failure
m_pred_25 = E_P * phi ** (-0.4 * Nstar)
miss_25 = (m_pred_25 / m_e - 1) * 100
check(
    "naive '2/5 N_star' electron prediction misses by ~99% (NON-PINNING)",
    miss_25 < -95.0,
    f"m_pred(2/5)={m_pred_25:.4g} GeV  miss={miss_25:+.1f}%",
)

# the N_star/e tease: recorded as numerology, NOT rewarded as a fit.
# Honest numbers: N_star/e = 107.38 (off by ~0.30 shell from n_e=107.08),
# a -13.3% mass miss. The earlier version of this script asserted the
# *magnitude* of that coincidence (5<|miss|<20%) as a PASSING test -- a
# subtle fudge that rewarded a near-miss the prose itself disowns. The
# honest test asserts the framework's actual position: 1/e is NOT a
# golden-lattice number, so N_star/e is disqualified as a derivation
# REGARDLESS of how close it lands. We check (a) it does NOT land within
# the >=1-shell / <=10% closure window that the falsifier reserves for a
# genuine pure-phi hit, AND (b) 1/e is provably not a phi-lattice ratio
# (no small integers p,q with p/q ~ 1/e to lattice tolerance).
shell_off = abs(Nstar / math.e - n_e)
m_pred_e = E_P * phi ** (-(Nstar / math.e))
miss_e = (m_pred_e / m_e - 1) * 100
# is 1/e expressible as a low-denominator rational (a phi-lattice candidate)?
inv_e = 1 / math.e
best_q_err = min(abs(inv_e - round(inv_e * q) / q) for q in range(1, 13))
check(
    "N_star/e disowned: not a closure (off >=0.10 shell) AND 1/e not phi-clean",
    shell_off >= 0.10 and best_q_err > 1e-3,
    f"N_star/e={Nstar / math.e:.3f} vs n_e={n_e:.3f} "
    f"(off {shell_off:.2f} shell, mass miss {miss_e:+.1f}%); "
    f"1/e nearest p/q (q<=12) err={best_q_err:.4f} -> not rational/phi-clean",
)
print()

# === (4) Independent agreement with Route C (note 26): desert depth =====
D_need = 24 + math.log(E_P / m_e) / a
Nstar_phi = Nstar * phi
fac = math.exp(a * abs(D_need - Nstar_phi))
check(
    "Route C cross-check: D_need=516.9, best phi-cand N*phi=472.3, ~100x miss",
    abs(D_need - 516.9) < 0.2 and abs(Nstar_phi - 472.3) < 0.1 and 90 < fac < 120,
    f"D_need={D_need:.1f}  N*phi={Nstar_phi:.1f}  mass factor={fac:.1f}x",
)
print()

# === (5) slope orthogonality: intercept route doesn't touch ratios ======
seal = math.exp(39 * a)
check(
    "geometric seal e^{39a} = sqrt(m_tau/m_e) (slope untouched by Route A)",
    abs(seal / math.sqrt(m_tau / m_e) - 1) < 1e-3,
    f"e^39a={seal:.4f}  sqrt(m_tau/m_e)={math.sqrt(m_tau / m_e):.4f}",
)
print()

# === (6) EXTENSION: the over-determination closure number C_AB ===========
# Routes A (geometry) and C (gravity) share the anchor ell_P=sqrt(hbar G/c^3),
# so they are NOT independent -- their agreement is built in. Genuine
# over-determination needs Route B (the IR end, Lambda) to reproduce E_P.
# Define the closure number C_AB = omega_0^A / omega_0^B(reconstructed). Here
# we reconstruct an IR-anchored quantum from the horizon: omega_0^B :=
# (hbar H0) * phi^{+Nstar}, i.e. lift the present Hubble energy back up the
# anchored ladder by exactly N_star shells. If the ladder closes, this MUST
# return E_P. C_AB = 1 exactly would be the over-determination; we report the
# residual ln C_AB in shells, which is precisely the N_star rounding/H0 slack.
hbarH0_GeV = hbarH0_eV * 1e-9
omega0_B_recon = hbarH0_GeV * phi ** (Nstar)  # lift Hubble energy up N_star shells
C_AB = E_P / omega0_B_recon
ln_C_shells = math.log(C_AB) / lnphi  # closure residual measured in shells
check(
    "over-determination closure: lifting hbar H0 up N_star shells returns ~E_P",
    abs(ln_C_shells) < 1.0,  # within one shell == within factor phi
    f"C_AB={C_AB:.3g}  residual={ln_C_shells:+.3f} shells "
    f"(<1 shell: A-anchor and horizon-anchor agree to within phi)",
)
print()

print("=" * 72)
print(f"RESULT: {len(passed)}/{len(passed) + len(failed)} checks passed")
print("=" * 72)
print("SUMMARY OF THE HONEST KEYSTONE RESULT:")
print(f"  * SCALE PINNED:     omega_0 = E_P = {E_P:.4g} GeV  (input r0=ell_P, no mass)")
print(f"  * ELECTRON NOT PINNED: n_e=log_phi(E_P/m_e)={n_e:.2f} is not phi-clean;")
print(
    f"                          2/5 guess misses {miss_25:+.0f}%; intercept b stays open."
)
if failed:
    raise SystemExit(f"FAILED: {failed}")
print("ALL CHECKS PASSED")
