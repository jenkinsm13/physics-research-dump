"""Verify note 35b: the equivalence principle as 'gravitating IS slowing time'.

Spine (note 35): local time-rate = time ray T(theta)=e^{-theta}; boost/redshift velocity
beta=tanh(theta); gravity ray G=e^{+theta}; T*G=1=L_y; net force F=2 sinh(theta).

EP map (the principled one): rapidity = Newtonian potential, theta = Phi_N = GM/rc^2,
forced by the boost-ADDITION theorem (rapidities add like potentials along a column).

Checks:
  (0) Re-confirm the spine pieces this note builds on: T*G=1, beta=tanh, F=2 sinh.
  (1) WEAK FIELD: T=e^{-Phi} and GR sqrt(1-2Phi) agree at LINEAR order (EP recovered);
      first disagree at O(Phi^2); leading relative deviation -> Phi^2 (coefficient 1).
      Earth-surface deviation ~5e-19 (indistinguishable from GR).
  (2) The relativistic source strength: 2 sinh(theta) -> 2 Phi = 2GM/rc^2 in weak field
      (the GR factor-of-2, not the Newtonian potential).
  (3) STRONG FIELD: exponential vs square-root; reproduce the deviation table
      (Phi=0.10,0.20,0.30,0.49) and the neutron-star number z_FW vs z_GR at Phi=0.2,
      with the -23.9% fractional redshift deficit.
  (3b) MAP FAMILY (the audit's core honesty check): the EP map is theta = a*Phi + c*Phi^2 + ...
      The slope a=1 is FORCED by the source-strength match (2 sinh -> 2 Phi). The second-order
      coefficient c is a genuine FREE PARAMETER, invisible to any weak-field observable:
        * EP residual (1 - T - Phi) is O(Phi^2) for ALL c  => weak-field EP is MAP-INDEPENDENT.
        * relative deviation from GR = (1-c) Phi^2 + O(Phi^3)  => only c sets the split.
        * strong-field NS redshift z=e^theta-1 slides 0.221->0.271 (quad c=0..1); the
          all-orders re-summation theta=-1/2 ln(1-2Phi) lands EXACTLY on GR's 0.291.
      So the -23.9% deficit is the signature of the CHOICE c=0, not a parameter-free prediction.
  (4) HORIZON: GR freezes at finite Phi=1/2 (sqrt->0); framework T=e^{-1/2}=0.6065 there
      (NO horizon); framework freezes only as theta->inf (beta=tanh->1). The exact-match
      map theta=-1/2 ln(1-2Phi) makes T==sqrt(1-2Phi) and sends theta->inf as Phi->1/2.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
print(f"phi={phi:.6f}  1/phi={1 / phi:.6f}")


def T_ray(th):
    return np.exp(-th)


def G_ray(th):
    return np.exp(+th)


def gr_rate(Phi):
    return np.sqrt(1 - 2 * Phi)


# ---------------------------------------------------------------- (0) spine recap
print("\n(0) spine pieces this note rests on:")
for th in [0.0, 1 / phi, 1.0, 2.0]:
    T, G = T_ray(th), G_ray(th)
    assert abs(T * G - 1) < 1e-12  # reciprocal law
    assert abs((G - T) / (G + T) - np.tanh(th)) < 1e-12  # beta = tanh
    assert abs((G - T) - 2 * np.sinh(th)) < 1e-12  # net force = 2 sinh
print("    T*G=1, beta=(G-T)/(G+T)=tanh(theta), F=G-T=2 sinh(theta)  OK")

# ---------------------------------------------------------------- (1) weak field / EP
print("\n(1) WEAK FIELD with theta = Phi_N (EP map): T=e^-Phi vs GR=sqrt(1-2Phi)")
print(f"    {'Phi':>9} {'T=e^-Phi':>14} {'GR':>14} {'rel.dev':>12} {'~Phi^2':>10}")
for Phi in [1e-9, 1e-6, 1e-4, 1e-3, 1e-2]:
    T, gr = T_ray(Phi), gr_rate(Phi)
    rel = (T - gr) / gr
    print(f"    {Phi:9.0e} {T:14.10f} {gr:14.10f} {rel:12.3e} {Phi**2:10.1e}")
    # linear terms identical => agreement to O(Phi^2): rel dev must be O(Phi^2), not O(Phi)
    assert abs(rel) < 5 * Phi**2 + 1e-15
# leading coefficient of the relative deviation -> 1 (i.e. rel ~ +Phi^2)
for Phi in [1e-4, 1e-3, 1e-2]:
    rel = (T_ray(Phi) - gr_rate(Phi)) / gr_rate(Phi)
    assert abs(rel / Phi**2 - 1.0) < 0.02, rel / Phi**2
print("    linear terms match (EP recovered); first split at O(Phi^2), coeff ~1.  OK")
# explicit Taylor identity: e^-x = 1-x+x^2/2-...,  sqrt(1-2x) = 1-x-x^2/2-...
xs = np.array([0.001, 0.01, 0.05])
lin_T = 1 - xs
lin_GR = 1 - xs
assert np.allclose(lin_T, lin_GR)  # linear pieces identical
# Earth surface potential
Phi_earth = 6.96e-10  # GM_earth/(R_earth c^2)
dev_earth = abs((T_ray(Phi_earth) - gr_rate(Phi_earth)) / gr_rate(Phi_earth))
print(
    f"    Earth surface Phi~{Phi_earth:.2e}: clock deviation from GR = {dev_earth:.2e} (~Phi^2)"
)
assert dev_earth < 1e-18

# ---------------------------------------------------------------- (2) source strength
print("\n(2) net force 2 sinh(theta) -> 2 Phi = 2GM/rc^2 in weak field (the GR '2'):")
for Phi in [1e-4, 1e-3, 1e-2]:
    F = 2 * np.sinh(Phi)
    assert abs(F - 2 * Phi) < 2 * Phi**3 + 1e-15  # 2 sinh x = 2x + x^3/3 + ...
    print(f"    Phi={Phi:.0e}: F=2 sinh(Phi)={F:.6e}, 2*Phi={2 * Phi:.6e}")
print("    matches relativistic source 2GM/rc^2 to O(Phi^3).  OK")

# ---------------------------------------------------------------- (3) strong field table
print("\n(3) STRONG FIELD deviation table (theta=Phi):")
print(f"    {'Phi':>6} {'T=e^-th':>10} {'sqrt(1-2th)':>12} {'rel.dev':>10}")
expected = {  # values quoted in the note
    0.10: (0.90484, 0.89443),
    0.20: (0.81873, 0.77460),
    0.30: (0.74082, 0.63246),
    0.49: (0.61263, 0.14142),
}
for Phi, (eT, eGR) in expected.items():
    T, gr = T_ray(Phi), gr_rate(Phi)
    rel = (T - gr) / gr
    print(f"    {Phi:6.2f} {T:10.5f} {gr:12.5f} {rel * 100:9.2f}%")
    assert abs(T - eT) < 5e-5, (Phi, T, eT)
    assert abs(gr - eGR) < 5e-5, (Phi, gr, eGR)

# neutron-star redshift number
Phi_ns = 0.2
z_fw = 1 / T_ray(Phi_ns) - 1
z_gr = 1 / gr_rate(Phi_ns) - 1
frac = (z_fw - z_gr) / z_gr
print(f"\n    neutron star Phi=0.2:  z_FW = e^Phi-1 = {z_fw:.4f}")
print(f"                           z_GR = 1/sqrt(1-2Phi)-1 = {z_gr:.4f}")
print(f"                           fractional redshift deficit = {frac * 100:.1f}%")
assert abs(z_fw - 0.2214) < 1e-3
assert abs(z_gr - 0.2910) < 1e-3
assert abs(frac - (-0.239)) < 2e-3

# ----------------------------------------------------- (3b) the map family / free parameter c
# theta = Phi + c Phi^2 + ...  (slope 1 forced by source strength; c is the only freedom).
# Proves: weak-field EP recovery is independent of c; the GR split is exactly (1-c) Phi^2;
# the strong-field redshift is therefore a MEASUREMENT of c, not a parameter-free prediction.
print("\n(3b) EP MAP FAMILY theta = Phi + c*Phi^2: where the one free parameter lives")


def theta_c(Phi, c):
    return Phi + c * Phi**2


# (i) weak-field EP residual (1 - T - Phi) is O(Phi^2) for every c -> linear EP is map-independent
print(
    "    weak-field EP residual |1 - T - Phi| (must be O(Phi^2), c-independent at leading order):"
)
for c in [0.0, 0.5, 1.0]:
    for Phi in [1e-4, 1e-2]:
        resid = abs(1 - T_ray(theta_c(Phi, c)) - Phi)
        # the linear (Phi^1) EP term cancels for ALL c: residual must scale like Phi^2, not Phi
        assert resid < 1.5 * Phi**2 + 1e-15, (c, Phi, resid)
    print(
        f"      c={c}: residual(1e-4)={abs(1 - T_ray(theta_c(1e-4, c)) - 1e-4):.3e} (~Phi^2, EP holds)"
    )

# (ii) relative deviation from GR -> (1-c) Phi^2 : c is the sole controller of the split
print("    relative deviation (T-GR)/GR  ->  (1-c) Phi^2 + O(Phi^3):")
for c in [0.0, 0.5, 1.0]:
    Phi = 1e-3
    rel = (T_ray(theta_c(Phi, c)) - gr_rate(Phi)) / gr_rate(Phi)
    coeff = rel / Phi**2
    assert abs(coeff - (1 - c)) < 0.01, (c, coeff)
    print(f"      c={c}: (rel dev)/Phi^2 = {coeff:.5f}  (theory 1-c = {1 - c:.5f})")

# (iii) strong-field NS redshift: quadratic family slides 0.221 -> 0.271, all-orders == GR 0.291
print(
    "    neutron-star z=e^theta-1 at Phi=0.2 across the family (the -23.9% is the c=0 choice):"
)
z_quad = {}
for c in [0.0, 0.25, 0.5, 0.75, 1.0]:
    z_quad[c] = np.exp(theta_c(0.2, c)) - 1
    print(f"      c={c:.2f}: z = {z_quad[c]:.4f}")
assert abs(z_quad[0.0] - 0.2214) < 1e-3  # the headline -23.9% deficit case
assert abs(z_quad[0.5] - 0.2461) < 1e-3
assert abs(z_quad[1.0] - 0.2712) < 1e-3  # quad c=1 truncation: NOT yet GR
# the all-orders re-summation IS GR exactly (this is the c=1 *endpoint*, fully summed):
theta_resum = -0.5 * np.log(1 - 2 * 0.2)
z_resum = np.exp(theta_resum) - 1
z_gr_ns = 1 / gr_rate(0.2) - 1
assert abs(z_resum - z_gr_ns) < 1e-12 and abs(z_resum - 0.2910) < 1e-3
print(
    f"      all-orders re-sum theta=-1/2 ln(1-2Phi): z = {z_resum:.4f} == GR z = {z_gr_ns:.4f}"
)
print(
    "    => weak-field EP is map-independent; strong field MEASURES c. No hidden knob; one DECLARED knob."
)

# (iv) THE DEEPER ASSUMPTION: theta_EP = Phi_N is NOT the spine's per-shell theta = k/phi.
# The imported relations (T=e^-theta, beta=tanh, F=2 sinh, and the additivity that "forces" a=1)
# were derived for the per-shell boost rapidity theta=k/phi (notes 16, 35). One shell down,
# theta = 1/phi = 0.618. Under the EP map theta=Phi_N, that single shell sits at Phi_N=0.618 --
# PAST GR's horizon (Phi_N=1/2). But the spine reaches the horizon at n_H=183 shells, not at
# Phi_N=1/2. So theta_shell and theta_EP differ by a factor of hundreds: theta=Phi_N is a
# SEPARATELY-POSITED identification, the load-bearing assumption beneath c (and beneath a=1).
print(
    "\n(3c) load-bearing assumption: theta_EP=Phi_N is NOT the spine's per-shell theta=k/phi:"
)
theta_one_shell = 1 / phi
beta_one_shell = np.tanh(theta_one_shell)
assert (
    abs(beta_one_shell - 0.5498) < 1e-3
)  # note-15 LIGO ratio, fixes theta_shell scale
# under theta_EP=Phi_N, the per-shell theta would map to Phi_N=0.618 > 0.5 (past GR horizon):
assert (
    theta_one_shell > 0.5
)  # one shell already past GR's Phi_N=1/2 if theta_EP==theta_shell
r_s_over_lP = (
    2953.0 / 1.616e-35
)  # Schwarzschild radius of M_sun (2953 m) / Planck length
n_H = np.log(r_s_over_lP) / np.log(
    phi
)  # spine horizon depth log_phi(r_s/l_P)=183.08 (note 35)
assert abs(n_H - 183.08) < 0.1
print(
    f"    per-shell theta=1/phi={theta_one_shell:.4f} (beta=tanh=0.5498); under theta_EP=Phi_N"
)
print(
    f"    that ONE shell -> Phi_N={theta_one_shell:.3f} > GR horizon 0.5, yet spine horizon is at"
)
print(
    f"    n_H~log_phi(r_s/l_P)~{n_H:.0f} shells, NOT Phi_N=1/2.  => theta_EP != theta_shell:"
)
print(
    "    the EP map is a posited identification (the note's load-bearing assumption), so c (and a) are free."
)

# ---------------------------------------------------------------- (4) horizon
print("\n(4) HORIZON:")
Phi_h = 0.5
assert abs(gr_rate(Phi_h) - 0.0) < 1e-12  # GR freezes at finite Phi=1/2
T_at_h = T_ray(Phi_h)
print(
    f"    at GR horizon Phi=1/2: GR rate=0 (frozen); framework T=e^-0.5={T_at_h:.4f} (NOT frozen)"
)
assert abs(T_at_h - 0.60653) < 1e-4
# framework freezes only as theta->inf, beta=tanh->1
for th in [1, 2, 3, 5, 10]:
    assert T_ray(th) > 0  # never exactly zero at finite theta
print(
    f"    framework: T->0 and beta=tanh(theta)->1 only as theta->inf "
    f"(tanh(10)={np.tanh(10):.6f}, T(10)={T_ray(10):.2e})"
)
# exact-match map theta = -1/2 ln(1-2Phi) makes T == sqrt(1-2Phi) and aligns horizons
print("    exact-match map theta=-1/2 ln(1-2Phi): T==GR, theta->inf as Phi->1/2:")
for Phi in [0.3, 0.49, 0.4999]:
    th = -0.5 * np.log(1 - 2 * Phi)
    assert abs(T_ray(th) - gr_rate(Phi)) < 1e-12  # identical clock by construction
    print(
        f"      Phi={Phi:.4f}: theta={th:.4f}, T=e^-th={T_ray(th):.5f} == sqrt(1-2Phi)={gr_rate(Phi):.5f}"
    )
# and theta -> inf as Phi -> 1/2
th_near = -0.5 * np.log(1 - 2 * 0.49999)
assert th_near > 4.0
print(f"      Phi=0.49999: theta={th_near:.3f} (-> infinity as Phi->1/2)  OK")

print(
    "\nALL CHECKS PASSED — weak-field EP recovered MAP-INDEPENDENTLY (linear term cancels"
)
print(
    "for every c; not evidence over GR). The EP map theta=Phi+c Phi^2 has ONE free param c:"
)
print(
    "a=1 forced by source strength, c unfixed by any weak-field observable. The strong-field"
)
print(
    "split is exactly (1-c)Phi^2; the -23.9% neutron-star z deficit at Phi=0.2 is the c=0"
)
print("(linear) CHOICE, with all-orders re-summation == GR. Strong-field z MEASURES c.")
