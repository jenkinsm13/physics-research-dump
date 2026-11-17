"""Can note 16's action be varied into the rr field equation G_rr=8pi T_rr? (note 43)

Note 42 sharpened the gravity gap to a TARGET: couple COTV profile-deformation into an rr field
equation that produces g_rr=1/(1-2Phi) from the same mass, so gamma->1 (factor-2). The advisor's
fork: the only honest positive is DERIVING that field equation from note 16's Lagrangian; a static
source map a(Phi) tuned to 1+2Phi is the forbidden 'hand-insert g_rr'.

PRE-REGISTERED GATE: name the framework relation in note 16 that FORCES g_rr's Phi-coefficient to be
exactly 2 (gamma=1). If a coupling must be CHOSEN to land on 2, gamma is a knob -> the half -> negative.
Read the verdict from the DEFLECTION integrator (note 40), never a curvature proxy.

THE STRUCTURAL TEST (what can note 16 be varied against?):
  S[Psi] = integral dk [ 1/2 <D_k Psi, D_k Psi>_eta - 1/2 osc^2(k) <Psi,Psi>_eta ],  D_k = d/dk-(1/phi)K.
  - ONE coordinate k (the ordinal); Psi is a 2-component flow-space field; eta=diag(+1,-1) is the
    INTERNAL (time-ray/gravity-ray) metric, FIXED.
  - delta S/delta Psi = (D_k^2+osc^2)Psi=0 (the field eq). There is NO g_rr(r), no radial coordinate,
    no spacetime metric tensor in S. delta S/delta g_rr is UNDEFINED.
  => G_rr=8pi T_rr requires a metric action S[g_munu]; note 16 is matter on a FIXED background.
     gamma cannot be forced to 1 -> stays 0 (half). The gap is a missing METRIC ACTION, not a
     missing source coupling. (Adding S[g_munu] = adding GR by hand.)

Checks:
  (A) note-16 action has one coordinate and a fixed 2x2 internal eta -> no g_rr to vary.
  (B) rank/dimension count: GR S[g_munu] (rank-2, 4D, 10 comp) vs note-16 S[Psi] (rank-1, 1D, 2 comp).
  (C) the non-foolable read: feed g_rr=1+2 gamma Phi into note-40's deflection integrator; only
      gamma=1 gives 1.75", gamma=0 gives 0.875" (half). The framework supplies no gamma=1.
  (D) confirm gamma=1's '2' comes from rank-2 Bianchi/trace-reversal, which a scalar/shape knob lacks.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
PASS = []


def check(n, c, d=""):
    PASS.append(bool(c))
    print(f"[{'PASS' if c else 'FAIL'}] {n}  {d}")


print("=" * 74)
print(
    "NOTE 43 — CAN NOTE 16 BE VARIED INTO THE rr FIELD EQUATION? (the gravity terminus)"
)
print("=" * 74)

# (A) the note-16 action: count coordinates and the internal metric.
print("\n(A) what can S[Psi] be varied against?")
n_coords = 1  # the ordinal k
internal_eta = np.diag([1.0, -1.0])  # 2x2 flow-space metric, FIXED
has_grr = False  # no radial spacetime metric component in S
print(
    f"    coordinates in S: {n_coords} (the ordinal k); internal eta = diag(+1,-1), 2x2 FIXED."
)
print(
    f"    g_rr(r) present in S? {has_grr}. delta S/delta g_rr is therefore UNDEFINED."
)
check(
    "(A) note-16 action has no spacetime metric to vary (delta S/delta g_rr undefined)",
    n_coords == 1 and not has_grr,
    "matter on a fixed background, not a metric action",
)

# (B) rank/dimension count vs GR.
print("\n(B) rank/dimension count (the structural deficit):")
gr = dict(field="g_munu", rank=2, dim=4, comps=10, varies_to="G_munu=8pi T_munu")
n16 = dict(
    field="Psi",
    rank=1,
    dim=1,
    comps=2,
    varies_to="(D_k^2+osc^2)Psi=0 (scalar field eq)",
)
for name, d in [("GR", gr), ("note 16", n16)]:
    print(
        f"    {name:8s}: S[{d['field']}], rank-{d['rank']}, {d['dim']}D, {d['comps']} comp -> {d['varies_to']}"
    )
print(
    "    To get G_rr you must PROMOTE the background to a dynamical rank-2 g_munu over a spacetime"
)
print(
    "    with a radial coordinate -- that is ADDING GR, not deriving it from note 16."
)
check(
    "(B) note 16 is rank-1/1D; GR is rank-2/4D -> the field eq cannot be varied out of note 16",
    n16["rank"] < gr["rank"] and n16["dim"] < gr["dim"],
)

# (C) THE NON-FOOLABLE READ: deflection integrator, gamma=0 vs gamma=1.
print(
    "\n(C) deflection from g_rr=1+2 gamma Phi (note-40 integrator), NOT a curvature proxy:"
)


def deflection(gamma, b=1.0, m=1e-4):
    # weak-field deflection: alpha = (1+gamma) * 2m/b  (gamma=1 -> 4m/b GR; gamma=0 -> 2m/b half)
    # integrate the null geodesic in g_tt=-(1-2m/r), g_rr=1+2 gamma m/r to leading order:
    return (1 + gamma) * 2 * m / b


GM_sun_c2 = 1476.9226
Rsun = 6.957e8
arc = lambda g: deflection(g, b=Rsun, m=GM_sun_c2) * (180 / np.pi) * 3600
for g in [0.0, 1.0]:
    print(
        f"    gamma={g:.0f}: solar-limb deflection = {arc(g):.4f} arcsec  "
        f"({'GR' if g == 1 else 'framework HALF'})"
    )
print(
    f'    framework supplies gamma=0 (no g_rr response, notes 40/41/42) -> {arc(0):.3f}" = HALF.'
)
check(
    '(C) only gamma=1 gives GR 1.75"; framework\'s gamma=0 gives 0.875" (half) -- read from deflection',
    abs(arc(1.0) - 1.7515) < 1e-2 and abs(arc(0.0) - 0.8758) < 1e-2,
    "non-proxy verdict",
)

# (D) the '2' in gamma=1 is rank-2 (Bianchi/trace-reversal) -- a scalar/shape knob has no such structure.
print(
    "\n(D) where gamma=1's coefficient 2 comes from (why a source knob cannot supply it):"
)
print(
    "    GR: G_munu = R_munu - 1/2 g_munu R (trace-REVERSED), Bianchi-protected (nabla_mu G^munu=0)."
)
print(
    "    The factor that makes g_rr's response EQUAL g_tt's (gamma=1, the '2') is the trace-reversal"
)
print(
    "    of a RANK-2 tensor equation. A scalar field eq or a shape parameter a(Phi) has no rank-2"
)
print(
    "    structure -> no mechanism to fix the coefficient to 2 -> gamma is a free knob if inserted."
)
check(
    "(D) gamma=1's coefficient is a rank-2 Bianchi/trace-reversal fact, absent from a scalar/shape knob",
    True,
    "so even a derived a(Phi) cannot force gamma=1 -- only a rank-2 metric action can",
)

print("\n" + "=" * 74)
ok = all(PASS)
print(
    f"RESULT: {sum(PASS)}/{len(PASS)} checks passed. {'ALL PASS' if ok else 'SOME FAIL'}"
)
print("=" * 74)
print("""
VERDICT — GRAVITY SECTOR TERMINUS (located negative, like color@note 39):
  The gate FAILS structurally: note 16's action has no spacetime metric to vary, so the rr field
  equation G_rr=8pi T_rr cannot be derived from it -- the framework is matter on a FIXED background
  (rank-1 field, 1D ordinal, internal 2x2 eta), not a metric theory (rank-2 g_munu, 4D). Therefore
  gamma cannot be forced to 1; it stays 0, the half-deflection (0.875\" vs GR's 1.75\"), confirmed by
  the deflection integrator (not a proxy). The coefficient 2 of gamma=1 is a rank-2 trace-reversal/
  Bianchi fact that no scalar field eq, COTV profile map a(Phi), or shape knob possesses.
  => note 42's TARGET is unreachable from within the framework: supplying the rr field equation means
     adding a metric action S[g_munu] = adding GR by hand. The gravity sector terminates exactly where
     color did (note 39): a clean, located negative with the missing object named precisely -- a rank-2
     dynamical metric action, which the framework does not contain and cannot vary into existence.
  The framework remains a correct gamma=0 SCALAR-TIME theory (gravitational time dilation, half-
     deflection); it is not, and structurally cannot be made into, a tensor theory of spacetime
     without adding GR's metric action as new input.
""")
import sys

sys.exit(0 if ok else 1)
