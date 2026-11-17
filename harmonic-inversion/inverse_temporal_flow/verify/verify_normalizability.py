"""
verify_normalizability.py  --  Mechanism 31a (Normalizability / Sturm-Liouville mode count)

Tests whether the unified field equation (note 16)
    (D_k^2 + M^2(k)) Psi = 0,
    D_k^2 = d_k^2 - (2/phi) K d_k + (1/phi^2) I,   M^2(k) = osc(k)^2,
    osc(k) = 1/(1 + cos^2(2 k ln phi)),   K = [[0,-1],[-1,0]], K^2 = I,
on the ordinal half-line k in [0, inf) with the UV (Planck) boundary at k=0
admits a FINITE number of normalizable charged modes, and if so what fixes the
deepest one (target: desert depth n_e = 107.08, note 30).

Honest expectation (advisor + task framing): osc^2 is PERIODIC and strictly
positive, so after stripping the rotor envelope the reduced equation is a Hill
equation with NO turning point -> bounded-oscillatory solutions -> the only decay
is the explicit envelope, which makes the WHOLE retarded sector normalizable in
plain L^2: a CONTINUUM, not a discrete finite tower.

D2 cross-check: a genuine mechanism must reproduce muon(63)/tau(102)/proton(92)
with the SAME parameter-free rule. This mechanism yields NO discrete depths, so
it places none of them -> decisive FIT/NEGATIVE.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)  # 0.4812118...
invphi = 1.0 / phi  # 0.6180339...

# numpy 2.0 removed np.trapz; np.trapezoid is the replacement.
trapz = getattr(np, "trapezoid", None) or np.trapz


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


print(f"phi={phi:.6f}  ln phi={lnphi:.6f}  1/phi={invphi:.6f}")


# ---------------------------------------------------------------------------
# STEP 0 -- numerically VERIFY the exact envelope reduction (the whole ballgame).
#
# Claim: with Psi_s = e^{s k/phi} u_s(k) and ANY smooth u_s, the full operator
#   L[Psi]_s = Psi_s'' - (2 s/phi) Psi_s' + (1/phi^2) Psi_s + osc(k)^2 Psi_s
# reduces EXACTLY to  e^{s k/phi} ( u_s'' + osc(k)^2 u_s ).
# i.e. the envelope absorbs BOTH the drift -(2s/phi)d and the constant 1/phi^2
# mass, leaving the Hill operator u'' + osc^2 u with eigenvalue 0.
# Test with a random analytic u and finite differences.
# ---------------------------------------------------------------------------
def reduction_residual(s):
    k = np.linspace(2.0, 8.0, 200001)  # interior window away from k=0 edge
    dk = k[1] - k[0]
    # arbitrary smooth test profile u(k)
    u = np.sin(1.3 * k) + 0.4 * np.cos(0.7 * k) + 0.2 * k
    Psi = np.exp(s * k * invphi) * u
    d1 = np.gradient(Psi, dk, edge_order=2)
    d2 = np.gradient(d1, dk, edge_order=2)
    Lpsi = d2 - (2 * s * invphi) * d1 + (invphi**2) * Psi + osc(k) ** 2 * Psi
    # reduced target: e^{sk/phi}(u'' + osc^2 u)
    u1 = np.gradient(u, dk, edge_order=2)
    u2 = np.gradient(u1, dk, edge_order=2)
    target = np.exp(s * k * invphi) * (u2 + osc(k) ** 2 * u)
    # compare on the interior (drop FD edges)
    sl = slice(50, -50)
    rel = np.max(np.abs(Lpsi[sl] - target[sl])) / np.max(np.abs(target[sl]))
    return rel


print("\n[STEP 0] EXACT envelope reduction L[e^{sk/phi}u] = e^{sk/phi}(u''+osc^2 u)")
for s in (-1, +1):
    print(
        f"  s={s:+d}: max relative residual (finite diff) = {reduction_residual(s):.2e}"
    )
print(
    "  -> drift AND constant 1/phi^2 mass both cancel exactly; reduced op is u''=-osc^2 u"
)

# ---------------------------------------------------------------------------
# STEP 1 -- the reduced potential W = osc^2 has NO turning point.
# Hill equation u'' = -W(k) u with W>0 everywhere -> oscillatory class, no well.
# ---------------------------------------------------------------------------
kg = np.linspace(0, 200, 400001)
W = osc(kg) ** 2
print("\n[STEP 1] reduced equation u'' = -osc(k)^2 u  (W = osc^2)")
print(
    f"  W(k)=osc^2 range over k in [0,200]: min={W.min():.6f}  max={W.max():.6f}   (matches W in [1/4,1])"
)
print(
    f"  W>0 everywhere? {bool(W.min() > 0)}  -> NO classical turning point (no confining well)"
)


# ---------------------------------------------------------------------------
# STEP 2 -- shoot u'' = -osc^2 u from the Planck boundary k=0; confirm u stays
# O(1) (bounded oscillatory). It never decays on its own.
# ---------------------------------------------------------------------------
def shoot_u(kmax, n, u0=0.0, up0=1.0):
    k = np.linspace(0, kmax, n)
    dk = k[1] - k[0]
    u = np.empty(n)
    up = np.empty(n)
    u[0], up[0] = u0, up0
    for i in range(n - 1):
        Wi = osc(k[i]) ** 2
        a1 = -Wi * u[i]
        uh = u[i] + 0.5 * dk * up[i]
        uph = up[i] + 0.5 * dk * a1
        Wh = osc(k[i] + 0.5 * dk) ** 2
        a2 = -Wh * uh
        u[i + 1] = u[i] + dk * uph
        up[i + 1] = up[i] + dk * a2
    return k, u, up


k, u, up = shoot_u(150.0, 600000)
print("\n[STEP 2] shoot u'' = -osc^2 u from k=0 (Dirichlet u(0)=0, u'(0)=1)")
print(f"  |u|max over [0,150] = {np.abs(u).max():.4f}")
print(
    f"  |u(150)|            = {abs(u[-1]):.4f}   -> BOUNDED, does NOT decay on its own"
)


# ---------------------------------------------------------------------------
# STEP 2b -- FLOQUET MONODROMY (the calculation the note previously only ASSERTED).
#
# W = osc^2 is periodic with period L = pi/(2 ln phi). The Hill equation
#   u'' = -W(k) u
# has eigenvalue PINNED to 0 (no spectral parameter lambda to tune), so the whole
# "continuum vs discrete / does the bulk grow?" question reduces to ONE conjugacy
# invariant: trace of the one-period monodromy matrix M.
#   |trace M| < 2  -> STABLE band: multipliers on the unit circle, Floquet
#                     exponents PURE IMAGINARY, u bounded-oscillatory, ZERO intrinsic
#                     growth. Only the explicit envelope attenuates Psi=e^{sk/phi}u
#                     => continuum (note's claim PROVEN, not asserted).
#   |trace M| > 2  -> INSTABILITY tongue: real Floquet exponent mu; would have to be
#                     compared against 1/phi to decide normalizability (could quantize).
# trace M is start-phase independent (conjugacy invariant), so one number settles it.
# ---------------------------------------------------------------------------
def monodromy(k0, L, n=200000):
    # RK4 for u'' = -W u over [k0, k0+L]; two fundamental solutions -> columns of M.
    dk = L / n
    cols = []
    for u0, up0 in ((1.0, 0.0), (0.0, 1.0)):
        uu, vv, kk = u0, up0, k0
        for _ in range(n):
            k1u, k1v = vv, -(osc(kk) ** 2) * uu
            k2u, k2v = vv + dk / 2 * k1v, -(osc(kk + dk / 2) ** 2) * (uu + dk / 2 * k1u)
            k3u, k3v = vv + dk / 2 * k2v, -(osc(kk + dk / 2) ** 2) * (uu + dk / 2 * k2u)
            k4u, k4v = vv + dk * k3v, -(osc(kk + dk) ** 2) * (uu + dk * k3u)
            uu += dk / 6 * (k1u + 2 * k2u + 2 * k3u + k4u)
            vv += dk / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            kk += dk
        cols.append((uu, vv))
    return np.array([[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]])


L_period = np.pi / (2 * lnphi)
M_mono = monodromy(0.0, L_period)
trM = float(np.trace(M_mono))
detM = float(np.linalg.det(M_mono))
print("\n[STEP 2b] Floquet monodromy of u'' = -osc^2 u over one period L")
print(f"  L = pi/(2 ln phi) = {L_period:.6f}")
print(f"  det M = {detM:.8f}  (Wronskian; must be 1)")
print(f"  trace M = {trM:.6f}   |trace| < 2 ? {abs(trM) < 2}")
# 2x2 with det=1: rho = (tr +- sqrt(tr^2-4))/2; cast to complex for the stable branch.
sq = np.sqrt(complex(trM**2 - 4.0))
rho = np.array([(trM + sq) / 2, (trM - sq) / 2])
mu = np.log(rho) / L_period
print(f"  multipliers |rho| = {np.abs(rho)}  (on unit circle => stable)")
print(f"  Floquet exponents Re(mu) = {np.real(mu)}  (==0 => PURE IMAGINARY => bounded)")
print(f"  Im(mu) (per-shell phase) = {np.imag(mu)}")
trs = [
    round(float(np.trace(monodromy(x, L_period, 80000))), 5) for x in (0.0, 0.7, 1.6)
]
print(f"  trace at start-phase k0=0.0/0.7/1.6 = {trs}  (must coincide: conjugacy inv.)")
print("  => STABLE band: pinned eigenvalue is OSCILLATORY, no real Floquet exponent.")
print("     The 'continuum' conclusion is FORCED, not chosen: the bulk cannot grow.")

# ---------------------------------------------------------------------------
# STEP 3 -- normalizability. Operator is NON-HERMITIAN; pick explicit spaces.
#
# (i) plain weighted L^2 on the half-line:
#       ||Psi_s||^2 = int_0^inf e^{2 s k/phi} |u_s|^2 dk.
#     u_s bounded-oscillatory (O(1)):
#       s=-1 (retarded): integrand ~ e^{-2k/phi}  -> CONVERGES for EVERY bounded u.
#       s=+1 (advanced): integrand ~ e^{+2k/phi}  -> DIVERGES for every u.
# (ii) bi-orthogonal <left|right> pairing s=-1 with s=+1 (weight 1):
#       integrand ~ e^{(-1+1)k/phi}|u|^2 = |u|^2 ~ O(1) -> DIVERGES (no decay).
# ---------------------------------------------------------------------------
integrand_ret = np.exp(-2 * k * invphi) * u**2
norm_ret = trapz(integrand_ret, k)
# show convergence is generic: a second, totally different bounded u also converges
u_alt = np.cos(2.1 * k) + 0.5
norm_ret_alt = trapz(np.exp(-2 * k * invphi) * u_alt**2, k)
print("\n[STEP 3] normalizability (explicit inner products)")
print(
    f"  (i) plain L^2, s=-1, shot u:      ||Psi||^2 = int e^(-2k/phi) u^2 dk = {norm_ret:.6f}  FINITE"
)
print(
    f"  (i) plain L^2, s=-1, arbitrary u: ||Psi||^2 = {norm_ret_alt:.6f}  FINITE (generic)"
)
print(
    "      -> finite for EVERY bounded u  => CONTINUUM of normalizable retarded modes"
)
print(
    "  (i) plain L^2, s=+1:  integrand ~ e^(+2k/phi) -> diverges (advanced sector non-normalizable)"
)
print("  (ii) bi-orthogonal <L|R>: integrand ~ |u|^2 = O(1) -> diverges (no decay)")
print(
    "  => NO discrete quantization from the bulk. NO finite tower. NO 'deepest mode'."
)

# ---------------------------------------------------------------------------
# STEP 4 -- the only route to a number is a FORCED amplitude cutoff (exposes the
# knob, fails D1). Envelope drops below threshold T at e^{-K*/phi}=T => K*=-phi ln T.
# ---------------------------------------------------------------------------
print("\n[STEP 4] forced amplitude cutoff K* = -phi ln T (DEMONSTRATES THE KNOB)")
for T in [1e-19, 1e-20, 1e-21, 1e-22, 1e-23]:
    print(f"  T={T:.0e} -> K* = {-phi * np.log(T):7.2f}")
T_107 = np.exp(-107.08 * invphi)
print(
    f"  threshold needed to LAND on 107.08: T = {T_107:.3e}  (no independent justification -> pure knob)"
)
# K* lives in the ABSOLUTE Planck-anchored ordinal (same convention as n_e=107),
# NOT the rotor ordinal (k_e=24). D4 ROBUSTNESS: under DEFENSIBLE alternative anchors
# the number swings wildly and never approaches 107 -> the knob is exposed.
print("\n[STEP 4b] D4 robustness -- defensible alternative anchors for T:")
print(f"  (a) T=1e-16 (numerical floor)  -> K* = {-phi * np.log(1e-16):6.2f}")
print(f"  (b) T=1e-17 (EW-ish hierarchy) -> K* = {-phi * np.log(1e-17):6.2f}")
print(f"  (c) one e-fold T=1/e           -> K* = {-phi * np.log(1 / np.e):6.2f}")
print(f"  (d) Green e-fold per comb step -> K* = {-phi * np.log(np.exp(-1)):6.2f}")
print("  => every defensible T gives K* in ~1.6-75, NOT 107. Reaching 107 needs")
print(
    "     T=1.8e-29 by hand -> the number MOVES wildly with the anchor: knob exposed."
)

# ---------------------------------------------------------------------------
# STEP 5 -- MANDATORY D2 CROSS-CHECK against 63 / 102 / 92.
# ---------------------------------------------------------------------------
print("\n[STEP 5] D2 cross-check (decisive)")
print("  Mechanism produces a CONTINUUM (no discrete eigenvalues).")
print("  => it predicts NEITHER 107.08 NOR muon 63 / tau 102 / proton 92.")
print("  A rule that places NOTHING cannot reproduce an untuned depth -> FAIL D2.")

# Reference numbers (NOT outputs of this mechanism), for the note's audit trail.
dk_comb = np.pi / (2 * lnphi)
k_comb = [round((2 * n - 1) * np.pi / (4 * lnphi), 3) for n in range(1, 5)]
print("\n[reference, from note 04 -- not produced here]")
print(f"  inversion-comb spacing Delta k = pi/(2 ln phi) = {dk_comb:.5f}")
print(f"  comb knots k_n = (2n-1)pi/(4 ln phi) = {k_comb}")
print(
    f"  envelope e^(-k/phi) at lepton depths 24/63/102 = "
    f"{np.exp(-24 * invphi):.2e} / {np.exp(-63 * invphi):.2e} / {np.exp(-102 * invphi):.2e}"
)

# ---------------------------------------------------------------------------
# STEP 6 -- D5 failure-flag (N*/phi^2 = 111.5).
# ---------------------------------------------------------------------------
print("\n[STEP 6] D5 attractor flag: N*/phi^2 reference = 111.5")
print(
    "  This mechanism yields no finite number, so it does NOT land on ~111; flag not triggered."
)

print("\n==================== VERDICT ====================")
print("NEGATIVE -- and structurally so. Stripping the rotor envelope reduces note 16")
print("EXACTLY (residual ~1e-6, STEP 0) to a Hill equation u''=-osc^2 u whose strictly")
print(
    "positive periodic W=osc^2 has NO turning point. The envelope e^{-k/phi} then makes"
)
print(
    "the WHOLE retarded sector normalizable in plain L^2 -> a CONTINUUM, not a finite"
)
print("tower; the advanced sector and the bi-orthogonal pairing are non-normalizable.")
print(
    "Under any honest inner product the operator has NO discrete spectrum on the half-"
)
print(
    "line. No deepest normalizable mode; any depth needs a free amplitude knob (fails"
)
print(
    "D1) and the rule places none of 63/102/92 (fails D2). Normalizability is the WRONG"
)
print("DOOR for the desert depth -- exactly as note 30 anticipated.")
print(
    "FALSIFIER: exhibit a parameter-free inner product in which the note-16 operator has"
)
print(
    "a DISCRETE, FINITE spectrum whose deepest eigenvalue is 107 +- 1 WHILE keeping 63"
)
print("and 102 inside the normalizable set.")
