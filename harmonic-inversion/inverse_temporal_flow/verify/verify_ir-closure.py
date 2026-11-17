#!/usr/bin/env python3
"""Mechanism E -- Cross-Scale Closure: the advanced mode vs the IR floor.

Tests whether the depth at which the advanced (s=+1, growing e^{+k/phi}) mode
would exceed a parameter-free IR/horizon norm reproduces the electron desert
depth n_e = 107.08 (note 30) -- and, decisively, whether the SAME rule
reproduces the muon (63), tau (102) or proton (92) tower (note 04).

Design choice: self-checking via assertions, so the script's EXIT CODE alone
certifies every number embedded in 31e-ir-closure.md. phi = (1+sqrt5)/2 is the
only irrational input; N_star, Theta_H come from notes 08 & 10.

Run:  python3 verify_ir-closure.py   (exit 0 == all embedded numbers confirmed)
"""

import math

phi = (1 + math.sqrt(5)) / 2.0  # 1.6180339887...
lnphi = math.log(phi)  # 0.4812118251...
inv_phi = 1.0 / phi  # 0.6180339887...

# ---------------------------------------------------------------- corpus inputs
N_star = 291.88  # note 08: log_phi(R_H / ell_P)  -- IR horizon shell
Theta_H = N_star / phi  # note 10: horizon rapidity  = 180.39
n_e = 107.08  # note 30: electron desert depth (absolute Planck ordinal)
# rotor tower (note 04) -- the INDEPENDENT cross-check depths:
k_e, k_mu, k_tau = 24.0, 63.0, 102.0
n_p = 91.9  # proton depth ~ log_phi(E_P/m_p)
flag = N_star / phi**2  # note 30 FAILURE FLAG ~ 111.5 (soft attractor)

# ------------------------------------- the four parameter-free closure readings
# "advanced growth e^{+K/phi} reaches the IR ceiling seeded at the UV (k=0)"
C1 = N_star  # growth fills full ladder:  K/phi = N*/phi  => K = N*
C2 = N_star / phi  # ceiling one phi-fold down: K = N*/phi
C3 = N_star / phi**2  # rapidity-of-rapidity:      K = N*/phi^2  (== flag)
C4 = Theta_H  # K equals horizon rapidity in shells (== C2 numerically)

closures = dict(C1=C1, C2=C2, C3=C3, C4=C4)

# ----------------------------------------------------- D2 structural cross-check
# The mechanism owns exactly ONE UV scale (k=0) and ONE IR scale (N*). Any
# f(N*, phi) returns a SINGLE number; it has no per-generation IR data, so it
# cannot generate the 24/63/102 tower. We exhibit that the only in-range closure
# (C3 ~ 111.5) misses every tower member and equals the failure flag.
tower = {"electron": n_e, "muon": k_mu, "tau": k_tau, "proton": n_p}
cross = {name: (C3, C3 - val) for name, val in tower.items()}

# ------------------------------------------------ D4 robustness re-derivation
# Adversarial re-derivation (independent pass). Two separable knobs exist:
#   (a) the CLOSURE FORM -- which power of 1/phi discounts N_star. The rotor
#       rapidity theta=k/phi justifies exactly ONE factor 1/phi (=> C2=180).
#       The SECOND factor in C3 (=> 111.5) has no dynamical warrant; it is
#       chosen solely because it lands in range. This is the dominant knob.
#   (b) the IR-CEILING CONVENTION -- N_star uses the Hubble radius. Switching
#       to the particle horizon (~3.2x R_H) shifts N_star by log_phi(3.2).
# Result of (b): the in-range output stays pinned to ~111-112, NEVER 107.
shift_particle_horizon = math.log(3.2) / lnphi  # ~2.42 shells
N_star_ph = N_star + shift_particle_horizon  # particle-horizon ceiling
C3_ph = N_star_ph / phi**2  # in-range closure under the alternative ceiling
# Algebraic identity: "ceiling minus one rapidity-fold" == C3 (NOT independent):
#   N*(1 - 1/phi) = N*/phi^2  because  1 - 1/phi = 1/phi^2.
C3_alt_route = N_star - Theta_H

# What IR ceiling WOULD be required for C3-form to select the electron exactly?
# N_107/phi^2 = 107.08  =>  N_107 = 107.08 * phi^2.  Compare to the true horizon.
N_required_for_107 = n_e * phi**2  # the ceiling that would yield 107.08
ceiling_deficit = N_star - N_required_for_107  # how far below the real horizon

# ----------------------------------------------------------- assertions (D1-D5)
assert abs(phi - 1.6180339887) < 1e-9
assert abs(lnphi - 0.4812118251) < 1e-9
assert abs(Theta_H - 180.39) < 0.05, Theta_H
assert abs(flag - 111.49) < 0.05, flag  # FAILURE FLAG reproduced
assert abs(C1 - 291.88) < 0.05
assert abs(C2 - 180.39) < 0.05
assert abs(C3 - 111.49) < 0.05
assert abs(C3 - flag) < 0.05  # the in-range closure IS the flag
assert abs(C3 - n_e) > 4.0  # it is NOT a hit on 107.08
# robustness: equally-defensible ceilings swing the answer by >70 shells
assert (C3 < C2 < C1) and (C1 - C3) > 70  # knob exposed under D4
# D4 re-derivation: under the particle-horizon ceiling the output stays ~112,
# still on the flag, still NOT 107 -- the closure-FORM, not N_star, is the knob.
assert abs(C3_ph - 112.41) < 0.05, C3_ph
assert abs(C3_ph - n_e) > 4.0  # alternative ceiling does NOT rescue 107
# the "ceiling minus one fold" route is algebraically identical to C3, not new:
assert abs(C3_alt_route - C3) < 1e-9
# selecting 107 exactly would require a ceiling ~11.5 shells below the horizon,
# with NO clean phi-structure (280.34 is not N*/phi^p for integer p) -> a knob.
assert abs(N_required_for_107 - 280.34) < 0.05, N_required_for_107
assert abs(ceiling_deficit - 11.54) < 0.05, ceiling_deficit

print("phi=%.10f  lnphi=%.10f  1/phi=%.10f" % (phi, lnphi, inv_phi))
print(
    "N_star=%.2f  Theta_H=N*/phi=%.2f  N*/phi^2=%.2f  <-- FAILURE FLAG (note 30)"
    % (N_star, Theta_H, flag)
)
print(
    "closures:  C1(=N*)=%.2f  C2(=N*/phi)=%.2f  C3(=N*/phi^2)=%.2f  C4(=Theta_H)=%.2f"
    % (C1, C2, C3, C4)
)
print("target n_e = %.2f" % n_e)
print(
    "only in-range closure C3:  C3 - n_e = %+.2f   C3 - flag = %+.2f"
    % (C3 - n_e, C3 - flag)
)
print("-- D2 cross-check (single IR scale -> single number, no tower) --")
for name, (pred, resid) in cross.items():
    print(
        "   %-9s actual=%6.2f   closure(C3)=%.2f   residual=%+6.2f"
        % (name, tower[name], pred, resid)
    )
print(
    "robustness swing  C3 -> C2 -> C1  =  %.1f -> %.1f -> %.1f  (>70 shells: knob exposed)"
    % (C3, C2, C1)
)
print("-- D4 re-derivation under alternative IR ceiling (particle horizon) --")
print(
    "   N* shift = log_phi(3.2) = %+.2f  ->  N*_ph=%.2f  ->  C3_ph=%.2f  (still ~112, not 107)"
    % (shift_particle_horizon, N_star_ph, C3_ph)
)
print(
    "   '(ceiling - one rapidity-fold)' route = %.2f  ==  C3  (algebraic identity, not independent)"
    % C3_alt_route
)
print(
    "   ceiling needed for C3-form to hit 107.08 = n_e*phi^2 = %.2f  =>  %.2f shells below horizon (no clean phi-power)"
    % (N_required_for_107, ceiling_deficit)
)
print(
    "VERDICT: failure-flag-111  (in-range closure lands on 111.5, +4.4 above 107, not a result)"
)
print("ALL ASSERTIONS PASSED")
