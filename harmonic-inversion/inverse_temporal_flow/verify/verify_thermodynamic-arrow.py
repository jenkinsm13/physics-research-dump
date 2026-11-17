"""Machine-precision verification of note 35d (35d-thermodynamic-arrow.md).

Run: python3 verify_thermodynamic-arrow.py   (numpy only; exit 0 = all pass)

Thesis (35d, HONEST form): the arrow of time and the attractiveness of gravity are
NOT independently choosable -- both descend from the single generator K, so they share
sign(theta) as an exact INTERNAL THEOREM (not an empirical prediction). The arrow itself
(which side, +theta, the universe sits on) is an INPUT (low-entropy boundary condition),
not a derivation. On the time ray T=e^{-theta} (K-eigenvalue -1) entropy is produced;
on the gravity ray G=e^{+theta} (K-eigenvalue +1); T*G=1 ties them. The sign-lock is a
SELF-CONSISTENCY theorem -- its non-vacuous content is the lattice bound inf_k osc=1/2>0
(check 6), NOT the tautology "no shell has theta>0 and theta<0 at once" (check 5).

Checks (every boxed claim of the note):
  (1) Spine recap: K eigenvalues +-1; T*G=1 identically; F=2 sinh theta; beta=tanh theta.
  (2) Entropy production per shell = 1/phi = the single derivative d theta/dk, read 3 ways:
        (a) surprisal of the forward Boltzmann weight  dS = d(-ln p_F) = d theta = 1/phi;
        (b) per-shell log-decay of the time ray  -d ln T/dk = 1/phi;
        (c) one-way leg of the detailed-balance affinity  (1/2) d/dk ln[k(+k)/k(-k)] = 1/phi.
  (3) Branch entropy S_br(0)=ln2 (max at now), monotone decreasing to 0 deep in flow
      (note 05 sec6); flow entropy sigma=sinh(theta)/(1+cos^2) grows -> gravity CONSUMES
      branch entropy while DUMPING flow entropy. Directional, not per-chronon numerical.
  (4) Horizon sector (note 15): n_H(Msun)=183.08, S_CFT=n_H lnphi=ln(rs/lP)=88.10 (c=3),
      S_BH=pi(rs/lP)^2=1.05e77 (textbook value, recovered BY CONSTRUCTION of the radius map).
      Honest log bookkeeping: ln S_BH = lnpi + 2 n_H lnphi = 177.35 (NOT 178.73 = ln(A/lP^2)).
  (5) THE SIGN-LOCK: across theta including NEGATIVE theta,
        sign(sigma) == sign(F) == sign(theta)
      everywhere except the now. HONEST: this is a tautology (sigma>0<=>theta>0,
      F<0<=>theta<0; the "falsifier" asks theta to be both + and -). Documented as a
      self-consistency theorem, NOT validated against the world.
  (6) THE NON-VACUOUS CONTENT: the lattice osc(k)=1/(1+cos^2) is bounded in [1/2,1],
      so sigma/F = osc/2 in [1/4,1/2] is sign-fixed. The sign-lock carries information
      ONLY because inf_k osc = 1/2 > 0; a lattice able to vanish/sign-flip would break it.
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LNPHI = np.log(PHI)
INV_PHI = 1.0 / PHI
K = np.array([[0.0, -1.0], [-1.0, 0.0]])

# Solar-mass horizon inputs (note 15)
RS = 2954.0  # Schwarzschild radius of 1 Msun, metres
LP = 1.6163e-35  # Planck length, metres


def osc(k):
    # flow-reversal lattice 1/(1+cos^2(2 k lnphi)); EVEN in k, cancels in detailed balance
    return 1.0 / (1 + np.cos(2 * k * LNPHI) ** 2)


def kappa_signed(k):
    return osc(k) * np.exp(-k / PHI)


def Sbr(k):
    th = k / PHI
    return np.log(2 * np.cosh(th)) - th * np.tanh(th)


def sigma(k):
    # entropy-production rate along the flow = -G_flow = sinh(theta)/(1+cos^2) (note 05 sec3)
    return np.sinh(k / PHI) * osc(k)


def force(k):
    # net chronogravitational pull = G - T = 2 sinh(theta) (note 35)
    return 2 * np.sinh(k / PHI)


PASS = True


def chk(label, cond, detail=""):
    global PASS
    ok = bool(cond)
    PASS = PASS and ok
    print(f"   [{'OK' if ok else 'FAIL'}] {label}   {detail}")


print(
    f"phi = {PHI:.12f}   1/phi = {INV_PHI:.12f}   lnphi = {LNPHI:.12f}   ln2 = {np.log(2):.12f}"
)

print("\n=== (1) Spine recap (note 35): one generator, K-eigenvalues +-1 ===")
ev = np.sort(np.linalg.eigvalsh(K))
chk("K eigenvalues = (-1,+1)", np.allclose(ev, [-1, 1]), f"{np.round(ev, 12)}")
maxTG = 0.0
maxF = 0.0
maxB = 0.0
for th in [0.0, INV_PHI, 1.0, 2.5, 5.0]:
    T, G = np.exp(-th), np.exp(+th)
    maxTG = max(maxTG, abs(T * G - 1))
    maxF = max(maxF, abs((G - T) - 2 * np.sinh(th)))
    maxB = max(maxB, abs((G - T) / (G + T) - np.tanh(th)))
chk(
    "T*G = 1 identically (time x gravity = conserved unit)",
    maxTG < 1e-12,
    f"maxres {maxTG:.1e}",
)
chk("F = G-T = 2 sinh(theta)", maxF < 1e-12, f"maxres {maxF:.1e}")
chk("beta = (G-T)/(G+T) = tanh(theta)", maxB < 1e-12, f"maxres {maxB:.1e}")
chk(
    "one-shell beta = tanh(1/phi) = 0.5498 (note-15 LIGO ratio)",
    abs(np.tanh(INV_PHI) - 0.5497576946573435) < 1e-12,
    f"{np.tanh(INV_PHI):.6f}",
)

print(
    "\n=== (2) Entropy production per shell = 1/phi = d theta/dk, read three equivalent ways ==="
)


# (a) surprisal of the forward weight p_F(k) ~ e^{-k/phi}: S_surprisal(k) = -ln p_F = k/phi + lnZ
#     dS/dk = 1/phi exactly. Confirm by finite difference on the analytic surprisal.
def surprisal(k):
    Z = 1.0 / (1 - np.exp(-INV_PHI))  # golden partition function (note 05 sec4)
    pF = np.exp(-k / PHI) / Z
    return -np.log(pF)


dk = 1e-6
slope_a = (surprisal(3 + dk) - surprisal(3 - dk)) / (2 * dk)
chk(
    "(a) dS/dk from surprisal of e^{-k/phi}  = 1/phi",
    abs(slope_a - INV_PHI) < 1e-6,
    f"{slope_a:.9f}",
)
# (b) per-shell log-decay of the time ray T=e^{-theta}, theta=k/phi: -d ln T/dk = 1/phi
slope_b = -(np.log(np.exp(-(3 + dk) / PHI)) - np.log(np.exp(-(3 - dk) / PHI))) / (
    2 * dk
)
chk(
    "(b) -d ln T/dk (time-ray decay rate)     = 1/phi",
    abs(slope_b - INV_PHI) < 1e-6,
    f"{slope_b:.9f}",
)
# (c) detailed-balance affinity A(k)=ln[k(+k)/k(-k)]=-2k/phi; one-way leg = -(1/2)dA/dk = 1/phi.
#     First confirm the affinity is exactly -2k/phi (oscillatory lattice cancels).
maxA = max(
    abs(np.log(kappa_signed(k) / kappa_signed(-k)) - (-2 * k / PHI))
    for k in [0.3, 1.0, 1.632, 3.0, 5.7]
)
chk(
    "    detailed-balance ratio k(+k)/k(-k)=e^{-2k/phi} (lattice cancels)",
    maxA < 1e-14,
    f"maxres {maxA:.1e}",
)
slope_c = (
    -0.5
    * (
        np.log(kappa_signed(3 + dk) / kappa_signed(-(3 + dk)))
        - np.log(kappa_signed(3 - dk) / kappa_signed(-(3 - dk)))
    )
    / (2 * dk)
)
chk(
    "(c) one-way leg -(1/2)dA/dk              = 1/phi",
    abs(slope_c - INV_PHI) < 1e-6,
    f"{slope_c:.9f}",
)
print(
    f"   --> ALL THREE give the entropy-production rate = 1/phi = {INV_PHI:.10f} per shell."
)
print(
    "       Established comparison: this is dS/dk>0 (2nd law) with equality only at theta=0;"
)
print(
    "       a theorem, not a fit. No textbook 'value' for the rate -- the rate IS golden."
)

print(
    "\n=== (3) Branch entropy down, flow entropy up (note 05 sec6) -- direction only ==="
)
Sb = [Sbr(k) for k in [0, 1, 3, 10, 50]]
chk(
    "S_br(0) = ln2 (max branch entropy at the now)",
    abs(Sb[0] - np.log(2)) < 1e-12,
    f"{Sb[0]:.9f}",
)
chk(
    "S_br monotone decreasing along +theta",
    all(np.diff(Sb) < 0),
    f"{[round(s, 4) for s in Sb]}",
)
chk("S_br -> 0 deep in inverse flow", Sb[-1] < 1e-9, f"S_br(50)={Sb[-1]:.2e}")
sg = [
    sigma(k) for k in [0, 1, 3, 10]
]  # envelope grows (sinh); raw value modulated by lattice
chk(
    "flow entropy sigma(0)=0, envelope sinh grows",
    sg[0] < 1e-12 and np.sinh(10 / PHI) > np.sinh(1 / PHI),
    f"sinh(1/phi)={np.sinh(INV_PHI):.4f} -> sinh(10/phi)={np.sinh(10 / PHI):.2e}",
)
print(
    "   --> gravity CONSUMES branch entropy (ln2->0) while DUMPING flow entropy (0->inf)."
)
print(
    "       Structural (Penrose-like), NOT a per-chronon numerical balance against S_BH."
)

print(
    "\n=== (4) Horizon sector (note 15) -- textbook value recovered BY CONSTRUCTION ==="
)
nH = np.log(RS / LP) / LNPHI
chk("n_H(Msun) = 183.08", abs(nH - 183.08) < 0.01, f"{nH:.5f}")
S_CFT = nH * LNPHI
chk(
    "S_CFT = n_H lnphi = ln(rs/lP)  (c=3, exact)",
    abs(S_CFT - np.log(RS / LP)) < 1e-12,
    f"{S_CFT:.6f}",
)
S_BH = np.pi * (RS / LP) ** 2
chk(
    "S_BH = pi(rs/lP)^2 ~ 1.05e77 (textbook M_sun value)",
    1.0e77 < S_BH < 1.1e77,
    f"{S_BH:.3e}",
)
# Honest log bookkeeping: ln S_BH = lnpi + 2 n_H lnphi, NOT ln(A/lP^2)=ln4pi+2 n_H lnphi.
lnSBH = np.log(S_BH)
chk(
    "ln S_BH = lnpi + 2 n_H lnphi = 177.35 (NOT 178.73)",
    abs(lnSBH - (np.log(np.pi) + 2 * nH * LNPHI)) < 1e-9,
    f"ln S_BH={lnSBH:.5f}; ln(A/lP^2)={np.log(4 * np.pi) + 2 * nH * LNPHI:.5f}",
)

print(
    "\n=== (5) SIGN-LOCK (centerpiece): sign(sigma)==sign(F)==sign(theta), incl. theta<0 ==="
)
# Sample BOTH sides of the now. On +theta: sigma>0 (entropy produced) AND F>0 (attraction).
# On -theta (advanced/time-reverse): sigma<0 AND F<0 -- they flip TOGETHER. Never opposite.
ks = np.concatenate([np.linspace(-6, -0.05, 400), np.linspace(0.05, 6, 400)])
sig_v = np.sign(sigma(ks))  # uses osc>0, so sign tracks sinh(theta) -> sign(theta)
F_v = np.sign(force(ks))
th_v = np.sign(ks)
locked = np.all((sig_v == F_v) & (F_v == th_v))
chk(
    "sign(sigma)==sign(F)==sign(theta) for all sampled theta != 0",
    locked,
    f"{ks.size} samples on both sides of the now",
)
# Explicitly: is there ANY shell with forward time (sigma>0) AND repulsive gravity (F<0)?
# HONEST NOTE: this can never be nonzero -- sigma>0 <=> theta>0, F<0 <=> theta<0, so it
# asks for theta both positive and negative. It is a SELF-CONSISTENCY THEOREM, not an
# empirical falsifier. We assert it = 0 to document the tautology, NOT to validate the world.
violations = np.sum((sigma(ks) > 0) & (force(ks) < 0))
chk(
    "SELF-CONSISTENCY (not a falsifier): #{sigma>0 & F<0}=0 -- tautology, theta cannot be +&-",
    violations == 0,
    f"{violations} found",
)
# At the now both vanish together (the only sign-zero):
chk(
    "at the now theta=0: sigma=F=0 (single fixed point)",
    abs(sigma(0.0)) < 1e-12 and abs(force(0.0)) < 1e-12,
    "",
)

print("\n=== (6) Extension: the lattice bound that makes the sign-lock NON-VACUOUS ===")
# The ONLY non-trivial moving part: sign(sigma)==sign(F) iff osc never changes sign.
# osc = 1/(1+cos^2) in [1/2,1] strictly -- cos^2 in [0,1] => denom in [1,2]. Bounded away
# from 0, so the sigma/F ratio = osc/2 in [1/4,1/2] can never flip sign. THIS bound (not the
# tautology above) is the actual content: had the lattice been able to vanish/sign-flip, the
# sign-lock would genuinely fail. inf_k osc = 1/2 > 0 is a real fact about the golden lattice.
kgrid = np.linspace(-200, 200, 2_000_001)
o = osc(kgrid)
chk(
    "osc(k) in [1/2, 1] for all k (cos^2 in [0,1])",
    o.min() >= 0.5 - 1e-9 and o.max() <= 1.0 + 1e-9,
    f"min={o.min():.6f}, max={o.max():.6f}",
)
# UPPER bound osc=1 on the inversion shells k_n=(2n-1)pi/(4 lnphi): there 2 k_n lnphi=(2n-1)pi/2,
# cos=0, cos^2=0 -- these are the torsion-zeros (tau_Frenet=0), where the sinh is UNmodulated.
kn = np.array([(2 * n - 1) * np.pi / (4 * LNPHI) for n in range(1, 8)])
chk(
    "osc = 1 on inversion shells k_n=(2n-1)pi/(4 lnphi) (cos^2=0, torsion-zeros)",
    np.allclose(osc(kn), 1.0, atol=1e-12),
    f"osc(k_1..k_7)={np.round(osc(kn), 6)}",
)
# LOWER bound osc=1/2 midway between inversion shells, k=m pi/(2 lnphi): cos^2=1.
km = np.array([m * np.pi / (2 * LNPHI) for m in range(1, 8)])
chk(
    "osc = 1/2 (lower bound) at k=m pi/(2 lnphi), midway shells (cos^2=1)",
    np.allclose(osc(km), 0.5, atol=1e-12),
    f"osc={np.round(osc(km), 6)}",
)
nz = kgrid[np.abs(kgrid) > 1e-6]
ratio = sigma(nz) / force(nz)
chk(
    "sigma/F = osc/2 in [1/4,1/2], strictly positive (sign can NEVER flip)",
    ratio.min() >= 0.25 - 1e-9 and ratio.max() <= 0.5 + 1e-9 and ratio.min() > 0,
    f"min={ratio.min():.6f} max={ratio.max():.6f}",
)
print(
    "   --> sign-lock is non-vacuous PRECISELY because inf_k osc(k)=1/2>0; a lattice that"
)
print(
    "       could vanish/sign-flip would break it on a measure-nonzero set of shells."
)

print("\n" + ("ALL CHECKS PASSED -- exit 0" if PASS else "SOME CHECK FAILED -- exit 1"))
raise SystemExit(0 if PASS else 1)
