"""Verify note 40: does the framework reproduce strong-field GR, or only g_tt?

The make-or-break test. Notes 35/35b established that the time ray T=e^{-theta},
under the EP map theta=Phi_N (with the c=1 resummation theta=-1/2 ln(1-2Phi)),
reproduces GR's gravitational time dilation g_tt = -(1-2Phi) EXACTLY. That fixes
ONE metric component. GR fixes the FULL metric, in particular g_rr = 1/(1-2Phi).

This script tests, with hard numbers, whether the framework's single time ray /
single scalar field (note 16) determines the spatial sector g_rr and hence the
classic tensor observables (light deflection's factor-2, perihelion precession),
or whether it is structurally a scalar-potential theory that matches g_tt only.

  (1) g_rr TEST. GR: g_rr = 1/(1-2Phi), DIVERGES at Phi=1/2 (the horizon).
      Framework spatial sector (note 02): Omega^2 = kappa_Frenet in [1/2, sqrt5],
      a property of the BASE WORLDLINE, mass-independent, BOUNDED. Print both vs
      Phi to show divergence-vs-bounded -> the framework's own metric refutes the
      "reciprocal law T*G=1 maps to g_tt*g_rr=-1" rescue.

  (2) LIGHT DEFLECTION. Numerically integrate the null geodesic in a static,
      spherically symmetric metric ds^2 = -A(r)dt^2 + B(r)dr^2 + r^2 dphi^2 for:
        (GR)        A=1-2Phi, B=1/(1-2Phi)        -> 4GM/c^2 b (factor 2, gamma=+1, 1.75")
        (framework) A=1-2Phi, B=1   (PPN gamma=0)  -> 2GM/c^2 b (Einstein-1911, half, 0.875")
        (Nordstrom) A=1-2Phi, B=1-2Phi (conf flat) -> ~0        (gamma=-1, cancels)
      Including Nordstrom places the scalar-vs-tensor verdict precisely: the
      framework is the Einstein-1911 gamma=0 case (flat space, curved time, HALF),
      NOT Nordstrom's gamma=-1 (zero bending). The deflection integral
      (closest-approach form, integrated below) is confirmed against the closed
      PPN result delta = (1+gamma) * 2GM/(c^2 b).

  (3) FACTOR-2 / PPN gamma. The deflection ratio framework/GR = (1+gamma)/2 with
      gamma=0 => 1/2. Show it is ORTHOGONAL to the c-knob of 35b: the c=1
      resummation buys g_tt=sqrt(1-2Phi) (temporal sector) but supplies NO g_rr.

  (4) PERIHELION. PPN advance per orbit = (2 - beta + 2 gamma)/3 * (6 pi GM/c^2 a(1-e^2)).
      gamma=0, best-case beta=1 => (2-1+0)/3 = 1/3 of GR. Mercury: 43"/cy * 1/3 ~ 14".

  (5) VERDICT NUMBERS: assemble the comparison table values.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
print(f"phi={phi:.6f}  1/phi={1 / phi:.6f}  ln(phi)={np.log(phi):.6f}")
print("=" * 70)


# ---------------------------------------------------------------------------
# (1) g_rr test: GR diverges, framework spatial sector (kappa_Frenet) is bounded
# ---------------------------------------------------------------------------
def kappa_frenet(t):
    # Note 00/02 closed form, u = cos^2(2t); kappa in [1/2, sqrt5].
    u = np.cos(2 * t) ** 2
    return np.sqrt(5 - 3 * u) / (1 + u) ** 1.5


print("(1) g_rr TEST -- GR's spatial sector DIVERGES, framework's is BOUNDED")
print(f"    {'Phi':>6} {'GR g_rr=1/(1-2Phi)':>20} {'framework Omega^2 range':>26}")
kf_lo, kf_hi = 0.5, np.sqrt(5)
for Phi in [0.0, 0.1, 0.2, 0.3, 0.4, 0.49]:
    grr_gr = 1.0 / (1 - 2 * Phi)
    print(
        f"    {Phi:>6.2f} {grr_gr:>20.4f} {f'[{kf_lo:.3f}, {kf_hi:.3f}] (mass-indep)':>26}"
    )
# Confirm kappa_Frenet bounds by sampling the worldline
ts = np.linspace(0, 2 * np.pi, 200001)
kf = kappa_frenet(ts)
print(
    f"    kappa_Frenet sampled range: [{kf.min():.6f}, {kf.max():.6f}]  "
    f"(expect [0.5, {np.sqrt(5):.6f}])"
)
print(
    f"    => framework Omega^2=kappa_Frenet NEVER tracks 1/(1-2Phi); "
    f"at Phi=0.49 GR g_rr={1 / (1 - 0.98):.1f}, framework <= {np.sqrt(5):.3f}."
)
print("    The 'T*G=1 => g_tt*g_rr=-1' rescue identifies g_rr with G^2=e^{+2theta};")
print("    but G is the advanced TIME ray (note 35), not a radial proper length,")
print("    and the framework's ACTUAL spatial metric (note 02) is the bounded")
print("    kappa_Frenet -- which contradicts g_rr=1/(1-2Phi). Reciprocal law killed.")
print("=" * 70)


# ---------------------------------------------------------------------------
# (2) Light deflection: numerical null-geodesic integration
# ---------------------------------------------------------------------------
# Static spherically symmetric: ds^2 = -A(r) dt^2 + B(r) dr^2 + r^2 dphi^2.
# Null geodesic deflection with impact parameter set by closest approach r0:
#   (dphi/dr)^2 = B(r) / ( r^2 * ( (r/r0)^2 * A(r0)/A(r) - 1 ) )
# total bending angle = 2 * integral_{r0}^{inf} (dphi/dr) dr  - pi.
# Units: GM/c^2 = m (geometric). Work in units where m=1, take large r0 (weak-ish
# field) so we cleanly extract the leading 4m/b (GR) vs 2m/b (framework) and the
# closed-form PPN check; then convert to arcsec at the solar limb.


_trapz = getattr(np, "trapezoid", None) or np.trapz  # np>=2.0 renamed trapz


def deflection(A, B, r0, n=2_000_000):
    """Null-geodesic bending for metric -A dt^2 + B dr^2 + r^2 dphi^2, closest r0.

    dphi/dr = sqrt(B) / ( r * sqrt( (r/r0)^2 (A0/A) - 1 ) ), bend = 2*int_{r0}^inf - pi.
    The integrand has an integrable 1/sqrt(r-r0) singularity at r=r0. Substitute
    r = r0/(1 - t^2): t->0 is r=r0, t->1 is r->inf. The dr/dt ~ t Jacobian cancels
    the sqrt(r-r0) zero of the radicand, regularising the closest-approach endpoint.
    """
    A0 = A(r0)
    t = np.linspace(0.0, 1.0 - 1e-7, n)
    u = 1.0 - t**2  # u in (0,1], r = r0/u
    r = r0 / u
    dr_dt = r0 * 2.0 * t / u**2  # dr/dt
    Ar = A(r)
    Br = np.broadcast_to(B(r), r.shape)
    radicand = (r / r0) ** 2 * (A0 / Ar) - 1.0
    radicand = np.where(radicand <= 0, np.nan, radicand)
    integrand = np.sqrt(Br) / (r * np.sqrt(radicand)) * dr_dt
    integrand[~np.isfinite(integrand)] = 0.0  # only the t=0 endpoint (measure zero)
    half = _trapz(integrand, t)
    return 2 * half - np.pi


# Metrics (m = GM/c^2 = 1)
def A_gr(r):
    return 1 - 2.0 / r


def B_gr(r):
    return 1.0 / (1 - 2.0 / r)


def A_fw(r):
    return 1 - 2.0 / r  # framework: g_tt matches (time dilation)


def B_fw(r):
    return np.ones_like(np.atleast_1d(r)) if hasattr(r, "__len__") else 1.0


# Nordstrom 1913: conformally flat, g_mn = (1-2Phi) eta_mn, so the SAME factor
# multiplies dt^2 and dr^2. This curves space with the WRONG sign (PPN gamma=-1):
# the spatial term over-compensates and light bending CANCELS to zero. Including
# it makes the scalar-vs-tensor verdict precise: the framework is NOT Nordstrom
# (gamma=-1, zero bending) but the Einstein-1911 gamma=0 case (flat space -> half).
def A_nord(r):
    return 1 - 2.0 / r


def B_nord(r):
    return 1 - 2.0 / r  # conformal factor on the spatial part too


print("(2) LIGHT DEFLECTION -- numerical null-geodesic integration (m=GM/c^2=1)")
print(
    f"    {'r0':>10} {'b~r0':>10} {'GR delta':>14} {'4m/b':>12} "
    f"{'FW delta':>14} {'2m/b':>12} {'FW/GR':>7} {'Nord delta':>13} {'/2m/b':>7}"
)
for r0 in [100.0, 1000.0, 10000.0]:
    d_gr = deflection(A_gr, B_gr, r0)
    d_fw = deflection(A_fw, B_fw, r0)
    d_nd = deflection(A_nord, B_nord, r0)
    b = r0 / np.sqrt(A_gr(r0))  # impact parameter ~ r0 in weak field
    print(
        f"    {r0:>10.0f} {b:>10.1f} {d_gr:>14.6e} {4 / b:>12.6e} "
        f"{d_fw:>14.6e} {2 / b:>12.6e} {d_fw / d_gr:>7.4f} "
        f"{d_nd:>13.6e} {d_nd / (2 / b):>7.4f}"
    )
print("    => GR delta -> 4m/b (gamma=+1); framework -> 2m/b (gamma=0, HALF);")
print("       Nordstrom -> ~0 (gamma=-1, CANCELS). Framework is the in-between")
print("       Einstein-1911 gamma=0 case, NOT Nordstrom. ratio FW/GR -> 1/2.")
print("=" * 70)


# ---------------------------------------------------------------------------
# (2b/3) Solar-limb hard number in arcsec via the closed PPN form
# ---------------------------------------------------------------------------
# delta = (1+gamma) * 2GM/(c^2 b).  GR gamma=1 -> 1.75"; framework gamma=0 -> half.
G = 6.674e-11
c = 2.998e8
Msun = 1.989e30
Rsun = 6.957e8
m_sun = G * Msun / c**2  # GM/c^2 in metres
b = Rsun  # grazing the solar limb


def arcsec(rad):
    return rad * (180 / np.pi) * 3600


delta_newt = 2 * m_sun / b  # gamma=0 part = "Einstein 1911" = framework
delta_gr = 2 * (1 + 1) * m_sun / b  # gamma=1 -> 4m/b
print("(3) SOLAR-LIMB DEFLECTION -- the HARD NUMBER (closed PPN, b=Rsun)")
print(f"    GM/c^2 (sun) = {m_sun:.4f} m,  b = Rsun = {b:.3e} m")
print(
    f"    GR        (gamma=1, 4GM/c^2 b): delta = {arcsec(delta_gr):.4f} arcsec  (=1.75)"
)
print(
    f"    Newtonian (gamma=0, 2GM/c^2 b): delta = {arcsec(delta_newt):.4f} arcsec  (=0.875)"
)
print(f"    FRAMEWORK = gamma=0 = {arcsec(delta_newt):.4f} arcsec = HALF of GR.")
print("    Why HALF not zero: the framework keeps the g_tt (time-dilation) half;")
print("    only the g_rr (spatial-curvature) half is missing. Nordstrom (conformally")
print("    flat, gamma=-1) CANCELS even the g_tt half -> 0; framework's bounded")
print("    mass-independent kappa_Frenet does NOT cancel -> half survives.")
print("    ORTHOGONAL to the c-knob: c=1 resummation gives g_tt=sqrt(1-2Phi) exactly,")
print(
    "    but supplies NO g_rr -- so even the most GR-like framework bends light by half."
)
print("=" * 70)


# ---------------------------------------------------------------------------
# (4) Perihelion precession -- PPN
# ---------------------------------------------------------------------------
# Per-orbit advance = (2 - beta + 2 gamma)/3 * 6 pi GM / (c^2 a (1-e^2)).
# GR: beta=gamma=1 -> coefficient (2-1+2)/3 = 1 -> 6 pi GM/...
# Framework: gamma=0 (no spatial curvature, ALL maps). beta is set by the g_00
# expansion, which IS map (c)-dependent -- UNLIKE gamma, which is c-independent:
#   c=0 map  T=e^{-Phi}     -> g_00 = -(1 - 2Phi + 2Phi^2 - ...) -> beta=1 -> 1/3
#   c=1 map  T=sqrt(1-2Phi) -> g_00 = -(1 - 2Phi)               -> beta=0 -> 2/3
# So the c=1 ("most GR-like") map gives the LARGER 2/3, not 1/3: beta=0 is the
# best case (closest to GR), beta=1 the worst. Framework spans 1/3..2/3 of GR
# and NEVER reaches GR's coefficient 1.
print("(4) PERIHELION PRECESSION -- PPN coefficient (2 - beta + 2 gamma)/3")
for label, beta, gamma in [
    ("GR (beta=gamma=1)", 1, 1),
    ("framework c=1 map (gamma=0, beta=0): BEST/most GR-like", 0, 0),
    ("framework c=0 map (gamma=0, beta=1): worst", 1, 0),
]:
    coeff = (2 - beta + 2 * gamma) / 3
    print(f"    {label:<54} coeff = {coeff:.4f}  (x GR)")
mercury_gr = 42.98  # arcsec/century, GR
print(f"    Mercury observed (anomalous) ~ 42.98 ''/cy; GR predicts {mercury_gr:.2f}.")
print(
    f"    Framework spans {mercury_gr / 3:.1f}..{2 * mercury_gr / 3:.1f} ''/cy "
    f"(c=0..c=1); best case (c=1, 2/3 GR) -> {2 * mercury_gr / 3:.1f} ''/cy,"
)
print(
    f"    still off by ~{mercury_gr - 2 * mercury_gr / 3:.0f}''/cy, "
    f"never reaching GR's {mercury_gr:.1f}."
)
print("=" * 70)


# ---------------------------------------------------------------------------
# (5) Summary table values
# ---------------------------------------------------------------------------
print("(5) COMPARISON TABLE (Newtonian | Nordstrom | framework | GR)")
print(
    f"    {'observable':<22} {'Newtonian':>13} {'Nordstrom':>13} "
    f"{'framework':>14} {'GR':>13}"
)
# Dilation factor sqrt(-g_tt): Nordstrom/framework/GR ALL = sqrt(1-2Phi) at this
# order -- they agree in the TIME sector (Pound-Rebka cannot separate them) and
# differ ONLY in the spatial sector g_rr (the gamma row below). That is why light
# deflection, not redshift, is the decisive test.
print(
    f"    {'sqrt(-g_tt) dilation':<22} {'1-Phi':>13} {'sqrt(1-2Phi)':>13} "
    f"{'sqrt(1-2Phi)*':>14} {'sqrt(1-2Phi)':>13}"
)
print(
    f"    {'g_rr (spatial)':<22} {'1 (flat)':>13} {'1-2Phi (conf)':>13} "
    f"{'bounded kappa':>14} {'1/(1-2Phi)':>13}"
)
print(
    f"    {'light defl. (solar)':<22} {'0.875"':>13} {'0"':>13} "
    f"{'0.875"':>14} {'1.75"':>13}"
)
print(
    f"    {'perihelion (x GR)':<22} {'0 (none)':>13} {'--':>13} "
    f"{'1/3..2/3':>14} {'1':>13}"
)
print(f"    {'PPN gamma':<22} {'0':>13} {'-1':>13} {'0':>14} {'1':>13}")
print("    * with the c=1 resummation; g_tt only, no g_rr companion.")
print()
print("VERDICT: framework reproduces g_tt (gravitational time dilation) only.")
print("It is a SCALAR-POTENTIAL theory (one field theta(r)/Psi(k), note 16 is a")
print("(1+1) scalar Klein-Gordon -- no G_mu_nu, no T_mu_nu). PPN gamma=0: light")
print('bends by HALF (0.875"), perihelion 1/3..2/3 GR. VLBI pins gamma=1 to ~1e-4,')
print("excluding gamma=0 overwhelmingly. The framework FAILS the classic tensor")
print("tests -- the same failure mode as scalar gravity generally. PRECISELY: it is")
print("the Einstein-1911 gamma=0 point (flat space, curved time -> bends to HALF),")
print("NOT Nordstrom's conformally-flat gamma=-1 (bends to ZERO). Both are scalar")
print("theories killed by the 1919 eclipse, at different wrong values; neither = GR.")
print("EXIT 0")
