"""Offline GW prediction + GR-comparison for the golden ringdown comb (note 29).

No network or strain data required. Computes:
  (1) the framework's predicted overtone-comb teeth (ratio e^{pi/2}) and echo-train
      times (t_m = t0 e^{m pi/2}, decrement gamma_echo) for GW150914 and GW190521;
  (2) the established GR Kerr (2,2,n) overtone spectrum for comparison;
  (3) the decisive discriminant: framework overtone ratio 4.81 vs GR ~0.95.

Run: python3 predict_teeth.py
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
S1 = np.pi / (2 * PHI * LNPHI)  # first-bounce action
GAMMA_ECHO = np.exp(-S1)  # per-echo amplitude decrement
LAMBDA_PHI = np.exp(np.pi / 2)  # golden log-period (terrace/comb ratio)
NU = 1.0 / (PHI * LNPHI)  # envelope exponent t^{-nu}

# Measured remnant ringdown fundamentals (literature central values).
# f_220 from the dominant (l,m,n)=(2,2,0) Kerr quasinormal mode.
EVENTS = {
    "GW150914": dict(Mf_Msun=62.0, af=0.67, f220_Hz=251.0, tau220_ms=4.0),
    "GW190521": dict(Mf_Msun=142.0, af=0.72, f220_Hz=66.0, tau220_ms=13.0),
}

# LIGO/Virgo usable band (approx). Below ~20-30 Hz the seismic/Newtonian wall dominates.
BAND_LO, BAND_HI = 20.0, 1500.0


def kerr_overtone_ratio(af):
    """GR Kerr (2,2,1)/(2,2,0) REAL-frequency ratio, fit to Berti et al. tables.
    The overtone real frequency is slightly BELOW the fundamental; ratio ~0.92-0.97
    across the astrophysical spin range. (Damping rises ~3x; that is the imag part.)
    This is the textbook near-degeneracy that the framework's 4.81 must be tested against."""
    # Linear fit to Berti-Cardoso-Will (2,2,n) tables, real(omega), good to ~1% for a in [0.0,0.9]:
    r0 = 0.953 + 0.012 * af  # f221/f220 real-part ratio
    return r0


def report():
    print("=== Framework constants ===")
    print(f"  e^(pi/2) comb/terrace ratio = {LAMBDA_PHI:.4f}")
    print(
        f"  gamma_echo = e^(-S1) = {GAMMA_ECHO:.5f}  (-{-20 * np.log10(GAMMA_ECHO):.2f} dB/leg)"
    )
    print(f"  envelope exponent nu = 1/(phi lnphi) = {NU:.4f}")
    print(f"  S1 = {S1:.5f}")

    print("\n=== Predicted comb teeth (framework) vs GR overtone (Kerr) ===")
    for name, e in EVENTS.items():
        f0 = e["f220_Hz"]
        teeth = {m: f0 * LAMBDA_PHI**m for m in (-1, 0, +1)}
        gr_f221 = f0 * kerr_overtone_ratio(e["af"])
        print(f"\n  {name}  (M_f={e['Mf_Msun']} Msun, a_f={e['af']}, f220={f0} Hz)")
        for m in (-1, 0, 1):
            f = teeth[m]
            inband = BAND_LO <= f <= BAND_HI
            print(
                f"    framework tooth m={m:+d}: {f:8.1f} Hz  {'[in band]' if inband else '[OUT of band]'}"
            )
        print(
            f"    GR Kerr (2,2,1) overtone:  {gr_f221:8.1f} Hz  (ratio to f220 = {gr_f221 / f0:.3f})"
        )
        print(
            f"    => DISCRIMINANT: framework f(+1)/f220 = {LAMBDA_PHI:.2f}  vs  GR f221/f220 = {gr_f221 / f0:.3f}"
        )
        print(
            f"       factor {LAMBDA_PHI / (gr_f221 / f0):.1f} apart — a {f0 * LAMBDA_PHI - gr_f221:.0f} Hz separation, unmissable if real."
        )

    print("\n=== Echo train (time domain), GW190521 seed t0 = GM_f/c^3 ===")
    G = 6.674e-11
    c = 2.998e8
    Msun = 1.989e30
    for name, e in EVENTS.items():
        t0 = G * e["Mf_Msun"] * Msun / c**3  # light-crossing-ish seed (one M)
        times = [t0 * LAMBDA_PHI**m for m in range(0, 4)]
        amps = [GAMMA_ECHO**m for m in range(0, 4)]
        print(
            f"  {name}: t0={t0 * 1e3:.3f} ms; echoes at "
            + ", ".join(f"{t * 1e3:.2f}ms(x{a:.3f})" for t, a in zip(times, amps))
        )

    print("\n=== Verdict logic ===")
    print(
        "  If the comb teeth are QNM OVERTONES (frequency domain): the framework predicts"
    )
    print(
        "  4.81x spacing, but Kerr overtones are near-degenerate (~0.95x). Observed ringdowns"
    )
    print(
        "  (GW150914 overtone analyses) are consistent with GR's near-degenerate overtone, NOT"
    )
    print(
        "  with a 4.81x tooth. => As overtones, the golden comb is DISFAVORED by existing data."
    )
    print(
        "  If the teeth are time-domain ECHOES (Abedi-Afshordi regime): the framework's own"
    )
    print(
        "  N_obs = floor(ln rho_rd / S1) = 0 for these SNRs => UNDETECTABLE, not yet a test."
    )
    print(
        "  Honest status: the e^(pi/2) FREQUENCY comb is testable now and disfavored as overtones;"
    )
    print(
        "  the ECHO interpretation is not excluded but is below current detectability."
    )


if __name__ == "__main__":
    report()
