#!/usr/bin/env python3
"""
verify_gauge-structure.py  —  Note 18, Electroweak from Flow-Space.

Checks every claim in 18-gauge-structure.md to machine precision where the claim
is an identity, and to the stated bracket where it is an empirical comparison.

The flow-space generators (note 10/14/04/07):
    K   = [[0,-1],[-1,0]]   boost          (so(1,1), gravity/flow)        K^2 = I
    sx  = [[0, 1],[ 1,0]]   spinor half-boost generator (note 07)        sx^2 = I
    sz  = [[1, 0],[ 0,-1]]  time-reversal involution T (note 14)         sz^2 = I
    sy  = [[0,-i],[ i,0]]   quadrature partner                           sy^2 = I
    J   = [[0,-1],[ 1,0]]   compact rotor (note 04, Wick of K)           J^2 = -I

Claim chain:
  (A) {sx, sy, sz} close su(2): the SU(2)_L doublet algebra is the spinor
      half-boost + the now-involution + their commutator. EXACT.
  (B) U(1)_Y is the rotor J (note 04), the compact sibling of the boost.
  (C) Weinberg: tan^2 theta_W = g'^2/g^2 = 1/phi  =>  sin^2 = 1/phi^2 EXACTLY
      (because phi+1 = phi^2). Bare/unbroken value. NOTE: 3/8 is a GUT *seed*,
      not data -- the +1.86% is theory-to-theory, and is where the whole miss is born.
  (D) Running one boost shell (quantum 1/phi): sin^2 -> 1/phi^3 = 0.23607,
      compare measured sin^2 theta_W(m_Z) = 0.23121 (+2.1%, MS-bar).
      HONESTY: the running FACTOR is the strong part -- 1/phi = 0.6180 matches the
      *real* SM running ratio 0.2312/0.375 = 0.6165 to 0.24%. The +2.1% miss is the
      bare 1/phi^2-vs-3/8 offset carried down, not a separate error.
  (E) m_W/m_Z is NOT an independent observable. At tree level (rho=1)
      cos^2 = 1 - sin^2 is an identity, so given the angle it carries zero new info.
      With phi^3 = 2phi+1 it collapses EXACTLY: cos^2 theta_W = 2/phi^2,
      m_W/m_Z = sqrt2/phi, tan^2(run) = 1/(2phi). Reported as the golden shadow of
      the angle, not a second test.
  (E') SCHEME: +2.1% is MS-bar (0.23121). On-shell sin^2 = 1-(mW/mZ)^2 = 0.22305
      gives +5.8%. We compare in MS-bar and disclose both.
  (F) Higgs/vev analog: osc(0) = 1/2 order parameter; M^2 = osc^2.
  (G) SU(3)_color honesty: c_CFT ~ 3 gives N_colors = 3 (the count), not the 8 su(3) generators.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
TOL = 1e-12


def ok(name, residual, tol=TOL):
    flag = "PASS" if abs(residual) <= tol else "FAIL"
    print(f"  [{flag}] {name:54s} residual={residual:.3e}")
    return abs(residual) <= tol


def cmp(name, pred, meas, bracket_pct):
    miss = 100 * (pred - meas) / meas
    flag = "PASS" if abs(miss) <= bracket_pct else "FAIL"
    print(
        f"  [{flag}] {name:40s} pred={pred:.5f} meas={meas:.5f} miss={miss:+.2f}% (bracket +-{bracket_pct}%)"
    )
    return abs(miss) <= bracket_pct


allpass = True

# ---- generators ----
K = np.array([[0, -1], [-1, 0]], dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
J = np.array([[0, -1], [1, 0]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def comm(a, b):
    return a @ b - b @ a


print("=== (0) generator squares ===")
allpass &= ok("K^2 = I (boost, note 10)", np.linalg.norm(K @ K - I2))
allpass &= ok("sx^2 = I (spinor half-boost, note 07)", np.linalg.norm(sx @ sx - I2))
allpass &= ok("sz^2 = I (now-involution T, note 14)", np.linalg.norm(sz @ sz - I2))
allpass &= ok("J^2 = -I (rotor, note 04)", np.linalg.norm(J @ J + I2))

print("\n=== (A) SU(2)_L algebra from {half-boost, T, quadrature} ===")
allpass &= ok("[sx,sy] = 2i sz", np.linalg.norm(comm(sx, sy) - 2j * sz))
allpass &= ok("[sy,sz] = 2i sx", np.linalg.norm(comm(sy, sz) - 2j * sx))
allpass &= ok("[sz,sx] = 2i sy", np.linalg.norm(comm(sz, sx) - 2j * sy))
# Half-boost is the SU(2) doublet rep: exp((a/2) sx) is the note-07 spinor descent.
a = 1 / phi
half = np.cosh(a / 2) * I2 + np.sinh(a / 2) * sx  # closed form since sx^2 = I
full = np.cosh(a) * I2 + np.sinh(a) * sx
allpass &= ok(
    "half-boost squares to full boost (cover, note 07)",
    np.linalg.norm(half @ half - full),
)

print("\n=== (B) U(1)_Y = rotor; (C) Weinberg identity ===")
# The exact identity that makes the geometry work: (1/phi)/(1+1/phi) = 1/phi^2
R = 1 / phi
sin2_bare = R / (1 + R)
allpass &= ok(
    "sin^2 = (1/phi)/(1+1/phi) equals 1/phi^2 exactly", sin2_bare - 1 / phi**2
)
allpass &= ok("phi + 1 = phi^2 (the load-bearing identity)", (phi + 1) - phi**2)
print(f"    tan^2 theta_W(bare) = g'^2/g^2 = 1/phi = {1 / phi:.6f}")
print(f"    sin^2 theta_W(bare) = 1/phi^2        = {1 / phi**2:.6f}")
print("    NOTE: 3/8 is a GUT seed (theory), not data -- this is theory-to-theory.")
allpass &= cmp("(C) bare sin^2 vs 3/8 GUT seed (theory)", 1 / phi**2, 0.375, 3.0)

print("\n=== (D) running one boost shell: sin^2 -> 1/phi^3 ===")
sin2_run = 1 / phi**3
allpass &= ok("1/phi^2 * 1/phi = 1/phi^3", (1 / phi**2) * (1 / phi) - 1 / phi**3)
allpass &= cmp("(D) sin^2(m_Z) = 1/phi^3 vs PDG MS-bar 0.23121", sin2_run, 0.23121, 3.0)
allpass &= cmp("(D) sin^2(m_Z) = 1/phi^3 vs eff-lep 0.23155", sin2_run, 0.23155, 3.0)
# HONESTY: "one shell" is NOT the GUT->EW interval in the framework's own metric.
# On r_n = r0 phi^n, the SU(5)->mZ span (~1e14) is ~67 shells, not one.
nshells_gut_ew = np.log(2e16 / 91.1876) / lnphi
print(
    f"    HONEST: GUT->EW = log_phi(M_GUT/m_Z) = {nshells_gut_ew:.0f} shells on r_n=r0 phi^n, NOT one."
)
print(
    "    'one shell' is a CHOSEN decomposition: net suppression happens to equal 1/phi."
)
# The 0.24% 'running-ratio' agreement is NOT independent content: it is algebraically
# the ratio of the bare miss to the run miss, re-expressing the same two numbers.
real_run_ratio = 0.23121 / 0.375  # measured(MZ) / GUT seed(3/8)
miss_run = (1 / phi**3 - 0.23121) / 0.23121
miss_bare = (1 / phi**2 - 0.375) / 0.375
allpass &= ok(
    "0.24% run-ratio = (1+miss_run)/(1+miss_bare)-1 (NOT independent)",
    (1 / phi - real_run_ratio) / real_run_ratio
    - ((1 + miss_run) / (1 + miss_bare) - 1),
)
print(
    f"    1/phi={1 / phi:.5f} vs 0.2312/0.375={real_run_ratio:.5f} (0.24%) = ratio of the two misses, not a 3rd datum."
)

print("\n=== (E) m_W/m_Z is the tree-level shadow of the angle (NOT independent) ===")
mW, mZ = 80.377, 91.1876
mWmZ_meas = mW / mZ  # on-shell ratio
# Exact golden collapse via phi^3 = 2phi+1:
allpass &= ok("phi^3 = 2 phi + 1", phi**3 - (2 * phi + 1))
allpass &= ok(
    "cos^2 theta_W = 1 - 1/phi^3 = 2/phi^2 (exact)", (1 - 1 / phi**3) - 2 / phi**2
)
allpass &= ok(
    "m_W/m_Z = sqrt(1-1/phi^3) = sqrt2/phi (exact)",
    np.sqrt(1 - 1 / phi**3) - np.sqrt(2) / phi,
)
allpass &= ok(
    "tan^2 theta_W(run) = 1/(phi^3-1) = 1/(2 phi) (exact)",
    1 / (phi**3 - 1) - 1 / (2 * phi),
)
mWmZ_run = np.sqrt(2) / phi
mWmZ_bare = np.sqrt(1 - 1 / phi**2)
allpass &= cmp("(E) m_W/m_Z = sqrt2/phi vs on-shell meas", mWmZ_run, mWmZ_meas, 2.0)
print(
    f"    (bare/broken sqrt(1-1/phi^2) = {mWmZ_bare:.5f}, miss {100 * (mWmZ_bare - mWmZ_meas) / mWmZ_meas:+.1f}% — data prefer the RUN value, as expected)"
)
print("    NOT a second observable: cos^2 = 1 - sin^2 is the rho=1 tree identity.")

print("\n=== (E') scheme disclosure ===")
s2_onshell = 1 - mWmZ_meas**2
print(f"    MS-bar: sin^2 = 0.23121, miss {100 * (sin2_run - 0.23121) / 0.23121:+.2f}%")
print(
    f"    on-shell: sin^2 = 1-(mW/mZ)^2 = {s2_onshell:.5f}, miss {100 * (sin2_run - s2_onshell) / s2_onshell:+.2f}%"
)
print("    HEADLINE compared in MS-bar (+2.1%); on-shell (+5.8%) disclosed.")

print("\n=== (F) Higgs / vev analog (osc order parameter) ===")


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


allpass &= ok("osc(0) = 1/2 = c(0) (now-surface vev weight)", osc(0) - 0.5)
# inversion shell k1: osc = 1 (unbroken / mass-shell M^2 = 1)
k1 = (2 * 1 - 1) * np.pi / (4 * lnphi)
allpass &= ok("osc(k1) = 1 (unbroken phase, M^2=1)", osc(k1) - 1.0)
print(
    "    vacuum: osc runs 1/2 (now, broken) -> 1 (inversion shell, symmetric); M^2 = osc^2"
)

print("\n=== (G) SU(3)_color honesty ===")
c_CFT = 2.94  # note: spine/index emergent central charge ~ 2.94 -> 3
N_colors = round(c_CFT)
print(
    f"    c_CFT = {c_CFT} -> N_colors = {N_colors} (the COUNT of colors = 3 emergent dims)"
)
print(
    "    su(3) needs dim = 8 generators; the c~3 sector supplies N=3, NOT the algebra."
)
print(
    "    HONEST: color count closes; the 8 gluon generators do NOT close from c~3 alone."
)
allpass &= ok("N_colors from round(c_CFT) = 3", N_colors - 3)

print("\n=== Extension: m_W/m_Z = silver/gold (note 12 two-metal comb) ===")
silver = 1 + np.sqrt(2)  # delta_S, silver ratio (note 12)
# Leading silver constant is sqrt2 = delta_S - 1; gold quantum is phi.
allpass &= ok(
    "(silver-1)/phi = sqrt2/phi = m_W/m_Z", (silver - 1) / phi - np.sqrt(2) / phi
)
allpass &= ok(
    "silver amplitude (sqrt2-1)^2 = delta_S^-2", (np.sqrt(2) - 1) ** 2 - 1 / silver**2
)
print(
    f"    m_W/m_Z = sqrt2/phi = {np.sqrt(2) / phi:.5f} = (one silver)/(one gold) [CONJECTURE]"
)
print(
    f"    next-beat conjecture: sqrt2/phi^2 = {np.sqrt(2) / phi**2:.5f} (one further silver factor)"
)

print("\n=== HEADLINE (single falsifiable number) ===")
print(f"    sin^2 theta_W(m_Z) = 1/phi^3 = {1 / phi**3:.5f} vs 0.23121 (MS-bar): +2.1%")

print("\n" + "=" * 64)
print("ALL CHECKS PASS" if allpass else "SOME CHECK FAILED")
print("=" * 64)
import sys

sys.exit(0 if allpass else 1)
