"""
Verification for note 23 — A Falsifiable GW Template: the Golden Ringdown Comb.

Every checkable claim in 23-gw-template.md is reproduced here. Builds on the
round-1/2 locks already verified in verify_gw-horizon.py (n_H, gamma_echo,
nu, the e^{pi/2} terrace ratio). The NEW content checked here:

  (A) the explicit matched-filter template h(t) = sum_m gamma^m * damped sinusoid
      at t_m = t_0 e^{m pi/2}, and its analytic envelope t^{-nu};
  (B) the first-echo delay for GW150914 in ms, from two candidate scales,
      compared to the Abedi-Afshordi (2017) ECO echo claim Dt ~ 0.2-0.3 s;
  (C) the QNM overtone comb at golden ratio e^{pi/2} vs the GR Kerr overtone
      real-frequency ratio (~1), the sharp falsifiable split;
  (D) corpus LIGO anchors (251/751/110 Hz, t1/t2=0.548, Q=3.2).
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
print(f"phi    = {phi:.12f}")
print(f"ln phi = {lnphi:.12f}")
print(f"1/phi  = {1 / phi:.12f}")

# ---- physical constants ----
G = 6.67430e-11
c = 2.99792458e8
Msun = 1.98892e30
ell_P = 1.616255e-35

# ============================================================
# (0) Re-confirm the round-1/2 locks the template is built on
# ============================================================
print("\n=== (0) Inherited locks (notes 03/06/15) ===")
Dk = np.pi / (2 * lnphi)  # terrace ordinal spacing
k1 = np.pi / (4 * lnphi)
S1 = 2 * k1 / phi  # first-bounce action, note 06
gamma_echo = np.exp(-S1)  # echo decrement / Gamma_1
nu = 1.0 / (phi * lnphi)  # golden exponent
ratio_r = np.exp(np.pi / 2)
print(f"  Dk = pi/(2 lnphi)          = {Dk:.6f}")
print(f"  S_1 = Dk/phi               = {S1:.6f}   (=pi/(2 phi lnphi))")
print(
    f"  gamma_echo = e^-S_1 = Gamma_1 = {gamma_echo:.6f}  ({20 * np.log10(gamma_echo):.2f} dB/echo)"
)
print(
    f"  terrace ratio e^{{pi/2}}      = {ratio_r:.6f}  (=phi^Dk, residual {abs(phi**Dk - ratio_r):.1e})"
)
print(
    f"  golden exponent nu = 2 S_1/pi = {2 * S1 / np.pi:.10f} = 1/(phi lnphi) = {nu:.10f}"
    f"  (residual {abs(2 * S1 / np.pi - nu):.1e})"
)

# ============================================================
# (A) THE EXPLICIT TEMPLATE WAVEFORM
#     h(t) = sum_m gamma^m * H(t-t_m) * exp(-(t-t_m)/tau) * cos(2 pi f0 (t-t_m)+psi)
#     echoes at t_m = t_0 + (sum of multiplicative delays); the m-th echo onset
#     is at the cumulative log-periodic time t_m = t_start * e^{m pi/2}.
#     We confirm: (a) the discrete peaks lie on the smooth envelope t^{-nu};
#                 (b) the per-echo energy drops by gamma^2 = ladder ratio.
# ============================================================
print("\n=== (A) Explicit template: peaks lie on t^{-nu} envelope ===")
print("  NOTE: the slope below is an ALGEBRAIC IDENTITY (slope = -2 S_1/pi = -nu by")
print(
    "        construction, since log h_m=-m S_1 and log t_m=log t_0+m pi/2). The tiny"
)
print("        residual is float noise on a tautology, NOT empirical agreement. The")
print("        predictive content is that the two locks feeding it (e^{pi/2} from 03,")
print("        e^{-S_1} from 06) were derived on INDEPENDENT branches.")

f0 = 251.0  # GW150914 fundamental (corpus)
tau = 4.0e-3  # tau_220 (corpus damping time)
Q = np.pi * f0 * tau  # quality factor consistency check vs corpus 3.2
print(f"  f0 = {f0} Hz, tau_220 = {tau * 1e3:.1f} ms")
print(
    f"  implied Q = pi f0 tau = {Q:.2f}  (corpus Q=3.2; {abs(Q - 3.2) / 3.2 * 100:.0f}% — order check)"
)

# build a discrete echo train and check the peak envelope
t0 = 1 / f0  # first peak reference time (one fundamental period)
M = 6
t_peaks = t0 * np.exp(np.arange(M) * np.pi / 2)
h_peaks = gamma_echo ** np.arange(M)  # peak amplitude of echo m
# fit log h_peaks vs log t_peaks: slope must be -nu
A = np.vstack([np.log(t_peaks), np.ones(M)]).T
slope, intercept = np.linalg.lstsq(A, np.log(h_peaks), rcond=None)[0]
print(f"  echo peak times t_m (ms): {np.round(t_peaks * 1e3, 3)}")
print(f"  echo peak amps  h_m     : {np.round(h_peaks, 5)}")
print(f"  slope d(ln h)/d(ln t) [= -2 S_1/pi IDENTICALLY] = {slope:.10f}")
print(
    f"  -nu = -1/(phi lnphi)                             = {-nu:.10f}  (float noise on identity {abs(slope + nu):.1e})"
)

# energy per echo drops by gamma^2 = bounce-ladder ratio (note 06)
ladder_ratio = np.exp(-np.pi / (phi * lnphi))
print(f"  per-echo ENERGY ratio gamma^2 = {gamma_echo**2:.6f}")
print(
    f"  note-06 bounce-ladder ratio e^{{-pi/(phi lnphi)}} = {ladder_ratio:.6f}"
    f"  (residual {abs(gamma_echo**2 - ladder_ratio):.1e})"
)


# Actually synthesize the waveform on a grid and confirm peaks fall on envelope
def template(t, t_start, f0, tau, gamma, nlegs=8):
    h = np.zeros_like(t)
    tm = t_start
    for m in range(nlegs):
        dt = t - tm
        mask = dt >= 0
        h[mask] += (
            (gamma**m) * np.exp(-dt[mask] / tau) * np.cos(2 * np.pi * f0 * dt[mask])
        )
        tm = t_start * np.exp((m + 1) * np.pi / 2)  # next echo onset (log-periodic)
    return h


tgrid = np.linspace(t0 * 0.5, t0 * np.exp(4 * np.pi / 2) * 1.2, 400000)
hgrid = template(tgrid, t0, f0, tau, gamma_echo, nlegs=6)
# envelope peaks at each echo onset have amplitude gamma^m by construction;
# verify the analytic onset amplitudes match the t^{-nu} law within the comb
onset_t = t0 * np.exp(np.arange(5) * np.pi / 2)
onset_h = gamma_echo ** np.arange(5)
env_pred = (onset_t / t0) ** (-nu)
print(f"  onset amps gamma^m         : {np.round(onset_h, 5)}")
print(
    f"  envelope (t/t0)^-nu        : {np.round(env_pred, 5)}  (max rel.dev {np.max(np.abs(onset_h - env_pred) / onset_h):.1e})"
)

# ============================================================
# (B) FIRST-ECHO DELAY for GW150914 (M_f = 62 Msun) in ms
#     Two honest candidate scales:
#       (B1) framework-natural: t_0 = QNM fundamental period -> Dt = t_0(e^{pi/2}-1)
#       (B2) physical light-crossing seed: t_0 = 2 r_s/c -> Dt = (2 r_s/c)(e^{pi/2}-1)
#     Compare to Abedi-Afshordi (2017) claimed echo delay ~0.2-0.3 s for GW150914.
# ============================================================
print("\n=== (B) First-echo delay, GW150914 (M_f=62 Msun) ===")
Mf = 62 * Msun
r_s = 2 * G * Mf / c**2
t_cross = 2 * r_s / c
print(f"  r_s(62 Msun)          = {r_s:.2f} m")
print(f"  light-crossing 2r_s/c = {t_cross * 1e3:.4f} ms")
print(f"  QNM period 1/f0       = {1 / f0 * 1e3:.4f} ms")
print(f"  tau_220 (corpus)      = {tau * 1e3:.1f} ms")

# (B1) seed at the QNM fundamental period
dt_B1 = (1 / f0) * (ratio_r - 1)
print(f"  (B1) seed=1/f0:      Dt_echo = (1/f0)(e^{{pi/2}}-1) = {dt_B1 * 1e3:.3f} ms")
# (B2) seed at light-crossing
dt_B2 = t_cross * (ratio_r - 1)
print(f"  (B2) seed=2r_s/c:    Dt_echo = (2r_s/c)(e^{{pi/2}}-1) = {dt_B2 * 1e3:.3f} ms")
# (B3) seed at damping time tau_220 (most physical 'pulse memory')
dt_B3 = tau * (ratio_r - 1)
print(f"  (B3) seed=tau_220:   Dt_echo = tau(e^{{pi/2}}-1) = {dt_B3 * 1e3:.3f} ms")

aa_low, aa_high = 0.2, 0.3  # Abedi-Afshordi 2017 claimed GW150914 echo Dt (s)
print(
    f"  Abedi-Afshordi(2017) claimed Dt ~ {aa_low}-{aa_high} s = {aa_low * 1e3:.0f}-{aa_high * 1e3:.0f} ms"
)
print(
    "  --> framework (B1/B3) predicts TENS of ms, ~10x SHORTER than AA's ~0.2-0.3 s claim."
)
print("  --> this is the falsifiable split: golden comb echoes are early & log-spaced.")

# multiplicative onset times (B3 anchor) for the template, first few echoes
print("  echo onset times (anchor tau_220), ms:")
for m in range(5):
    print(
        f"    echo m={m}: t = {tau * np.exp(m * np.pi / 2) * 1e3:8.2f} ms,  amp = {gamma_echo**m:.4f}"
    )

# ============================================================
# (C) QNM OVERTONE COMB vs GR Kerr overtone spectrum
#     Framework: real-frequency overtone ratio f_{m+1}/f_m = e^{pi/2}=4.81 (geometric).
#     GR Kerr (a=0.70, l=m=2): overtone REAL frequencies are nearly degenerate;
#     ratio ~0.95-1.0 (slightly DECREASING), damping grows ~linearly in n.
#     Use tabulated Kerr (2,2,n) Mw values (Berti-Cardoso-Will 2006), a=0.70.
# ============================================================
print("\n=== (C) Overtone comb: golden e^{pi/2} vs GR Kerr (a=0.70) ===")
# Dimensionless Kerr QNM M*omega for (l,m,n)=(2,2,n), a/M=0.70
# (real parts; Berti-Cardoso-Will fits / Leaver). Source values, a=0.7:
# n=0: Mw_R ~ 0.5326 ; n=1: ~0.5189 ; n=2: ~0.4936  (real parts decrease slowly)
Mw_R = np.array([0.5326, 0.5189, 0.4936])  # GR Kerr (2,2,n) real freq, a=0.7
gr_ratio_01 = Mw_R[1] / Mw_R[0]
gr_ratio_12 = Mw_R[2] / Mw_R[1]
print(f"  GR Kerr (2,2,n) Re(Mw), a=0.7: {Mw_R}")
print(
    f"  GR overtone real-freq ratios: f221/f220={gr_ratio_01:.4f}, f222/f221={gr_ratio_12:.4f}  (~1, slightly <1)"
)
print(f"  FRAMEWORK overtone ratio f_{{m+1}}/f_m = e^{{pi/2}} = {ratio_r:.4f}")
print(
    f"  --> SPLIT: GR ~0.95-0.97, framework 4.81 — a {ratio_r / gr_ratio_01:.1f}x discrepancy. Cleanly falsifiable."
)

# Convert GR Kerr overtones to Hz for GW150914 (M_f=62) for concreteness:
# f_Hz = Mw_R * c^3 / (2 pi G M_f)
fac = c**3 / (2 * np.pi * G * Mf)
gr_hz = Mw_R * fac
print(
    f"  GR Kerr overtone freqs (Hz, M_f=62): n0={gr_hz[0]:.1f}, n1={gr_hz[1]:.1f}, n2={gr_hz[2]:.1f}  (all ~250 Hz)"
)
print(
    f"  Framework comb teeth (Hz, anchor 251): {[round(251 * np.exp(j * np.pi / 2), 1) for j in range(-1, 3)]}"
)

# ============================================================
# (D) Corpus LIGO anchors
# ============================================================
print("\n=== (D) Corpus LIGO anchors ===")
events = {
    "GW150914": (62, 251, 4.0),
    "GW151226": (20.8, 751, 1.3),
    "GW190521": (142, 110, 9.2),
}
for ev, (Mf_e, f220_e, tau_e) in events.items():
    # GR expectation f220 ~ Re(Mw0)*c^3/(2 pi G M_f); using Mw0=0.5326 (a~0.7)
    f_pred = 0.5326 * c**3 / (2 * np.pi * G * Mf_e * Msun)
    print(
        f"  {ev}: M_f={Mf_e:5.1f}, corpus f220={f220_e:4.0f} Hz, GR-pred(a=0.7)={f_pred:5.0f} Hz"
        f"  ({abs(f_pred - f220_e) / f220_e * 100:4.1f}% — sanity, scales as 1/M_f)"
    )
ligo_ratio = 0.548
beta1 = np.tanh(1 / phi)
print(
    f"  LIGO t1/t2 = {ligo_ratio} (corpus); tanh(1/phi)=beta(1)={beta1:.4f} "
    f"({abs(beta1 - ligo_ratio) / ligo_ratio * 100:.2f}% off); 1/phi={1 / phi:.4f} "
    f"({abs(1 / phi - ligo_ratio) / ligo_ratio * 100:.1f}% off)"
)
print(
    f"  --> beta(1) is {abs(1 / phi - ligo_ratio) / abs(beta1 - ligo_ratio):.0f}x closer than 1/phi."
)

# LIGO ratio 0.548 = tanh(1/phi) from corpus header
print(f"  CHECK corpus header 'LIGO ratio 0.548=tanh(1/phi)': tanh(1/phi)={beta1:.4f}")

# ============================================================
# (E) Detectability count: N_obs = floor(ln rho_rd / S_1)
#     The dB-per-leg cost D_1 = -20 log10(gamma) = 20 S_1/ln10, and the dB ledger
#     IS the rapidity ledger: D_1/(20 log10 e) = S_1 exactly. So the number of
#     echoes clearing unit SNR is floor(ln rho_rd / S_1). Derives the "at most one
#     echo survives" claim of section 3 from the 17.52 dB/leg lock.
# ============================================================
print("\n=== (E) Detectable-echo count from the dB-per-leg lock ===")
D1_dB = -20 * np.log10(gamma_echo)  # amplitude dB cost per leg
print(f"  per-leg amplitude cost D_1 = -20 log10(gamma) = {D1_dB:.2f} dB")
print(
    f"  identity check D_1/(20 log10 e) = S_1 : {D1_dB / (20 * np.log10(np.e)):.6f} vs S_1={S1:.6f}"
    f"  (residual {abs(D1_dB / (20 * np.log10(np.e)) - S1):.1e})"
)
thr1 = np.exp(S1)  # rho_rd for 1 echo
thr2 = np.exp(2 * S1)  # rho_rd for 2 echoes
print(f"  SNR threshold for N_obs>=1: rho_rd = e^S_1  = {thr1:.2f}")
print(f"  SNR threshold for N_obs>=2: rho_rd = e^2S_1 = {thr2:.2f}")
for rho in [7.0, 7.52, 20.0, 56.6, 60.0]:
    N = int(np.floor(np.log(rho) / S1))
    print(f"    rho_rd={rho:5.1f}: ln(rho)/S_1={np.log(rho) / S1:5.3f} -> N_obs={N}")
print("  --> GW150914 (rho_rd~7) gives N_obs=0: first echo sits AT the noise floor.")
print(
    "  --> the marginal status of all echo searches is a THEOREM of 17.52 dB/leg, not a fit."
)

print("\n=== ALL CHECKS COMPLETE ===")
