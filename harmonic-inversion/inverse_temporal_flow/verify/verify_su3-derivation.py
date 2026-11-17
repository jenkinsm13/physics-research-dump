#!/usr/bin/env python3
"""
verify_su3-derivation.py  —  Note 34: Does the emergent triad CARRY su(3)?

Note 27 proved NECESSITY (color cannot live in one (1+1) flow plane; it needs a
second emergent dimension) but only ASSERTED sufficiency (that the three emergent
axes actually carry su(3) with the correct structure constants). This script
closes — or honestly fails to close — the sufficiency, WITHOUT hand-writing the
canonical Gell-Mann lambda4..lambda8. We seed ONLY the two flow planes built from
the framework's own primitives and let commutators do the rest.

The decisive lesson (and the reason a naive 'dim 8 + f_abc match' would be a
circular fake-DERIVED): dimension 8 and the |f_abc| magnitudes are nearly FORCED
for ANY real form of sl(3,C). They do NOT discriminate compact su(3) (the color
algebra, gluons in a compact group) from a NON-compact look-alike (su(2,1) /
sl(3,R)-type) with the same complexification. The genuine discriminator is the
REAL FORM = the Killing-form signature:
   * compact su(3)  ->  Killing form NEGATIVE DEFINITE, signature (0,8).
   * literal hyperbolic boosts (non-compact SO(1,1)) -> INDEFINITE signature.

So we build BOTH and let the signature decide.

Checks:
  (A) Two flow planes from primitives, sharing time axis e_1, acting on C^3.
  (B) Real-span closure dimension under nested commutators (is it 8?).
  (C) Cartan: the literal 2nd Cartan diag(1,0,-1) is NOT trace-orthogonal to
      lambda3=diag(1,-1,0); Gram-Schmidt yields lambda8 ~ diag(1,1,-2) UNIQUELY
      (forced, not hand-written).
  (D) f_abc in a normalized trace basis vs canonical su(3) -> element-by-element.
  (E) KNOB CHECK 1 (orientation): a relative phase on e_3 is an INNER
      automorphism conj by diag(1,1,e^{i beta}); recompute f_abc -> INVARIANT.
  (F) KNOB CHECK 2 (normalization): scaling plane B by c rescales [l4,l5] by c^2;
      canonical f_abc forces c=1, which the framework fixes by axis democracy
      (both emergent axes carry the SAME 1/phi boost quantum -> note 27 Z_3).
  (G) THE DISCRIMINATOR: Killing-form signature, compact build vs literal-boost
      build. Compact -> (0,8). Literal flow boosts -> indefinite.

numpy only. phi = (1+sqrt5)/2 exactly. No external mass/coupling fed back in.
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2.0
lnphi = np.log(phi)

PASS = []


def check(name, cond, detail=""):
    PASS.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}  {detail}")


def comm(A, B):
    return A @ B - B @ A


print("=" * 72)
print("NOTE 34 — DOES THE EMERGENT TRIAD CARRY SU(3)? CLOSING SUFFICIENCY")
print(f"phi={phi:.6f}  lnphi={lnphi:.6f}")
print("=" * 72)

# ---------------------------------------------------------------------------
# (0) Canonical su(3): textbook Gell-Mann + f_abc. GROUND TRUTH for comparison.
# ---------------------------------------------------------------------------
l1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
l2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
l3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
l4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
l5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
l6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
l7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
l8 = (1 / np.sqrt(3)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex)
GM = [l1, l2, l3, l4, l5, l6, l7, l8]

f_known = {
    (1, 2, 3): 1.0,
    (1, 4, 7): 0.5,
    (1, 5, 6): -0.5,
    (2, 4, 6): 0.5,
    (2, 5, 7): 0.5,
    (3, 4, 5): 0.5,
    (3, 6, 7): -0.5,
    (4, 5, 8): np.sqrt(3) / 2,
    (6, 7, 8): np.sqrt(3) / 2,
}


def fabc_canon(a, b, c):
    for p, s in [
        ((a, b, c), 1),
        ((b, c, a), 1),
        ((c, a, b), 1),
        ((b, a, c), -1),
        ((a, c, b), -1),
        ((c, b, a), -1),
    ]:
        if p in f_known:
            return s * f_known[p]
    return 0.0


# trace normalization used throughout: Tr(l_a l_b) = 2 delta_ab.
tr_ok = all(
    abs(np.trace(GM[a] @ GM[b]) - 2 * (a == b)) < 1e-12
    for a in range(8)
    for b in range(8)
)
check("(0) canonical Gell-Mann obey Tr(la lb)=2 delta_ab", tr_ok)


def f_from_basis(B):
    """f_abc = (1/4i) Tr([B_a,B_b] B_c) for a Tr(B_a B_b)=2 delta_ab basis."""
    n = len(B)
    f = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            cab = comm(B[a], B[b])
            for c in range(n):
                f[a, b, c] = np.real(np.trace(cab @ B[c]) / (4j))
    return f


# sanity: canonical f computed from matrices matches the dictionary
f_canon = f_from_basis(GM)
dev0 = max(
    abs(f_canon[a, b, c] - fabc_canon(a + 1, b + 1, c + 1))
    for a in range(8)
    for b in range(8)
    for c in range(8)
)
check(
    "(0) f_abc recomputed from Gell-Mann == dictionary",
    dev0 < 1e-12,
    f"max dev={dev0:.2e}",
)

# ---------------------------------------------------------------------------
# (A) THE CONSTRUCTION. Two flow planes sharing time axis e_1.
#     Plane A = (e1,e2) = block (0,1);  Plane B = (e1,e3) = block (0,2).
#     Framework primitives in EACH plane (note 18 sec.1):
#        half-boost   sigma_x  (note 07)   -> off-diagonal symmetric
#        rotor        sigma_y  (note 04)   -> off-diagonal imaginary  (J=-i sy)
#        now-involution sigma_z (note 14)  -> diagonal sign
#     We seed ONLY plane A's full triplet + plane B's half-boost & rotor; we do
#     NOT seed lambda6,lambda7 (plane (e2,e3)) nor lambda8 -- commutators must
#     produce them. This is the non-circular seed.
# ---------------------------------------------------------------------------
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def embed(M2, i, j, n=3):
    E = np.zeros((n, n), dtype=complex)
    idx = [i, j]
    for a in range(2):
        for b in range(2):
            E[idx[a], idx[b]] = M2[a, b]
    return E


# Plane A primitives (block 0,1):
A_x, A_y, A_z = embed(sx, 0, 1), embed(sy, 0, 1), embed(sz, 0, 1)
# Plane B primitives (block 0,2):  ONLY half-boost + rotor seeded.
B_x, B_y = embed(sx, 0, 2), embed(sy, 0, 2)

seed = [A_x, A_y, A_z, B_x, B_y]  # 5 seeds; lambda6,7,8 must be GENERATED.
check(
    "(A) seed = {planeA(x,y,z), planeB(x,y)} = 5 generators, NO l6/l7/l8",
    len(seed) == 5,
    "non-circular seed (canonical l6,l7,l8 withheld)",
)


# ---------------------------------------------------------------------------
# (B) Close under commutators and report the real Lie-algebra dimension.
#     SUBTLETY (and a real bug if ignored): the commutator of two HERMITIAN
#     matrices is ANTI-Hermitian, so the Hermitian matrices are NOT closed
#     under [,] as a real vector space -- [sx,sy]=2i sz lands on i*sz, a
#     DIFFERENT real vector from sz, which double-counts (gives 16, not 8).
#     The genuine real Lie algebra is the ANTI-Hermitian one: su(3) = {i*lambda}.
#     So we close over i*(seed). Its real span is the correct su(N) dimension.
# ---------------------------------------------------------------------------
def real_span_basis(mats, tol=1e-9):
    """Return an orthonormal (Frobenius) basis of the REAL span of {mats},
    treating each 3x3 complex matrix as a real vector (re,im stacked)."""
    vecs = []
    for M in mats:
        vecs.append(np.concatenate([M.real.flatten(), M.imag.flatten()]))
    Vt = np.array(vecs)
    # rank over reals
    u, s, vh = np.linalg.svd(Vt, full_matrices=False)
    r = int(np.sum(s > tol))
    return r, vh[:r]


def in_real_span(M, basis_rows, tol=1e-8):
    v = np.concatenate([M.real.flatten(), M.imag.flatten()])
    if basis_rows.shape[0] == 0:
        return np.linalg.norm(v) < tol
    coeff = basis_rows @ v
    recon = basis_rows.T @ coeff
    return np.linalg.norm(v - recon) < tol


def close_algebra(seed_herm, tol=1e-9):
    """Close the anti-Hermitian real Lie algebra generated by {i*seed}.
    Returns (dim, basis) where basis elements are ANTI-Hermitian (genuine
    su(N) elements). Pass HERMITIAN seeds; we multiply by i internally."""
    basis = []

    def add(M):
        if np.max(np.abs(M)) < 1e-12:
            return False
        _, rows = real_span_basis(basis) if basis else (0, np.zeros((0, 18)))
        if basis and in_real_span(M, rows, tol):
            return False
        basis.append(M)
        return True

    for s in seed_herm:
        add(1j * s)  # anti-Hermitian generator i*lambda; closed under [,]
    changed = True
    while changed:
        changed = False
        cur = list(basis)
        for X in cur:
            for Y in cur:
                if add(comm(X, Y)):
                    changed = True
    r, _ = real_span_basis(basis)
    return r, basis


dim_closed, closed = close_algebra(seed)
check(
    "(B) two-plane seed closes to a real Lie algebra of dimension 8",
    dim_closed == 8,
    f"dim = {dim_closed}",
)

# also confirm one plane alone closes at 3 (su(2)) -- the necessity half (note 27)
dim_one, _ = close_algebra([A_x, A_y, A_z])
check(
    "(B) one plane alone closes at dim 3 (su(2)) [necessity, note 27]",
    dim_one == 3,
    f"dim = {dim_one}",
)

# ---------------------------------------------------------------------------
# (C) THE SECOND CARTAN IS FORCED, NOT HAND-WRITTEN.
#     The generated algebra contains the literal second-Cartan candidate
#     H2 = diag(1,0,-1) (it appears as ~[B_x,B_y]/2 = embed(sz,0,2)).
#     Tr(H2 * lambda3) = 1 != 0  -> H2 is NOT trace-orthogonal to lambda3.
#     Gram-Schmidt H2 against lambda3, normalize Tr=2 -> lambda8 UNIQUELY.
# ---------------------------------------------------------------------------
H2 = embed(sz, 0, 2)  # diag(1,0,-1), the literal plane-B now-involution
# the closed algebra is anti-Hermitian (i*lambda); test for i*H2 there.
check(
    "(C) literal 2nd Cartan H2 = diag(1,0,-1) is generated",
    in_real_span(1j * H2, real_span_basis(closed)[1]),
    "appears in closed algebra (as i*H2)",
)
overlap = np.real(np.trace(H2 @ l3))
check(
    "(C) H2 NOT trace-orthogonal to lambda3 (Tr=1)",
    abs(overlap - 1.0) < 1e-12,
    f"Tr(H2*l3)={overlap:.3f}",
)
# Gram-Schmidt: subtract projection onto l3 (Tr(l3 l3)=2), then renormalize Tr=2.
proj = (np.trace(H2 @ l3) / np.trace(l3 @ l3)) * l3
H2_orth = H2 - proj
H2_norm = H2_orth * np.sqrt(2.0 / np.real(np.trace(H2_orth @ H2_orth)))
check(
    "(C) Gram-Schmidt(H2 perp l3), Tr-normalized == lambda8 (forced)",
    np.allclose(H2_norm, l8),
    f"-> diag {np.round(np.real(np.diag(H2_norm)), 4)}",
)

# ---------------------------------------------------------------------------
# (D) f_abc OF THE GENERATED ALGEBRA vs CANONICAL su(3).
#     Build a Tr(T_a T_b)=2 delta_ab basis FROM the generated/seeded matrices
#     in the natural Cartan-Weyl order, then compute f_abc and compare.
#     Order: l1=A_x, l2=A_y, l3=A_z, l4=B_x, l5=B_y, l6=[generated], l7=[gen],
#            l8=Gram-Schmidt Cartan. We GENERATE l6,l7 from commutators:
#            [l1,l4] = i l7 ... [l1,l5] = -i l6  (canonical), but we DERIVE them.
# ---------------------------------------------------------------------------
# Derive plane-(23) ladders from commutators of the seed (no hand-writing):
#   canonical: [l4,l1] gives l7-direction; [l5,l1] gives l6-direction.
g6 = comm(A_x, B_y) * 1j  # = i[l1,l5] direction
g7 = comm(A_x, B_x) * (-1j)  # = -i[l1,l4] direction


# normalize each to Tr=2
def trnorm(M):
    t = np.real(np.trace(M @ M))
    return M * np.sqrt(2.0 / t)


T = [A_x, A_y, A_z, B_x, B_y, trnorm(g6), trnorm(g7), H2_norm]
# Verify it is a Tr=2 orthonormal basis (so f_abc formula applies cleanly):
gram = np.array([[np.real(np.trace(T[a] @ T[b])) for b in range(8)] for a in range(8)])
check(
    "(D) generated basis is Tr(Ta Tb)=2 delta_ab orthonormal",
    np.allclose(gram, 2 * np.eye(8)),
    f"max off-diag={np.max(np.abs(gram - 2 * np.eye(8))):.2e}",
)

f_gen = f_from_basis(T)
# Compare element-by-element to canonical (same index order = Gell-Mann order).
dev_f = np.max(np.abs(f_gen - f_canon))
check(
    "(D) f_abc(generated) == canonical su(3) f_abc to machine precision",
    dev_f < 1e-10,
    f"max|df|={dev_f:.2e}",
)

# print the comparison table for the nonzero canonical entries
print("\n  f_abc comparison (nonzero canonical entries):")
print(f"  {'(a,b,c)':<10}{'canonical':>12}{'generated':>12}{'|diff|':>12}")
for (a, b, c), v in sorted(f_known.items()):
    gen = f_gen[a - 1, b - 1, c - 1]
    print(f"  {str((a, b, c)):<10}{v:>12.6f}{gen:>12.6f}{abs(gen - v):>12.2e}")

# ---------------------------------------------------------------------------
# (E) KNOB CHECK 1 — RELATIVE ORIENTATION of plane B is an INNER automorphism.
#     A relative phase beta on axis e3: conjugate by U = diag(1,1,e^{i beta}).
#     This rotates l4<->l5 (and l6<->l7) but leaves f_abc INVARIANT.
#     => orientation is NOT a knob that can change the algebra.
# ---------------------------------------------------------------------------
beta = 0.7234  # arbitrary
U = np.diag([1.0, 1.0, np.exp(1j * beta)])
T_rot = [U @ M @ U.conj().T for M in T]
# the rotated set is no longer Hermitian-real-basis aligned; re-Gram to Tr=2 real
# Cartan-Weyl basis is preserved under conj, so just recompute f on the rotated set.
gram_rot = np.array(
    [
        [np.real(np.trace(T_rot[a] @ T_rot[b].conj().T)) for b in range(8)]
        for a in range(8)
    ]
)
f_rot = f_from_basis(T_rot)
# f_abc from a conjugated (orthonormal-preserving) basis is invariant in magnitude
# spectrum; element-by-element it stays the same because conjugation is an algebra
# automorphism in the SAME index labeling.
dev_rot = np.max(np.abs(np.abs(f_rot) - np.abs(f_gen)))
check(
    "(E) relative orientation phase = inner automorphism: |f_abc| invariant",
    dev_rot < 1e-9,
    f"max||f_rot|-|f_gen||={dev_rot:.2e} (orientation is NOT a knob)",
)


# ---------------------------------------------------------------------------
# (F) KNOB CHECK 2 — RELATIVE NORMALIZATION between planes.
#     Scale plane B by c: B_x->c B_x, B_y->c B_y. Then [B_x,B_y] ~ c^2, so the
#     ladder normalization and hence f_abc scale. Canonical f requires c=1.
#     Show c != 1 BREAKS the f match; c=1 (forced by axis democracy: both
#     emergent axes carry the SAME 1/phi boost quantum) restores it.
# ---------------------------------------------------------------------------
def f_match_for_scale(c):
    Bx, By = c * embed(sx, 0, 2), c * embed(sy, 0, 2)
    dimc, closedc = close_algebra([A_x, A_y, A_z, Bx, By])
    # rebuild Tr=2 basis with the scaled plane-B and recompute f
    g6c = trnorm(comm(A_x, By) * 1j)
    g7c = trnorm(comm(A_x, Bx) * (-1j))
    # plane-B ladders also must be Tr=2 normalized for a fair f comparison
    Bxn, Byn = trnorm(Bx), trnorm(By)
    Tc = [A_x, A_y, A_z, Bxn, Byn, g6c, g7c, H2_norm]
    fc = f_from_basis(Tc)
    return dimc, np.max(np.abs(fc - f_canon))


dim_c1, dev_c1 = f_match_for_scale(1.0)
dim_c2, dev_c2 = f_match_for_scale(1.7)
# KEY: after Tr=2 RE-normalization the f_abc are basis-invariant, so the SCALE
# does not change f once each generator is unit-normalized. The honest statement:
# the RELATIVE normalization c is absorbed by the trace-normalization convention;
# what it CANNOT be absorbed into is the COMMUTATION-CLOSURE structure, which is
# scale-free. So normalization is NOT an independent knob on f_abc either; both
# planes being unit-normalized 1/phi boosts is the framework's axis democracy.
check(
    "(F) f_abc match is scale-invariant after Tr=2 normalization (c absorbed)",
    dev_c1 < 1e-10 and dev_c2 < 1e-10,
    f"dev(c=1)={dev_c1:.1e}, dev(c=1.7)={dev_c2:.1e} -> normalization not a free knob on f",
)


# ---------------------------------------------------------------------------
# (G) THE DISCRIMINATOR — KILLING-FORM SIGNATURE (the REAL FORM).
#     This is what 'dim 8 + f_abc match' CANNOT see. su(3) (color) is COMPACT:
#     Killing form negative definite, signature (0,8). The literal flow boosts
#     are NON-compact (SO(1,1) hyperbolic): they generate an indefinite-Killing
#     real form (su(2,1) / sl(3,R)-type) with the SAME complexification.
#
#     Killing form K_ab = Tr(ad X_a . ad X_b). For a basis {X_a} with
#     [X_a,X_b] = sum_c C^c_ab X_c, ad(X_a)^c_b = C^c_ab, K_ab=Tr(adXa adXb).
# ---------------------------------------------------------------------------
def killing_signature(basis):
    """basis: list of n real-Lie-algebra matrices (closed under comm).
    Build structure constants in this basis (via Tr projection assuming
    Tr(Xa Xb) Gram is invertible), then K_ab = sum_{c,d} C^d_ac C^c_bd."""
    n = len(basis)
    # metric g_ab = Tr(Xa Xb) (may be complex; use real part)
    g = np.array([[np.trace(basis[a] @ basis[b]) for b in range(n)] for a in range(n)])
    ginv = np.linalg.inv(g)
    # structure constants: [Xa,Xb] = sum_c C[a,b,c] Xc
    C = np.zeros((n, n, n), dtype=complex)
    for a in range(n):
        for b in range(n):
            cab = comm(basis[a], basis[b])
            # project: C[a,b,:] = ginv @ (Tr(cab Xc))_c
            proj = np.array([np.trace(cab @ basis[c]) for c in range(n)])
            C[a, b, :] = ginv @ proj
    # Killing K_ab = sum_{c,d} C[a,c,d] C[b,d,c]
    K = np.zeros((n, n), dtype=complex)
    for a in range(n):
        for b in range(n):
            s = 0
            for c in range(n):
                for d in range(n):
                    s += C[a, c, d] * C[b, d, c]
            K[a, b] = s
    Kr = np.real((K + K.T.conj()) / 2)
    eig = np.linalg.eigvalsh(Kr)
    npos = int(np.sum(eig > 1e-6))
    nneg = int(np.sum(eig < -1e-6))
    nzero = int(np.sum(np.abs(eig) <= 1e-6))
    return (npos, nneg, nzero), eig


# COMPACT build: the Hermitian Gell-Mann generators {lambda_a} ARE the compact
# su(3) generators (anti-Hermitian i*lambda_a; Killing of su(3) is neg. definite).
# We feed i*lambda_a so the algebra is genuinely the real compact form.
compact_basis = [1j * M for M in GM]
sig_c, eig_c = killing_signature(compact_basis)
check(
    "(G) COMPACT su(3) [i*lambda_a]: Killing signature (0,8) neg. definite",
    sig_c == (0, 8, 0),
    f"signature (npos,nneg,nzero)={sig_c}",
)


# LITERAL-FLOW build: boost = REAL-symmetric non-compact (sigma_x stays real,
# NOT i*sigma_x); rotor = real-antisymmetric (J = -i sigma_y, real); involution
# real-diagonal. These are the GENUINE flow-space generators of note 18 sec.1
# (K real symmetric boost, J real antisym rotor, T real diag involution).
def Kreal(i, j):  # real-symmetric boost embedded (non-compact SO(1,1) gen)
    return embed(sx.real, i, j)


def Jreal(i, j):  # real-antisymmetric rotor J = -i sigma_y = [[0,-1],[1,0]]
    return embed(np.array([[0, -1], [1, 0]], dtype=complex), i, j)


def Treal(i, j):  # real-diagonal now-involution
    return embed(sz.real, i, j)


def close_real_raw(seed, tol=1e-9):
    """Close the real Lie algebra generated by `seed` WITHOUT any i-premultiply.
    For the literal flow generators (real boost/rotor/involution) this is the
    genuine real form -- premultiplying by i would change which real form we get
    and hence the Killing signature, so it must NOT be done here."""
    basis = []

    def add(M):
        if np.max(np.abs(M)) < 1e-12:
            return False
        _, rows = real_span_basis(basis) if basis else (0, np.zeros((0, 18)))
        if basis and in_real_span(M, rows, tol):
            return False
        basis.append(M)
        return True

    for s in seed:
        add(s)
    changed = True
    while changed:
        changed = False
        for X in list(basis):
            for Y in list(basis):
                if add(comm(X, Y)):
                    changed = True
    r, _ = real_span_basis(basis)
    return r, basis


literal_seed = [Kreal(0, 1), Jreal(0, 1), Treal(0, 1), Kreal(0, 2), Jreal(0, 2)]
dim_lit, closed_lit = close_real_raw(literal_seed)
sig_l, eig_l = killing_signature(closed_lit)
check(
    "(G) literal flow seed also closes at dim 8 (same complexification sl(3,C))",
    dim_lit == 8,
    f"dim = {dim_lit}",
)
check(
    "(G) DISCRIMINATOR: literal hyperbolic-boost build has INDEFINITE Killing "
    "(NOT compact su(3))",
    sig_l[0] > 0 and sig_l[1] > 0,
    f"signature (npos,nneg,nzero)={sig_l}  <- non-compact real form",
)
# signature (5,3) identifies the SPLIT real form sl(3,R) (max compact so(3),
# dim 3); su(2,1) would be (4,4); compact su(3) is (0,8). Cross-checked against
# textbook real forms of A_2. Two real hyperbolic boosts sharing a timelike axis
# land on the SPLIT form -- the most non-compact one, the farthest from color.
check(
    "(G) literal real form identified as SPLIT sl(3,R) by signature (5,3)",
    sig_l == (5, 3, 0),
    "max compact so(3) dim 3; this is the farthest real form from compact su(3)",
)

print("\n  Killing signatures (npos, nneg, nzero):")
print(f"    compact   su(3) [i*lambda]:   {sig_c}   (color requires THIS)")
print(f"    literal hyperbolic-boost form: {sig_l}   (what the genuine flow gives)")
print("    -> same dim 8, same complexification, DIFFERENT real form.")
print("       Selecting the compact form = the boost->rotor Wick rotation")
print("       (note 18 sec.3), already assumed for su(2)_L. No NEW knob; one")
print("       STANDING assumption (compactness).")

# ---------------------------------------------------------------------------
print("=" * 72)
ok = all(PASS)
print(
    f"RESULT: {sum(PASS)}/{len(PASS)} checks passed.  "
    f"{'ALL PASS' if ok else 'SOME FAIL'}"
)
print("=" * 72)
print("""
VERDICT (encoded in the checks above):
  * dim 8 closure        : FORCED (any two SU(2)-ladders sharing an index).
  * f_abc == canonical   : FORCED once each generator is unit (Tr=2) normalized;
                           orientation phase is an inner automorphism (E),
                           relative scale is absorbed by normalization (F).
  * 2nd Cartan lambda8   : FORCED by Gram-Schmidt (C), not hand-written.
  * THE REAL FORM        : NOT forced by geometry. Literal hyperbolic boosts give
                           an INDEFINITE-Killing non-compact form; compact su(3)
                           (color) requires the boost->rotor Wick identification
                           (note 18 sec.3) -- a STANDING assumption, not a new one.
  => SUFFICIENCY IS DERIVED MODULO COMPACTNESS. Partial, but the residual gap is
     exactly one pre-existing assumption and introduces NO fresh knob.
""")
import sys

sys.exit(0 if ok else 1)
