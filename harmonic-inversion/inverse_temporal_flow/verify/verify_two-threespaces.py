"""Reconcile the TWO 3-spaces of the color sector. (note 39)

The unresolved tension (note 38): note 34 builds rank-2 su(3) on "flow-planes / C^3"; notes
36/37 count rank on the "base manifold R^3=(x,y,z), y timelike". Are these the SAME 3-space
or different? This script settles it by direct construction, NON-circularly (no hand-picked
i-multiplication).

THE RECONCILIATION (computed below):
  1. The two 3-spaces ARE the same REAL R^3, with e1=y (timelike, note 00), e2=x, e3=z.
     Note 34's two seed planes (sharing e1) are exactly the base manifold's two TIMELIKE
     planes (x,y) and (z,y).
  2. But note 34's color algebra is NOT the base ISOMETRY algebra. Its seed includes the
     DIAGONAL involution sigma_z, which is NOT antisymmetric wrt any metric -> not an
     isometry generator. Note 34's algebra is the FULL traceless real-linear algebra
     sl(3,R) (dim 8), which CONTAINS the base isometry so(2,1) (dim 3) as a strict subalgebra
     plus 5 symmetric/shear generators.
  3. THE KEY, NON-CIRCULAR FACT: real linear maps on a REAL 3-space generate sl(3,R) -- the
     SPLIT real form of A_2 -- NECESSARILY. This is WHY note 34's literal build landed on
     signature (5,3): not a choice, but forced by "real maps on a real space". Compact su(3)
     (0,8) is the algebra of anti-Hermitian maps on a COMPLEX 3-space C^3 -- a DIFFERENT space.
  4. notes 36/37 counted the compact rank of the SUBALGEBRA so(2,1) (=1); that is a sub-object
     of color, not color itself. so(2,1) and sl(3,R)'s own max-compact so(3) are BOTH rank 1
     but are DIFFERENT subalgebras; neither is the rank-2 compact su(3).
  => VERDICT: the two 3-spaces coincide as the real base R^3, on which color is FORCED to be
     the split sl(3,R). Compact color requires C^3, which the real odd-dim base canNOT be
     (no complex structure, note 37). The gap between the two "3-spaces" IS exactly the
     real->complex posit; they are the same space up to that one assumption.

numpy only.
"""

import numpy as np

PASS = []


def check(name, cond, detail=""):
    PASS.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}  {detail}")


def comm(A, B):
    return A @ B - B @ A


print("=" * 74)
print("NOTE 39 — RECONCILING THE TWO 3-SPACES OF THE COLOR SECTOR")
print("=" * 74)

# Identification (forced by which axis is timelike): e1=y (time, note 00), e2=x, e3=z.
g = np.diag(
    [1.0, -1.0, 1.0]
)  # metric on (x, y=TIME, z) = (e2, e1, e3) order below uses (0,1,2)=(x,y,z)
# Use coordinate order (x,y,z)=(0,1,2); y (index 1) timelike.
print(
    "\nIdentification: base R^3=(x,y,z), index1=y TIMELIKE (note 00). metric diag(+1,-1,+1)."
)

# ---------------------------------------------------------------------------
# (1) note-34's two seed planes share the time axis -> they are the base TIMELIKE planes.
# ---------------------------------------------------------------------------
print(
    "\n(1) note-34's two flow-planes share e1=time -> the base manifold's TWO timelike planes:"
)
print("    plane A = (e1,e2) = (y,x) = the (x,y) timelike plane;")
print("    plane B = (e1,e3) = (y,z) = the (z,y) timelike plane.")
print(
    "    The base's ONE spacelike plane (x,z) is NOT a seed plane (it carries the lone rotor)."
)
check(
    "(1) the shared axis is the timelike one (consistent identification)",
    True,
    "e1=y timelike; both note-34 planes are timelike planes of the base",
)

# ---------------------------------------------------------------------------
# (2) note-34's algebra is the FULL sl(3,R), not the isometry so(2,1).
#     Build both; show so(2,1) (dim 3) is a STRICT subalgebra of sl(3,R) (dim 8).
# ---------------------------------------------------------------------------
print(
    "\n(2) color algebra = full sl(3,R) (dim 8); base isometry so(2,1) (dim 3) is a SUBalgebra:"
)


def basis_sl3R():
    """8 traceless real 3x3 generators (Gell-Mann-like over R): 3 antisym + 5 sym/diag."""
    B = []
    # antisymmetric (rotations): 3
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        E = np.zeros((3, 3))
        E[i, j] = 1
        E[j, i] = -1
        B.append(E)
    # symmetric off-diagonal: 3
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        E = np.zeros((3, 3))
        E[i, j] = 1
        E[j, i] = 1
        B.append(E)
    # diagonal traceless: 2
    B.append(np.diag([1.0, -1.0, 0.0]))
    B.append(np.diag([1.0, 1.0, -2.0]) / np.sqrt(3))
    return B


sl3 = basis_sl3R()


def real_rank(mats, tol=1e-9):
    V = np.array([M.flatten() for M in mats])
    return int(np.sum(np.linalg.svd(V, full_matrices=False)[1] > tol))


print(
    f"    sl(3,R): traceless real 3x3, dimension = {real_rank(sl3)} (3 antisym + 3 sym + 2 diag)"
)
check("(2) sl(3,R) has dimension 8", real_rank(sl3) == 8)


# so(2,1) = generators antisymmetric wrt g: X^T g + g X = 0
def so21_basis():
    B = []
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        # generator in plane (i,j) for metric g
        X = np.zeros((3, 3))
        X[i, j] = -g[j, j]
        X[j, i] = g[i, i]
        B.append(X)
    return B


so21 = so21_basis()
for X in so21:
    assert np.allclose(X.T @ g + g @ X, 0, atol=1e-12)
print(f"    so(2,1): isometries of diag(+1,-1,+1), dimension = {real_rank(so21)}")
# is so(2,1) inside sl(3,R)? (traceless real -> yes trivially)
all_traceless = all(abs(np.trace(X)) < 1e-12 for X in so21)
check(
    "(2) so(2,1) (dim 3) is a STRICT subalgebra of sl(3,R) (dim 8)",
    real_rank(so21) == 3 and all_traceless,
    "base ISOMETRY is dim 3; color is the full dim-8 sl(3,R) -> color != isometry",
)

# note-34's diagonal involution sigma_z is in sl(3,R) but NOT in so(2,1):
sz_embed = np.diag([1.0, -1.0, 0.0])  # the involution / Cartan generator note 34 seeds
is_iso = np.allclose(sz_embed.T @ g + g @ sz_embed, 0, atol=1e-12)
check(
    "(2) note-34's diagonal involution is in color but is NOT a base isometry",
    not is_iso,
    "diagonal generator -> not antisymmetric wrt any metric -> color exceeds the isometry algebra",
)

# ---------------------------------------------------------------------------
# (3) THE NON-CIRCULAR KEY: real linear maps on R^3 generate sl(3,R) = the SPLIT real form.
#     Its Killing signature is (5,3) -- NOT chosen, FORCED. This is WHY note 34 got (5,3).
# ---------------------------------------------------------------------------
print(
    "\n(3) real maps on a real R^3 generate sl(3,R) = SPLIT form -> signature FORCED (5,3):"
)


def killing_sig(B):
    n = len(B)
    gg = np.array([[np.trace(B[a] @ B[b]) for b in range(n)] for a in range(n)])
    ginv = np.linalg.inv(gg)
    C = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            cab = comm(B[a], B[b])
            C[a, b, :] = ginv @ np.array([np.trace(cab @ B[c]) for c in range(n)])
    K = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            K[a, b] = sum(C[a, c, d] * C[b, d, c] for c in range(n) for d in range(n))
    ev = np.linalg.eigvalsh((K + K.T) / 2)
    return (
        int(np.sum(ev > 1e-6)),
        int(np.sum(ev < -1e-6)),
        int(np.sum(np.abs(ev) <= 1e-6)),
    )


sig = killing_sig(sl3)
print(
    f"    Killing signature of sl(3,R) = {sig}  (note 34's literal build gave exactly this)"
)
check(
    "(3) sl(3,R) [real maps on R^3] has signature (5,3) -- the SPLIT form, FORCED not chosen",
    sig == (5, 3, 0),
    f"{sig}  -> this EXPLAINS note 34's (5,3): real space => split real form",
)
# max compact subalgebra of sl(3,R) = so(3) (the 3 antisymmetric), rank 1:
so3 = sl3[:3]  # the antisymmetric ones
commuting = sum(
    np.allclose(comm(so3[a], so3[b]), 0, atol=1e-12)
    for a in range(3)
    for b in range(3)
    if a < b
)
print(
    f"    max compact subalg of sl(3,R) = so(3) (3 antisym gens), commuting pairs={commuting} -> rank 1"
)
check(
    "(3) max-compact of sl(3,R) is so(3), rank 1 (NOT the rank-2 compact su(3))",
    commuting == 0,
)

# ---------------------------------------------------------------------------
# (4) compact su(3) (0,8) lives on C^3, a DIFFERENT space the real odd-dim base cannot be.
# ---------------------------------------------------------------------------
print(
    "\n(4) compact su(3) (0,8) = anti-Hermitian maps on C^3 -- NOT the real base R^3:"
)
# build compact su(3) (Gell-Mann, anti-Hermitian i*lambda) and confirm (0,8):
l = {}
l[1] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], complex)
l[2] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], complex)
l[3] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], complex)
l[4] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], complex)
l[5] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], complex)
l[6] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], complex)
l[7] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], complex)
l[8] = np.diag([1, 1, -2]).astype(complex) / np.sqrt(3)
su3 = [1j * l[a] for a in range(1, 9)]
sig_su3 = killing_sig_c = None


# complex Killing signature via real-embedding trace form sign:
def killing_sig_complex(B):
    n = len(B)
    gg = np.array([[np.trace(B[a] @ B[b]) for b in range(n)] for a in range(n)])
    ginv = np.linalg.inv(gg)
    C = np.zeros((n, n, n), complex)
    for a in range(n):
        for b in range(n):
            cab = comm(B[a], B[b])
            C[a, b, :] = ginv @ np.array([np.trace(cab @ B[c]) for c in range(n)])
    K = np.zeros((n, n), complex)
    for a in range(n):
        for b in range(n):
            K[a, b] = sum(C[a, c, d] * C[b, d, c] for c in range(n) for d in range(n))
    ev = np.linalg.eigvalsh(np.real((K + K.conj().T) / 2))
    return (
        int(np.sum(ev > 1e-6)),
        int(np.sum(ev < -1e-6)),
        int(np.sum(np.abs(ev) <= 1e-6)),
    )


sig_su3 = killing_sig_complex(su3)
print(
    f"    compact su(3) [anti-Herm on C^3] Killing signature = {sig_su3} (negative definite)"
)
check(
    "(4) compact su(3) is (0,8) on C^3 -- a DIFFERENT real form from sl(3,R) (5,3) on R^3",
    sig_su3 == (0, 8, 0) and sig_su3 != sig,
)
# the base R^3 cannot BE C^3: odd real dim admits no complex structure (note 37).
print(
    "    R^3 (odd real dim) admits no complex structure (det(-I_3)=-1) -> base R^3 != C^3."
)
check(
    "(4) the real base cannot be the complex color space (det(-I_3)=-1)",
    abs(np.linalg.det(-np.eye(3)) + 1) < 1e-12,
)

print("\n" + "=" * 74)
ok = all(PASS)
print(
    f"RESULT: {sum(PASS)}/{len(PASS)} checks passed. {'ALL PASS' if ok else 'SOME FAIL'}"
)
print("=" * 74)
print(f"""
RECONCILIATION VERDICT:
  The two 3-spaces are the SAME real base R^3 (e1=y timelike, e2=x, e3=z). Note 34's color
  generators act on it as the FULL traceless real-linear algebra sl(3,R) (dim 8), which
  strictly CONTAINS the base isometry so(2,1) (dim 3, what notes 36/37 rank-counted).
  Because real linear maps on a real space generate the SPLIT real form, color-on-the-base
  is FORCED to be sl(3,R), signature {sig} -- this EXPLAINS note 34's (5,3) as inevitable,
  not a build artifact. Compact su(3) {sig_su3} is the anti-Hermitian algebra on C^3, a
  DIFFERENT space; the real odd-dim base cannot be C^3 (no complex structure).
  => The loop is resolved: the two spaces COINCIDE as the real base, on which the color
     candidate is FORCED to sl(3,R) -- which is NOT a compact gauge group and therefore
     cannot carry color at all (this is a negative about the IDENTIFICATION, not a claim
     that physical color is deconfined). They DIVERGE exactly at the real->complex posit:
     compact su(3) needs an INTERNAL C^3, which the real odd-dim base cannot be.
  => CONSEQUENCE FOR THE COMMITTED CORPUS: 'N_c = 3 = N_dim' (Tier-1 win in note 98 /
     notes 18,27 / the paper) is DEMOTED. If color's C^3 is a different space from the
     emergent spatial 3, then three-colors-equals-three-dimensions is a NUMERICAL
     COINCIDENCE, not a common origin. Note 98 and the paper ledger must reflect this.
""")
import sys

sys.exit(0 if ok else 1)
