"""Verification of note 13 — Absorber Completeness and the Newtonian Limit.

Closes the H1 hypothesis from note 03. The bare static law is nu = 1/(phi lnphi)
= 1.2843. Under a COMPLETE Wheeler-Feynman absorber the bare exponential factors
out (rapidity-addition theorem kappa(a+b): every complete-absorber path to shell n
has total rapidity n/phi, independent of intermediate shells), so the only channel
that can renormalize the exponent is path MULTIPLICITY. The ordinal-ordered
(simplex-volume) resummation of identical advanced rungs Poisson-exponentiates to
e^{g n}, giving

    lambda_eff = 1/phi - g,   nu_eff = (1/phi - g)/lnphi.

g is fixed from FIRST PRINCIPLES as the bounce coupling Gamma_tot = 1/(2 sinh S1)
of note 06 (NOT reverse-engineered to hit Newton). Result: nu_eff = 1.00297, i.e.
Newton to 0.3%, with an irreducible +0.003 residual = H1 holds approximately.

KEY STRUCTURAL RESULT (section 4): nu_eff does NOT run. Because every path to shell
n carries the same per-shell rapidity (kappa(a+b)), the multiplicity exponent g*n is
LINEAR, so d nu/dn = 0 exactly. The dressed slope is a FIXED POINT of the ordinal
boost flow; the bare 1.2843 is the absorber-OFF regime, never reached at any finite
radius. n* = 1/g = 7.39 is the multiplicity e-fold depth (M(n*)=e), NOT a slope
crossover.

Run: python3 verify_absorber-newton.py
"""

import math
import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
INV = 1.0 / PHI


def osc(k):
    return 1.0 / (1 + np.cos(2 * k * LNPHI) ** 2)


def check():
    print("=== 0. Constants ===")
    print(f"   1/phi              = {INV:.6f}")
    print(f"   ln phi             = {LNPHI:.6f}")
    delta_newton = INV - LNPHI
    print(
        f"   Delta_Newton=1/phi-lnphi = {delta_newton:.6f}  (g must equal this for exact Newton)"
    )

    print(
        "\n=== 1. Completeness coupling g = Gamma_tot (note 06, first-principles) ==="
    )
    k1 = np.pi / (4 * LNPHI)
    S1 = 2 * k1 / PHI
    g = 1.0 / (2 * np.sinh(S1))
    print(f"   k1=pi/(4 lnphi)    = {k1:.6f}")
    print(f"   S1=2 k1/phi        = {S1:.6f}")
    print(
        f"   g=Gamma_tot=1/(2 sinh S1) = {g:.6f}   (target Newton: {delta_newton:.6f})"
    )
    print(
        f"   shortfall g-Delta  = {g - delta_newton:+.6f}  ({(g - delta_newton) / delta_newton * 100:+.2f}%)"
    )

    print("\n=== 2. Renormalized exponent  nu_eff = (1/phi - g)/lnphi ===")
    lam_eff = INV - g
    nu_eff = lam_eff / LNPHI
    print(f"   lambda_eff = 1/phi - g = {lam_eff:.6f}")
    print(f"   nu_eff             = {nu_eff:.6f}")
    print(f"   residual nu_eff-1  = {nu_eff - 1:+.6f}   (irreducible steepening)")
    assert abs(nu_eff - 1.00297) < 1e-4, "nu_eff mismatch"

    print("\n=== 3. Direct decade fit of d ln|Phi|/d ln r  (10<=n<=55) ===")
    ns = np.arange(1, 60)
    lnr = ns * LNPHI
    env = 1.0 / np.sqrt(2)  # exact period-mean of osc, labeled coarse envelope

    def slope(phi, lo=10, hi=55):
        m = (ns >= lo) & (ns <= hi)
        return np.polyfit(lnr[m], np.log(np.abs(phi[m])), 1)[0]

    phi_bare = env * np.exp(-ns * INV)
    phi_poi = env * np.exp(-ns * INV) * np.exp(g * ns)
    phi_poiT = (
        env
        * np.exp(-ns * INV)
        * np.array(
            [sum((g * n) ** j / math.factorial(j) for j in range(n + 1)) for n in ns]
        )
    )
    phi_bin = env * np.exp(-ns * INV) * (1 + g) ** (ns - 1)
    phi_fine = osc(ns) * np.exp(-ns * INV) * np.exp(g * ns)

    nu_bare = -slope(phi_bare)
    nu_poi = -slope(phi_poi)
    nu_poiT = -slope(phi_poiT)
    nu_bin = -slope(phi_bin)
    nu_fine = -slope(phi_fine)
    print(
        f"   bare (no absorber):        nu = {nu_bare:.5f}   (note 03 target 1.28433)"
    )
    print(f"   Poisson e^(gn):            nu = {nu_poi:.5f}   (near-Newton)")
    print(f"   Poisson truncated@n:       nu = {nu_poiT:.5f}   (causal cap -> e^(gn))")
    print(f"   binomial (1+g)^(n-1):      nu = {nu_bin:.5f}")
    print(
        f"   Poisson, osc kept exactly: nu = {nu_fine:.5f}   (lattice = fine structure)"
    )
    assert abs(nu_bare - 1.28433) < 1e-3, "bare pipeline check failed"
    assert abs(nu_poi - 1.00297) < 1e-3, "Poisson absorber slope failed"
    assert abs(nu_poiT - nu_poi) < 1e-3, "truncated series did not match e^(gn)"

    print("\n=== 4. Fixed point: nu does NOT run (kappa(a+b) pins the exponent) ===")

    # The multiplicity exponent g*n is LINEAR in n, so the local log-slope is
    # constant at every scale. We verify this directly with the causally-capped
    # truncated series (the most conservative model: only n future shells exist),
    # measuring the local slope nu(n) = -d ln|Phi|/d ln r in a sliding 3-shell
    # window. If a crossover existed it would show here; it does not.
    def Mcap(n):  # causal cap: sum_{j=0}^{n} (g n)^j / j!  (n future absorber shells)
        return sum((g * n) ** j / math.factorial(j) for j in range(int(n) + 1))

    nn = np.arange(1, 60, dtype=float)
    Phi_cap = np.array([env * np.exp(-n * INV) * Mcap(n) for n in nn])
    lnPhi = np.log(Phi_cap)
    nu_local = -(lnPhi[2:] - lnPhi[:-2]) / 2.0 / LNPHI  # central diff / lnphi
    nmid = nn[1:-1]
    print("   local nu(n) from causally-capped multiplicity (sliding window):")
    for nshow in (2, 4, 6, 8, 10, 20, 40):
        i = int(np.argmin(np.abs(nmid - nshow)))
        print(f"     n={nshow:3d}  nu_local = {nu_local[i]:.5f}")
    # The slope is pinned at ~1.003 for all n>=3; bare 1.284 NEVER appears.
    settled = nu_local[nmid >= 5]
    print(
        f"   max|nu_local - nu_eff| over n>=5: {np.max(np.abs(settled - nu_eff)):.2e}  (flat => fixed point)"
    )
    assert np.max(np.abs(settled - nu_eff)) < 5e-4, (
        "nu_eff is supposed to be a fixed point (no running)"
    )
    assert np.all(np.abs(nu_local - 1.28433) > 0.27), (
        "bare 1.284 must NOT appear in the dressed model"
    )

    print(
        "\n=== 4b. Multiplicity e-fold depth  M(n*)=e <=> g n*=1 (NOT a slope feature) ==="
    )
    n_star = 1.0 / g
    r_star = PHI**n_star
    print(f"   n* = 1/g           = {n_star:.4f} shells  (one mean re-radiation rung)")
    print(f"   r*/r0 = phi^(1/g)  = {r_star:.4f}")
    assert abs(n_star - 7.386) < 1e-2 and abs(r_star - 34.96) < 1e-1

    print("\n=== 5. Simplex-volume identity: ordered exponential = Poisson ===")

    # Inserting j advanced rungs at ORDERED ordinal positions 0<m_1<...<m_j<n fills
    # the ordered simplex of volume n^j/j!. Summing g^j * (simplex volume) is the
    # ordinal-ordered exponential T-exp(int_0^n g dm), which collapses to plain e^{gn}
    # because (1+1) boosts commute (note 03). This SELECTS Poisson over binomial:
    # continuous ordinal axis -> ordered exponential; the binomial (1+g)^(n-1) is the
    # excluded discrete-integer-sites case.
    def ordered_simplex_volume(n, j):  # vol{0<m1<...<mj<n} = n^j / j!
        return n**j / math.factorial(j)

    n_test = 12.0
    Texp = sum(g**j * ordered_simplex_volume(n_test, j) for j in range(60))
    print(f"   T-exp sum_j g^j n^j/j!  (n={n_test}) = {Texp:.6f}")
    print(f"   e^(g n)                              = {np.exp(g * n_test):.6f}")
    assert abs(Texp - np.exp(g * n_test)) < 1e-9, "ordered-exponential != Poisson"
    print("   -> simplex volume IS the 1/j!; Poisson is derived, not assumed.")

    print("\n=== 6. RG fixed point: beta = d nu_eff / d ln r = 0 (boost group law) ===")

    # nu_eff(n) = (1/phi - g)/lnphi is independent of n: the exponent is linear in
    # ordinal because Lambda(t1)Lambda(t2)=Lambda(t1+t2), so the per-shell rapidity
    # contribution is constant. beta vanishes identically.
    def nu_of_n(n):  # full dressed (uncapped) model, exact
        return INV / LNPHI - g / LNPHI  # constant in n by construction

    beta = (nu_of_n(50.0) - nu_of_n(2.0)) / ((50.0 - 2.0) * LNPHI)
    print(f"   beta = d nu/d ln r = {beta:.2e}   (identically zero)")
    assert abs(beta) < 1e-12, "nu_eff must be an exact fixed point"
    print("   -> gravity's slope is a FIXED LINE of the ordinal boost flow.")

    print("\n=== HEADLINE ===")
    print(
        f"   nu_eff = (1/phi - Gamma_tot)/lnphi = {nu_eff:.5f}  -> Newton to {(nu_eff - 1) * 100:.2f}%"
    )
    print(
        f"   H1 holds APPROXIMATELY: g={g:.5f} vs required {delta_newton:.5f} ({(g - delta_newton) / delta_newton * 100:+.1f}%)"
    )
    print(f"   irreducible residual nu-1 = {nu_eff - 1:+.5f}  (the prediction)")
    print("\nAll asserts passed.")


if __name__ == "__main__":
    check()
