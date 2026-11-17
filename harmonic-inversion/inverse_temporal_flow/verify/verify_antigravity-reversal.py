"""Verify note 35c: anti-gravity as the reversed K-eigenvalue, and what the
reciprocal law T*G=1 structurally PERMITS (and forbids).

Built directly on the note-35 spine (all verified to machine precision there):
  ONE generator drives the worldline: d_k V = (1/phi) K V, K=[[0,-1],[-1,0]], K^2=I,
  eigenvalues EXACTLY +-1. Null rays of V(k)=(cosh th, -sinh th):
     TIME ray  T(th)=V0+V1=e^{-th}  (K-eigenvalue -1; decays forward = arrow of time)
     GRAVITY   G(th)=V0-V1=e^{+th}  (K-eigenvalue +1; grows toward source = attraction)
  Reciprocal law T*G=1=L_y identically. Net force F=G-T=2 sinh th. boost beta=tanh th.

This note asks: is "anti-gravity" literally theta<0 (time ray dominant)? What does the
reciprocal law permit?

CHECKS:
  (1) F=2 sinh(theta) is ODD: sign(F)=sign(theta), UNIQUE zero at theta=0 (the now).
      Hard number: the force flips sign at exactly ONE place. F<0 for theta<0 = repulsion.
  (2) Mirror of the verified one-shell attraction: F(-1/phi)=-F(+1/phi), and
      beta(-1/phi)=-tanh(1/phi)=-0.5498 (exact negative of note-15 LIGO ratio).
  (3) theta -> -theta swaps the rays EXACTLY: T(-th)=G(th), G(-th)=T(th); F->-F, beta->-beta.
      => theta<0 is the time-REFLECTION of theta>0 across the now (CPT-like), not a new substance.
  (4) Reciprocal law T*G=1 holds IDENTICALLY for theta<0 too (NOT forbidden). What it forbids
      is gravity SHIELDING: cannot lower G at fixed T because T=1/G. G->0 forces T->+inf
      (theta->-inf, anti-horizon/de Sitter limit, beta->-1). Verify T=1/G numerically.
  (5) Q3 cosmology (note 21) -- HONEST mapping, NOT conflation:
      note-21 horizon is Theta_H = N_star/phi = +180.39 -- a LARGE POSITIVE scale-rapidity
      (gravity-dominant, beta->+1), NOT theta<0. Local force-direction theta != cumulative
      scale-rapidity Theta. Cosmic acceleration is a small offset from the de Sitter balance
      w=-1 (the cosmological analog of theta=0), via horizon phase Phi_res=-cos(2 N ln phi).
      Reproduce note-21's quoted number; assert the analogy is to w=-1, not to theta=0 directly.
  (5b) AUDIT -- the SIGN of (1+w0) is a PHASE KNOB, not a prediction. Phi_res=-cos(2 N lnphi)
      is the cosine of a ~280-rad argument; the depletion shell is N_star=291.88, not the
      integer 291 note 21 truncates to. Show 1+w0 runs quintessence -> de Sitter -> phantom
      within Delta N ~ 1 (zero-crossing at N~292.15, just past N_star). Only the AMPLITUDE
      bound |1+w0| <= 1/N_star is robust/sign-free; landing on quintessence is a convention.
  (6) EXTENSION -- shielding cost C(theta)=2(cosh theta -1)=G+T-2 (identity-level, no cosmology):
      EVEN in theta (no energetic side-preference; the now is the unique min); C'=F=2 sinh theta;
      C''=C+2; (1/4)[(C'')^2-(C')^2]=G*T=1 (reciprocal law = the cost's discriminant); and the
      cost to shield gravity to G=eps diverges as ~1/eps (inverse-law: no free anti-gravity).
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
K = np.array([[0.0, -1.0], [-1.0, 0.0]])
print(f"phi={phi:.6f}  1/phi={1 / phi:.6f}  lnphi={lnphi:.6f}")


def T(th):  # time ray, K-eigenvalue -1
    return np.exp(-th)


def G(th):  # gravity ray, K-eigenvalue +1
    return np.exp(+th)


def F(th):  # net force = imbalance = G - T = 2 sinh theta
    return G(th) - T(th)


def beta(th):
    return (G(th) - T(th)) / (G(th) + T(th))


# ---- (1) F is odd; sign(F)=sign(theta); unique zero at the now ----
print("\n(1) Net force F=G-T=2 sinh(theta) is ODD -> sign(F)=sign(theta):")
print(f"    {'theta':>8} {'F=2sinh':>10} {'sign':>6}")
for th in [-2.0, -1 / phi, -0.3, 0.0, 0.3, 1 / phi, 2.0]:
    f = F(th)
    assert abs(f - 2 * np.sinh(th)) < 1e-12
    assert np.sign(f) == np.sign(th) or th == 0.0
    tag = (
        "  <- the now: F=0 (only zero)"
        if th == 0.0
        else (" REPULSIVE" if f < 0 else " attractive")
    )
    print(f"    {th:8.4f} {f:+10.5f} {int(np.sign(f)):+6d}{tag}")
# uniqueness: 2 sinh(theta)=0  <=> theta=0 (sinh is strictly monotone). Verify densely.
grid = np.linspace(-6, 6, 200001)
zeros = grid[np.abs(2 * np.sinh(grid)) < 1e-9]
assert len(zeros) >= 1 and np.all(np.abs(zeros) < 1e-4), zeros
print(
    "    => UNIQUE sign-change of F on [-6,6]: theta=0 (the now). HARD NUMBER confirmed."
)

# ---- (2) Mirror of the verified one-shell attraction ----
print("\n(2) Mirror about the now (one shell = 1/phi of rapidity):")
F_plus, F_minus = F(1 / phi), F(-1 / phi)
b_plus, b_minus = beta(1 / phi), beta(-1 / phi)
assert abs(F_minus + F_plus) < 1e-12  # F(-x) = -F(x)
assert abs(b_minus + b_plus) < 1e-12
assert abs(b_plus - 0.5498) < 5e-4  # note-15 LIGO ringdown ratio
assert abs(b_plus - np.tanh(1 / phi)) < 1e-12
print(
    f"    F(+1/phi)= {F_plus:+.5f} (attraction)   F(-1/phi)= {F_minus:+.5f} (repulsion)"
)
print(
    f"    beta(+1/phi)= {b_plus:+.4f} (=note-15 LIGO 0.5498)   beta(-1/phi)= {b_minus:+.4f}"
)
print(
    f"    => repulsion one shell into the time side has EXACTLY the magnitude of "
    f"attraction one shell into the gravity side: |F|={abs(F_plus):.5f}."
)

# ---- (3) theta -> -theta swaps the rays (CPT-like time reflection across the now) ----
print("\n(3) theta -> -theta swaps the two null rays exactly (T<->G):")
for th in [0.3, 1 / phi, 1.0, 2.5]:
    assert abs(T(-th) - G(th)) < 1e-12
    assert abs(G(-th) - T(th)) < 1e-12
    assert abs(F(-th) + F(th)) < 1e-12
    assert abs(beta(-th) + beta(th)) < 1e-12
print("    T(-th)=G(th), G(-th)=T(th), F->-F, beta->-beta for all tested theta. OK")
print(
    "    => theta<0 is the time-REFLECTION of theta>0 across the now (note-14 T-fixed pt),"
)
print("       i.e. CPT-like, NOT a separate material/substance. (answers Q2)")

# ---- (4) Reciprocal law holds for theta<0; it forbids SHIELDING, not repulsion ----
print("\n(4) Reciprocal law T*G=1 -- check the NEGATIVE (time-dominant) side too:")
print(f"    {'theta':>8} {'T':>12} {'G':>12} {'T*G':>10}")
for th in [-5.0, -2.0, -1 / phi, -0.5, -0.1]:
    prod = T(th) * G(th)
    assert abs(prod - 1.0) < 1e-12  # identically 1 on BOTH sides
    print(f"    {th:8.4f} {T(th):12.5f} {G(th):12.5f} {prod:10.6f}")
print(
    "    => T*G=1 IDENTICALLY for theta<0: the law does NOT forbid the repulsive side."
)
# What it forbids: suppressing G at fixed T. Since T=1/G, shielding gravity (G->0)
# FORCES the clock to run away (T->+inf). Demonstrate the constraint surface T = 1/G.
G_vals = np.array([1e-3, 1e-2, 0.1, 0.5])  # attempt to shield gravity below unity
T_required = 1.0 / G_vals  # forced by T*G=1
assert np.allclose(T_required, [1000.0, 100.0, 10.0, 2.0])
th_required = -np.log(G_vals)  # since G=e^{th} => th=ln G ; T=e^{-th}=1/G
print(
    f"    Shielding G to {G_vals} forces T=1/G={T_required} (clock speed-up); "
    f"theta=ln G={np.round(th_required, 3)}."
)
print(
    "    => no local 'anti-gravity device' kills G without an UNBOUNDED time speed-up"
)
print("       (G->0  <=>  theta->-inf, anti-horizon/de Sitter limit, beta->-1).")
print(f"    beta(theta->-inf) limit check: beta(-20)={beta(-20.0):.6f} (->-1). OK")

# ---- (5) Q3 cosmology: HONEST distinction, reproduce note-21 number, NO conflation ----
print("\n(5) Cosmology (note 21) -- structural ANALOG, not the same theta:")
N_star = 291.88
Theta_H = N_star / phi  # cumulative scale-rapidity Planck->Hubble
assert abs(Theta_H - 180.39) < 0.01
print(
    f"    note-21 horizon scale-rapidity Theta_H = N_star/phi = {Theta_H:.2f}  "
    f"(LARGE POSITIVE, gravity-side, beta->+1) -- NOT theta<0."
)
# reproduce note-21's w0 EXACTLY from the horizon phase (avoid introducing a fresh number)
N_corpus = (
    291  # INTEGER corpus shell used in note 21 (the actual depletion shell is 291.88)
)
Phi_res = -np.cos(2 * N_corpus * lnphi)
w0 = -1.0 + Phi_res / N_star
print(f"    horizon phase Phi_res = -cos(2*{N_corpus}*lnphi) = {Phi_res:+.4f}")
print(f"    w0 = -1 + Phi_res/N_star = {w0:.5f}   (note-21 quotes -0.99693)")
assert abs(w0 - (-0.99693)) < 5e-4, w0
one_plus_w0 = 1.0 + w0
print(
    f"    1+w0 = {one_plus_w0:+.5f}  (note-21's quoted side: quintessence, at INTEGER N=291)"
)
print("    => cosmic acceleration is a small offset from the de Sitter balance w=-1,")
print("       the COSMOLOGICAL analog of the now (theta=0) -- a structural analog,")
print("       NOT a literal theta<0. (Q3)")

# ---- (5b) HONEST AUDIT: the SIGN of (1+w0) is a phase knob, NOT a robust prediction ----
# Phi_res = -cos(2 N lnphi) is the cosine of a LARGE argument (~280 rad), acutely phase-
# sensitive to the shell convention. The depletion shell is N_star=291.88, NOT the integer
# 291. Show 1+w0 runs quintessence -> de Sitter -> phantom within Delta N ~ 1 of the shell.
print(
    "\n(5b) AUDIT -- sign of (1+w0) across the shell-convention ambiguity (phase knob):"
)
print(f"    {'N':>9} {'1+w0':>11}   side")
sides = {}
for N in [291.0, 291.5, N_star, 292.16, 292.5, 293.0]:
    opw = -np.cos(2 * N * lnphi) / N_star
    side = (
        "QUINTESSENCE"
        if opw > 1e-5
        else ("de Sitter" if abs(opw) <= 1e-5 else "PHANTOM")
    )
    sides[N] = side
    print(f"    {N:9.2f} {opw:+11.6f}   {side}")
# The cosine zero-crossing (de Sitter) sits at N ~ 292.15, only ~0.3 beyond N_star=291.88.
Ns = np.linspace(291.0, 294.0, 300001)
c = np.cos(2 * Ns * lnphi)
crossings = Ns[:-1][np.diff(np.sign(c)) != 0]
print(f"    cos(2 N lnphi) zero-crossing in [291,294]: N = {np.round(crossings, 3)}")
assert any(abs(x - 292.15) < 0.02 for x in crossings)
# HARD: the sign genuinely flips -- N=291 is quintessence, N=293 is phantom.
assert sides[291.0] == "QUINTESSENCE" and sides[293.0] == "PHANTOM"
# At the TRUE depletion shell the quintessence margin is already 3.5x smaller than the
# integer-truncated value note 21 quotes -- the result is not robust to the convention.
opw_int, opw_true = (
    -np.cos(2 * 291.0 * lnphi) / N_star,
    -np.cos(2 * N_star * lnphi) / N_star,
)
assert opw_int > opw_true > 0 and opw_int / opw_true > 3.0
print(
    f"    => |1+w0| at N=291 is {opw_int / opw_true:.1f}x the value at N_star=291.88, and the"
)
print(
    "       SIGN flips to phantom by N=293. Landing on quintessence requires truncating"
)
print(
    "       N_star=291.88 -> 291. The SIGN is a phase knob; only the AMPLITUDE is robust."
)
# What IS robust (geometry-locked): the amplitude bound |1+w0| <= 1/N_star, BOTH sides.
amp_bound = 1.0 / N_star
for N in [291.0, 291.88, 292.5, 293.0]:
    assert abs(-np.cos(2 * N * lnphi) / N_star) <= amp_bound + 1e-12
print(
    f"    ROBUST result: |1+w0| <= 1/N_star = {amp_bound:.5f} (sub-percent), sign-free. OK"
)

# ---- (6) EXTENSION: shielding cost C(theta)=2(cosh theta -1)=G+T-2 -- identity-level ----
print(
    "\n(6) EXTENSION -- shielding cost functional C(theta) = G+T-2 = 2(cosh theta - 1):"
)


def C(th):
    return G(th) + T(th) - 2.0


# (a) cost is EVEN: repulsion and attraction one shell out cost the same; the now is the min.
assert abs(C(1 / phi) - C(-1 / phi)) < 1e-12
assert abs(C(1 / phi) - 2 * (np.cosh(1 / phi) - 1)) < 1e-12
C_shell = C(1 / phi)
assert abs(C_shell - 0.39428) < 5e-5
assert C(0.0) == 0.0  # the now is the unique minimum
print(
    f"    C(+1/phi)=C(-1/phi)={C_shell:.5f} (cost is EVEN: no energetic side-preference);"
)
print("    C(0)=0 is the unique minimum, C''(0)=2cosh0=2>0.")

# (b) gradient is the force; curvature is C+2; discriminant recovers T*G=1.
dth = 1e-6
for th in [-1.0, -0.3, 0.4, 1 / phi, 1.5]:
    Cp_num = (C(th + dth) - C(th - dth)) / (2 * dth)  # numeric C'
    assert abs(Cp_num - F(th)) < 1e-6  # C' = F = 2 sinh theta
    assert abs((2 * np.cosh(th)) - (C(th) + 2.0)) < 1e-12  # C'' = C + 2
    disc = 0.25 * (
        (2 * np.cosh(th)) ** 2 - (2 * np.sinh(th)) ** 2
    )  # 1/4[(C'')^2-(C')^2]
    assert abs(disc - 1.0) < 1e-12  # = G*T = 1, the reciprocal law as the discriminant
print("    C'(theta)=F=2 sinh theta (gradient is the force); C''=C+2; and")
print(
    "    (1/4)[(C'')^2-(C')^2]=G*T=1 -- the reciprocal law is the cost's DISCRIMINANT. OK"
)

# (c) cost to shield gravity to G=eps diverges as 1/G (inverse-law, not one-for-one).
print(f"    {'G=eps':>9} {'theta=ln eps':>13} {'C=G+T-2':>12} {'~1/G':>10}")
for eps in [0.5, 0.1, 1e-2, 1e-3]:
    th = np.log(eps)
    cost = C(th)
    assert abs(cost - (eps + 1.0 / eps - 2.0)) < 1e-9
    print(f"    {eps:9.0e} {th:13.4f} {cost:12.4f} {1.0 / eps:10.1f}")
# verify the asymptotic: C / (1/G) -> 1 as G->0
assert abs(C(np.log(1e-4)) / (1e4) - 1.0) < 1e-3
print(
    "    => shielding cost C ~ 1/G diverges as gravity is cancelled (no free anti-gravity). OK"
)

print(
    "\nALL CHECKS PASSED -- F=2 sinh(theta) odd (unique zero at the now); theta<0 is the"
)
print(
    "time-reflection of theta>0 (CPT-like); T*G=1 on BOTH sides (repulsion permitted,"
)
print(
    "shielding forbidden). Cosmology: structural analog only -- |1+w0|<=1/N_star is robust,"
)
print(
    "but the SIGN (quintessence vs phantom) is a phase knob, NOT a prediction (5b). The"
)
print(
    "shielding cost C=G+T-2 is even, has gradient F and discriminant T*G=1, and ~1/G (Ext)."
)
