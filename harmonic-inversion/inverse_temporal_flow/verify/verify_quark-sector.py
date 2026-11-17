#!/usr/bin/env python3
"""
verify_quark-sector.py  —  Note 17: The Quark Sector and CKM from the Rotor.

Checks every embedded number in 17-quark-sector.md to machine precision where the
claim is exact (group identities, mass-ratio<->ordinal algebra) and against PDG-2024
data where the claim is a physical prediction (Cabibbo angle, Wolfenstein lambda,
CKM hierarchy). Honest: physical fits print the measured value and the % miss; only
the algebraic identities are asserted at 1e-12.

Builds on:
  - note 04 (lepton rotor: ordinals 24/63/102, step 39, delta_theta_g = 78 ln phi - 12 pi)
  - note 07 (fermions on osc=1/2 nodes; half-boost double cover)
  - note 10 (master boost group V(k), Lambda, the compact SO(2) real form = the rotor)
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
dtg = 78 * lnphi - 12 * np.pi  # lepton rotor angle per generation (note 04)

PASS = True


def check(name, got, want, tol=1e-9, kind="exact"):
    global PASS
    ok = abs(got - want) <= tol
    if kind == "exact" and not ok:
        PASS = False
    flag = "OK " if ok else ("..  " if kind != "exact" else "XX ")
    print(f"  [{flag}] {name:42s} got={got:.6g}  want={want:.6g}")
    return ok


def report(name, pred, meas):
    miss = abs(pred - meas) / abs(meas) * 100
    print(f"   ~    {name:42s} pred={pred:.5g}  meas={meas:.5g}  miss={miss:5.1f}%")
    return miss


print("=" * 74)
print("NOTE 17 — QUARK SECTOR & CKM FROM THE ROTOR")
print("=" * 74)

# ---------------------------------------------------------------------------
# 0. Constants and the lepton calibration (note 04). Three equispaced ordinals
#    24/63/102 -> least-squares slope collapses to the endpoint slope.
# ---------------------------------------------------------------------------
print("\n[0] Lepton mass calibration  ln m = a*k + b  (note 04, equispaced 24/63/102)")
me, mmu, mtau = 0.510999, 105.658, 1776.86  # MeV
ke, kmu, ktau = 24, 63, 102
a = (np.log(mtau) - np.log(me)) / (ktau - ke)
b = np.log(me) - a * ke
check("slope a", a, 0.1045383421, tol=1e-9)
check(
    "e^{39 a} = geom-mean gen step",
    np.exp(39 * a),
    np.sqrt((mmu / me) * (mtau / mmu)),
    tol=1e-6,
)
check("a/lnphi (mass = phi^{a/lnphi . k})", a / lnphi, 0.2172397616, tol=1e-9)


def kord(m_MeV):
    return (np.log(m_MeV) - b) / a


# ---------------------------------------------------------------------------
# 1. Quark mass-ordinals (PDG 2024; u,d,s @ 2 GeV, c,b @ own mass, t pole).
# ---------------------------------------------------------------------------
print("\n[1] Quark ordinals on the lepton calibration")
M = dict(u=2.16, d=4.70, s=93.5, c=1273.0, b=4183.0, t=172570.0)  # MeV
o = {q: kord(m) for q, m in M.items()}
for q in ["u", "d", "s", "c", "b", "t"]:
    print(f"        k_{q} = {o[q]:7.2f}")
# Honest: NOT a clean step-39 progression like leptons.
print(
    f"        up-type steps   c-u, t-c = {o['c'] - o['u']:.1f}, {o['t'] - o['c']:.1f}"
)
print(
    f"        down-type steps s-d, b-s = {o['s'] - o['d']:.1f}, {o['b'] - o['s']:.1f}"
)
print("        (deliberately NOT equispaced -> quarks are a distorted sub-lattice)")

# ---------------------------------------------------------------------------
# 2. The mass-ratio = phi-power-of-ordinal identity (EXACT, the bridge).
#    m_i/m_j = exp(a(k_i-k_j)) = phi^{(a/lnphi)(k_i-k_j)}.
# ---------------------------------------------------------------------------
print("\n[2] Mass ratio <-> ordinal gap is exact (the rotor-chord bridge)")
md, ms = M["d"], M["s"]
check(
    "sqrt(md/ms) via ordinals",
    np.exp(a * (o["d"] - o["s"]) / 2),
    np.sqrt(md / ms),
    tol=1e-12,
)
check(
    "sqrt(md/ms) = phi^{a(kd-ks)/(2lnphi)}",
    phi ** (a * (o["d"] - o["s"]) / (2 * lnphi)),
    np.sqrt(md / ms),
    tol=1e-12,
)

# ---------------------------------------------------------------------------
# 2a. HONESTY: the "framework route" through the lepton calibration is
#     IDENTICALLY sqrt(md/ms). lnphi cancels, the slope a cancels, the
#     intercept b never enters. The framework supplies the INTERPRETATION
#     (a half-boost chord), not the digit. Prove the cancellation to roundoff.
# ---------------------------------------------------------------------------
print("\n[2a] HONESTY: phi and the slope a cancel -> the digit is pure GST sqrt(md/ms)")
framework_route = phi ** (a * (o["d"] - o["s"]) / (2 * lnphi))
naive_ratio = np.sqrt(md / ms)
check(
    "framework route == sqrt(md/ms) to roundoff",
    framework_route,
    naive_ratio,
    tol=1e-15,
)
print(
    "        => phi^{a(kd-ks)/(2lnphi)} = exp[(ln md - ln ms)/2] = sqrt(md/ms) IDENTICALLY."
)
print("           No phi-digit is added. The claim is structural, not numerical.")

# ---------------------------------------------------------------------------
# 3. HARD NUMBER 1 — Cabibbo angle = down-sector half-chord = sqrt(m_d/m_s).
#    (Gatto-Sartori-Tonin, here a rotor half-step on the down sub-lattice.)
# ---------------------------------------------------------------------------
print("\n[3] HARD NUMBER 1 — Cabibbo angle from the down-sector mass chord")
lam_pred = np.sqrt(md / ms)
print(f"        lambda_pred = sqrt(m_d/m_s) = {lam_pred:.5f}")
m_lam = report("Wolfenstein lambda  = sqrt(md/ms)", lam_pred, 0.2250)
m_Vus = report("|V_us| = sin theta_c", lam_pred, 0.2243)
thc_pred = np.degrees(np.arcsin(lam_pred))
m_thc = report("theta_c (deg)", thc_pred, 13.04)
# Honest input band: m_d carries ~10% uncertainty (PDG: 4.70 +0.48/-0.17 MeV).
# The falsifiable band is WIDER than the headline agreement.
lo, hi = np.sqrt((4.70 - 0.17) / ms), np.sqrt((4.70 + 0.48) / ms)
print(
    f"        honest input band from m_d=4.70(+0.48/-0.17): lambda in [{lo:.3f}, {hi:.3f}]"
)
print(
    "        => the 0.4%% agreement rides on the lattice m_d/m_s; it is GST's, not a phi-prediction."
)

# ---------------------------------------------------------------------------
# 4. CKM hierarchy — lambda, lambda^2, lambda^3 vs measured (honest brackets).
# ---------------------------------------------------------------------------
print("\n[4] CKM hierarchy  (lambda, lambda^2, lambda^3) — honest brackets")
Vus, Vcb, Vub = 0.2243, 0.0408, 0.00382
report("|V_us| ~ lambda", lam_pred, Vus)
report("|V_cb| ~ lambda^2", lam_pred**2, Vcb)  # high: needs Wolfenstein A
report("|V_ub| ~ lambda^3", lam_pred**3, Vub)  # high
A = Vcb / lam_pred**2
print(f"        Wolfenstein A = Vcb/lambda^2 = {A:.3f}  (so V_cb = A lambda^2, A~0.81)")
report("|V_cb| = A lambda^2 (A=0.812)", A * lam_pred**2, Vcb)
# Honest: the single-sector 2->3 chords do NOT rescue V_cb. The down cross-chord
# OVERSHOOTS badly (266%); the linear ratio undershoots. They bracket but the
# bracket is wide and unselective -> V_cb requires the unexplained A~0.81.
report(
    "down cross-chord sqrt(ms/mb) vs Vcb", np.sqrt(M["s"] / M["b"]), Vcb
)  # 266% high
report("linear m_s/m_b           vs Vcb", M["s"] / M["b"], Vcb)  # undershoots
print("        => 0.0224 < Vcb=0.0408 < 0.150 : wide unselective bracket, NOT a win.")
report(
    "|V_ub/V_cb| ~ sqrt(mu/mc)", np.sqrt(M["u"] / M["c"]), Vub / Vcb
)  # undershoots 56%
print("        => V_ub residual ~ CP apex sqrt(rho^2+eta^2)~0.42, seat = rotor phase.")

# ---------------------------------------------------------------------------
# 5. The rotor angle delta_theta_g and its relation to the chord (note 04/10).
#    The compact SO(2) rotor steps by |delta_theta_g| = 0.16459 per LEPTON gen;
#    sin of it brackets lambda but is not the precise hit (the precise hit is the
#    down-sector MASS chord). Report honestly.
# ---------------------------------------------------------------------------
print("\n[5] Rotor angle (note 04 compact real form) vs the chord")
check("delta_theta_g = 78 lnphi - 12 pi", dtg, -0.1645894884, tol=1e-9)
report("sin|delta_theta_g| (rotor) vs lambda", np.sin(abs(dtg)), 0.2250)
report("|delta_theta_g| (rotor)    vs lambda", abs(dtg), 0.2250)
print("        => the mass-chord sqrt(md/ms)=0.2242 is the sharp predictor;")
print("           the bare lepton-rotor sine 0.1638 only brackets it (~27% low).")

# Extension A: the CP apex sqrt(rho^2+eta^2) as the 2-step rotor phase sin(2|dtg|).
# Boost-group native: chord moduli on SO(1,1), CP PHASE on the compact SO(2) rotor.
# Honest bracket: measured apex 0.383 lies between sin(2|dtg|) and sin(3|dtg|).
apex_meas = np.hypot(0.1591, 0.3486)  # PDG rhobar=0.159, etabar=0.349 -> apex
print("        Extension A: CP apex = accumulated rotor phase (compact SO(2) leg)")
report("apex ~ sin(2|delta_theta_g|)", np.sin(2 * abs(dtg)), apex_meas)
print(
    "        bracket: sin(2|dtg|)=%.3f < apex=%.3f < sin(3|dtg|)=%.3f (parameter-free, phi-carrying)"
    % (np.sin(2 * abs(dtg)), apex_meas, np.sin(3 * abs(dtg)))
)

# ---------------------------------------------------------------------------
# 6. Half-boost / parity class (note 07): doubled-depth shells land on osc=1/2.
# ---------------------------------------------------------------------------
print("\n[6] Parity class consistency (note 07 half-boost node)")


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


kn = lambda n: (2 * n - 1) * np.pi / (4 * lnphi)
check("osc(2 k_1) = 1/2 (fermion node)", osc(2 * kn(1)), 0.5, tol=1e-12)

# ---------------------------------------------------------------------------
# 7. EXTENSION — the strain ratio as a one-shot Wolfenstein A.
#    A_strain = sqrt[ (s-d)(c-u) / (b-s)(t-c) ] from the §1 ordinal steps.
#    Honest: this is O(1) (~1.01), brackets A=O(1) but does NOT pin 0.81; it is
#    high by the same ~25% as the raw lambda^2 miss. Prediction: A_strain should
#    drift toward 0.81 when the quark ordinals are recomputed at a COMMON scale
#    (the table mixes 2GeV / own-mass / pole). Falsifier if it stays at 1.0.
# ---------------------------------------------------------------------------
print("\n[7] EXTENSION — strain ratio A_strain vs Wolfenstein A")
sd, bs = o["s"] - o["d"], o["b"] - o["s"]
cu, tc = o["c"] - o["u"], o["t"] - o["c"]
A_strain = np.sqrt((sd * cu) / (bs * tc))
print(
    f"        gaps: down (s-d,b-s)=({sd:.1f},{bs:.1f})  up (c-u,t-c)=({cu:.1f},{tc:.1f})"
)
report("A_strain = sqrt[(s-d)(c-u)/((b-s)(t-c))]", A_strain, A)
print("        => A_strain ~ 1.01 brackets A=O(1) but does NOT pin 0.81 (high ~25%).")
print(
    "           Prediction: A_strain -> 0.81 under common-scale ordinal recomputation."
)

# ---------------------------------------------------------------------------
print("\n" + "=" * 74)
print("EXACT-IDENTITY CHECKS:", "ALL PASS" if PASS else "SOME FAILED")
print("Physical fits are reported with honest % miss above (not pass/fail).")
print(
    "Headline number: lambda = sqrt(m_d/m_s) = %.4f vs PDG 0.2250 (%.1f%%)."
    % (lam_pred, abs(lam_pred - 0.2250) / 0.2250 * 100)
)
print("HONESTY: this is the GST relation; phi and slope a cancel (see [2a]).")
print("The framework owns the INTERPRETATION (half-boost chord), not the digit;")
print("input band from m_d is lambda in [%.3f, %.3f]." % (lo, hi))
print("=" * 74)
import sys

sys.exit(0 if PASS else 1)
