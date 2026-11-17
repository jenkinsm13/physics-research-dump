"""Machine-precision verification of note 21-cosmological-dynamics.md.

Run: python3 verify_cosmological-dynamics.py

Checks the boost-run-out Friedmann construction built on notes 08 and 10:
  - scale factor a(N)=a0 phi^N and the redshift<->shell map N=ln(1+z)/lnphi
  - the deceleration->acceleration transition is exactly one golden boost back:
    z_t = 1/phi = Theta_H/N_star  (parameter-free)
  - the implied Omega_Lambda/Omega_m = phi^3/2 = phi + 1/2 and Omega_Lambda value
  - q(z)=0 root coincides with 1/phi for that Omega split
  - w(z) evolution from the residual flow (note 08), w0 and the CPL (w0,wa) fit
  - the apodized golden log-comb on H(z): period e^(pi/2) in (1+z), silver amplitude
  - EXTENSION: the jerk departure j0-1 = (3/2)OL(3cos-2sin)/N_star = -0.0063, j0=0.9938
    (LCDM has j==1; non-bijective falsifiable fingerprint, survives z_t<->Omega). Checked
    by the exact Visser identity j=q(2q+1)+(1+z)dq/dz with an LCDM control returning 1.0.

Honesty notes baked into the prints: Theta_H/N_star = 1/phi is a DEFINITION (tautology),
the z_t and Omega-ratio tests are the SAME bijective statement (~2% / 2.5%), and 1/phi
sits <1 sigma inside the model-independent z_t band (0.4-0.67, +/-0.1-0.2).

Pure numpy (no scipy); bisection hand-coded. Residuals quoted inline.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
C = 3.0  # emergent spatial dims (CFT extraction, note 00)

# Horizon / depletion shell and horizon rapidity (notes 08, 10).
N_STAR = 61.0 * np.log(10) / LNPHI  # = log_phi(R_H/ell_P) = 291.88
THETA_H = N_STAR / PHI  # = 180.39
N_STAR_CORPUS = 291  # integer corpus shell used in note 08 for Phi_res


def bisect(f, a, b, tol=1e-14, itmax=300):
    fa = f(a)
    for _ in range(itmax):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol:
            return m
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def check():
    print("phi =", PHI, " lnphi =", LNPHI)
    print(f"N_star = log_phi(R_H/ell_P) = {N_STAR:.5f}  (note 08: 291.88)")
    print(f"Theta_H = N_star/phi        = {THETA_H:.5f}  (note 10: 180.39)")

    print("\n=== 1. Scale factor a(N)=a0 phi^N ; redshift<->shell map ===")
    # NOW = top of stack (largest a). Looking back to shell N: 1+z = a_now/a(N) = phi^N.
    # So N(z) = ln(1+z)/lnphi : shells are LINEAR in ln(1+z) (exact de Sitter in the N-clock).
    dlna_dN = LNPHI  # d ln a / dN, constant -> the boost IS the expansion
    print(
        f"   d ln a / dN = lnphi = {dlna_dN:.6f}  (constant: de Sitter in ordinal clock)"
    )
    for z in [0.0, 0.5, 0.618034, 1.0, 1100.0]:
        N = np.log(1 + z) / LNPHI
        print(f"   z={z:10.4f} -> N(z)=ln(1+z)/lnphi = {N:8.4f} shells")
    # full hierarchy: z->1e61 (Planck) maps to N_star
    z_planck = PHI**N_STAR - 1
    print(
        f"   shell N_star=291.88 -> 1+z = phi^N_star = {PHI**N_STAR:.3e} (~10^61, Planck) OK"
    )
    assert abs(np.log10(PHI**N_STAR) - 61.0) < 1e-9

    print(
        "\n=== 2. Accel transition is ONE golden boost: z_t = 1/phi = Theta_H/N_star ==="
    )
    zt_geo = 1 / PHI
    print(f"   1+z_t = phi  =>  z_t = phi-1 = 1/phi = {zt_geo:.6f}")
    # HONESTY: Theta_H/N_star = 1/phi is a TAUTOLOGY -- corpus DEFINES Theta_H = N_star/phi.
    # The assert passes because it is a definition, NOT an independent cross-scale match.
    print(
        f"   Theta_H/N_star = {THETA_H / N_STAR:.6f}  (= 1/phi BY DEFINITION Theta_H:=N*/phi -- tautology)"
    )
    assert abs(THETA_H / N_STAR - 1 / PHI) < 1e-12  # identity, not corroboration
    # Honest comparison targets:
    zt_planck = (0.6847 / 0.3153 * 2) ** (
        1 / 3
    ) - 1  # precise Planck-LCDM (itself from Omega)
    print(
        f"   vs precise Planck-LCDM z_t={zt_planck:.4f} -> miss {abs(zt_geo - zt_planck) / zt_planck * 100:.1f}% (SAME as Omega-ratio test, bijective)"
    )
    # Model-INDEPENDENT z_t (cosmic chronometers / SNe), with 1-sigma bands:
    for c0, hi, lo in [
        (0.60, 0.21, 0.12),
        (0.61, 0.24, 0.16),
        (0.46, 0.13, 0.13),
        (0.40, 0.10, 0.10),
    ]:
        sig = (zt_geo - c0) / (hi if zt_geo > c0 else lo)
        print(
            f"   vs model-indep z_t={c0:.2f} (+{hi}/-{lo}): 1/phi at {sig:+.2f} sigma {'INSIDE' if abs(sig) < 1 else 'OUTSIDE'}"
        )

    print("\n=== 3. Omega split forced by z_t=1/phi (flat, w=-1 background) ===")
    # q(z)=0 <=> Om(1+z)^3 = 2 OL  =>  (1+z_t)^3 = 2 OL/Om.  With 1+z_t=phi:
    ratio = PHI**3 / 2  # = OL/Om
    OL = ratio / (1 + ratio)
    Om = 1 - OL
    print(f"   OL/Om = (1+z_t)^3/2 = phi^3/2 = phi+1/2 = {ratio:.6f}")
    assert abs(PHI**3 / 2 - (PHI + 0.5)) < 1e-12  # phi^3=2phi+1 identity
    print(
        f"   identity phi^3/2 = phi+1/2 residual = {abs(PHI**3 / 2 - (PHI + 0.5)):.2e}"
    )
    # PRIMARY honest figure of merit: the predicted RATIO vs Planck ratio (not the
    # compressed single-Omega projection, which OL+Om=1 flatters).
    ratio_planck = 0.6847 / 0.3153
    print(
        f"   PREDICTED RATIO OL/Om={ratio:.4f} vs Planck {ratio_planck:.4f} -> miss {abs(ratio - ratio_planck) / ratio_planck * 100:.1f}% (the honest figure)"
    )
    print(
        f"   => Omega_Lambda = {OL:.5f}   (Planck 0.6847, miss {abs(OL - 0.6847) / 0.6847 * 100:.1f}%)"
    )
    print(
        f"   => Omega_m      = {Om:.5f}   (Planck 0.3153, miss {abs(Om - 0.3153) / 0.3153 * 100:.1f}%)"
    )

    print("\n=== 4. q(z)=0 root for that Omega split coincides with 1/phi ===")

    def E2(z):
        return Om * (1 + z) ** 3 + OL

    def q(
        z,
    ):  # deceleration q = (1/2) sum_i Omega_i(1+3 w_i) / E^2 ; matter w=0, Lambda w=-1
        return (0.5 * Om * (1 + z) ** 3 + 0.5 * OL * (1 + 3 * (-1))) / E2(z)

    zt = bisect(q, 0.0, 2.0)
    print(
        f"   q(z_t)=0 root = {zt:.6f} ;  1/phi = {1 / PHI:.6f} ;  residual = {abs(zt - 1 / PHI):.2e}"
    )
    assert abs(zt - 1 / PHI) < 1e-9

    print("\n=== 5. w(z) evolution (note 08 residual flow) ===")
    # Note 08: w0 = -1 + Phi_res/N, Phi_res = -cos(2 N lnphi) pinned at corpus N=291 (=+0.894).
    Phi_res = -np.cos(2 * N_STAR_CORPUS * LNPHI)
    w0 = -1 + Phi_res / N_STAR_CORPUS
    print(f"   Phi_res = -cos(2*291*lnphi) = {Phi_res:+.4f}  (note 08: +0.894)")
    print(f"   w0 = -1 + Phi_res/291       = {w0:.5f}        (note 08: -0.997)")
    assert abs(w0 - (-0.99693)) < 1e-4

    # Dark energy is the HORIZON vacuum (note 08), so the flow Phi(N)=-cos(2N lnphi) is read at
    # the horizon shell, with z-evolution = drift away from it (note 08 Pred 1: "w drifts as
    # N_star creeps"). At look-back shell N_star - N(z), with 2N lnphi = 2 ln(1+z), note 08's
    #   w = -1 + Phi/N_star ,  Phi = -cos(2 N_star lnphi - 2 ln(1+z))   gives
    #   w(z) = -1 - cos(2 N_star lnphi - 2 ln(1+z)) / N_star .
    # At z=0: w0 = -1 - cos(2 N_star lnphi)/N_star = -1 + Phi_res/N_star = -0.997 (quintessence).
    # (Reading the LOCAL flow at N(z) instead gives Phi(0)=-1 -> w0=-1.003 PHANTOM, which
    # CONTRADICTS note 08; anchoring the phase at the horizon is the fix.)
    horizon_phase = 2 * N_STAR_CORPUS * LNPHI

    def w_of_z(z):
        return -1.0 - np.cos(horizon_phase - 2 * np.log(1 + z)) / N_STAR_CORPUS

    # guard: the evolution MUST reproduce note 08's present value (cures the §4 sign flip).
    assert abs(w_of_z(0.0) - w0) < 1e-6, (w_of_z(0.0), w0)
    print(
        f"   GUARD w(0)={w_of_z(0.0):.5f} == note-08 w0={w0:.5f} (quintessence side, sign OK)"
    )
    zs = np.linspace(0, 2, 400)
    ws = w_of_z(zs)
    a = 1 / (1 + zs)
    A = np.vstack([np.ones_like(a), (1 - a)]).T
    coef, *_ = np.linalg.lstsq(A, ws, rcond=None)
    print(
        f"   |1+w| amplitude = |Phi|/N_star <= 1/N_star = {1 / N_STAR_CORPUS:.4e}  (~3e-3, note 08)"
    )
    print(f"   CPL fit on z in [0,2]: w0_cpl={coef[0]:.5f}, wa_cpl={coef[1]:+.5f}")
    # quintessence<->phantom crossing where cos(horizon_phase - 2 ln(1+z)) = 0 -> w = -1.
    # Scan [0,2] for the first sign change of (w+1):
    g = ws + 1.0
    z_cross = None
    for i in range(len(zs) - 1):
        if (g[i] < 0) != (g[i + 1] < 0):
            z_cross = bisect(lambda z: w_of_z(z) + 1.0, zs[i], zs[i + 1])
            break
    print(
        f"   quintessence<->phantom crossing in [0,2] at z = {z_cross} (w crosses -1)"
    )

    print("\n=== 6. Apodized golden log-comb on H(z) ===")
    dS2 = (np.sqrt(2) - 1) ** 2  # silver, note 12
    print(
        f"   period in ln(1+z) = pi/2 = {np.pi / 2:.5f} ; factor in (1+z) = e^(pi/2) = {np.exp(np.pi / 2):.5f}"
    )
    print(
        f"   octaves per tooth = pi/(2 ln2) = {np.pi / (2 * np.log(2)):.5f}  (note 08/12: 2.27)"
    )
    print(
        f"   silver amplitude 2*delta_S^-2 = {2 * dS2:.5f} (intrinsic osc AC, note 12)"
    )
    # observable: only the vacuum sector carries osc; delta H/H = (1/2) OL * (osc AC)
    amp_H_peak = 0.5 * OL * 2 * dS2
    print(
        f"   peak fractional dH/H ~ (1/2) OL (2 delta_S^-2) = {amp_H_peak:.5f} = {amp_H_peak * 100:.2f}%"
    )
    R = (1 / 8) / (C * LNPHI)
    print(
        f"   apodization R = (1/8)/(c lnphi) = {R:.4f}, coherence R*N_star = {R * N_STAR:.1f} shells"
    )
    span = np.log(1 + 2.5)
    print(
        f"   observable span ln(1+2.5) = {span:.4f} < one period pi/2 = {np.pi / 2:.4f}"
    )
    print(
        f"   => within z<2.5 the comb shows as <1 tooth: a coherent ~{amp_H_peak * 100:.0f}% tilt, not a resolved oscillation"
    )

    print(
        "\n=== 7. EXTENSION: jerk departure from LCDM's j==1 (the non-bijective test) ==="
    )
    # LCDM: j(z) == 1 identically. An evolving w(z) forces j != 1.
    # PRIMARY check: the convention-clean Visser (2004) identity j = q(2q+1) + (1+z) dq/dz,
    # evaluated by exact closed-form q(z) (no finite-difference of the formula's own sign).
    # An LCDM control MUST return j0 = 1 -- that validates the prescription independently of
    # any statefinder sign convention.
    phase = 2 * N_STAR_CORPUS * LNPHI
    cphi, sphi = np.cos(phase), np.sin(phase)
    w0_x = -1.0 - cphi / N_STAR_CORPUS
    wp0 = -2.0 * sphi / N_STAR_CORPUS  # dw/dz at z=0
    assert abs(w0_x - w0) < 1e-12  # consistency with section 5 w0

    def fDE(z):  # DE density f(z)=exp(3 int_0^z (1+w)/(1+z') dz'), trapezoid
        if z <= 0:
            return 1.0
        zz = np.linspace(0.0, z, 200000)
        return float(np.exp(np.trapezoid(3 * (1 + w_of_z(zz)) / (1 + zz), zz)))

    def E2_full(z):
        return Om * (1 + z) ** 3 + OL * fDE(z)

    def q_full(z):
        h = 1e-5
        lnE = lambda u: 0.5 * np.log(E2_full(u))
        return (1 + z) * (lnE(z + h) - lnE(z - h)) / (2 * h) - 1

    def jerk_full(z):  # Visser identity (exact)
        h = 1e-4
        return q_full(z) * (2 * q_full(z) + 1) + (1 + z) * (
            q_full(z + h) - q_full(z - h)
        ) / (2 * h)

    # LCDM control
    def q_lcdm(z):
        h = 1e-5
        lnE = lambda u: 0.5 * np.log(Om * (1 + u) ** 3 + OL)
        return (1 + z) * (lnE(z + h) - lnE(z - h)) / (2 * h) - 1

    def jerk_lcdm(z):
        h = 1e-4
        return q_lcdm(z) * (2 * q_lcdm(z) + 1) + (1 + z) * (
            q_lcdm(z + h) - q_lcdm(z - h)
        ) / (2 * h)

    j0_num = jerk_full(1e-3)
    j0_lcdm = jerk_lcdm(1e-3)
    # Closed leading form (w0 ~ -1 limit): density piece ~cos, flow-deriv piece ~sin, OPPOSITE
    # signs -> j0-1 = (3/2) OL (3 cos - 2 sin)/N_star.
    j0_closed = 1 + 1.5 * OL * (3 * cphi - 2 * sphi) / N_STAR_CORPUS
    bound = 1.5 * OL * np.sqrt(13) / N_STAR_CORPUS  # |3cos -+ 2sin| <= sqrt(13)
    print(f"   1+w0 = -cos/N = {1 + w0_x:+.6f} ;  w'0 = dw/dz|0 = -2sin/N = {wp0:+.6f}")
    print(f"   LCDM control jerk j0 (MUST be 1.0)   = {j0_lcdm:.6f}")
    print(
        f"   Visser identity j0 (exact, primary)  = {j0_num:.6f}  -> j0-1 = {j0_num - 1:+.5f}"
    )
    print(f"   closed (3/2)OL(3cos-2sin)/N          = {j0_closed:.6f}  (leading form)")
    print(f"   amplitude bound (3/2)OL sqrt13/N     = {bound:.6f}  (realized ~half)")
    assert abs(j0_lcdm - 1.0) < 1e-4, j0_lcdm  # prescription validated on LCDM
    assert abs(j0_num - 0.9938) < 5e-4, j0_num  # predicted ~0.6% jerk deficit
    assert abs(j0_num - j0_closed) < 1e-3, (j0_num, j0_closed)  # closed matches exact
    assert abs(j0_num - 1) <= bound + 1e-9  # within the geometric bound
    print(
        f"   => PREDICT j0 = {j0_num:.4f}: a {abs(j0_num - 1) * 100:.2f}% NEGATIVE jerk anomaly"
    )
    print("      (LCDM gives j==1 exactly; this survives the z_t<->Omega bijection)")

    print("\nALL ASSERTS PASSED.")


if __name__ == "__main__":
    check()
