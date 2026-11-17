"""Verification for note 12 — Golden Log-Periodicity: One Comb from Leptons to H(z).

Checks the master identity Delta_k * ln(phi) = pi/2 (exact), the universal
log-periodicity constant Lambda_phi = phi^Delta_k = e^(pi/2), the integer
DSI log-frequency omega_phi = 4, the cross-axis conversions (radial/cosmic/mass),
and the tie of the 0.44% generation-step defect to note 04's drift invariant
delta_theta_g = 78 ln(phi) - 12 pi.

[8] SHARPEN (section 2a): by FFT on an integer-period grid, the harmonic tower of
    osc on the radial axis is supported ONLY on {4n} -- the rigorous form of
    "osc IS the omega_phi=4 modulation P", proving it rather than asserting it.
[9] EXTENSION: the exact comb amplitudes (G&R 3.613). DC term = 1/sqrt2 (the
    blessed period-mean envelope, derived not assumed); tooth spacing is GOLDEN
    (omega_phi=4) while tooth amplitude decay is the SILVER ratio
    delta_S^{-2} = (sqrt2-1)^2 = 3-2sqrt2 per harmonic. Coefficients checked
    against FFT to machine precision.

Run: python3 verify_golden-log-periodicity.py
"""

import numpy as np

phi = (1 + 5**0.5) / 2
lnphi = np.log(phi)


def approx(a, b, tol):
    ok = abs(a - b) <= tol
    print(
        f"    {'PASS' if ok else 'FAIL'}  |{a:.12g} - {b:.12g}| = {abs(a - b):.2e}  (tol {tol:.0e})"
    )
    return ok


fails = 0
print(f"phi = {phi:.15f}   ln phi = {lnphi:.15f}\n")

# [1] master identity: Delta_k * ln phi = pi/2 EXACT
Dk = np.pi / (2 * lnphi)  # inversion-comb (flow-reversal) ordinal spacing
print(f"[1] Delta_k = pi/(2 ln phi) = {Dk:.10f}  (corpus 3.26425)")
print("    Delta_k * ln phi == pi/2 :")
fails += not approx(Dk * lnphi, np.pi / 2, 1e-12)

# [2] universal log-periodicity constant Lambda_phi = phi^Delta_k = e^(pi/2)
Lam = phi**Dk
print(f"\n[2] Lambda_phi = phi^Delta_k = {Lam:.12f}")
print("    == e^(pi/2) (and == note 03 terrace ratio r_{n+1}/r_n) :")
fails += not approx(Lam, np.exp(np.pi / 2), 1e-12)

# [3] NEW EQUATION: DSI log-frequency omega_phi = 2pi/ln(Lambda_phi) = 4 EXACT
omega = 2 * np.pi / np.log(Lam)
print(f"\n[3] omega_phi = 2 pi / ln(Lambda_phi) = {omega:.12f}")
print("    == 4 exactly :")
fails += not approx(omega, 4.0, 1e-12)

# [3b] envelope exponent D = 1/(phi lnphi) = note 03 static-law nu (V(k) tie)
# the retarded null projection kappa(+k)=osc(k) e^{-k/phi}; on the radial axis
# k=log_phi(r/r0) makes e^{-k/phi} = (r/r0)^{-1/(phi lnphi)}, so D = nu.
D = 1 / (phi * lnphi)
print(f"\n[3b] D = 1/(phi lnphi) = {D:.10f}")
print("    == note 03 static-law exponent nu = 1.2843 :")
fails += not approx(D, 1.2843, 1e-3)

# [4] cosmic axis: octaves per comb tooth = log2(Lambda_phi) = pi/(2 ln2)
oct_tooth = np.log2(Lam)
print(f"\n[4] octaves/tooth = log2(Lambda_phi) = {oct_tooth:.12f}")
print("    == pi/(2 ln2)  (note 08 ~2.27) :")
fails += not approx(oct_tooth, np.pi / (2 * np.log(2)), 1e-12)
print(f"    shells/octave ln2/lnphi = {np.log(2) / lnphi:.10f}  (note 08 1.4404)")

# [5] generation step = 6 full log-periods = 12 reversals; 0.44% defect = delta_theta_g
P = 2 * Dk  # full period of cos(2k lnphi)
print(f"\n[5] full log-period P = 2 Delta_k = {P:.10f} = pi/lnphi")
print(
    f"    12*Delta_k = {12 * Dk:.10f}  vs Delta_g = 39  ->  {(12 * Dk / 39 - 1) * 100:.3f}% defect"
)
dtheta_g = 78 * lnphi - 12 * np.pi
print(f"    delta_theta_g = 78 lnphi - 12 pi = {dtheta_g:.12f}  (note 04 -0.16459)")
print("    12*Delta_k - 39 == -delta_theta_g/(2 lnphi) :")
fails += not approx(12 * Dk - 39, -dtheta_g / (2 * lnphi), 1e-12)

# [6] mass axis (model-dependent, via note 04 empirical slope a)
a = 0.104538
print(f"\n[6] lepton slope a = {a} (note 04, empirical)")
print(f"    mass tooth e^(a Delta_k) = {np.exp(a * Dk):.6f}")
print(f"    per-generation e^(39 a)  = {np.exp(39 * a):.6f}  (note 04 58.968)")
print("    e^(39 a) ~ sqrt(m_tau/m_e) = sqrt(206.77*16.82) :")
fails += not approx(np.exp(39 * a), np.sqrt(206.77 * 16.82), 0.02)

# [7] apodization window (note 08)
R = (1 / 8) / (3 * lnphi)
print(
    f"\n[7] apodization R = (1/8)/(3 lnphi) = {R:.6f} ; coherence ~ {R * 291.88:.2f} shells"
)

# [8] SHARPEN (section 2a): osc's harmonic tower lands identically on {4n}.
# On the radial axis 2k lnphi = 2 ln(r/r0); cos^2 x = (1+cos 2x)/2 gives
# osc = 2/(3+cos(4 ln r)) -> ONLY base frequency present is 4. Confirm by FFT
# on an integer-period grid (zero spectral leakage), and check the spectrum is
# supported only on multiples of 4.
N = 2**18
L = 40 * np.pi  # 40 full 2pi periods of psi=4 ln r => exact integer periods
x = np.linspace(0, L, N, endpoint=False)  # x = ln(r/r0)
oscr = 1 / (1 + np.cos(2 * x) ** 2)  # 2k lnphi -> 2x on the radial axis
F = np.fft.rfft(oscr) / N
mag = np.abs(F)
# index spacing of angular freq 4 on this grid: w = 2pi k / L => k(w=4) = 4 L/(2pi) = 80
k4 = 4 * L / (2 * np.pi)
on_lattice = np.zeros_like(mag, dtype=bool)
for n in range(0, N // 2 // int(round(k4))):
    on_lattice[int(round(n * k4))] = True
off_power = mag[~on_lattice].max()
print("\n[8] osc harmonic tower lands only on {4n} (section 2a):")
print(f"    max off-lattice |coeff| = {off_power:.2e}  (must be ~0)")
fails += not approx(off_power, 0.0, 1e-10)

# [9] EXTENSION: exact comb amplitudes; golden spacing, SILVER amplitude decay.
# osc = (1/sqrt2)[1 + 2 sum (-1)^n delta_S^{-2n} cos(4n ln r)],  delta_S = 1+sqrt2.
silver = 1 + np.sqrt(2)
decay = silver**-2  # = 3 - 2 sqrt2 = (sqrt2-1)^2
print("\n[9] EXTENSION: closed-form comb amplitudes (G&R 3.613):")
print(f"    DC term 1/sqrt2 = {1 / np.sqrt(2):.10f}  (= period-mean envelope)")
print("    silver decay (sqrt2-1)^2 == 3-2sqrt2 == 1/delta_S^2 :")
fails += not approx(decay, 3 - 2 * np.sqrt(2), 1e-12)
fails += not approx(decay, (np.sqrt(2) - 1) ** 2, 1e-12)


def cn_pred(n):  # predicted cosine coefficient of cos(4n ln r) in osc
    return 1 / np.sqrt(2) if n == 0 else np.sqrt(2) * (-1) ** n * decay**n


print("    FFT cosine coefficients c_n vs closed form sqrt2 (-1)^n delta_S^{-2n}:")
for n in range(0, 4):
    ki = int(round(n * k4))
    c_fft = np.real(F[ki]) if n == 0 else 2 * np.real(F[ki])
    pred = cn_pred(n)
    print(f"      n={n}: FFT {c_fft:+.8f}  pred {pred:+.8f}")
    fails += not approx(c_fft, pred, 1e-9)
print(
    f"    tail share: n>=2 power / total AC = "
    f"{sum(cn_pred(n) ** 2 for n in range(2, 50)) / sum(cn_pred(n) ** 2 for n in range(1, 50)) * 100:.2f}% "
    f"(n=1 tooth dominates)"
)

print(
    f"\n=== {'ALL CHECKS PASSED' if fails == 0 else str(fails) + ' CHECK(S) FAILED'} ==="
)
print(
    f"Universal constant: Lambda_phi = e^(pi/2) = {np.exp(np.pi / 2):.10f}, omega_phi = 4"
)
raise SystemExit(fails)
