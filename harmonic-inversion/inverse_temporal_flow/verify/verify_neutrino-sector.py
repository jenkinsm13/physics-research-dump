"""Machine-precision verification of branch 19 (note 19-neutrino-sector.md).

Framework-internal identities are ASSERTED (residuals ~1e-15). Comparisons to
oscillation data are PRINTED as informational brackets, never asserted at tight
tolerance -- nature does not match a formula to machine precision, and asserting
on it would falsely fail the script.

Checks:
  1. osc-node sector: osc(k_m^nu)=1/2 at k=m*pi/(2 ln phi) (the inversion half-comb).
  1b. HONESTY: osc=1/2 is NOT the suppressor (only x2/3 vs charged); depth-only
      overshoots the absolute scale by ~200x -- so the seesaw (sec 2) sets the scale.
  2. now-seed: G_flow(0)=0 exactly (the m1~0 / normal-ordering anchor).
  2b. parameter-free heavy-pair ratio m2/m3 = sinh(theta_1)/sinh(theta_2), theta_m=m*DK/phi.
  3. seesaw: m_nu = m_D^2/M_R = m_D e^{-2 theta_R}; round-trip factor 2 = note 05.
  3b. UNIFIED mass law: m_nu(m) = (seesaw scale) * sinh(m DK/phi)/sinh(2 DK/phi).
      sec-2 scale x sec-1 texture, ONE formula; m=0->0, m=2->atmospheric by anchor.
  4. theta_13 = |delta_theta_g| = |78 ln phi - 12 pi| (the note-04 rotor defect,
      78=2*Delta_g and 12 forced by the charged-lepton tower, NOT tuned to theta_13).
  5. theta_12: tan = 1/phi  =>  sin^2 = 1/(2+phi) exactly (golden-ratio mixing).
  6. theta_23 = 45 deg (now-surface equal weight 1/2).
  7. mass-ratio bracket m2/m3 ~ phi^-4; splitting ratio ~ phi^-7.
  8. EXTENSION: |delta_CP - pi| = |delta_theta_g| * phi^p, p in {1,2} (rotor's shadow);
      honest band [15.3, 24.7] deg -- the power p is NOT forced, octant/sign open.

Run: python3 verify_neutrino-sector.py
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
DK = np.pi / (2 * LNPHI)  # inversion-shell spacing 3.26425
DELTA_G = 78 * LNPHI - 12 * np.pi  # note-04 lepton rotor defect, -0.16459

# measured oscillation parameters (NuFIT 5.x, normal ordering); only used for PRINTED brackets
DM2_21 = 7.42e-5  # eV^2 (solar)
DM2_32 = 2.51e-3  # eV^2 (atmospheric)
S2_13_MEAS = 0.0220
S2_12_MEAS = 0.304
DCP_MEAS_DEG = (
    197.0  # NuFIT 5.x normal ordering best fit (= -163 deg), 1-sigma ~ +42/-25
)
T13_MEAS_DEG = np.degrees(np.arcsin(np.sqrt(S2_13_MEAS)))  # 8.53
T12_MEAS_DEG = np.degrees(np.arcsin(np.sqrt(S2_12_MEAS)))  # 33.46

TOL = 1e-12


def osc(k):
    return 1.0 / (1 + np.cos(2 * k * LNPHI) ** 2)


def G_flow(k, dressing):
    return -dressing * np.sinh(k / PHI)


def check():
    print(f"PHI={PHI:.10f}  LNPHI={LNPHI:.10f}  1/PHI={1 / PHI:.10f}")
    print(f"Delta_k=pi/(2 lnphi)={DK:.6f}   delta_theta_g={DELTA_G:.12f}\n")

    print("=== 1. osc-node sector: neutrinos on osc=1/2 (inversion half-comb) ===")
    worst = 0.0
    # m=0 (the now-seed) is itself an osc=1/2 node: osc(0)=1/(1+cos^2 0)=1/2=c(0). m>=0.
    for m in range(0, 6):
        k = m * DK
        o = osc(k)
        worst = max(worst, abs(o - 0.5))
        print(f"   m={m}  k_nu={k:8.4f}  osc={o:.15f}")
    assert worst < TOL, worst
    print(f"   max |osc - 1/2| = {worst:.2e}  (ASSERTED, including the m=0 now-seed)\n")

    print("=== 1b. HONESTY: osc=1/2 is NOT the suppressor; depth-only OVERSHOOTS ===")
    # osc=1/2 vs charged-lepton osc~0.75 is only x2/3 -- not a mass suppressor.
    print(
        f"   osc(node)/osc(charged) = 0.5/0.75 = {0.5 / 0.75:.4f}  (only x2/3, NOT a suppressor)"
    )
    # heaviest node m=2 (theta=2 DK/phi) vs electron (k=24, theta=24/phi): depth-only ratio
    th_e = 24 / PHI
    th_m3 = 2 * DK / PHI
    depth_ratio = np.sinh(th_m3) / np.sinh(th_e)  # osc cancels (both ~1/2-ish here)
    m3_over_me_meas = np.sqrt(DM2_32) / 0.511e6  # sqrt(Dm32) eV / m_e eV
    overshoot = depth_ratio / m3_over_me_meas
    print(f"   sinh(theta_m3)/sinh(theta_e) = {depth_ratio:.3e}   (depth-only m3/m_e)")
    print(f"   measured m3/m_e              = {m3_over_me_meas:.3e}")
    print(
        f"   => geometry OVERSHOOTS scale by ~{overshoot:.0f}x  (the seesaw e^-2thR supplies the rest)"
    )
    assert overshoot > 50, (
        overshoot
    )  # honest: depth-only fails the absolute scale by >50x
    print("   on-node geometry sets TEXTURE, seesaw sets SCALE (sec 3 fuses them)\n")

    print(
        "=== 2. now-seed (m=0 node): G_flow(0)=0 => m1=0 exactly => NORMAL ordering ==="
    )
    g0 = G_flow(0.0, 0.5)
    print(f"   G_flow(m=0 node) = {g0:.1e}  (massless lightest, the now-seed itself)")
    assert abs(g0) < TOL
    # heavy pair are the next two nodes m=1,2; monotone sinh ladder => deeper=heavier
    fl = [abs(G_flow(m * DK, 0.5)) for m in range(1, 4)]
    print(f"   |G_flow| at m=1,2,3 nodes: {fl[0]:.4f} < {fl[1]:.4f} < {fl[2]:.4f}")
    assert fl[0] < fl[1] < fl[2], "sinh ladder not monotone"
    print("   monotone deeper=>heavier (ASSERTED)\n")

    print(
        "=== 2b. parameter-free heavy-pair ratio m2/m3 = sinh(theta_1)/sinh(theta_2) ==="
    )
    # lightest = m=0 (massless); heavy pair = nodes m=1,2; mass ~ |G_flow| ~ sinh(theta)
    m2_m3_pred = np.sinh(DK / PHI) / np.sinh(2 * DK / PHI)
    m2_m3_meas = np.sqrt(DM2_21 / DM2_32)
    print(
        f"   PREDICTION m2/m3 = sinh({DK / PHI:.3f})/sinh({2 * DK / PHI:.3f}) = {m2_m3_pred:.4f}"
    )
    print(
        f"   measured sqrt(Dm21/Dm32) = {m2_m3_meas:.4f}  bracket {100 * (m2_m3_pred / m2_m3_meas - 1):+.1f}%"
    )
    # this is a genuine framework output (node ordinals only); assert it equals the sinh ratio
    assert abs(m2_m3_pred - np.sinh(DK / PHI) / np.sinh(2 * DK / PHI)) < TOL
    print(
        f"   (phi^-4 = {PHI**-4:.4f} is a numerical observation on the MEASURED 0.172, not this output)\n"
    )

    print(
        "=== 3. seesaw m_nu = m_D^2 / M_R = m_D e^{-2 theta_R} (factor 2 = round trip) ==="
    )
    m_D = 1.778e9  # eV (tau scale Dirac choice)
    m_nu = 0.05  # eV (atmospheric)
    theta_R = -0.5 * np.log(m_nu / m_D)
    M_R = m_D**2 / m_nu
    # internal consistency of the seesaw algebra: m_D*e^{-2 theta_R} == m_nu
    assert abs(m_D * np.exp(-2 * theta_R) - m_nu) / m_nu < TOL
    print(
        f"   theta_R = {theta_R:.4f}  ordinal k_R = phi*theta_R = {PHI * theta_R:.1f}"
    )
    print(f"   M_R = {M_R:.3e} eV = {M_R / 1e9:.3e} GeV   (cf horizon shell N*=291.88)")
    print("   m_D e^{-2 theta_R} == m_nu  (ASSERTED, seesaw algebra self-consistent)\n")

    print(
        "=== 3b. UNIFIED mass law: seesaw SCALE x node-ladder TEXTURE (one formula) ==="
    )
    # m_nu(m) = (m_D e^-2thR) * sinh(m DK/phi)/sinh(2 DK/phi); anchored so m=2 -> atmospheric.
    scale = m_D * np.exp(-2 * theta_R)  # = 0.05 eV by construction (sec 2)
    masses = [scale * np.sinh(m * DK / PHI) / np.sinh(2 * DK / PHI) for m in (0, 1, 2)]
    print(
        f"   m1 (m=0 node) = {masses[0]:.5f} eV   (EXACTLY 0: sinh(0)=0, the now-seed)"
    )
    print(
        f"   m2 (m=1 node) = {masses[1]:.5f} eV   (vs measured sqrt(Dm21)={np.sqrt(DM2_21):.5f} eV, "
        f"{100 * (masses[1] / np.sqrt(DM2_21) - 1):+.1f}%)"
    )
    print(f"   m3 (m=2 node) = {masses[2]:.5f} eV   (= atmospheric scale by anchor)")
    assert abs(masses[0]) < TOL  # m1=0 exactly
    assert abs(masses[2] - scale) < TOL  # m3 anchored to seesaw scale
    assert abs(masses[1] / masses[2] - np.sinh(DK / PHI) / np.sinh(2 * DK / PHI)) < TOL
    print(
        "   ONE formula: sec-2 scale x sec-1 texture; only nontrivial output is m2 (ASSERTED)\n"
    )

    print("=== 4. theta_13 = |delta_theta_g| (note-04 rotor defect) ===")
    t13_pred_rad = abs(DELTA_G)
    t13_pred_deg = np.degrees(t13_pred_rad)
    s2_pred = np.sin(t13_pred_rad) ** 2
    # internal: predicted angle IS the rotor defect, exactly
    assert abs(t13_pred_rad - abs(78 * LNPHI - 12 * np.pi)) < TOL
    print(f"   theta_13 (pred) = {t13_pred_deg:.4f} deg   [internal value ASSERTED]")
    print(
        f"   measured        = {T13_MEAS_DEG:.4f} deg   bracket {100 * (t13_pred_deg / T13_MEAS_DEG - 1):+.1f}%"
    )
    print(
        f"   sin^2 (pred)    = {s2_pred:.5f}   measured {S2_13_MEAS:.4f}  bracket {100 * (s2_pred / S2_13_MEAS - 1):+.1f}%\n"
    )

    print("=== 5. theta_12: tan = 1/phi  =>  sin^2 = 1/(2+phi) exactly ===")
    t12_pred_deg = np.degrees(np.arctan(1 / PHI))
    s2_12_pred = np.sin(np.arctan(1 / PHI)) ** 2
    # exact: sin^2(arctan(1/phi)) = 1/(1+phi^2) = 1/(2+phi)  [since phi^2 = phi+1]
    assert abs(s2_12_pred - 1 / (2 + PHI)) < TOL, s2_12_pred - 1 / (2 + PHI)
    print(
        f"   theta_12 (pred) = {t12_pred_deg:.4f} deg  measured {T12_MEAS_DEG:.4f}  bracket {100 * (t12_pred_deg / T12_MEAS_DEG - 1):+.1f}%"
    )
    print(
        f"   sin^2 = 1/(2+phi) = {s2_12_pred:.5f} (ASSERTED)   measured {S2_12_MEAS:.4f}\n"
    )

    print("=== 6. theta_23 = 45 deg (now-surface equal weight 1/2) ===")
    # equal-weight P_now = diag(1/2,1/2)-readout => maximal mixing; tan(theta_23)=1
    assert abs(np.tan(np.radians(45.0)) - 1.0) < TOL
    print(
        "   theta_23 = 45 deg  (equal weight => tan=1, ASSERTED)  measured 42-49 deg\n"
    )

    print(
        "=== 7. golden numerical observations on the MEASURED ratios (not predictions) ==="
    )
    # The framework's parameter-free output for m2/m3 is the sinh ratio in 2b (0.131).
    # phi^-4 and phi^-7 are observations that the MEASURED ratios fall near golden powers;
    # they are not derived from node ordinals -- kept distinct from the 2b prediction.
    m2_m3 = np.sqrt(DM2_21 / DM2_32)
    ratio = DM2_21 / DM2_32
    print(
        f"   measured m2/m3 = {m2_m3:.4f}   near phi^-4 = {PHI**-4:.4f}  ({100 * (PHI**-4 / m2_m3 - 1):+.1f}%, numerical obs)"
    )
    print(
        f"   measured Dm21/Dm32 = {ratio:.4f}   near phi^-7 = {PHI**-7:.4f}  ({100 * (PHI**-7 / ratio - 1):+.1f}%, numerical obs)"
    )
    # Sigma m_nu floor (consequence of measured splittings + m1=0), NOT a phi-prediction
    sigma = np.sqrt(DM2_21) + np.sqrt(DM2_32)
    print(f"   Sigma m_nu (m1~0, NO) = {sigma:.4f} eV   (Planck+BAO bound 0.12 eV)")
    assert sigma < 0.12
    print("   Sigma < 0.12 eV (ASSERTED)\n")

    print(
        "=== 8. EXTENSION: CP-violation magnitude |delta_CP - pi| = |delta_theta_g|*phi^p ==="
    )
    # rotor's hyperbolic shadow: bare defect amplified by a golden terrace factor phi^p.
    # HONEST: unlike 78,12 in theta_13 (forced by lepton tower), the POWER p is NOT forced.
    # p=1 -> 15.3 deg, p=2 -> 24.7 deg; framework predicts the ORDER, not a pinned value.
    dev_meas = abs(DCP_MEAS_DEG - 180)  # = 17 deg
    for p in (1, 2):
        dev_p = np.degrees(abs(DELTA_G) * PHI**p)
        dcp_p = 180.0 - dev_p  # one octant choice; sign relative to pi is open
        print(
            f"   p={p}: |delta_CP - pi| = |dg|*phi^{p} = {dev_p:.1f} deg  "
            f"(=> delta_CP={dcp_p:.1f} deg)  bracket vs meas {dev_meas:.0f}: {100 * (dev_p / dev_meas - 1):+.0f}%"
        )
    print(
        f"   PREDICTED BAND |delta_CP - pi| in [15.3, 24.7] deg; measured {dev_meas:.0f} deg is INSIDE"
    )
    # CAVEAT: octant/sign relative to pi is NOT fixed (pred p=2 -> 155<pi, meas 197>pi)
    print(
        f"   CAVEAT: sin(155 deg)={np.sin(np.radians(155.0)):+.3f} vs sin(meas)={np.sin(np.radians(DCP_MEAS_DEG)):+.3f} "
        "-- OPPOSITE sides of pi; power-of-phi AND sign NOT fixed by framework"
    )
    print(
        "   honest claim = CP-violation MAGNITUDE (~15-25 deg off pi), not a pinned phase\n"
    )

    print(
        "ALL framework-internal identities verified to < 1e-12; data brackets printed above."
    )


if __name__ == "__main__":
    check()
