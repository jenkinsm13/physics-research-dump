"""Machine-precision verification of note 08-cosmology-darkflow.md.

Run: python3 verify_cosmology.py
Checks the depletion shell, the two-decay distinction, the Lambda exponent,
the convergence discriminator, the signed residual flow, and the extension's
route ratio. Residuals quoted inline.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
C = 3.0  # emergent spatial dimensions from CFT extraction (note 00)


def check():
    # Cosmic hierarchy: R_H / ell_P ~ 10^61.
    log10_ratio = 61.0
    n_oct = log10_ratio / np.log10(2)  # = log2(R/l)

    print("=== 1. Depletion shell N_star = log_phi(R_H/ell_P) ===")
    N_star_oct = n_oct * (np.log(2) / LNPHI)
    N_star_logphi = log10_ratio * np.log(10) / LNPHI
    print(f"   n_oct = log2(10^61)        = {n_oct:.4f}   (note 202.64)")
    print(f"   N_star = n_oct*ln2/lnphi   = {N_star_oct:.4f}")
    print(
        f"   N_star = log_phi(R/l)      = {N_star_logphi:.4f}   (note 291.88, corpus 291)"
    )
    print(f"   identity residual          = {abs(N_star_oct - N_star_logphi):.2e}")

    print("\n=== 2. Two decays: per-octave factor 2^-c vs per-shell rate c*lnphi ===")
    factor_per_octave = 2**-C
    rate_per_shell = C * LNPHI
    # per-octave factor converted to per-shell rate via ln2/lnphi shells per octave
    factor_from_rate = np.exp(-rate_per_shell) ** (np.log(2) / LNPHI)
    print(f"   2^-c per octave            = {factor_per_octave:.6f} (=1/8)")
    print(f"   c*lnphi per shell (lam_en) = {rate_per_shell:.6f}   (note 1.4436)")
    print(f"   (2^-c)^(lnphi/ln2)=e^-clnphi per shell = {np.exp(-rate_per_shell):.6f}")
    print(
        f"   factor<->rate consistency residual = {abs(factor_per_octave - factor_from_rate):.2e}"
    )
    print("   corpus lambda_ord = 1/8 is a PER-SHELL CORRELATION rate, distinct object")

    print("\n=== 3. Lambda exponent = horizon curvature (no lambda used) ===")
    log10_LamlP2 = -2 * n_oct * np.log10(2)
    meas = np.log10(1.1e-52 * 2.6e-70)
    print(
        f"   -2 n_oct log10(2)          = {log10_LamlP2:.4f}   (= -2*61 = (lP/R_H)^2)"
    )
    print(f"   measured log10(Lam lP^2)   = {meas:.4f}   (note -121.54)")
    print(f"   residual                   = {abs(log10_LamlP2 - meas):.4f} decades")

    print("\n=== 4. Convergence discriminator (rate-discriminating, the §2 trap) ===")
    for name, lam in [("energy c*lnphi", C * LNPHI), ("CORPUS 1/8 (wrong)", 1 / 8)]:
        growth = 1 / PHI - lam
        k = np.arange(1, 201)
        term = np.sinh(k / PHI) * np.exp(-lam * k) / (1 + np.cos(2 * k * LNPHI) ** 2)
        verdict = "DIVERGES" if growth > 0 else "converges"
        print(
            f"   lam={lam:6.4f} ({name:18s}): 1/phi-lam={growth:+.4f} -> {verdict}; "
            f"term[200]={term[-1]:.2e}"
        )

    print("\n=== 5. Signed residual flow at N_star (pinned to spine -cos) ===")
    Phi_res = -np.cos(2 * 291 * LNPHI)
    u = np.cos(2 * 291 * LNPHI) ** 2
    tau = -3 * np.cos(2 * 291 * LNPHI) / (5 - 3 * u)
    print(
        f"   Phi_res = -cos(2*291*lnphi) = {Phi_res:+.4f}   (note +0.894, sign POSITIVE)"
    )
    print(f"   tau_Frenet(291 lnphi)       = {tau:+.4f}   (same sign)")
    # Magnitude is geometry-fixed; sign follows the dilution convention (a forward
    # residual flow raises w toward -1), landing on the quintessence side w > -1.
    woff = +Phi_res / 291
    print(
        f"   |1+w(0)| = |Phi_res|/N_star = {abs(woff):.4e}   (note 3.1e-3, magnitude)"
    )
    print(
        f"   w(0) = -1 + Phi_res/N_star  = {-1 + woff:.4f}   (note -0.997, quintessence)"
    )
    print(f"   dN_star/dlnR_H = ln2/lnphi  = {np.log(2) / LNPHI:.4f}   (note 1.44)")

    print("\n=== 6. Relic comb period & extension route ratio R ===")
    spacing = np.pi / (2 * LNPHI)
    oct_per_feature = spacing / (np.log(2) / LNPHI)  # = pi/(2 ln2)
    print(f"   inversion-shell spacing pi/(2lnphi) = {spacing:.4f} shells (note 3.264)")
    print(
        f"   octaves per feature pi/(2 ln2)      = {oct_per_feature:.4f}   (note 2.27)"
    )
    # Ratio of two PER-SHELL rates (correlation 1/8 over energy c*lnphi) -- NOT the
    # per-octave factor 2^-c over a per-shell rate (the factor-vs-rate sin of sec 2).
    lam_ord = 1 / 8
    R = lam_ord / (C * LNPHI)
    print(f"   route ratio R = lam_ord/(c lnphi)   = {R:.4f}   (note 0.0866)")
    print(f"   depletion-shell width dN ~ R*N_star = {R * 291:.1f} shells (note ~25)")
    print(
        f"   in octaves                          = {R * 291 * LNPHI / np.log(2):.1f} (note ~17)"
    )


if __name__ == "__main__":
    check()
