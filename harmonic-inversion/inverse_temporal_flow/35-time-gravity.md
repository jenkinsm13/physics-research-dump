# 35 — Time and Gravity: One Force, Opposing Directions

*Michael's thesis: time-flow and gravity are not two phenomena but **one force pointing
two opposite ways**. The spine (note 00) already said "gravity *is* inverse temporal
flow"; this note sharpens that from an identity-of-substance into an identity-of-force:
they are the two opposite-sign eigendirections of a single generator — the boost $K$,
at the fixed rate $1/\varphi$ per shell. Core identities verified to machine precision
in `verify/verify_time-gravity.py` (exit 0).*

---

## The claim, made precise

In flow-space the chronon worldline is driven by **one** generator,
$$\partial_k\mathbf V=\frac1\varphi K\,\mathbf V,\qquad K=\begin{pmatrix}0&-1\\-1&0\end{pmatrix},\qquad K^2=I.$$
$K$ has eigenvalues $\boxed{+1\ \text{and}\ -1}$ — **equal magnitude, opposite sign**.
That single fact is the whole thesis in the algebra: there is one force quantum,
$1/\varphi$ per shell, and it acts with $+$ along one null direction and $-$ along the
other. "The same force in opposing directions" is not a metaphor here; it is the
spectrum of $K$.

## The two directions are time and gravity

Diagonalize $K$ on its null (light-cone) eigenrays. The chronon two-vector
$\mathbf V=(\cosh\theta,-\sinh\theta)$ decomposes exactly into them:
$$\underbrace{\;G(\theta)\equiv V_0-V_1=e^{+\theta}\;}_{\text{gravity ray, }K\text{-eigenvalue }+1}
\qquad\qquad
\underbrace{\;T(\theta)\equiv V_0+V_1=e^{-\theta}\;}_{\text{time ray, }K\text{-eigenvalue }-1}.$$

- The **time ray** $T=e^{-\theta}$ **decays** with depth — the retarded branch, the
  arrow of time, entropy production (notes 00, 05). It is the $-1$ eigendirection: the
  force pointing *forward/outward*.
- The **gravity ray** $G=e^{+\theta}$ **grows** toward the source — the advanced branch,
  attraction (notes 00, 03). It is the $+1$ eigendirection: the *same* force pointing
  *backward/inward*.

One generator. Two signs. Forward flow and inward pull are the two faces of $K$.

## The reciprocal trade-off law (the heart of it)

Because the two eigenvalues are exactly $\pm1$, the two rays are reciprocal:
$$\boxed{\;T(\theta)\cdot G(\theta)=e^{-\theta}\,e^{+\theta}=1=L_y\quad\text{identically.}\;}$$
**Time $\times$ gravity is the conserved unit.** This is the force-level reading of the
spine's $L_y=1$: whatever the worldline spends on the time ray it must recover on the
gravity ray, and vice versa. Where time flows fast ($T$ large, shallow), gravity is weak
($G$ small); descend a shell and the boost trades $1/\varphi$ of time-rate for $1/\varphi$
of gravity-rate, the product pinned at unity. **Gravitating is slowing time, exactly —
the same conserved quantity moving from one ray to the other.** (This is the $G_{\rm sym}^2-G_{\rm flow}^2=\mathrm{osc}^2$
invariant of note 10, read on the bare null amplitudes.)

## The imbalance is the force; the now is balance

The *net* chronogravitational pull is the asymmetry between the two rays,
$$\mathcal F(\theta)=G-T=e^{+\theta}-e^{-\theta}=2\sinh\theta,$$
which is exactly (twice) the flow component $G_{\rm flow}=-\osc\sinh\theta$. It vanishes
**only** at $\theta=0$ — the now-surface, the time-reversal fixed point (note 14) — where
$G=T=1$: equal time and gravity, *zero net force*. Move off the now and the imbalance
grows as $2\sinh\theta$: shallow shells are time-dominated ($T>G$, the future streams
forward), deep shells are gravity-dominated ($G>T$, the well pulls in). The **boost
velocity**
$$\beta(\theta)=\frac{G-T}{G+T}=\tanh\theta$$
measures how far the balance has tipped: $\beta(0)=0$ (pure now, no gravity), one shell
down $\beta=\tanh(1/\varphi)=0.5498$ (the note-15 LIGO ringdown ratio $0.548$), and
$\beta\to1$ at the horizon, where gravity wins completely and **time freezes** ($T\to0$).
The event horizon is simply where the force has rotated entirely onto the gravity ray.

## What this buys us

Michael's framing is correct and it tightens the whole structure. We had "gravity is
inverse temporal flow" as a *statement about what gravity is*. Now it is a *conservation
law about a single force*:

> One generator $K$ (rate $1/\varphi$), eigenvalues $\pm1$. Its $-1$ ray is forward time
> ($e^{-\theta}$, decaying); its $+1$ ray is gravity ($e^{+\theta}$, growing). Their
> product is the conserved unit $L_y=1$, so time-rate and gravity-strength trade
> one-for-one; their difference $2\sinh\theta$ is the net force, zero at the now and
> saturating at the horizon. Gravity and the arrow of time are the two signs of one boost.

## Threads, with their audited verdicts (sibling notes 35a–35d)

Each thread was developed and then adversarially audited for overclaimed agreement with
established physics. The honest scorecard:

**35a — Chronogravitational potential. (PASS, exact.)** The single force *does* descend
from one scalar potential: $U(\theta)=-2\cosh\theta$, $\mathcal F=-U'=2\sinh\theta$ to
machine precision, and the two null rays $e^{\pm\theta}$ are exactly the $\pm1$
eigenfunctions of $d/d\theta$ — "two opposite gradients of one potential," literally.
$U''(0)=-2$: the now is an *unstable maximum* (the force points away toward the horizon).
New invariant $U^2-\mathcal F^2=4L_y=4$ — the reciprocal law as a fixed hyperbola, i.e.
the Lorentz $\gamma$ relation $1-\beta^2=\mathrm{sech}^2\theta$ in disguise. ($V_{\rm grav}$
of note 16 is the osc-dressed *gradient* $-\tfrac12U'\propto\sinh$, not $U$ itself.)

**35b — Equivalence principle. (HONEST PASS, with two named assumptions.)** The weak-field
limit *does* recover GR's time dilation — $T=e^{-\theta}\approx1-\theta$ matches
$1-\Phi_N$ with rapidity $=$ Newtonian potential. But the audit is decisive on what this
means: the recovery is **map-independent** (any slope-1 map $\theta=\Phi+c\Phi^2+\dots$
cancels the linear term, for *every* $c$), so passing GPS/Pound–Rebka is *not* evidence
for the framework over GR — it shows the framework *contains* GR's weak field, as a
unification must. The strong-field deviation ($-23.9\%$ on a neutron-star redshift,
$z=0.221$ vs GR's $0.291$) is a genuine falsifier but is the signature of **one declared
choice** $c=0$; an all-orders re-summation $\theta=-\tfrac12\ln(1-2\Phi)$ lands *exactly*
on GR. Deeper still: $\theta_{EP}=\Phi_N$ is a *posited* identification, **not** the
spine's per-shell rapidity $\theta=k/\varphi$ (they differ by a factor of hundreds — one
shell is $\theta=0.618$, but the horizon is at $n_H\approx183$ shells). So: EP recovered
in the limit, deviation quantified, both resting on a stated map — not a forced fit, and
the assumptions are now visible.

**35c — Anti-gravity. (SPLIT: identity solid, cosmology demoted.)** Repulsion *is* the
$\theta<0$ branch (time ray dominant) — the exact CPT-like reflection of attraction across
the now, $\theta\to-\theta$ swapping $T\leftrightarrow G$, with $K$'s spectrum unchanged at
$\pm1$. The reciprocal law $T\cdot G=1$ *permits* repulsion but *forbids gravity
shielding*: suppressing $G\to\epsilon$ forces the clock $T=1/G\to\infty$ at cost
$C\sim1/G$ (unbounded) — no free anti-gravity. The cosmic-acceleration link, however, was
a **phase knob** (the sign of $1+w_0$ flips quintessence↔phantom within $\Delta N\sim1.3$
shells of the convention) and was retracted; only the sign-free amplitude bound
$|1+w_0|\le1/N_\star$ survives.

**35d — Thermodynamic arrow. (INTERNAL THEOREM, not a derivation of the arrow.)** The
arrow ($\mathrm{sign}\,\sigma$) and gravity ($\mathrm{sign}\,\mathcal F$) share
$\mathrm{sign}\,\theta$ because *both* come from the one generator $K$:
$\sigma/\mathcal F=\osc/2\in[\tfrac14,\tfrac12]>0$, so they **cannot be chosen
independently** — a genuine self-consistency theorem (non-vacuous only because the golden
lattice has $\inf_k\osc=\tfrac12>0$). But the framework does **not** derive *which* side
the universe occupies — that remains a low-entropy-boundary *input* (the Penrose past
hypothesis), exactly the mainstream position. The "find forward-time + repulsive-gravity"
falsifier was an unfalsifiable tautology and was reframed.

**Net.** The thesis is *mathematically exact* where it is internal (35a, the $\pm1$
spectrum, $T\cdot G=1$, the single potential) and *honestly limited* where it touches
established physics: it contains GR's weak field (35b), permits but bounds repulsion
(35c), and locks the arrow to gravity's sign without selecting the arrow (35d). One force,
two signs, is the right picture — and the audit makes its reach and its assumptions
precise rather than letting either run loose.
