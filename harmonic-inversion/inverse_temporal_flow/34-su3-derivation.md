# 34 — Does the Emergent Triad Carry $SU(3)$? Closing the Sufficiency

*Note 27 proved color **necessity** — the four generators $\{\lambda_4,\lambda_5,\lambda_6,\lambda_7\}$
plus the second Cartan $\lambda_8$ cannot live in a single $(1{+}1)$ flow plane, so color
**requires** the third emergent dimension — but only **asserted sufficiency** (that the
three emergent axes actually carry $\mathfrak{su}(3)$ with the correct structure
constants). This note closes the sufficiency by explicit construction, and finds the
honest answer: **sufficiency is derived modulo one pre-existing assumption (compactness),
with no fresh knob.** The genuine result is identifying *exactly* what the residual gap
is — the real form, not the structure constants. Reproduced by
`verify/verify_su3-derivation.py` (16/16 checks pass, exit 0).*

---

## The construction (non-circular seed)

Two flow planes share the common time axis $e_1$, acting on $\mathbb C^3=\mathrm{span}\{e_1,e_2,e_3\}$:
plane $A=(e_1,e_2)$, plane $B=(e_1,e_3)$. We seed **only** the framework primitives —
plane $A$'s full triplet $\{$half-boost $\sigma_x$ (note 07), rotor $\sigma_y$ (note 04),
now-involution $\sigma_z$ (note 14)$\}$ and plane $B$'s half-boost and rotor — **five
generators**. We deliberately withhold the canonical $\lambda_6,\lambda_7,\lambda_8$:
the commutators must generate them, or the closure is circular.

## Step 1 — closure to dimension 8, forced

Closing the five seeds under commutators (over the genuine anti-Hermitian real form
$\{i\lambda\}$ — the Hermitian set is *not* closed, since $[\sigma_x,\sigma_y]=2i\sigma_z$
lands on a different real vector) gives a real Lie algebra of **dimension exactly 8**,
with one plane alone closing at dimension 3 ($\mathfrak{su}(2)$, the necessity half of
note 27). The dimension-8 closure is *forced* — any two $SU(2)$ ladder-systems sharing
one index generate the rank-2 algebra $A_2$.

## Step 2 — the second Cartan is forced, not hand-written

The literal plane-$B$ involution $H_2=\mathrm{diag}(1,0,-1)$ is generated, but is **not**
trace-orthogonal to $\lambda_3=\mathrm{diag}(1,-1,0)$: $\mathrm{Tr}(H_2\lambda_3)=1$.
Gram–Schmidt of $H_2$ against $\lambda_3$, normalized to $\mathrm{Tr}=2$, yields
**uniquely**
$$\lambda_8=\tfrac1{\sqrt3}\,\mathrm{diag}(1,1,-2),$$
the canonical eighth generator — derived, not assumed.

## Step 3 — the structure constants match canonically

Building a $\mathrm{Tr}(T_aT_b)=2\delta_{ab}$ basis from the generated matrices
(deriving $\lambda_6,\lambda_7$ from $[\,\sigma_x^A,\sigma_{y,x}^B]$) and computing
$f_{abc}=\tfrac1{4i}\mathrm{Tr}([T_a,T_b]T_c)$, **every** structure constant matches
canonical $\mathfrak{su}(3)$ to machine precision:

| $(a,b,c)$ | canonical | generated | $|{\rm diff}|$ |
|---|---|---|---|
| $(1,2,3)$ | $1$ | $1.000000$ | $0$ |
| $(1,4,7)$ | $\tfrac12$ | $0.500000$ | $0$ |
| $(1,5,6)$ | $-\tfrac12$ | $-0.500000$ | $0$ |
| $(2,4,6)$ | $\tfrac12$ | $0.500000$ | $0$ |
| $(2,5,7)$ | $\tfrac12$ | $0.500000$ | $0$ |
| $(3,4,5)$ | $\tfrac12$ | $0.500000$ | $0$ |
| $(3,6,7)$ | $-\tfrac12$ | $-0.500000$ | $0$ |
| $(4,5,8)$ | $\tfrac{\sqrt3}2$ | $0.866025$ | $0$ |
| $(6,7,8)$ | $\tfrac{\sqrt3}2$ | $0.866025$ | $0$ |

## The two candidate knobs — both closed

**Orientation (relative phase of plane $B$).** A relative phase $\beta$ on axis $e_3$ is
conjugation by $U=\mathrm{diag}(1,1,e^{i\beta})$ — an **inner automorphism**. It rotates
$\lambda_4\leftrightarrow\lambda_5$ but leaves $|f_{abc}|$ invariant (verified to
$2\times10^{-16}$ at $\beta=0.72$). Orientation is *not* a knob.

**Relative normalization (scale of plane $B$).** Scaling plane $B$ by $c$ rescales the
ladders, but the $\mathrm{Tr}=2$ normalization absorbs $c$ exactly — $f_{abc}$ is
scale-invariant after each generator is unit-normalized ($\mathrm{dev}=2\times10^{-16}$
at $c=1$ and $c=1.7$). The framework fixes the unit normalization by **axis democracy**:
both emergent axes carry the *same* $1/\varphi$ boost quantum (note 27's $\mathbb Z_3$
triality). Normalization is *not* a free knob on the bracket.

## The genuine discriminator — and the residual gap

Here is the result that distinguishes this from a circular "dim 8 + $f_{abc}$ match"
exercise. **Dimension 8 and the $|f_{abc}|$ magnitudes do not discriminate compact
$\mathfrak{su}(3)$ (the color algebra, with confined gluons in a *compact* group) from a
non-compact look-alike** — both share the complexification $\mathfrak{sl}(3,\mathbb C)$.
The true discriminator is the **real form**, read off the Killing-form signature:

| build | Killing signature $(n_+,n_-,n_0)$ | real form |
|---|---|---|
| compact $\mathfrak{su}(3)$ ($i\lambda_a$) | $(0,8,0)$ — neg. definite | **color** requires this |
| **literal** flow boosts (real-symmetric $\sigma_x$) | $(5,3,0)$ — indefinite | split $\mathfrak{sl}(3,\mathbb R)$ |

The genuine flow primitives are **non-compact hyperbolic boosts** ($SO(1,1)$), and two of
them sharing a timelike axis close on the **split real form** $\mathfrak{sl}(3,\mathbb R)$
— the form *farthest* from compact $\mathfrak{su}(3)$. Color does not come for free from
the literal boosts: it requires selecting the **compact** form, i.e. the boost$\to$rotor
Wick identification $\theta\to i\theta$ that note 18 §3 *already* invokes to get
$SU(2)_L$. So the residual gap is exactly **one standing assumption (compactness)** —
not a new one, and it carries no free parameter.

## Verdict

**Partial — sufficiency is derived modulo compactness.** Everything except the real form
is *forced*: the dimension-8 closure, the Gram–Schmidt $\lambda_8$, the canonical
$f_{abc}$ (with orientation an inner automorphism and normalization fixed by axis
democracy). The one thing geometry does *not* force is compact-vs-split; and selecting
compact $\mathfrak{su}(3)$ is the *same* Wick rotation already assumed for the
electroweak sector. So note 27's "structurally constrained, not derived" sharpens to:
**the structure constants are derived; only the real form rests on a pre-existing
(not fresh) assumption.** That is a genuine advance — the assumption is now named
precisely and shown to introduce no new knob, and $N_c=3=N_{\rm dim}$ stands as one fact.

**Falsifier:** if the framework's $1/\varphi$ boost quantum could be shown to force the
*compact* form intrinsically (a reason the chronon flow must Wick-rotate boosts to rotors
in the color sector, not merely the electroweak one), sufficiency would be fully derived.
Conversely, if the split form $\mathfrak{sl}(3,\mathbb R)$ were the physical one, color
would be non-compact (deconfined) — contradicting QCD, which is itself the evidence that
the compactness assumption is correct.

**Update (note 36): the compactness IS an assumption, now localized to a rank deficit.**
Asking whether the chronon flow must compactify boosts to rotors gives a *split* verdict.
The manifold is $S^1\times\mathbb R$ — a compact spatial circle (the closed base curve)
and the non-compact boost line (the Matryoshka nesting). For $U(1)$ charge, compactness
is **forced** (charge is a winding on the closed curve, topology quantizes it). For
$SU(3)$ it is **not**: $SU(3)$ is rank 2, but the base curve supplies exactly *one*
independent spatial circle ($y=xz$ is slaved, and no two coordinate rotors commute), so
the maximal spatial compact torus is rank 1. The rank-2 torus this section's two planes
provided came from *sharing the time axis* $e_1$ — i.e. boost planes, which is why the
literal build gave $\mathfrak{sl}(3,\mathbb R)$ $(5,3)$. So "derived modulo compactness"
sharpens to: the compactness assumption is exactly the missing second commuting compact
circulation, and it is not in the base geometry. See note 36.
