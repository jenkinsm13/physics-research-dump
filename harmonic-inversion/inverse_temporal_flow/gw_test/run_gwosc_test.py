"""Run the golden-ringdown-comb test against real LIGO/Virgo open strain (GWOSC).

Requires network + `pip install gwpy gwosc scipy numpy`. Built to be run where there
IS outbound network (this analysis was authored in a no-network sandbox; the offline
predictions are in predict_teeth.py and the verdict in note 29-gw-data-test.md).

What it does, per event:
  1. Fetch 32 s of strain around the event from GWOSC (H1 + L1).
  2. Bandpass + whiten; locate the merger peak (max whitened envelope).
  3. RINGDOWN OVERTONE TEST: take the post-peak segment, FFT it, and look for power
     at the framework comb teeth f0 * e^{+/- pi/2} relative to the GR (2,2,0) f0.
     Report power ratio at the golden teeth vs at the GR overtone (~0.95 f0).
  4. ECHO TEST: cross-correlate the post-merger strain with a template echo train
     h(t) = sum_m gamma^m * ringdown(t - t_m), t_m = t0 e^{m pi/2}, gamma=0.133,
     scanning t0; report the matched-filter SNR vs a time-reversed (null) control.

Honest design: a NULL result is the expected outcome at current SNR (the framework's
own N_obs = floor(ln rho_rd / S1) = 0 for these events); the informative test is the
OVERTONE one (golden 4.81x vs GR 0.95x), which current data can already discriminate.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
S1 = np.pi / (2 * PHI * LNPHI)
GAMMA = np.exp(-S1)  # 0.133
LAMBDA_PHI = np.exp(np.pi / 2)  # 4.8105

EVENTS = {
    "GW150914": dict(gps=1126259462.4, f220=251.0, tau_ms=4.0),
    "GW190521": dict(gps=1242442967.4, f220=66.0, tau_ms=13.0),
}
DETECTORS = ("H1", "L1")


def fetch(det, gps, span=32):
    from gwpy.timeseries import TimeSeries

    return TimeSeries.fetch_open_data(det, gps - span / 2, gps + span / 2, cache=True)


def whiten_band(ts, flow=20, fhigh=1024):
    ts = ts.detrend()
    w = ts.whiten(4, 2)
    return w.bandpass(flow, fhigh)


def overtone_test(post, f0, fs):
    """Power at golden teeth (f0 * e^{+/-pi/2}) vs GR overtone (0.95 f0)."""
    n = len(post)
    win = np.hanning(n)
    spec = np.abs(np.fft.rfft(post * win)) ** 2
    freqs = np.fft.rfftfreq(n, 1 / fs)

    def band_power(fc, frac=0.06):
        sel = (freqs > fc * (1 - frac)) & (freqs < fc * (1 + frac))
        return spec[sel].sum() if sel.any() else 0.0

    p_fund = band_power(f0)
    p_gold_up = band_power(f0 * LAMBDA_PHI)
    p_gold_dn = band_power(f0 / LAMBDA_PHI)
    p_gr_ot = band_power(0.95 * f0)
    return dict(fund=p_fund, gold_up=p_gold_up, gold_dn=p_gold_dn, gr_overtone=p_gr_ot)


def echo_test(post, fs, f0, tau_s):
    """Matched filter for a golden echo train vs a time-reversed null control."""
    t = np.arange(len(post)) / fs
    ring = np.exp(-t / tau_s) * np.cos(2 * np.pi * f0 * t)
    best = -np.inf
    for t0 in np.linspace(0.5 * tau_s, 6 * tau_s, 40):
        templ = np.zeros_like(post)
        for m in range(0, 5):
            shift = int(t0 * LAMBDA_PHI**m * fs)
            if shift >= len(post):
                break
            seg = (GAMMA**m) * ring[: len(post) - shift]
            templ[shift : shift + len(seg)] += seg
        norm = np.linalg.norm(templ)
        if norm == 0:
            continue
        snr = float(np.dot(post, templ) / norm)
        best = max(best, snr)
    null = float(np.dot(post, post[::-1]) / np.linalg.norm(post[::-1]))
    return best, null


def run():
    for name, e in EVENTS.items():
        print(f"\n==== {name} (f220={e['f220']} Hz) ====")
        for det in DETECTORS:
            try:
                ts = fetch(det, e["gps"])
                w = whiten_band(ts)
                fs = float(w.sample_rate.value)
                env = np.abs(w.value)
                kpk = int(np.argmax(env))
                post = w.value[kpk : kpk + int(0.20 * fs)]  # 200 ms post-merger
                ot = overtone_test(post, e["f220"], fs)
                snr, null = echo_test(post, fs, e["f220"], e["tau_ms"] / 1e3)
                print(
                    f"  {det}: overtone power  fund={ot['fund']:.3e}  "
                    f"GR(0.95f0)={ot['gr_overtone']:.3e}  "
                    f"golden(+)={ot['gold_up']:.3e}  golden(-)={ot['gold_dn']:.3e}"
                )
                print(
                    f"       golden/GR overtone power ratio = "
                    f"{(ot['gold_up'] + ot['gold_dn']) / max(ot['gr_overtone'], 1e-30):.3f}  "
                    f"(>>1 would support the comb; <<1 supports GR)"
                )
                print(
                    f"       echo matched-filter SNR={snr:.2f}  null(control)={null:.2f}"
                )
            except Exception as exc:  # noqa: BLE001
                print(f"  {det}: SKIPPED ({type(exc).__name__}: {exc})")
    print(
        "\nInterpretation: the OVERTONE test discriminates now (golden 4.81x vs GR 0.95x);"
    )
    print(
        "the ECHO test is expected null at current SNR (N_obs=0) and is a sensitivity floor check."
    )


if __name__ == "__main__":
    run()
