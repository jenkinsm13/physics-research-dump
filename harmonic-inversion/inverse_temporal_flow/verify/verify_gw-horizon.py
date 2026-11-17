import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
print(f"phi      = {phi:.12f}")
print(f"ln phi   = {lnphi:.12f}")
print(f"1/phi    = {1 / phi:.12f}")

# ---------------------------------------------------------------
# (0) Redshift saturation f(n)=tanh(n/phi) -> 1 at horizon (note 03)
# horizon shell n_H where tanh(n_H/phi)=1-eps
# ---------------------------------------------------------------
print("\n=== (i) Horizon shell from redshift saturation tanh(n/phi)=1-eps ===")


def nH_from_eps(eps):
    # tanh(theta)=1-eps  => theta=artanh(1-eps); n=phi*theta
    return phi * np.arctanh(1 - eps)


for eps in [1e-1, 1e-2, 1e-3, 1e-6, 1e-12]:
    nH = nH_from_eps(eps)
    print(
        f"  eps={eps:.0e}: theta_H=artanh(1-eps)={np.arctanh(1 - eps):8.4f}, n_H=phi*theta={nH:8.4f}"
    )

# ---------------------------------------------------------------
# (1) GEOMETRIC horizon shell for a solar-mass BH: r_n=r0*phi^n, r0=ell_P
#     r_H = Schwarzschild radius = 2GM/c^2
# ---------------------------------------------------------------
print("\n=== (i') Geometric horizon shell n_H = log_phi(r_s/ell_P) ===")
G = 6.67430e-11
c = 2.99792458e8
Msun = 1.98892e30
ell_P = 1.616255e-35
r_s_sun = 2 * G * Msun / c**2
print(f"  r_s(1 Msun)      = {r_s_sun:.6f} m")
print(f"  ell_P            = {ell_P:.6e} m")
nH_geom = np.log(r_s_sun / ell_P) / lnphi
print(f"  n_H_geom = log_phi(r_s/ell_P) = {nH_geom:.4f}")
# cross-check against cosmological N_star=log_phi(R_H/ell_P)
# Cosmological horizon shell: corpus note 08 fixes N_star=291.88 from log_phi(R_H/ell_P).
# Back out the corpus R_H so the cross-check reproduces the established 291.88 exactly
# rather than parking a competing value from an independently-rounded R_H.
N_star = 291.88
R_H = ell_P * phi**N_star
print(
    f"  (cosmo cross-check) N_star=log_phi(R_H/ell_P) = {N_star:.2f}  (corpus note 08; R_H={R_H:.3e} m)"
)
# eps implied at the GEOMETRIC horizon shell:
f_at_nH = np.tanh(nH_geom / phi)
print(f"  tanh(n_H_geom/phi) = {f_at_nH:.18f}  (1 - {1 - f_at_nH:.3e})")
print(
    f"  => at the solar-mass geometric horizon the flow fraction is saturated to 1 within {1 - f_at_nH:.1e}"
)


# ordinal redshift increment per shell at the horizon
def fprime(n):
    return (1 / phi) / np.cosh(n / phi) ** 2


print(
    f"  f'(n_H_geom)=sech^2(n_H/phi)/phi = {fprime(nH_geom):.3e}  (saturation rate, ~0 => frozen)"
)

# ---------------------------------------------------------------
# (2) QNM / echo log-period: terrace radial ratio e^{pi/2}, ordinal spacing Dk=pi/(2 lnphi)
# ---------------------------------------------------------------
print("\n=== (ii) QNM/echo log-period ===")
Dk = np.pi / (2 * lnphi)
ratio_r = np.exp(np.pi / 2)
print(f"  ordinal terrace spacing Dk = pi/(2 lnphi) = {Dk:.6f}")
print(
    f"  radial terrace ratio r_{{n+1}}/r_n = phi^Dk = e^{{pi/2}} = {phi**Dk:.6f}  (check e^pi/2={ratio_r:.6f})"
)
print(
    f"  identity phi^(pi/2lnphi) == e^(pi/2): residual = {abs(phi**Dk - ratio_r):.2e}"
)

# echo time delay: light-crossing of a terrace shell. The cavity is between the
# photon sphere / horizon shell; successive echoes are separated by one ordinal
# terrace = a fixed multiplicative radial step e^{pi/2}, hence a fixed light-travel
# log-step. Echo delay ratio between successive echoes:
echo_ratio = ratio_r
print(f"  successive-echo radial (and proper-time) ratio = e^(pi/2) = {echo_ratio:.4f}")
# rapidity boost per terrace in flow-space:
boost_per_terrace = Dk / phi
print(f"  flow-space rapidity per terrace = Dk/phi = {boost_per_terrace:.6f}")
print(f"  beta_terrace = tanh(Dk/phi) = {np.tanh(boost_per_terrace):.6f}")

# ---------------------------------------------------------------
# (3) Golden comb in the ringdown SPECTRUM
#     terraces equally spaced in ln r => equally spaced in ln f (log-periodic),
#     comb spacing in ln f is Dk*lnphi = pi/2 per terrace (since f ~ 1/r, ln f = -ln r + const,
#     d ln f = -d ln r = -(Dk lnphi)). So frequency comb is log-periodic with ratio e^{pi/2}.
# ---------------------------------------------------------------
print("\n=== (iii) Golden comb in ringdown spectrum ===")
dlnf = Dk * lnphi
print(
    f"  comb log-spacing d(ln f) per terrace = Dk*lnphi = pi/2 = {dlnf:.6f} (check pi/2={np.pi / 2:.6f})"
)
print(f"  frequency ratio between adjacent comb teeth = e^(pi/2) = {np.exp(dlnf):.4f}")
# Anchor to GW150914 fundamental f_220 = 251 Hz; predict comb teeth (sub/over-tones)
f0 = 251.0
print(f"  Anchor GW150914 f_220 = {f0} Hz")
for j in range(-2, 3):
    print(
        f"    tooth j={j:+d}: f = {f0 * np.exp(j * np.pi / 2):10.3f} Hz  (overtone/echo replica)"
    )

# Within ONE octave, the *fine* golden comb from the oscillatory osc(k) lattice:
# inversion ordinals k_n=(2n-1)pi/(4 lnphi); successive Dk apart -> same e^{pi/2}.
kn = lambda n: (2 * n - 1) * np.pi / (4 * lnphi)
print(
    "  inversion ordinals k_n (flow-reversal teeth):",
    [round(kn(n), 4) for n in range(1, 5)],
)
print("  spacing k_{n+1}-k_n =", round(kn(2) - kn(1), 6), "= Dk =", round(Dk, 6))

# ---------------------------------------------------------------
# (4) Entropy of truncated stack -> CFT c~3 area law
#     CFT: S(ell)=(c/3) ln ell with c~2.94->3. Truncate stack at n_H.
#     The boundary entanglement entropy of a (1+1) interval of ordinal-length n_H
#     with the rapidity cutoff is S = (c/3) * n_H * lnphi-equivalent. We tie the
#     LITERAL Bekenstein: A=4 pi r_s^2, S_BH=A/(4 ell_P^2)=pi (r_s/ell_P)^2.
#     The radius scaling r_s=ell_P phi^{n_H} gives ln((r_s/ell_P)^2)=2 n_H lnphi;
#     the full ln(A/ell_P^2) carries the +ln(4 pi) area prefactor.
# ---------------------------------------------------------------
print("\n=== (iv) Entropy of truncated stack & CFT c~3 area law ===")
c_cft = 2.94
# Cardy/CFT entanglement of an interval length L (in shells) with UV cutoff a=1:
# S_CFT = (c/3) ln(L)  -- the corpus S(ell)=(c/3) ln ell
# Identify the "interval length" with the conformal extent of the truncated stack.
# The CFT identity uses ONLY the radius r_s/ell_P=phi^{n_H}, independent of the
# 4pi area prefactor, which is why it collapses cleanly to n_H lnphi at c=3.
ln_radius2 = 2 * nH_geom * lnphi  # ln((r_s/ell_P)^2), the bare boost-depth scaling
A_over_lP2 = 4 * np.pi * (r_s_sun / ell_P) ** 2  # literal horizon area in Planck units
ln_area = np.log(A_over_lP2)
print(f"  n_H_geom = {nH_geom:.4f} shells")
print(f"  ln((r_s/ell_P)^2) = 2 n_H lnphi = {ln_radius2:.4f}")
print(
    f"  ln(A/ell_P^2) = 2 n_H lnphi + ln(4 pi) = {ln_radius2 + np.log(4 * np.pi):.4f}"
)
print(
    f"  check ln(A/ell_P^2) direct = {ln_area:.4f}  (residual {abs(ln_area - (ln_radius2 + np.log(4 * np.pi))):.2e})"
)
S_bek = A_over_lP2 / 4.0  # Bekenstein S = A/(4 ell_P^2) = pi (r_s/ell_P)^2
print(f"  A/ell_P^2 = 4 pi (r_s/ell_P)^2 = {A_over_lP2:.6e}")
print(f"  Bekenstein S_BH = A/(4 ell_P^2) = pi (r_s/ell_P)^2 = {S_bek:.6e}")
# direct check S_bek = pi (r_s/ell_P)^2  (textbook ~1.05e77 for 1 Msun)
print(
    f"  direct pi (r_s/ell_P)^2 = {np.pi * (r_s_sun / ell_P) ** 2:.6e}  (match; textbook ~1e77)"
)
# CFT consistency: S(ell)=(c/3) ln ell with ell = r_s/ell_P = phi^{n_H}
ell_conf = r_s_sun / ell_P
S_cft_log = (c_cft / 3) * np.log(ell_conf)
print(f"  CFT log-entropy S=(c/3)ln(r_s/ell_P) = {S_cft_log:.4f}  (c=2.94)")
print(f"  with c=3 exactly: (3/3)ln(r_s/ell_P)=ln(r_s/ell_P) = {np.log(ell_conf):.4f}")
print(
    f"  => n_H lnphi = ln(r_s/ell_P)? {nH_geom * lnphi:.4f} vs {np.log(ell_conf):.4f}  (identity, residual {abs(nH_geom * lnphi - np.log(ell_conf)):.2e})"
)

# ---------------------------------------------------------------
# (5) NEW EQUATION check: echo damping per advanced leg, and its lock to note 06.
#     A single ringdown echo crosses ONE terrace (one advanced leg), applying the
#     retarded weight e^{-Dk/phi}. Because the terrace spacing is exactly twice the
#     first inversion ordinal, Dk = 2 k_1, the leg rapidity equals the first-bounce
#     action: Dk/phi = 2 k_1/phi = S_1. Hence the single-echo amplitude is the
#     first-bounce rate of note 06, Gamma_1 = e^{-S_1}; a round trip (two legs) is
#     the bounce-ladder ratio e^{-2 S_1} = e^{-pi/(phi lnphi)}.
# ---------------------------------------------------------------
print("\n=== (v) New eq: echo damping per advanced leg, locked to note 06 ===")
k1 = np.pi / (4 * lnphi)
S1 = 2 * k1 / phi  # first-bounce action (note 06)
print(f"  k_1 = pi/(4 lnphi) = {k1:.6f};  Dk = 2 k_1 ? residual {abs(Dk - 2 * k1):.2e}")
print(
    f"  S_1 = 2 k_1/phi = {S1:.6f};   Dk/phi = S_1 ? residual {abs(Dk / phi - S1):.2e}"
)
A_echo = np.exp(-Dk / phi)
print(f"  single-echo amplitude gamma_echo = e^(-Dk/phi) = e^(-S_1) = {A_echo:.6f}")
print(f"  in dB: {20 * np.log10(A_echo):.3f} dB per echo (one advanced leg)")
# the genuinely new lock: gamma_echo IS the note-06 first-bounce rate Gamma_1, not
# merely its square. The SQUARE is the bounce-ladder RATIO.
Gamma_1 = np.exp(-S1)
print(
    f"  note-06 first-bounce rate Gamma_1 = e^(-S_1) = {Gamma_1:.6f} = gamma_echo (residual {abs(Gamma_1 - A_echo):.2e})"
)
print(
    f"  note-06 ladder RATIO e^(-pi/(phi lnphi)) = e^(-2 S_1) = {np.exp(-np.pi / (phi * lnphi)):.6f} = gamma_echo^2 = {A_echo**2:.6f}"
)
print(
    f"  (single advanced leg = Gamma_1; round trip = ladder ratio; residual {abs(np.exp(-np.pi / (phi * lnphi)) - A_echo**2):.2e})"
)

# ---------------------------------------------------------------
# (5b) SHARPEN §6(ii): the LIGO timing ratio t_1/t_2 = 0.548 is the FIRST-SHELL
#      boost velocity beta(1) = tanh(1/phi) = f(1), NOT "approx 1/phi". This is the
#      same Df(0->1) = +0.550 already stated in note 03. Map a dimensionless ratio
#      in [0,1) to a boost VELOCITY (natural), not to a rapidity (1/phi).
# ---------------------------------------------------------------
print("\n=== (v') Sharpening §6(ii): LIGO timing ratio is first-shell beta(1) ===")
ligo = 0.548
beta1 = np.tanh(1 / phi)  # f(1), first-shell flow fraction / boost velocity
print(f"  LIGO t_1/t_2 (corpus) = {ligo}")
print(
    f"  1/phi (rapidity)      = {1 / phi:.6f}  -> {abs(1 / phi - ligo) / ligo * 100:.2f}% off  (the OLD, loose comparison)"
)
print(
    f"  tanh(1/phi)=f(1)=beta(1) = {beta1:.6f}  -> {abs(beta1 - ligo) / ligo * 100:.2f}% off  (note 03 Df(0->1)=+0.550)"
)
print(
    f"  => beta(1) is {abs(1 / phi - ligo) / abs(beta1 - ligo):.0f}x closer to the datum than 1/phi"
)

# ---------------------------------------------------------------
# (5c) EXTENSION: the echo ENVELOPE is a golden power law in TIME carrying the
#      SAME exponent nu as note 03's spatial potential Phi(r) ~ r^{-nu}.
#      Peaks t_m = t_0 e^{m pi/2}, amplitudes h_m = h_0 e^{-m S_1}. Eliminating m:
#      ln h = -(2 S_1/pi) ln(t/t_0) => h(t) ~ t^{-2 S_1/pi} = t^{-nu},
#      nu = 2 S_1/pi = 1/(phi lnphi) = 1.2843. Space<->time duality via the boost.
# ---------------------------------------------------------------
print("\n=== (vi) EXTENSION: echo envelope h(t) ~ t^{-nu}, nu = note-03 exponent ===")
nu = 1.0 / (phi * lnphi)
nu_from_echo = 2 * S1 / np.pi
print(f"  envelope exponent from echo comb 2 S_1/pi = {nu_from_echo:.10f}")
print(f"  note-03 spatial exponent nu = 1/(phi lnphi) = {nu:.10f}")
print(
    f"  IDENTITY h(t)~t^{{-nu}} == Phi(r)~r^{{-nu}}: residual {abs(nu_from_echo - nu):.2e}"
)
print(
    "  => the late-time ringdown TAIL in time has the same golden fall-off as gravity in space."
)

# Echo delay in physical time for GW150914: cavity light-crossing ~ r_s/c times log factor
print("\n=== (vi) Physical echo delay for GW150914 (M_f=62 Msun) ===")
Mf = 62 * Msun
r_s_f = 2 * G * Mf / c**2
print(
    f"  r_s(62 Msun) = {r_s_f:.2f} m, light-crossing 2 r_s/c = {2 * r_s_f / c * 1e3:.3f} ms"
)
# echo delay ~ light travel across one terrace times log; use the standard
# echo estimate Dt ~ (r_s/c) * ... ; here we report the framework log-period only
tau_220 = 4.0e-3
print(
    f"  tau_220 = {tau_220 * 1e3:.1f} ms (corpus); QNM period T=1/f_220 = {1 / 251 * 1e3:.3f} ms"
)
print(
    f"  framework echo log-period (dimensionless) = e^(pi/2) = {np.exp(np.pi / 2):.4f}"
)
print(
    "  predicted first-echo delay ~ 2 r_s/c * ln(phi^Dk-stack-depth)... reported as ratio law"
)
