"""Does the chronon flow FORCE compact rotors (vs non-compact boosts)? (note 36)

The reframing this script tests: the flow does NOT "compactify the boost". The base
manifold ALREADY carries BOTH a genuinely-compact direction and a genuinely-non-compact
one, and they are different geometric directions of the Matryoshka structure:

  WITHIN a shell: the base curve r(t) is CLOSED (S^1). Its (x,z) projection is the unit
    circle x^2+z^2=1, traversed by t -> a genuine SO(2) ROTOR (J^2=-I, compact, period 2pi).
    Anything that is a circulation/winding here is FORCED compact by topology, no choice.
  ACROSS shells: the Matryoshka nesting r_n = r_0 phi^n is UNBOUNDED (n in Z). The boost
    rapidity theta=k/phi accumulates per shell -> a genuine SO(1,1) BOOST (K^2=+I, non-
    compact). The radial/dilation direction; gravity/time live here.

And the coupling FACTORS accordingly: c(k)=osc(k)*e^{-k/phi} = [compact cos-phase] x
[non-compact exp-envelope]. The cos(2k lnphi) is periodic (a circle); the e^{-k/phi} is not.

Checks:
  (1) base curve closed (S^1): r(0)=r(2pi); (x,z)=(sin,cos) is the unit circle.
  (2) spatial circulation is an SO(2) rotor: d/dt(x,z)=J(x,z), J^2=-I, eigenvalues +-i (COMPACT).
  (3) boost K: K^2=+I, eigenvalues +-1 (real, NON-compact). K and J are the two distinct
      real forms of so(2,C); iK has J's spectrum -> Wick rotation maps boost<->rotor.
  (4) the coupling factorizes: c(k)=[1/(1+cos^2(2k lnphi))]*[e^{-k/phi}]; the phase factor
      is EXACTLY Dk-periodic (compact circle), the envelope is strictly monotone (non-compact).
  (5) generation is a WINDING: delta_theta_g=78 lnphi-12pi is (accumulated phase) minus
      (12pi = 6 full windings) -> generation/charge is a near-closure on the compact circle,
      i.e. lives on S^1, not on the boost line.
  (6) THE MAKE-OR-BREAK (honest, left OPEN here): one compact circle = one U(1)/SO(2).
      SU(3) is rank 2 (needs >= 2 commuting compact circles). Does the within-shell
      structure supply >=2 independent compact circulations? Counted here; the resolution
      is the job of the note-36 threads.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
Dk = np.pi / (2 * lnphi)


def r(t):
    return np.array([np.sin(t), 0.5 * np.sin(2 * t), np.cos(t)])


print(f"phi={phi:.6f}  lnphi={lnphi:.6f}  Dk={Dk:.6f}")

# (1) closed curve, S^1
print("\n(1) base curve closed (S^1):")
print(f"    |r(0)-r(2pi)| = {np.linalg.norm(r(0) - r(2 * np.pi)):.2e}")
ts = np.linspace(0, 2 * np.pi, 2000)
xz_radii = [np.hypot(np.sin(t), np.cos(t)) for t in ts]
print(
    f"    (x,z) on unit circle: max|x^2+z^2 - 1| = {max(abs(np.array(xz_radii) - 1)):.2e}"
)
assert np.linalg.norm(r(0) - r(2 * np.pi)) < 1e-12
assert max(abs(np.array(xz_radii) - 1)) < 1e-12

# (2) spatial circulation = SO(2) rotor
print("\n(2) spatial circulation (x,z)=(sin t,cos t) is an SO(2) rotor:")
J = np.array([[0.0, 1.0], [-1.0, 0.0]])  # J (sin,cos)^T = (cos,-sin)^T = d/dt(sin,cos)
for t in [0.3, 1.1, 2.7]:
    xz = np.array([np.sin(t), np.cos(t)])
    dxz = np.array([np.cos(t), -np.sin(t)])  # d/dt
    assert np.allclose(J @ xz, dxz), (t, J @ xz, dxz)
print(f"    d/dt(x,z) = J(x,z) verified; J^2 = {np.round(J @ J, 12).tolist()} = -I")
evJ = np.linalg.eigvals(J)
print(f"    J eigenvalues = {np.round(evJ, 6)}  -> +-i (COMPACT, period 2pi)")
assert np.allclose(J @ J, -np.eye(2))
assert np.allclose(np.sort_complex(evJ), [-1j, 1j])

# (3) boost K vs rotor J: the two real forms
print("\n(3) boost K (across-shell) vs rotor J (within-shell):")
K = np.array([[0.0, -1.0], [-1.0, 0.0]])
print(
    "    K^2 = I (eigenvalues +-1, REAL, non-compact); J^2 = -I (eigenvalues +-i, compact)"
)
assert np.allclose(K @ K, np.eye(2))
# iK has the rotor spectrum -> Wick rotation theta->i theta maps boost<->rotor
ev_iK = np.linalg.eigvals(1j * K)
print(
    f"    eigenvalues(iK) = {np.round(ev_iK, 6)}  == spectrum of J  -> Wick rotation links them"
)
# compare as SETS (sort by imaginary part) to avoid sort_complex tie-breaking on
# machine-epsilon real parts; the physics is that {eig(iK)} = {+i,-i} = {eig(J)}.
assert np.allclose(sorted(ev_iK, key=lambda z: z.imag), [-1j, 1j], atol=1e-9)

# (4) the coupling factorizes: compact phase x non-compact envelope
print("\n(4) c(k)=osc(k)*e^{-k/phi} = [compact cos-phase] x [non-compact envelope]:")


def phase(k):
    return 1.0 / (1.0 + np.cos(2 * k * lnphi) ** 2)  # depends only on cos(2k lnphi)


def env(k):
    return np.exp(-k / phi)


# phase is Dk-periodic:
pp = max(abs(phase(k) - phase(k + Dk)) for k in [0.2, 0.7, 1.3, 2.1, 2.9])
print(f"    phase factor Dk-periodic: max|phase(k)-phase(k+Dk)| = {pp:.2e}  (a CIRCLE)")
# envelope strictly monotone (non-periodic):
en = [env(k) for k in [0.0, 1.0, 2.0, 3.0]]
mono = all(en[i] > en[i + 1] for i in range(len(en) - 1))
print(
    f"    envelope e^-k/phi strictly decreasing (non-compact LINE): {mono}; e^-k/phi @k=0..3 = {np.round(en, 4).tolist()}"
)
assert pp < 1e-6 and mono

# (5) generation is a winding on the compact circle
print("\n(5) generation rotor = a WINDING on the compact circle:")
dtg = 78 * lnphi - 12 * np.pi
print(
    f"    delta_theta_g = 78 lnphi - 12 pi = {78 * lnphi:.4f} - {12 * np.pi:.4f} = {dtg:.5f}"
)
print(
    "    the 12 pi = 6 full windings (2pi*6); generation/charge is a near-closure on S^1,"
)
print(
    "    NOT a displacement on the boost line -> charge lives on the compact direction."
)
assert abs(dtg - (-0.16459)) < 1e-3

# (6) MAKE-OR-BREAK: the rank computation, done. SU(3) is rank 2.
#     The PRE-REGISTERED GATE: to claim "compactness forced for SU(3)", name TWO
#     independent COMMUTING compact circulations the base curve supplies. Compute how
#     many there actually are.
print("\n(6) MAKE-OR-BREAK: count independent commuting COMPACT circulations.")


# (6a) Rebuild note-34's two planes using SPATIAL ROTORS ONLY (J^2=-I), no time axis.
#      Plane A = (e1,e2), Plane B = (e1,e3) -- but now check: are these COMPACT, and do
#      they COMMUTE (give rank 2), without using the time axis?
def emb(M2, i, j, n=3):
    E = np.zeros((n, n), dtype=complex)
    idx = [i, j]
    for a in range(2):
        for b in range(2):
            E[idx[a], idx[b]] = M2[a, b]
    return E


jrot = np.array([[0.0, 1.0], [-1.0, 0.0]])  # so(2) rotor, eigenvalues +-i (compact)
# The two Cartan (diagonal, commuting) candidates of su(3): only TWO exist and they
# are diag(1,-1,0) and diag(1,1,-2)/sqrt3. A compact circulation = an so(2) rotation in
# a coordinate plane. The base curve (x,z) supplies the (1,3)-plane rotor (verified (2)).
# Does it supply a SECOND, independent, commuting one?
R12 = emb(jrot, 0, 1)  # rotor in (e1,e2)
R13 = emb(jrot, 0, 2)  # rotor in (e1,e3) -- the base curve's actual circle
R23 = emb(jrot, 1, 2)  # rotor in (e2,e3)


# do any two of these COMMUTE? (commuting rotors = a maximal torus = the rank)
def commutes(A, B):
    return np.allclose(A @ B - B @ A, 0, atol=1e-12)


pairs = {
    "R12,R13": commutes(R12, R13),
    "R12,R23": commutes(R12, R23),
    "R13,R23": commutes(R13, R23),
}
print(
    f"    coordinate-plane rotors R_ij (each compact, J^2=-I). Commuting pairs: {pairs}"
)
n_commuting = sum(pairs.values())
print(
    f"    -> NO two distinct coordinate rotors commute (they share an axis): "
    f"{n_commuting} commuting pairs. Maximal compact torus from rotors alone = rank 1."
)
assert n_commuting == 0  # any two R_ij share an index -> never commute

# (6b) How many INDEPENDENT spatial circles does the base curve actually have?
#      The curve r(t)=(sin t, 1/2 sin2t, cos t): its ONLY closed circulation is the (x,z)
#      unit circle. y=1/2 sin2t = x*z is SLAVED to (x,z), not an independent circle.
#      Topologically the curve is ONE S^1. Count independent fundamental circles:
print("\n(6b) independent compact circles of the base curve r(t):")
# y - x z should vanish identically (y is slaved, not a free circle):
slave = max(abs(0.5 * np.sin(2 * t) - np.sin(t) * np.cos(t)) for t in ts)
print(f"    y = x z exactly (y slaved to the (x,z) circle): max|y - xz| = {slave:.2e}")
print("    so the curve has exactly ONE independent circulation (the (x,z) circle);")
print(
    "    the figure-eight projection is still one S^1. Independent compact circles = 1."
)
assert slave < 1e-12

# (6c) THE GATE. Name the SECOND independent commuting compact circulation. There isn't one.
print("\n(6c) PRE-REGISTERED GATE (name 2 independent commuting compact circulations):")
print("    available: 1 (the base-curve (x,z) circle). Needed for SU(3) rank 2: 2.")
print("    The note-34 'second plane' shared the TIME axis e1 -> it was a BOOST plane")
print(
    "    (non-compact, K^2=+I), which is why the literal build gave split sl(3,R) (5,3)."
)
print("    A purely-spatial second circle would need a second independent spatial S^1,")
print("    which the base curve does NOT supply (y is slaved to xz).")
print(
    "    VERDICT: U(1) compactness FORCED (1 circle, topology); SU(3) compactness NOT"
)
print(
    "    FORCED -- the rank-2 torus requires either the time axis (=> Wick rotation, an"
)
print("    ASSUMPTION) or a second spatial circle the manifold lacks. Honest split.")
rank_available = 1
rank_needed_su3 = 2
assert rank_available < rank_needed_su3

print("\n=== SUMMARY (honest SPLIT verdict) ===")
print("The base manifold is a cylinder S^1 x R: a COMPACT spatial circle (the closed")
print("(x,z) base curve, within-shell) and a NON-compact boost line (Matryoshka phi^n,")
print("across-shell = time/gravity). The boost is genuinely never compactified.")
print("")
print("U(1) / abelian charge: compactness is FORCED. Charge is a winding on the closed")
print("  curve (delta_theta_g a near-closure on S^1); topology quantizes it. A real")
print("  derivation, no assumption.")
print(
    "SU(3) / color: compactness is NOT FORCED by the manifold. SU(3) is rank 2, but the"
)
print(
    "  base curve supplies exactly ONE independent spatial circle (y is slaved to xz, so"
)
print(
    "  no two coordinate rotors commute -> maximal compact torus = rank 1 = U(1)). The"
)
print(
    "  rank-2 torus needs either the time axis (note-34's shared-e1 'second plane' = a"
)
print(
    "  BOOST, giving split sl(3,R) (5,3)) or a second spatial circle the curve lacks."
)
print(
    "  So compact color rests on the boost->rotor Wick rotation as a genuine ASSUMPTION,"
)
print("  NOT dissolved by the within-shell reframing.")
print("")
print("=> The question 'must the flow compactify boosts to rotors?' answers SPLIT:")
print("   for U(1) the compact rotor is already there (no compactification needed);")
print("   for SU(3) a compactification IS needed and is NOT forced by the geometry.")
print("\nALL ASSERTIONS PASSED")
