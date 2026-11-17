#!/usr/bin/env python3
"""Verify Mechanism 31d: rotor winding / anomaly bound for charged-generation TERMINATION.

Pre-registered disownment test (D1-D5). A clean NEGATIVE is the expected outcome:
the winding count reproduces the INPUT comb (24/63/102, step 39) but cannot terminate
the tower without a hand-tuned defect threshold, predicts an ALLOWED 4th tooth at k=141,
and yields NO absolute depth (no 107 / 92 / 111).
"""

import numpy as np

phi = (1 + 5**0.5) / 2
L = np.log(phi)  # ln phi = 0.481212
print(f"phi={phi:.6f}  ln phi={L:.6f}  1/phi={1 / phi:.6f}")

ke, kmu, ktau, k4 = 24, 63, 102, 141
step = 39
dk = np.pi / (2 * L)  # comb spacing 3.26425
print(f"comb spacing Dk = pi/(2 ln phi) = {dk:.5f} ; step/Dk = {step / dk:.4f} (~12)\n")

# --- winding per generation: 39 ln phi vs 3*2pi ---
theta_gen = step * L
defect_gen = 3 * 2 * np.pi - theta_gen
print(
    f"theta_gen = 39 ln phi      = {theta_gen:.4f} rad = 2pi * {theta_gen / (2 * np.pi):.5f}"
)
print(f"3 full turns               = {3 * 2 * np.pi:.4f} rad")
print(
    f"defect/gen                 = {defect_gen:+.5f} rad   (windings/gen = {theta_gen / (2 * np.pi):.5f} ~ 3)"
)
d78 = 78 * L - 12 * np.pi  # corpus two-generation figure, note 17
print(
    f"corpus 78 ln phi - 12 pi   = {d78:.5f} rad  (per gen {d78 / 2:+.5f}); |.|={abs(d78 / 2):.5f}\n"
)

# --- CROSS-CHECK (D2): comb-tooth condition 2k ln phi = (2n-1) pi/2 ---
print(
    "D2 cross-check: comb teeth (2k ln phi / pi should be near odd half-integer) and windings"
)
print(
    f"{'mode':>5} {'k':>4} {'2k lnphi/pi':>12} {'tooth':>6} {'signed miss':>12} {'winding':>9}"
)
# Corpus assigns each lepton to the comb tooth continuing the 7.5/19.5/31.5/43.5 sequence
# (one tooth per 12 reversals, note 04). round() snaps 43.195 to 43.0 -- wrong tooth -- so
# fix the tooth to the half-integer ABOVE the value, the one the comb sequence actually selects.
for name, k in [("e", ke), ("mu", kmu), ("tau", ktau), ("4th", k4)]:
    x = 2 * k * L / np.pi
    tooth = np.ceil(x - 0.5) + 0.5  # next half-integer of form integer+0.5 above x
    miss = tooth - x  # signed; grows monotonically by the equidistribution drift
    wind = k * L / (2 * np.pi)
    print(f"{name:>5} {k:>4} {x:>12.5f} {tooth:>6.1f} {miss:>12.3f} {wind:>9.4f}")
print(
    "  -> miss grows monotonically (Weyl equidistribution); 4th at k=141 is an ALLOWED tooth.\n"
)

# --- D1/D4 KNOB 1: termination is threshold-dependent (a KNOB) ---
print(
    "D1/D4 KNOB 1: 'N_max' depends entirely on chosen defect threshold Theta (a free knob):"
)
d78 = 78 * L - 12 * np.pi  # corpus two-generation defect, note 17
for label, Theta in [
    ("pi/2", np.pi / 2),
    ("pi/3", np.pi / 3),
    ("pi/4", np.pi / 4),
    ("1/phi", 1 / phi),
    ("ln phi", L),
    ("|dtheta_g|", abs(d78)),
    ("0.25 (tuned to 3)", 0.25),
]:
    Nmax = int(np.floor(Theta / abs(defect_gen)))
    print(
        f"   Theta = {label:>18} = {Theta:.5f}: N_max = floor(.../{abs(defect_gen):.4f}) = {Nmax}"
    )
# the EXACT window that yields N_max=3, and the test that no corpus constant lands in it
lo, hi = 3 * abs(defect_gen), 4 * abs(defect_gen)
print(f"   window for N_max=3: Theta in [{lo:.5f},{hi:.5f}) rad (width {hi - lo:.5f})")
consts = {
    "1/phi": 1 / phi,
    "ln phi": L,
    "|dtheta_g|": abs(d78),
    "pi/phi^2": np.pi / phi**2,
    "pi/4": np.pi / 4,
}
inside = [c for c, v in consts.items() if lo <= v < hi]
print(
    f"   corpus constants inside that window: {inside if inside else 'NONE -> unanchored knob'}"
)
print("   parameter-free choices give 0/2/5/7/9/12/19 -- never robustly 3.\n")

# --- D4 KNOB 2: the BREAKDOWN CRITERION itself is a knob (different quantity -> different count) ---
print("D1/D4 KNOB 2: which quantity is thresholded is ALSO a free choice:")
# alternative criterion: mode 'falls off its comb tooth' when tooth-miss reaches half-spacing (0.5)
m_e = (np.ceil(2 * ke * L / np.pi - 0.5) + 0.5) - 2 * ke * L / np.pi
m_mu = (np.ceil(2 * kmu * L / np.pi - 0.5) + 0.5) - 2 * kmu * L / np.pi
drift = abs(m_mu - m_e)  # per-generation drift on the half-integer (comb-tooth) axis
print(
    f"   alt criterion: tooth-miss drifts {drift:.4f}/gen on the .5-axis; cap at 0.5 -> "
    f"N ~ floor(0.5/{drift:.4f}) = {int(np.floor(0.5 / drift)) if drift else 'inf'}"
)
print(
    "   cumulative-defect vs comb-tooth-fall-off give DIFFERENT counts -> criterion is itself a knob.\n"
)

# --- D3: a '3' bound brushes the tau ---
print("D3: accumulated defect by generation vs the boundary that would forbid gen 4")
for g in range(1, 5):
    print(f"   gen {g}: cumulative |defect| = {abs(g * defect_gen):.4f} rad")
print(
    "   tau(g3)=0.2470, 4th(g4)=0.3292 -- one defect step apart; any Theta forbidding 4 nearly forbids 3.\n"
)

# --- D5: no drift to 111 / no absolute depth at all ---
print(
    "D5: the winding count yields COUNTS (0/2/3/9/12/19/inf), never an absolute depth."
)
print(
    f"   winding total at k=141 is {k4 * L / (2 * np.pi):.4f} turns; at the desert depth k=107 it is "
    f"{107 * L / (2 * np.pi):.4f} turns -- the rule is ordinal-agnostic."
)
print(
    f"   N*/phi^2 attractor = {(141) / phi**2:.4f} (if N*=141) -- the rule never approaches it: it emits"
)
print(
    "   dimensionless counts, with no map to 107.08, 91.9, or 111.5. D5 NOT triggered (correctly).\n"
)

print(
    "VERDICT: negative. Reproduces the input comb; cannot terminate the tower without a"
)
print(
    "tuned threshold; predicts a 4th lepton at k4=141 (ln m4 = a*141+b ~ 3e4 GeV) is ALLOWED."
)
