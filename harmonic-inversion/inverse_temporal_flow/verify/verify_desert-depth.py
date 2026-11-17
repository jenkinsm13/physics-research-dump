"""Disciplined search for a selection principle fixing the electron's desert depth.

Target: n_e = log_phi(E_P / m_e) = 107.08 (the one missing integer of note 97).
We enumerate candidate closed forms built ONLY from corpus constants and apply the
DISOWNMENT TEST from note 24 to each:
  (T1) closure: |candidate - n_e| < 0.10 shell (the window reserved for a real hit);
  (T2) no free knob: the candidate uses no integer/rational chosen to fit (we flag
       any candidate that needs a fitted integer as FITTED, not derived);
  (T3) not a nearest-integer / low-denominator-rational artifact: a bare "round to
       107" or "n_e/N* ~ 1/e" is disqualified regardless of closeness.
A candidate PASSES only if it clears all three. The honest expectation is that none do.

Run: python3 verify_desert-depth.py
"""

import numpy as np
from itertools import product

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)

# --- the target, computed from the audited Route-A scale (note 24) ---
E_P = 1.22089e19  # GeV
m_e = 0.51099895e-3  # GeV
N_E = np.log(E_P / m_e) / LNPHI
print(f"target  n_e = log_phi(E_P/m_e) = {N_E:.4f}")

# --- corpus integers/constants that are NOT free knobs (each has an independent origin) ---
NSTAR = 291.88  # horizon/depletion shell (note 08), defined from R_H/ell_P
C_CFT = 3  # emergent dimensions / colors (note 03/18)
KE, KMU, KTAU, K4 = 24, 63, 102, 141  # lepton ladder ordinals (note 04), step 39
DK = np.pi / (2 * LNPHI)  # inversion-shell spacing 3.26425
NH_SUN = (
    np.log(2953.0 / 1.616e-35) / LNPHI
)  # ~183 but uses arbitrary M_sun => FLAGGED arbitrary

results = []


def test(name, value, free_knob, low_denom_rational):
    resid = abs(value - N_E)
    t1 = resid < 0.10
    t2 = not free_knob
    t3 = not low_denom_rational
    passed = t1 and t2 and t3
    results.append((name, value, resid, t1, t2, t3, passed))


# (a) nearest integer — the null candidate; fails T3 by construction
test("round(n_e)=107", 107.0, free_knob=False, low_denom_rational=True)

# (b) N*/e — the audit's disowned coincidence; fails T3 (1/e not low-denom rational, dressed)
test("N*/e", NSTAR / np.e, free_knob=False, low_denom_rational=True)

# (c) 2/5 * N* — note 24's disowned guess; fails T1 badly
test("(2/5) N*", 0.4 * NSTAR, free_knob=False, low_denom_rational=True)

# (d) N* - n_H(Msun) - 1 — note 26 extension; uses arbitrary solar mass => FITTED/arbitrary
test("N* - n_H(Msun) - 1", NSTAR - NH_SUN - 1, free_knob=True, low_denom_rational=False)

# (e) tau ordinal + 5 (manifold's 5) — additive "5" is a free knob (why 5 not 3/8?)
test("k_tau + 5", KTAU + 5, free_knob=True, low_denom_rational=False)

# (f) 33rd inversion shell k_33 — nearest comb tooth; which n best matches?
n_best = round((N_E + 1.632) / DK)
k_n = (2 * n_best - 1) * np.pi / (4 * LNPHI)
test(f"inversion shell k_{n_best}", k_n, free_knob=False, low_denom_rational=False)

# (g) brute search: a*KE_lepton ladder with slope-free integer combos m*39 + r
#     does any pure lepton-ladder integer combination land within 0.1 of n_e?
best_combo = None
for p, q in product(range(-3, 6), range(-3, 6)):
    v = KE + p * 39 + q * round(DK)  # ladder step 39 and rounded comb step 3
    if abs(v - N_E) < abs((best_combo[1] if best_combo else 1e9) - N_E):
        best_combo = (f"24 + {p}*39 + {q}*3", v)
test(best_combo[0], best_combo[1], free_knob=True, low_denom_rational=False)

# --- report ---
print("\n  candidate                         value     |resid|   T1   T2   T3   PASS")
print("  " + "-" * 74)
for name, val, resid, t1, t2, t3, ok in results:
    print(
        f"  {name:32s} {val:8.3f}  {resid:7.3f}   "
        f"{'Y' if t1 else 'n'}    {'Y' if t2 else 'n'}    {'Y' if t3 else 'n'}    "
        f"{'PASS' if ok else 'fail'}"
    )

n_pass = sum(r[-1] for r in results)
print(f"\n  candidates passing all three disownment criteria: {n_pass}")
print(
    "  VERDICT:",
    "a selection principle survives — investigate."
    if n_pass
    else "no candidate survives the disownment test; the desert depth remains a genuine input.",
)

# sanity: confirm the manifold/scale constants are the audited ones
assert abs(LNPHI - 0.481212) < 1e-5
assert abs(DK - 3.26425) < 1e-4
assert abs(N_E - 107.08) < 0.05, N_E
print("\n  (constants check passed: lnphi, Dk, n_e all match the corpus)")
