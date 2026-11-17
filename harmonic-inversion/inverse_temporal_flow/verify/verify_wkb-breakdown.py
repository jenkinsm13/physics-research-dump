"""
verify_wkb-breakdown.py  —  Numerical verification for note 31b (Mechanism B).

Tests whether the adiabatic / WKB description of the charged carrier
Psi = osc * V breaks down at a UNIQUE depth that could single out n_e ~ 107.

Field equation (note 16): chi'' + osc^2(k) chi = 0 in the K-eigenbasis,
osc(k) = 1/(1 + cos^2(2 k ln phi)),  period Delta k = pi/(2 ln phi).

Result: the WKB adiabaticity parameter alpha(k) = |osc'/osc^2| is EXACTLY
periodic in k (a comb, not monotone in depth); the carrier is never adiabatic
anywhere (Q < 1 sub-critical, alpha is O(1) every period), so there is no
adiabatic regime to break down FROM. No parameter-free depth-monotone quantity
yields a finite cutoff. NEGATIVE.

Analytic backbone (used as self-checks below, since the whole point of a
rigorous negative is that the numbers must be exactly what the closed form says):
  u  = 2 k ln phi
  osc        = 1/(1+cos^2 u)                       in [1/2, 1]
  osc'       = 2 ln phi * sin(2u) * osc^2          (chain rule)
  alpha      = |osc'|/osc^2 = 2 ln phi * |sin(2u)| in [0, 2 ln phi]
            => alpha_max = 2 ln phi = 0.96242  (NOT 1.44; an earlier draft
               quoted a spurious 1.4422 — corrected here and cross-checked two
               independent ways below).
  per-period non-adiabaticity gain
            = <alpha> * Delta k
            = (2 ln phi * <|sin|>) * (pi/(2 ln phi))
            = (2 ln phi * 2/pi) * (pi/(2 ln phi))
            = 2  EXACTLY, independent of phi.
  A phi-independent integer (2) cannot encode a log-ratio of two external
  masses (107.08). That alone forecloses a bulk depth scale.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
Dk = np.pi / (2 * lnphi)  # comb / Hill period in k


def osc(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)


def dosc(k, h=1e-6):
    return (osc(k + h) - osc(k - h)) / (2 * h)


def ddosc(k, h=1e-4):
    return (osc(k + h) - 2 * osc(k) + osc(k - h)) / (h * h)


def alpha(k):
    # WKB adiabaticity parameter |M'/M^2| with M = osc (frozen-mass dispersion, note 16).
    # Closed form: alpha = 2 ln phi * |sin(4 k ln phi)|, so alpha_max = 2 ln phi exactly.
    return abs(dosc(k)) / osc(k) ** 2


def alpha_analytic(k):
    # 2 ln phi * |sin(2u)|, u = 2 k ln phi  ->  argument 4 k ln phi
    return 2 * lnphi * abs(np.sin(4 * k * lnphi))


def R(k):
    # off-shell adiabatic-carrier defect (note 16): R = osc'' + osc^3
    return ddosc(k) + osc(k) ** 3


def main():
    print(f"phi={phi:.6f}  lnphi={lnphi:.6f}  1/phi={1 / phi:.6f}  Delta k={Dk:.5f}")

    # 0. ANALYTIC SELF-CHECK: finite-difference alpha matches the closed form,
    #    and alpha_max is 2 ln phi = 0.9624 (the load-bearing corrected number).
    ks = np.linspace(0.01, 4 * Dk, 8000)
    fd = np.array([alpha(k) for k in ks])
    an = alpha_analytic(ks)
    print(
        f"\n[0] SELF-CHECK alpha (finite-diff vs closed form): "
        f"max|fd-analytic| = {np.max(np.abs(fd - an)):.2e}"
    )
    print(
        f"    analytic alpha_max = 2 ln phi = {2 * lnphi:.5f}  (NOT 1.4422; that was a draft error)"
    )
    assert abs(2 * lnphi - 0.96242) < 1e-4, "alpha_max must equal 2 ln phi"
    assert np.max(np.abs(fd - an)) < 1e-3, "finite-diff alpha must match closed form"

    # 1. osc range and sub-critical Q
    o = osc(np.linspace(0, 400, 4_000_001))
    Q = phi * o / 2
    print(f"\n[1] osc in [{o.min():.4f},{o.max():.4f}] (expect [0.5,1.0])")
    print(
        f"    Q=phi*osc/2 in [{Q.min():.4f},{Q.max():.4f}] -> sub-critical (max Q<1): {Q.max() < 1}"
    )

    # 2. adiabaticity alpha is exactly Delta-k periodic (a comb, NOT depth-monotone)
    a = np.array([alpha(k) for k in np.linspace(0, 4 * Dk, 4001)])
    maxdiff = max(abs(alpha(k) - alpha(k + Dk)) for k in np.linspace(0.5, 3, 20))
    print(
        f"\n[2] alpha=|osc'/osc^2| in [{a.min():.4f},{a.max():.4f}] (expect [0, {2 * lnphi:.4f}])"
    )
    print(f"    alpha exactly Dk-periodic: max|alpha(k)-alpha(k+Dk)| = {maxdiff:.2e}")

    # 3. no adiabatic regime to break down FROM: alpha ~ 0 at comb nodes, O(1) mid-period
    k1 = np.pi / (4 * lnphi)  # first comb node
    asamp = np.array([alpha(k) for k in np.linspace(0, Dk, 2001)])
    print(f"\n[3] alpha~0 at comb node k_1={k1:.3f}: {alpha(k1):.2e}")
    print(
        f"    over one period alpha in [{asamp.min():.4f},{asamp.max():.4f}] -> NOT uniformly small"
    )
    print(
        "    => the carrier is never adiabatic; there is no regime to break down FROM."
    )

    # 4. off-shell defect R: RMS matches corpus 0.66, R periodic, worst at comb.
    #    Analytic R at the comb node = 1 - 8 (ln phi)^2 = -0.8525.
    kp = np.linspace(0, Dk, 20001)
    Rp = np.array([R(k) for k in kp])
    Rdiff = max(abs(R(k) - R(k + Dk)) for k in np.linspace(0.5, 3, 15))
    print(
        f"\n[4] RMS(R=osc''+osc^3) over a period = {np.sqrt(np.mean(Rp**2)):.4f} (corpus 0.66)"
    )
    print(f"    R is Dk-periodic: max|R(k)-R(k+Dk)| = {Rdiff:.2e}")
    print(
        f"    R at comb k_1 = {R(k1):.4f}  (analytic 1 - 8 ln^2 phi = {1 - 8 * lnphi**2:.4f})"
    )

    # 5. DECISIVE: candidate depth-monotone quantities are linear / featureless (no cutoff).
    #    cumulative phase slope = <osc> = 1/sqrt2; per-period non-adiab. gain = 2 EXACTLY.
    kk = np.linspace(0, 150, 150001)
    dk = kk[1] - kk[0]
    Phi = np.cumsum(osc(kk)) * dk  # cumulative WKB phase
    cumA = (
        np.cumsum(np.array([alpha(k) for k in kk])) * dk
    )  # cumulative non-adiabaticity
    osc_mean = np.mean(osc(np.linspace(0, 1000, 1_000_001)))
    gain = np.mean(a) * Dk
    print(
        f"\n[5] cumulative phase Phi(k) is LINEAR, slope <osc> = {osc_mean:.4f} = 1/sqrt(2) -> no special depth"
    )
    print(
        f"    cumulative int alpha dk is LINEAR, per-period gain = {gain:.4f} (analytic EXACTLY 2)"
    )
    print(
        "    a phi-independent constant (2) cannot encode log_phi(E_P/m_e)=107.08 -> no bulk depth scale"
    )
    assert abs(gain - 2.0) < 0.05, "per-period non-adiabaticity gain must be ~2"

    # 6. D2 cross-check: nothing to predict, since there is no unique depth
    print(
        "\n[6] D2 CROSS-CHECK: mechanism yields NO unique depth -> cannot predict 107, 63, 102, or 92."
    )

    # 7. D4/D5 knob exposure: a forced envelope threshold slides to ANY target (incl. 111.5 trap).
    #    cutoff k* = T*phi where T = number of e-folds of e^{-k/phi} (a free threshold).
    print(
        "\n[7] Forced-threshold KNOB (e^-k/phi below e^-T => cutoff k* = T*phi): slides to any target"
    )
    for target in [63, 92, 102, 107, 111.5]:
        print(
            f"    to land cutoff={target:6.1f} need arbitrary e-fold count T = {target / phi:.2f}"
        )
    print(
        f"    D5: 107 (T={107 / phi:.1f}) and the N*/phi^2=111.5 attractor (T={111.5 / phi:.1f}) need"
    )
    print(
        "        nearly identical T -> the knob cannot even resolve target from attractor."
    )

    print(
        "\nVERDICT: NEGATIVE — periodic comb, never adiabatic, no parameter-free monotone cutoff."
    )


if __name__ == "__main__":
    main()
