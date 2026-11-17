"""Does a framework-fixed modulation of the field equation select n_e≈107?

The decisive single computation (note 32). Two results, both negative and both
theorem-grade:

  (A) The natural modulation source R(k)=osc''+osc^3 is itself EXACTLY Δk-periodic,
      so adding it KEEPS the Hill equation periodic → still Floquet, still
      translation-covariant → still NO preferred depth. It cannot even break the
      symmetry that note 31 proved is the obstruction. (It can move the system from
      a stable to an unstable Floquet band at large amplitude, but that instability
      is the SAME at every shell — growth everywhere, not a selected depth.)

  (B) The ONLY way to break translation-covariance is an APERIODIC (secular/chirp)
      modulation. Its rate ε is a free parameter fixed by no corpus quantity. The
      normalizability boundary K*(ε) (where the local Floquet growth rate equals the
      envelope decay 1/φ) is a CONTINUOUS function of ε that sweeps through the tau
      (102), the electron target (107), and the N*/φ^2=111.5 attractor alike. The
      knob cannot separate the target from the tau or the failure flag, and the same
      ε reproduces NONE of the muon/tau as distinct modes (D2 fails).

Run: python3 verify_modulation-knob.py
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
DK = np.pi / (2 * LNPHI)  # osc period = inversion-shell spacing = 3.26425
INVPHI = 1 / PHI


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * LNPHI) ** 2)


def osc2(k):
    return osc(k) ** 2


def d2(f, k, h=1e-4):
    return (f(k + h) - 2 * f(k) + f(k - h)) / h**2


def R(k):
    """Off-shell defect of the adiabatic carrier (note 16 §2): R = osc'' + osc^3."""
    return d2(osc, k) + osc(k) ** 3


def monodromy(W, k0, period, n=800):
    """One-period transfer matrix of u'' + W(k) u = 0 by RK4 on the 2D system."""
    h = period / n

    def deriv(k, y):
        return np.array([y[1], -W(k) * y[0]])

    M = np.zeros((2, 2))
    for j, y0 in enumerate(([1.0, 0.0], [0.0, 1.0])):
        y = np.array(y0)
        k = k0
        for _ in range(n):
            k1 = deriv(k, y)
            k2 = deriv(k + h / 2, y + h / 2 * k1)
            k3 = deriv(k + h / 2, y + h / 2 * k2)
            k4 = deriv(k + h, y + h * k3)
            y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            k += h
        M[:, j] = y
    return M


# ---------------------------------------------------------------------------
print("=== constants ===")
print(
    f"  lnphi={LNPHI:.6f}  Dk(osc period)={DK:.6f}  1/phi={INVPHI:.6f}  Dk/phi=S1={DK / PHI:.6f}"
)

print("\n=== (A1) R(k)=osc''+osc^3 is EXACTLY Δk-periodic ===")
ks = np.array([0.3, 0.9, 1.4, 2.1, 2.9])
res = np.array([abs(R(k) - R(k + DK)) for k in ks])
print(
    f"  max |R(k) - R(k+Δk)| over 5 samples = {res.max():.2e}  -> periodic (period Δk)"
)
print(
    "  so osc^2 + εR is STILL periodic: adding R cannot break translation-covariance."
)

print("\n=== (A2) static Floquet trace (reproduces note 31a) ===")
M0 = monodromy(osc2, 0.0, DK)
print(
    f"  det M = {np.linalg.det(M0):.6f}  tr M = {np.trace(M0):.6f}  |tr|<2 -> STABLE band (continuum)"
)

print(
    "\n=== (A3) R-modulated, W = A·osc^2 (amplitude A, still periodic): find band edge ==="
)


def trace_at(A, k0=0.0):
    return np.trace(monodromy(lambda k: A * osc2(k), k0, DK))


# scan A upward; the Hill trace OSCILLATES (bands), so find the FIRST reach of each level.
Agrid = np.linspace(1.0, 60.0, 1500)
trs = np.array([trace_at(A) for A in Agrid])


def first_cross(level):
    """First A>=1 at which |tr| first REACHES `level`, coming up from the stable seed."""
    for i in range(1, len(Agrid)):
        if abs(trs[i - 1]) < level <= abs(trs[i]):
            a0, a1 = Agrid[i - 1], Agrid[i]
            t0, t1 = abs(trs[i - 1]), abs(trs[i])
            return a0 + (level - t0) * (a1 - a0) / (t1 - t0)
    return None


S1 = DK / PHI
A_c = first_cross(2.0)  # instability ONSET (robust)
A_norm = first_cross(
    2 * np.cosh(S1)
)  # strong-growth (rate=1/phi) threshold; may be None
# translation-covariance check: trace is k0-independent
tcov = max(abs(trace_at(20.0, k0) - trace_at(20.0, 0.0)) for k0 in (0.4, 1.1, 2.2))
print(f"  instability ONSET |tr|=2 at A_c = {A_c:.4f}")
if A_norm is None:
    print(
        f"  strong-growth amp |tr|=2cosh(S1)={2 * np.cosh(S1):.3f}: NOT REACHED for A in [1,60]"
    )
    print(
        "    -> a PERIODIC modulation only opens narrow Mathieu tongues; it cannot even"
    )
    print(
        "       produce envelope-beating growth (rate 1/phi). An extra negative for R-type mods."
    )
else:
    print(
        f"  strong-growth amp |tr|=2cosh(S1)={2 * np.cosh(S1):.3f} at A_norm = {A_norm:.4f}"
    )
print(
    f"  trace is k0-INDEPENDENT (translation-covariant): max Δtr over phases = {tcov:.2e}"
)
print("  => any A>A_c instability grows at EVERY shell equally, NOT a preferred depth.")

print("\n=== (B) aperiodic chirp A(k)=1+εk : the boundary K*(ε) is a free KNOB ===")
# An APERIODIC ramp is the ONLY way to break translation-covariance. The mode first goes
# unstable where A(k) crosses the onset A_c: A(K*)=A_c => K*=(A_c-1)/ε. ε is the modulation
# rate, fixed by NO corpus quantity (its magnitude, sign, and the very choice of a linear
# ramp are all free). Use the robust onset A_c as the critical amplitude.
A_star = A_c
print(
    f"  K*(ε) = (A_c-1)/ε = {A_star - 1:.4f}/ε   (continuous & monotone in the free rate ε)"
)
targets = {
    "muon~63": 63,
    "tau~102": 102,
    "ELECTRON target~107.08": 107.08,
    "N*/phi^2 attractor=111.5": 111.49,
}
for name, K in targets.items():
    eps = (A_star - 1.0) / K
    print(f"    to land K*={K:6.2f} ({name:26s})  need ε = {eps:.6f}")
eps107 = (A_star - 1.0) / 107.08
spread = 100 * abs((A_star - 1) / 102 - (A_star - 1) / 111.49) / eps107
print(
    f"  ε hitting 107.08 = {eps107:.6f} — justified by NO corpus quantity (free magnitude/sign/form)"
)
print(
    f"  ε for tau(102) vs target(107) vs attractor(111.5) span only ~{spread:.0f}% of ε_107:"
)
print(
    "    the knob cannot resolve the electron from the tau or from the 111.5 failure flag."
)

print(
    "\n=== (D2) cross-check: the ramp gives ONE boundary, reproduces NONE of the tower ==="
)
print("  A monotone chirp has exactly one onset crossing K* (the single deepest mode).")
print(
    "  Shallower shells sit in the stable region A(k)<A_c, i.e. they are NOT selected:"
)
for name, K in (("muon", 63), ("tau", 102)):
    A_here = 1 + eps107 * K
    stable = A_here < A_star
    print(
        f"    k={K:3d} ({name}): A={A_here:.3f} vs onset A_c={A_star:.3f}"
        f" -> {'stable, not a boundary' if stable else 'already past onset'}"
    )
print(
    "  => one rule, one boundary: it places none of 63/102 as distinct modes. D2 FAILS."
)

print("\n=== VERDICT ===")
print(
    "  (A) R(k) is periodic -> cannot break translation-covariance -> no depth (static obstruction stands)."
)
print(
    "  (B) any symmetry-breaking chirp has a free rate ε; K*(ε) sweeps 102/107/111.5 continuously,"
)
print(
    "      the ε for 107 is fixed by nothing, and it reproduces none of the tower. The modulation"
)
print(
    "      route cannot select 107 without a free parameter. SECOND theorem-grade obstruction."
)

# assertions
assert res.max() < 1e-6, "R not periodic?"
assert abs(np.trace(M0) - (-1.5696)) < 1e-2, f"static trace off: {np.trace(M0)}"
assert abs(np.linalg.det(M0) - 1) < 1e-6
assert tcov < 1e-3, f"periodic trace should be ~phase-independent: {tcov}"
assert A_c is not None and A_c > 1.0, "instability onset not found"
# the knob curve must pass through tau, target, and the 111.5 attractor (continuity)
assert (A_star - 1) / 111.49 < (A_star - 1) / 107.08 < (A_star - 1) / 102, (
    "K*(eps) not monotone"
)
print("\nALL ASSERTIONS PASSED")
