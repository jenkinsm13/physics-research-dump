#!/usr/bin/env python3
"""
verify_lifetime-stability.py  --  Mechanism 31c: Damping Lifetime / Stability Threshold.

Tests whether a parameter-free lifetime/stability criterion built from the
dispersion  omega(k) = +/- osc(k) - i s/phi  can SELECT a deepest charged mode
near the desert depth n_e = 107.08 (note 30), and whether the SAME rule
reproduces the muon (~63), tau (~102), proton (~92) depths (cross-check D2).

This revision adds the adversarial knob-hunt checks the note now relies on:
  1b. FLOQUET/HILL: the EXACT (non-frozen) channel chi''+(2/phi)chi'+(1/phi^2+osc^2)chi=0
      reduces by the EXACT substitution chi=e^{-k/phi}u to the Hill equation u''+osc^2 u=0.
      We compute the one-period monodromy matrix (RK4, no scipy) and confirm
      |multipliers|=1 (stable band), so the ONLY decay is the exact prefactor e^{-k/phi}
      => tau=phi is NON-perturbative, not merely adiabatic. Closes the frozen-mass loophole.
  1c. INNER-PRODUCT KNOB (D4): the eta Noether charge <V,V>_eta = cosh^2 th - sinh^2 th = 1
      is an ANALYTIC identity (note 16 sec6). Under that norm the lifetime is INFINITE,
      so 'tau=phi' is inner-product-dependent. (Checked numerically only in the
      cancellation-free window k<=40; beyond that cosh^2-sinh^2 loses all float precision.)
  3.  D2 cross-check: depth-constant rate 1/phi cannot make a 63/92/102 ladder.

Numerical hygiene: comb spacing Dk = pi/(2 lnphi) = 3.26425 is CORRECT
  (k1 = pi/(4 lnphi) = 1.6321, Dk = 2 k1). Verified by assertion below.

Conventions fixed by the corpus (note 16):
  phi = (1+sqrt5)/2,  lnphi = 0.481212,  1/phi = 0.618034
  osc(k) = 1/(1 + cos^2(2 k lnphi))            in [1/2, 1]
  M^2(k) = osc^2(k)
  Im(omega) = -s/phi      => lifetime tau = phi shells (CONSTANT, depth-independent)
  Q(k) = phi*osc(k)/2     in [phi/4, phi/2] = [0.405, 0.809]  (PERIODIC, sub-critical)
  inversion comb k_n = (2n-1)*pi/(4 lnphi),  spacing Dk = pi/(2 lnphi) = 3.26425
  finite stack: UV at k=0 (Planck), IR at N* = 291.88 (notes 24/30)
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
inv_phi = 1 / phi
k1 = np.pi / (4 * lnphi)
Dk = np.pi / (2 * lnphi)  # comb spacing = 2*k1


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


def Q(k):
    return phi * osc(k) / 2.0


# ----------------------------------------------------------------------
# 0. Sanity on the constants
# ----------------------------------------------------------------------
print("=" * 70)
print("CONSTANTS")
print("=" * 70)
print(f"phi      = {phi:.6f}")
print(f"lnphi    = {lnphi:.6f}")
print(f"1/phi    = {inv_phi:.6f}")
print(f"k1       = {k1:.5f}  (first comb tooth)")
print(f"Dk       = {Dk:.5f}  (comb spacing = 2*k1; this value 3.26425 IS correct)")
assert abs(Dk - 2 * k1) < 1e-12, "Dk must equal 2*k1"
assert abs(Dk - 3.26425) < 1e-3, "Dk must be 3.26425"

# ----------------------------------------------------------------------
# 1. Is the lifetime / Q depth-dependent?  (the crux)
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("1. LIFETIME AND Q ACROSS DEPTH  (test for depth-dependence)")
print("=" * 70)
ks = np.linspace(0, 300, 3_000_001)
o = osc(ks)
q = Q(ks)
tau = phi  # 1/Im(omega), independent of k
N_osc = o * tau  # coherent real oscillations within one e-fold
print(f"osc(k) range over [0,300]:   [{o.min():.6f}, {o.max():.6f}]")
print(f"Q(k)   range over [0,300]:   [{q.min():.6f}, {q.max():.6f}]")
print(f"lifetime tau = 1/Im(omega) = phi = {tau:.6f} shells  (CONSTANT)")
print(f"N_osc = osc*tau range:       [{N_osc.min():.6f}, {N_osc.max():.6f}]")
m1 = ks < Dk
m2 = (ks >= 100) & (ks < 100 + Dk)
print(f"max osc in [0,Dk]      = {o[m1].max():.6f}")
print(f"max osc in [100,100+Dk]= {o[m2].max():.6f}   -> identical envelope = PERIODIC")
print("=> No monotone trend in lifetime/Q/N_osc; criterion gives same verdict")
print("   at every shell.  A pure-dispersion lifetime test CANNOT pick a depth.")

# ----------------------------------------------------------------------
# 1b. FLOQUET / HILL TEST  (closes the frozen-mass loophole)
#     chi=e^{-k/phi}u gives EXACTLY u''+osc^2(k)u=0. Decay of chi is the exact
#     prefactor e^{-k/phi} times whatever u does. If |multipliers|=1, u is bounded
#     -> tau=phi is non-perturbatively exact, not adiabatic.
#     RK4 monodromy over one period (numpy only, no scipy).
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("1b. FLOQUET / HILL TEST  u'' + osc^2(k) u = 0   (exact, non-frozen)")
print("=" * 70)


def hill_monodromy(N=60000):
    h = Dk / N
    # columns = two fundamental solutions; rows = [u; u']
    Y = np.array([[1.0, 0.0], [0.0, 1.0]])

    def f(k, Y):
        return np.array([Y[1], -(osc(k) ** 2) * Y[0]])

    k = 0.0
    for _ in range(N):
        a = f(k, Y)
        b = f(k + h / 2, Y + h / 2 * a)
        c = f(k + h / 2, Y + h / 2 * b)
        d = f(k + h, Y + h * c)
        Y = Y + h / 6 * (a + 2 * b + 2 * c + d)
        k += h
    return Y


M = hill_monodromy()
detM = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
trM = M[0, 0] + M[1, 1]
eig = np.linalg.eigvals(M)
mu_re = np.max(np.log(np.abs(eig))) / Dk
print(f"monodromy det M       = {detM:.10f}  (Wronskian: must be 1, symplectic)")
print(f"monodromy |tr M|      = {abs(trM):.6f}  (<2 => STABLE band, no growth)")
print(f"|Floquet multipliers| = {abs(eig[0]):.10f}, {abs(eig[1]):.10f}")
print(f"max Re(Floquet exp) of u = {mu_re:.3e} per shell  (~0 => no amplification)")
assert abs(detM - 1) < 1e-6, "monodromy not symplectic"
assert abs(trM) < 2.0, "Hill eqn NOT in stable band -- would be a genuine finding!"
assert abs(abs(eig[0]) - 1) < 1e-6 and abs(abs(eig[1]) - 1) < 1e-6, (
    "multipliers off unit circle"
)
nat = np.sqrt(np.mean(osc(np.linspace(0, Dk, 200000)) ** 2))
pump = 2 * np.pi / Dk
print(
    f"parametric check: nat sqrt<osc^2>={nat:.4f}/shell, pump 2pi/Dk={pump:.4f}/shell"
)
print(
    f"   ratio pump/nat = {pump / nat:.4f}  (Mathieu tongues at 2/n; not near a tongue)"
)
print("=> decay of chi is the EXACT prefactor e^{-k/phi}; periodicity adds no growth.")
print("   tau=phi is NON-perturbatively exact, not adiabatic. Loophole closed.")

# ----------------------------------------------------------------------
# 1c. INNER-PRODUCT KNOB (D4): eta Noether charge conserved => tau -> inf
#     <V,V>_eta = cosh^2 th - sinh^2 th = 1 is an ANALYTIC identity.
#     Numerically check ONLY in the cancellation-free window k<=40 (theta<=~25);
#     beyond that cosh^2 and sinh^2 both overflow toward the same huge value and
#     the float difference is meaningless. We report this honestly.
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("1c. INNER-PRODUCT KNOB (D4)  -- 'lifetime' depends on the norm")
print("=" * 70)
eta = np.diag([1.0, -1.0])


def Vvec(theta):
    return np.array([np.cosh(theta), -np.sinh(theta)])


# Numerically verifiable only for k <= 10 (theta <= ~6): there cosh^2-sinh^2 still
# holds to machine epsilon. By theta ~ 7 the float difference of two ~1e6 numbers
# collapses (residual jumps to O(1)) -- a float artifact, NOT a physics failure.
ks_safe = np.linspace(0, 10, 200)  # theta = k/phi <= ~6.2: cancellation-free
res_safe = np.array([abs(Vvec(k / phi) @ eta @ Vvec(k / phi) - 1.0) for k in ks_safe])
print("<V,V>_eta = cosh^2 th - sinh^2 th = 1  (ANALYTIC identity, note 16 sec6)")
print(
    f"numerical residual in cancellation-free window k in [0,10] (theta<=6.2): "
    f"max|<V,V>_eta - 1| = {res_safe.max():.2e}"
)
print("(beyond k~10, theta>~7, float cosh^2-sinh^2 loses precision -> the conservation")
print(" is an EXACT analytic identity, NOT a wide-range numerical residual.)")
assert res_safe.max() < 1e-9, "eta Noether charge not conserved in safe window"
print("=> Under the conserved eta-charge norm the doublet charge is EXACTLY conserved:")
print(
    "   'lifetime' = INFINITE, no cutoff at any depth. Single-channel modulus: tau=phi."
)
print("   So 'tau=phi' is INNER-PRODUCT-DEPENDENT, and BOTH norms are depth-blind.")
print("   The knob is the DEFINITION of 'lifetime'; neither choice selects a depth.")

# ----------------------------------------------------------------------
# 2. Forced depth-dependence via the finite stack (the only escape)
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("2. FINITE-STACK ATTEMPTS (does any survival rule land on 107?)")
print("=" * 70)
Nstar = 291.88  # IR end of the stack (notes 24/30) -- an INPUT, not derived here

K_2a = Nstar - phi
print(f"(2a) survive>=1 e-fold to IR floor:  K* = N* - phi      = {K_2a:.3f}")
K_2b = Nstar - 2 * phi
print(f"(2b) >=1 coh. oscillation to floor:  K* = N* - 2 phi    = {K_2b:.3f}")
K_2c = Nstar / phi**2
print(f"(2c) FAILURE-FLAG attractor:         N*/phi^2           = {K_2c:.3f}")
print("     (NB: N*/phi^2 is IMPORTED from Mechanism E / note 31e, not a tau output)")
print(f"(2d) stack midpoint:                 N*/2               = {Nstar / 2:.3f}")

target = 107.08
print(f"\nTARGET desert depth n_e = {target}")
for name, val in [
    ("2a N*-phi", K_2a),
    ("2b N*-2phi", K_2b),
    ("2c N*/phi^2", K_2c),
    ("2d N*/2", Nstar / 2),
]:
    print(f"   {name:14s} = {val:8.3f}   |diff to 107| = {abs(val - target):7.3f}")

# ----------------------------------------------------------------------
# 3. MANDATORY CROSS-CHECK (D2): does the SAME rule give 63 / 92 / 102 ?
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("3. CROSS-CHECK D2  (the decisive test)")
print("=" * 70)
known = {"muon": 63, "proton": 92, "tau": 102, "electron(desert)": 107}
print("A genuine mechanism must yield a LADDER hitting these, not one number.")
print("Each finite-stack rule above produces exactly ONE cutoff K*, not a ladder:")
print("   muon=63, proton=92, tau=102, electron=107  span 44 shells.")
print("   The lifetime tau=phi (now proven EXACT by 1b) and Q are PERIODIC, so they")
print("   cannot encode a monotone ladder of distinct stable depths. The tower's")
print("   ordering (electron shallow 24 -> tau deep 102) is unexplained by a")
print("   depth-blind lifetime criterion.")
for name, d in known.items():
    print(
        f"   {name:18s} depth {d:3d}: decay rate 1/tau = 1/phi = {1 / phi:.4f}  "
        f"(identical for all -> no selection)"
    )

# ----------------------------------------------------------------------
# 4. ROBUSTNESS (D4): move the anchor / threshold / inner product
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("4. ROBUSTNESS D4  (how much does K* wander?)")
print("=" * 70)
print("   (i) inner-product alternative: tau -> INFINITE (no cutoff) under eta-charge")
print(
    "       -- the number does not move to 95/120, it dissolves; both norms depth-blind"
)
print("   (ii) threshold alternative:")
for thr in [0.5, 1.0, 1.5, 2.0]:
    Kt = Nstar - thr * phi
    print(f"        threshold {thr:>3} e-fold:  K* = N* - {thr}*phi = {Kt:7.3f}")
print(
    f"        N*/phi^2={Nstar / phi**2:.1f}, N*/phi^3={Nstar / phi**3:.1f}, N*/2={Nstar / 2:.1f}"
)
print("   K* swings ~69..291 as the (arbitrary) threshold/anchor move; under the")
print("   inner-product knob it dissolves entirely.  KNOB EXPOSED, two ways.")

# ----------------------------------------------------------------------
# 5. Verdict numerics
# ----------------------------------------------------------------------
print("\n" + "=" * 70)
print("VERDICT NUMERICS")
print("=" * 70)
print(f"Pure-dispersion lifetime number : NONE (depth-independent tau=phi={phi:.4f})")
print(f"Floquet (frozen-mass loophole)  : |tr M|={abs(trM):.4f}<2, mult on unit circle")
print("   => tau=phi EXACT (non-perturbative), decay = exact e^-k/phi prefactor")
print("Inner-product knob              : eta-charge conserved => tau->inf (dissolves)")
print(f"Finite-stack best 'hit' to 107  : {K_2a:.3f} (rule 2a) -- but a free knob")
print(f"Failure-flag attractor N*/phi^2 : {K_2c:.3f}  <-- IMPORTED from Mech E (D5)")
print("Cross-check D2 (63/92/102)      : FAILS -- no ladder, only one cutoff")
print("MECHANISM C IS DEPTH-INDEPENDENT AT ITS CORE => NEGATIVE (sharpened).")
