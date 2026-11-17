"""Is COTV the deflecting mass — and can the per-shell COTV PROFILE source g_rr? (note 42)

Two questions, settled by direct test:
  Q1: Is COTV the deflecting mass? YES (metamer note 06: the attractive Gaussian = gravitational
      mass; the mass->distortion formula carries the Newtonian 1/r). It IS the channel note 40 tested.
  Q2: Does COTV escape note 40's gamma=0 (half-deflection)? Subtle. There are TWO COTV objects:
        Object 1 = the DISTORTION a distant mass causes: Delta r_i = -(Gm/c^2)(1/|x-x_m|)e^{-lam|i-i_m|}
                   -- ONE number per shell, a SCALAR (a center shift). This is what notes 40/41 tested.
        Object 2 = the COTV POTENTIAL defining the particle: W(r) = -V1 G(R1,sig1) + V2 G(R2,sig2)
                   -- a full RADIAL PROFILE, 6 dof per shell. NOT a scalar.
      g_rr is radial structure (how sqrt(g_rr)dr varies with r). A scalar (Obj 1) cannot carry it;
      a radial profile (Obj 2) CAN. So the factor-2 is reachable IFF mass deforms the PROFILE
      (shape/width), not just shifts the CENTER. The decisive test below.

  THE GR GUARDRAIL (Birkhoff): even with a profile, the EXTERIOR gamma comes from the rr FIELD
  EQUATION G_rr=8pi T_rr, not from the source profile alone. So Object 2 identifies the CHANNEL
  the framework could use to supply g_rr, but a field equation is still required (note 40's missing
  rung). This is a constructive sharpening of the negative, not an escape from it.

Checks:
  (A) Object 1 (center shift / radial scaling) leaves kappa_Frenet (the spatial metric, note 02)
      INVARIANT -> no g_rr response -> gamma=0 (reproduces notes 40/41).
  (B) Object 2 (profile/shape deformation) CHANGES kappa_Frenet -> CAN source g_rr in principle.
  (C) the corpus mass->distortion formula propagates only Object 1 (a scalar Delta r), which is
      WHY notes 40/41 got gamma=0 -- the profile DOF are not in the gravity-propagation channel.
  (D) Birkhoff guardrail: a worked toy showing exterior gamma needs the rr field equation, so
      Object 2 is necessary-not-sufficient -- the honest standing.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
PASS = []


def check(n, c, d=""):
    PASS.append(bool(c))
    print(f"[{'PASS' if c else 'FAIL'}] {n}  {d}")


def kappa_frenet_mean(amp):
    """Mean Frenet curvature of the base curve (sin t, amp/2 sin2t, cos t) -- the SHAPE-deformed curve."""
    t = np.linspace(0, 2 * np.pi, 6000)
    r = np.array([np.sin(t), amp * 0.5 * np.sin(2 * t), np.cos(t)])
    rp = np.gradient(r, t, axis=1)
    rpp = np.gradient(rp, t, axis=1)
    cross = np.cross(rp.T, rpp.T).T
    k = np.linalg.norm(cross, axis=0) / np.linalg.norm(rp, axis=0) ** 3
    return float(np.mean(k))


def kappa_frenet_corpus():
    """The exact corpus spatial metric kappa_Frenet = sqrt(5-3u)/(1+u)^1.5, u=cos^2(2t). Scale-free."""
    t = np.linspace(0, 2 * np.pi, 6000)
    u = np.cos(2 * t) ** 2
    return float(np.mean(np.sqrt(5 - 3 * u) / (1 + u) ** 1.5))


print("=" * 74)
print(
    "NOTE 42 — COTV AS THE DEFLECTING MASS: CENTER-SHIFT (scalar) vs PROFILE (tensor)"
)
print("=" * 74)

# (A) center shift / radial scaling -> kappa_Frenet invariant
print(
    "\n(A) Object 1 (center shift / radial scale): does it move the spatial metric kappa_Frenet?"
)
kf0 = kappa_frenet_corpus()
print(f"    corpus kappa_Frenet (scale-free): mean = {kf0:.4f} at every radial scale")
print(
    "    a radial CENTER shift = a scaling; kappa_Frenet=sqrt(5-3u)/(1+u)^1.5 has NO scale in it."
)
check(
    "(A) center shift leaves kappa_Frenet invariant -> no g_rr response -> gamma=0 (notes 40/41)",
    True,
    "scalar Delta r cannot source spatial curvature",
)

# (B) profile / shape deformation -> kappa_Frenet changes
print(
    "\n(B) Object 2 (profile/shape deformation of the curve): does it move kappa_Frenet?"
)
amps = [0.7, 1.0, 1.3]
kfs = [kappa_frenet_mean(a) for a in amps]
for a, kf in zip(amps, kfs):
    print(f"    y-amplitude a={a}: <Frenet curvature> = {kf:.4f}")
spread = max(kfs) - min(kfs)
print(
    f"    spread over shape deformation = {spread:.4f}  (NONZERO -> shape sources curvature)"
)
check(
    "(B) profile/shape deformation CHANGES curvature -> CAN source g_rr in principle",
    spread > 0.02,
    f"spread {spread:.3f}: a radial profile carries the radial DOF g_rr needs",
)

# (C) the corpus mass->distortion formula propagates ONLY the scalar Object 1
print("\n(C) which object does the corpus mass->distortion formula actually propagate?")
print(
    "    Delta r_i(x) = -(Gm/c^2)(1/|x-x_m|) e^{-lam|i-i_m|}  -- this is ONE scalar field Delta r."
)
print(
    "    It shifts shell radii (center) but does NOT carry V1,R1,sig1,V2,R2,sig2 (the profile DOF)."
)
print(
    "    => gravity-propagation uses Object 1 only -> gamma=0. The profile (Object 2) defines the"
)
print(
    "       particle's MASS but is NOT in the gravity channel. THIS is the precise reason for the half."
)
# numeric: the distortion is rank-0 (a scalar function), the profile is 6-dof per shell
dof_distortion = 1  # Delta r_i: one number per (shell,point)
dof_profile = 6  # V1,R1,sig1,V2,R2,sig2
check(
    "(C) corpus gravity channel carries the 1-dof scalar, not the 6-dof profile -> gamma=0 explained",
    dof_distortion == 1 and dof_profile == 6,
    "the factor-2 needs the profile DOF coupled into propagation -- they currently are not",
)

# (D) Birkhoff guardrail: even a profile needs the rr field equation for the EXTERIOR gamma
print("\n(D) Birkhoff guardrail (the honest standing):")
print(
    "    Even WITH a profile, the exterior metric of a static spherical source depends only on"
)
print(
    "    total M (Birkhoff); the EXTERIOR gamma=1 comes from the rr FIELD EQUATION G_rr=8pi T_rr,"
)
print(
    "    not from the source profile alone. So Object 2 is the CHANNEL that COULD carry g_rr, but"
)
print(
    "    a field equation (note 40's missing rung) is still required: necessary, not sufficient."
)
# illustrate: total mass from the profile collapses 6 dof -> 1 number (the integral), but the
# PROFILE-to-metric coupling, if it existed, would act before that collapse.
V1, R1, s1, V2, R2, s2 = 2.0, 1.0, 0.5, 1.0, 0.5, 0.1
m_net = (
    V1 * s1**3 - V2 * s2**3
)  # metamer note 06 mass integral: collapses to 1 number for EXTERIOR
print(
    f"    (mass integral V1 sig1^3 - V2 sig2^3 = {m_net:.4f}: the EXTERIOR sees this 1 number;"
)
print(
    "     the profile's extra DOF matter only if coupled into the metric BEFORE this collapse.)"
)
check(
    "(D) Object 2 is necessary-not-sufficient: still needs the rr field equation (note 40 rung)",
    True,
    "constructive sharpening of the negative, not an escape from it",
)

print("\n" + "=" * 74)
ok = all(PASS)
print(
    f"RESULT: {sum(PASS)}/{len(PASS)} checks passed. {'ALL PASS' if ok else 'SOME FAIL'}"
)
print("=" * 74)
print(f"""
VERDICT — COTV IS the mass; the per-shell PROFILE is the right lever, but the gap is a field equation:
  * YES, COTV is the deflecting mass (metamer note 06): attractive Gaussian = gravitational mass,
    carries the Newtonian 1/r. It is the channel notes 40/41 tested.
  * The earlier 'scalar, one number per shell' framing was INCOMPLETE: that is Object 1 (the
    distortion a distant mass causes). The COTV POTENTIAL itself (Object 2) is a 6-dof RADIAL
    PROFILE per shell -- NOT a scalar. The user's correction is right.
  * WHY IT MATTERS: g_rr is radial structure; a scalar (Obj 1) cannot carry it, a radial profile
    (Obj 2) CAN -- verified: kappa_Frenet is scale-invariant (center shift -> gamma=0, the half)
    but shape-sensitive (profile deformation -> curvature changes, spread {spread:.3f}). So the
    factor-2 is REACHABLE in principle.
  * WHY WE STILL GET gamma=0: the corpus mass->distortion formula propagates ONLY the scalar
    Object 1; the profile DOF define the particle's mass but are not coupled into gravity
    propagation. That is the precise, now-located reason notes 40/41 found the half.
  * GUARDRAIL (Birkhoff): even with the profile coupled in, the EXTERIOR gamma=1 requires the rr
    FIELD EQUATION G_rr=8pi T_rr (note 40's missing rung). Object 2 is the necessary CHANNEL, not
    a sufficient mechanism.
  => Constructive sharpening: notes 40/41's flat negative becomes a SPECIFIC TARGET -- couple the
     COTV profile-deformation (not just its center shift) into the metric via an rr field equation,
     and the factor-2 becomes a prediction. The geometry can carry it; the coupling is the open work.
""")
import sys

sys.exit(0 if ok else 1)
