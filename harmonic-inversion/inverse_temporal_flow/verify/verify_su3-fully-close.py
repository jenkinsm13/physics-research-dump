"""Is SU(3) color compactness FORCED by the chronon geometry, or an un-forced posit? (note 37)

CAREFUL SCOPING (per adversarial review). Note 34 already CONSTRUCTED a genuine rank-2
su(3): two flow planes sharing the time axis, dimension exactly 8, all nine f_abc canonical
to machine precision -- but in the SPLIT real form sl(3,R), Killing signature (5,3). So the
rank-2 algebra EXISTS in the geometry; that is settled and NOT in question here. What is in
question is narrower: is the second Cartan generator COMPACT (the maximal torus rank-2
compact, as color requires) by force of the geometry, or only by an added posit?

This note does NOT claim "su(3) cannot be built" (note 34 built it) nor "rank 2 isn't there"
(it is). It tests ONE thing: whether the geometry FORCES the COMPACT real form. Result: it
does not. We do not prove impossibility (the checks verify arithmetic + two theorems, and
(D) is a hand-enumeration, not an exhaustive search); we localize the assumption.

PRE-REGISTERED GATE (fixed before computing): to declare compactness FORCED, exhibit a
maximal-compact rank-2 torus built from forced framework objects -- i.e. a SECOND commuting
generator that is compact without an added choice. If the second commuting Cartan is forced
NON-compact (a boost) unless one posits a Wick rotation / complex structure, the honest
answer is NOT-FORCED: SU(3) compactness is an assumption, localized to exactly that posit.

The obstructions, in order of weight:
  (A) [LOAD-BEARING] The base R^3 carries a TIMELIKE direction (y, note 00), so its isometry
      is the NON-compact SO(2,1): maximal COMPACT torus = rank 1. The second commuting Cartan
      is a boost (non-compact) -- exactly why note 34's literal build gave split sl(3,R) (5,3).
      Compact rank 2 then needs the boost->rotor Wick rotation, the SAME posit note 18 already
      assumes for SU(2)_L. Not forced; assumption named.
  (B,C) [SUPPORTING, narrow] The cheapest ALTERNATIVE posit -- complexify the emergent R^3 ->
      C^3 -- is also not canonical: R^3 (odd real dim) admits no complex structure (no real
      3x3 J with J^2=-I; det(-I_3)=-1). NB: note 34 did NOT complexify the emergent 3-space
      (it used two time-sharing flow planes), so (B,C) only close the alternative escape, they
      do not bear on note 34's actual construction. They support NOT-FORCED, not IMPOSSIBLE.
  (D) Candidate compact circulations enumerated (not exhaustive): all collapse to the single
      (x,z) circle -> only rank 1 is manifestly COMPACT without a posit.
  (E) c_CFT->3 is a SCALAR central charge, not a 3-space with rotors -> cannot itself supply
      a second compact Cartan.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
lnphi = np.log(phi)
Dk = np.pi / (2 * lnphi)


def comm(A, B):
    return A @ B - B @ A


print("=" * 72)
print("NOTE 37 — CAN SU(3) COMPACTNESS BE FULLY CLOSED FROM THE CHRONON GEOMETRY?")
print("=" * 72)

# ---------------------------------------------------------------------------
# (A) so(2,1) on the base R^3 with y TIMELIKE (note 00: y is the temporal axis).
#     metric eta = diag(+1,-1,+1) for (x, y=time, z).
# ---------------------------------------------------------------------------
print("\n(A) Isometries of the base R^3 = (x, y=TIME, z), metric eta=diag(+1,-1,+1):")
eta = np.diag([1.0, -1.0, 1.0])


def in_so21(M):
    return np.allclose(M.T @ eta + eta @ M, 0, atol=1e-12)


# the three so(2,1) generators
Rxz = np.array(
    [[0, 0, 1], [0, 0, 0], [-1, 0, 0]], dtype=float
)  # rotation in spatial (x,z)
Bxy = np.array(
    [[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=float
)  # boost mixing x with time y
Bzy = np.array(
    [[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=float
)  # boost mixing z with time y
gens = {
    "Rxz (spatial rotation)": Rxz,
    "Bxy (x-time boost)": Bxy,
    "Bzy (z-time boost)": Bzy,
}
for name, M in gens.items():
    ev = np.linalg.eigvals(M)
    compact = np.all(np.abs(ev.real) < 1e-9)  # purely imaginary spectrum => compact
    print(
        f"    {name:24s} in so(2,1): {in_so21(M)}  eigenvalues={np.round(ev, 3)}  "
        f"{'COMPACT' if compact else 'non-compact (boost)'}"
    )
    assert in_so21(M)
# count compact generators and the maximal commuting compact set
compact_gens = [
    M for M in gens.values() if np.all(np.abs(np.linalg.eigvals(M).real) < 1e-9)
]
print(
    f"    compact generators: {len(compact_gens)} (only Rxz). Maximal compact torus = rank 1."
)
assert len(compact_gens) == 1

# ---------------------------------------------------------------------------
# (B) THE DIMENSION OBSTRUCTION. SU(3) needs C^3 = R^6; emergent c_CFT->3 is R^3.
# ---------------------------------------------------------------------------
print("\n(B) Dimension obstruction:")
print("    SU(3): acts on C^3 = R^6, dim(su3)=8, RANK 2.")
print("    emergent c_CFT -> 3 = THREE REAL spatial dimensions = R^3 (real dim 3).")
print("    R^3 vs C^3: real-dimension mismatch factor = 6/3 = 2. R^3 is NOT C^3.")
su3_realdim_needed = 6
emergent_realdim = 3
assert su3_realdim_needed == 2 * emergent_realdim

# ---------------------------------------------------------------------------
# (C) THE COMPLEX-STRUCTURE OBSTRUCTION (the clean killer).
#     R^3 admits NO complex structure: no real 3x3 J with J^2 = -I.
#     Proof: det(J^2) = det(-I_3) = (-1)^3 = -1, but det(J^2) = det(J)^2 >= 0.
# ---------------------------------------------------------------------------
print("\n(C) Complex-structure obstruction (R^3 cannot be complexified to C^{3/2}):")
det_negI3 = np.linalg.det(-np.eye(3))
print(f"    det(-I_3) = {det_negI3:.1f}  (= (-1)^3, odd dimension)")
print(
    "    any real J with J^2=-I would need det(J)^2 = det(-I_3) = -1 < 0 : IMPOSSIBLE."
)
assert abs(det_negI3 - (-1.0)) < 1e-12
# numerical confirmation: try to find a real antisymmetric 3x3 J with J^2=-I (none exists);
# real antisymmetric 3x3 always has a 0 eigenvalue (odd dim) -> J^2 has a 0 eigenvalue != -1.
rng_fail = []
for seed_a, seed_b, seed_c in [(1, 0, 0), (0.3, -1.1, 2.0), (1, 1, 1)]:
    A = np.array(
        [[0, seed_a, seed_b], [-seed_a, 0, seed_c], [-seed_b, -seed_c, 0]], float
    )
    ev = np.linalg.eigvals(A)
    has_zero = np.min(np.abs(ev)) < 1e-9
    rng_fail.append(has_zero)
    print(
        f"    real antisym 3x3 (a,b,c)=({seed_a},{seed_b},{seed_c}): eig={np.round(ev, 3)} "
        f"-> has a ZERO eigenvalue: {has_zero} (so J^2 has eigenvalue 0, never -1)"
    )
assert all(rng_fail), "every real antisymmetric 3x3 must have a zero eigenvalue"

# ---------------------------------------------------------------------------
# (D) ENUMERATE every candidate compact circulation -> all reduce to ONE circle.
# ---------------------------------------------------------------------------
print("\n(D) Enumerate candidate compact circulations of the framework:")
candidates = [
    ("(x,z) within-shell circle", "compact U(1)", "THE one circle (rank 1)"),
    ("across-shell boost phi^n", "NON-compact R", "not a circle"),
    (
        "y=xz figure-eight winding",
        "same S^1 (y slaved)",
        "= the (x,z) circle, not independent",
    ),
    (
        "cos2t period-doubling (2t)",
        "same loop, freq 2",
        "= the (x,z) circle, not independent",
    ),
    ("generation rotor delta_theta_g", "same (x,z) circle, sampled", "not independent"),
    ("Z_3 triality (note 27)", "DISCRETE Z_3", "adds no continuous rank"),
    ("c_CFT -> 3", "SCALAR central charge", "no rotor, no 3-space"),
]
for obj, kind, verdict in candidates:
    print(f"    - {obj:32s} {kind:22s} -> {verdict}")
n_independent_compact_circles = 1
print(
    f"    => manifestly-COMPACT commuting circles found (this enumeration, not exhaustive)"
    f" = {n_independent_compact_circles}."
)
print(
    "       (The rank-2 algebra ITSELF exists -- note 34 built it -- but its second Cartan"
)
print("        came out as a BOOST, non-compact. What is rank-1 is the COMPACT torus.)")
assert n_independent_compact_circles == 1

# ---------------------------------------------------------------------------
# (E) c_CFT is a scalar: reproduce it as the SLOPE of S(l) vs ln l (a number).
# ---------------------------------------------------------------------------
print("\n(E) c_CFT is a scalar (coefficient of ln l), not a geometric 3-space:")


def c_shell(k, beta=0.2, gamma=1.0, lam=0.5):
    return 1.0 / (1 + beta * k**gamma) * np.exp(-lam * k)


N = 60
C = np.array([[c_shell(abs(i - j)) for j in range(N)] for i in range(N)])


def entropy(ell):
    HA = C[:ell, :ell]
    rho = HA / np.trace(HA)
    ev = np.linalg.eigvalsh(rho)
    ev = ev[ev > 1e-12]
    return -np.sum(ev * np.log(ev))


ells = np.arange(5, N - 5)
S = np.array([entropy(e) for e in ells])
slope = np.polyfit(np.log(ells), S, 1)[0]
c_eff = 3 * slope
print(
    f"    60-shell CFT extraction: c = 3*slope = {c_eff:.3f}  (a SCALAR; the '3' is c/3's denom)"
)
print(
    "    -> 'three dimensions' is the central-charge reading of one NUMBER; it carries"
)
print("       no metric, no rotors, no two commuting circles. Nothing to host SU(3).")
assert 2.5 < c_eff < 3.4

# ---------------------------------------------------------------------------
print("\n" + "=" * 72)
print(
    "PRE-REGISTERED GATE: is the maximal-COMPACT rank-2 torus forced by the geometry?"
)
print("    The rank-2 ALGEBRA exists (note 34, su(3) dim 8, f_abc exact). But its 2nd")
print("    commuting Cartan is a BOOST (non-compact) -> compact torus rank 1. Compact")
print("    rank 2 requires an added posit (Wick rotation). GATE: NOT FORCED.")
print("=" * 72)
print("""
VERDICT — the question is CLOSED, with answer NOT FORCED (not 'impossible').

  What is settled and NOT in doubt: the rank-2 su(3) algebra EXISTS in the geometry
  (note 34 constructed it, dim 8, all nine f_abc canonical to machine precision). The
  question 'fully close it' is therefore ONLY about the REAL FORM -- compact (color) vs
  split sl(3,R) -- not about existence.

  Answer: the geometry does NOT FORCE the compact form. The load-bearing reason:
   (A) [decisive] the base R^3 carries a timelike axis (y, note 00) -> its isometry is
       the NON-compact SO(2,1) -> maximal COMPACT torus = rank 1; the second commuting
       Cartan is forced to be a boost. This is exactly why note 34's literal build landed
       on split sl(3,R), signature (5,3). Compact rank 2 then needs the boost->rotor Wick
       rotation -- the SAME posit note 18 already makes for SU(2)_L. The assumption is thus
       not new, but it IS a genuine, un-forced posit.
   (B,C) [supporting] the cheapest ALTERNATIVE posit -- complexify the emergent R^3 -> C^3
       -- is also not canonical (R^3, odd real dim, admits no complex structure: det(-I_3)
       =-1 forbids a real J with J^2=-I). NB this does NOT touch note 34's construction
       (which used time-sharing flow planes, not a complexified 3-space); it only shows the
       escape route is not canonical either. Supports NOT-FORCED, not IMPOSSIBLE.
   (D,E) [enumeration, non-exhaustive] every candidate manifestly-compact circulation
       collapses to the single (x,z) circle; c_CFT->3 is a scalar, hosting no rotors.

  So: U(1) abelian compactness is FORCED (rank-1 (x,z) circle = winding, topology, note 36);
  SU(3) compact color is NOT forced -- it rests on the boost->rotor Wick rotation, now
  localized to exactly the second Cartan. This MATCHES note 34 ('derived modulo compactness')
  and note 36, and does not overclaim impossibility: the checks verify the SO(2,1) compact
  rank, two real-linear-algebra theorems, and a non-exhaustive enumeration -- enough for
  NOT-FORCED, not enough for (and not claiming) impossibility.
""")
print("ALL ASSERTIONS PASSED (arithmetic + SO(2,1) rank + the two theorems; not an")
print("impossibility proof -- the verdict is NOT-FORCED, the assumption localized.)")
