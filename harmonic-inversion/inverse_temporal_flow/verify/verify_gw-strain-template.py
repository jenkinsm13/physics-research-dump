#!/usr/bin/env python3
"""
verify_gw-strain-template.py  --  Note 28 numerical verification.

Checks every falsifiable number in the operational GW matched-filter template:
  - boost-ladder constants S1, gamma_echo, Gamma_tot, e^{pi/2}, dB/leg
  - event-specific echo delays and comb teeth for GW150914 and GW190521
  - N_obs detectability floor and the matched-filter SNR threshold

All physics inputs are the framework constants (phi, lnphi) plus EXTERNAL
measured numbers used only as the carrier scale (NOT predicted here, stated
honestly): the remnant masses M_f and the MEASURED f_220 of each event
(251 Hz for GW150914, ~66 Hz for GW190521). The framework predicts only the
COMPANIONS of the measured carrier (the e^{pi/2} comb ratio and the
gamma_echo amplitude law) -- never the carrier itself. This note is a
GW-template route, not a scale-pinning route, so no electron mass is derived;
the absolute-scale keystone remains open (notes 24/25/26). The 1/M-at-fixed-
spin estimate (109.6 Hz) is retained ONLY as a labelled sanity cross-check;
the runnable tooth rides on the measured f_220.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)


def approx(name, got, want, tol=1e-3):
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    print(f"[{'OK ' if ok else 'XX '}] {name:34s} = {got:.6f}   (expect {want})")
    return ok


ok = True
print("=== framework constants ===")
ok &= approx("phi", phi, 1.6180339887, 1e-6)
ok &= approx("lnphi", lnphi, 0.4812118251, 1e-6)
ok &= approx("1/phi", 1 / phi, 0.6180339887, 1e-6)

# --- boost-ladder constants (notes 00,21,23) ---
S1 = np.pi / (2 * phi * lnphi)  # first bounce action
Gtot = 1 / (2 * np.sinh(S1))  # total absorber
gamma_echo = np.exp(-S1)  # = Gamma_1, per-echo amplitude ratio
dB_leg = 20 * np.log10(gamma_echo)  # amplitude dB per echo leg
ratio = np.exp(np.pi / 2)  # comb tooth ratio in f
eS1 = np.exp(S1)  # delay multiplier

print("\n=== boost-ladder / echo constants ===")
ok &= approx("S1 = pi/(2 phi lnphi)", S1, 2.0174, 1e-3)
ok &= approx("Gamma_tot = 1/(2 sinh S1)", Gtot, 0.13539, 1e-3)
ok &= approx("gamma_echo = e^{-S1}", gamma_echo, 0.13305, 1e-3)
ok &= approx("dB per echo leg", dB_leg, -17.524, 2e-3)
ok &= approx("e^{pi/2} comb ratio", ratio, 4.81048, 1e-3)
ok &= approx("e^{S1} delay multiplier", eS1, 7.5184, 1e-3)


# --- N_obs detectability floor ---
def Nobs(rho_rd):
    return int(np.floor(np.log(rho_rd) / S1))


print("\n=== N_obs = floor( ln(rho_rd) / S1 ) ===")
for rho in [7, 10, 15, 30, 50, 100]:
    print(f"     rho_rd={rho:6.1f}  ln rho={np.log(rho):.3f}  N_obs={Nobs(rho)}")
ok &= Nobs(7) == 0  # GW150914 -> 0 echoes
print(f"[{'OK ' if Nobs(7) == 0 else 'XX '}] GW150914 (rho_rd~7) N_obs == 0")
# need rho_rd > e^{S1}=7.52 for even one echo
ok &= approx("rho_rd for first echo (=e^{S1})", eS1, 7.5184, 1e-3)

# --- event-specific numbers ---
GMsun_c3 = 4.925490947e-6  # s, = G M_sun / c^3


def t0(Mf):
    return Mf * GMsun_c3


print("\n=== GW150914  (M_f = 62 Msun, measured f_220 = 251 Hz) ===")
Mf1 = 62.0
t0_1 = t0(Mf1)
dt1_1 = t0_1 * eS1
print(f"     t0 = GM/c^3            = {t0_1 * 1e3:.4f} ms")
print(f"     first echo delay Dt1   = {dt1_1 * 1e3:.4f} ms")
ok &= approx("GW150914 t0 (ms)", t0_1 * 1e3, 0.30538, 1e-3)
ok &= approx("GW150914 Dt1 (ms)", dt1_1 * 1e3, 2.2961, 2e-3)

f0_1 = 251.0
tooth_up_1 = f0_1 * ratio
tooth_dn_1 = f0_1 / ratio
print(f"     comb tooth up   f0*e^pi/2 = {tooth_up_1:.2f} Hz")
print(f"     comb tooth down f0/e^pi/2 = {tooth_dn_1:.2f} Hz")
ok &= approx("GW150914 tooth up (Hz)", tooth_up_1, 1207.43, 0.05)
ok &= approx("GW150914 tooth down (Hz)", tooth_dn_1, 52.18, 0.05)

print("\n=== GW190521  (M_f = 142 Msun) ===")
Mf2 = 142.0
t0_2 = t0(Mf2)
dt1_2 = t0_2 * eS1
# f scales ~ 1/M for fixed dimensionless spin: f_220(190521) = 251*(62/142)
f0_2 = f0_1 * (Mf1 / Mf2)
tooth_up_2 = f0_2 * ratio
print(f"     t0                     = {t0_2 * 1e3:.4f} ms")
print(f"     first echo delay Dt1   = {dt1_2 * 1e3:.4f} ms")
print(f"     est f_220 = 251*62/142 = {f0_2:.2f} Hz")
print(f"     comb tooth up          = {tooth_up_2:.2f} Hz")
ok &= approx("GW190521 t0 (ms)", t0_2 * 1e3, 0.69942, 1e-3)
ok &= approx("GW190521 Dt1 (ms)", dt1_2 * 1e3, 5.2587, 5e-3)
ok &= approx("GW190521 f_220 est (Hz)", f0_2, 109.56, 0.05)
ok &= approx("GW190521 tooth up (Hz)", tooth_up_2, 527.05, 0.1)

# --- matched-filter SNR of the echo train ---
g2 = gamma_echo**2
geom_boost = np.sqrt(g2 / (1 - g2))  # sqrt(sum_{m>=1} gamma^{2m})
print("\n=== echo-train matched filter ===")
print(f"     SNR boost sqrt(sum g^2m) = {geom_boost:.4f}")
rho_first5 = 5 / gamma_echo
rho_train5 = 5 / geom_boost
print(f"     rho_rd for 1st echo @SNR5 = {rho_first5:.2f}")
print(f"     rho_rd for train   @SNR5  = {rho_train5:.2f}")
ok &= approx("rho_rd first echo SNR5", rho_first5, 37.58, 0.05)
# train value = 5/sqrt(g^2/(1-g^2)) = 37.25 (the earlier 37.20 target was
# rounded one tick too low and failed at tol 0.05); keep the exact closed form.
ok &= approx("rho_rd train SNR5", rho_train5, 37.25, 0.05)

# Maslov phase per shell crossing
print(f"\n     Maslov phase per crossing i^Dn (Dn=1) = pi/2 = {np.pi / 2:.4f} rad")

# --- SHARPENED GW190521: ride the comb on the MEASURED f_220, not the 1/M est ---
# The 1/M-at-fixed-spin estimate (109.6 Hz) overshoots the actual measured
# GW190521 ringdown (f_220 ~ 66 Hz; heavier remnant, different spin). The
# honest, runnable prediction puts the +1 tooth at e^{pi/2} * (MEASURED f_220).
print("\n=== GW190521 sharpened: tooth on MEASURED f_220 ~ 66 Hz ===")
f0_2_meas = 66.0
tooth_up_2_meas = f0_2_meas * ratio
print(f"     measured f_220         = {f0_2_meas:.1f} Hz")
print(f"     +1 tooth = f0*e^pi/2   = {tooth_up_2_meas:.1f} Hz  (vs 527 from 1/M est)")
ok &= approx("GW190521 tooth on measured f0 (Hz)", tooth_up_2_meas, 317.49, 0.1)

# --- EXTENSION: comb finesse F = ratio spacing / damping width ---
# A resolvable tooth needs the log-spacing pi/2 to exceed the fractional
# ringdown linewidth 1/Q. Define the inversion-comb finesse
#     F = (pi/2) * Q_eff,   Q_eff = pi f_0 tau = quality factor of the seed.
# With the framework's own per-shell decay, the e-fold is phi shells (note 23),
# so the MINIMUM intrinsic quality to resolve one tooth from its neighbour is
#     Q_min = 1/(e^{pi/2}-1) -> the tooth is resolvable iff Q_eff > Q_min.
Q_min = 1.0 / (ratio - 1.0)
print("\n=== Extension: inversion-comb finesse ===")
print(f"     Q_min = 1/(e^pi/2 - 1) = {Q_min:.5f}  (resolve-one-tooth floor)")
ok &= approx("Q_min = 1/(e^{pi/2}-1)", Q_min, 0.26244, 1e-4)
# Kerr a~0.7 dominant (2,2,0) has Q_220 ~ 3.2 >> Q_min, so the comb teeth are
# always intrinsically resolvable when present -- the limit is SNR, not width.
Q_220 = 3.2
finesse = (np.pi / 2) * Q_220
print(f"     Kerr Q_220(a~0.7) ~ {Q_220}  ->  finesse F = (pi/2)Q = {finesse:.3f}")
ok &= approx("comb finesse F=(pi/2)Q_220", finesse, 5.0265, 1e-3)
ok &= Q_220 > Q_min
print(f"[{'OK ' if Q_220 > Q_min else 'XX '}] Q_220 > Q_min (teeth width-resolvable)")

print("\n=== RESULT:", "ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED", "===")
import sys

sys.exit(0 if ok else 1)
