# 35d — The Thermodynamic Arrow: Why the Universe Sits on the Time-Ray Side

*Branch of note 35. The spine there gave us one generator $K$ (rate $1/\varphi$ per shell),
eigenvalues exactly $\pm1$, and its two null eigenrays — the **time ray** $T(\theta)=e^{-\theta}$
($K$-eigenvalue $-1$, decaying) and the **gravity ray** $G(\theta)=e^{+\theta}$ ($K$-eigenvalue
$+1$, growing) — locked by the reciprocal law $T\cdot G=1=L_y$, with net force
$\mathcal F=G-T=2\sinh\theta$ and boost velocity $\beta=\tanh\theta$, $\theta=k/\varphi$. This note
asks the open thread 35d: **is the second law just the statement that the observable universe sits
on the $T$-dominant ($+\theta$) side of the now, and does that make the arrow of time and the
attractiveness of gravity the SAME selection?** The honest answer, sharpened below: the two are
**not independently choosable** — they share $\operatorname{sign}\theta$ as an exact *internal
theorem* — but the arrow *itself* (which side) is an **input**, not a derivation, and the sign-lock
is a self-consistency statement, not an empirical falsifier. Every number below is confirmed at
machine precision in `verify/verify_thermodynamic-arrow.py` (exit 0).*

---

## 1. Entropy production per shell *is* the time-ray decay rate $1/\varphi$

The forward (retarded) chronon weight is the Boltzmann factor of note 05, $p_F(k)\propto
e^{-k/\varphi}=e^{-\theta}=T(\theta)$ — the time ray itself. Its surprisal (the entropy carried by
sitting at depth $k$) is
$$S(k)=-\ln p_F(k)=\frac{k}{\varphi}+\ln Z,\qquad Z=\frac{1}{1-e^{-1/\varphi}}=2.16921,$$
so the **entropy produced per shell descended** is the pure golden rate
$$\boxed{\;\frac{dS}{dk}=\frac1\varphi=0.6180339887\ldots\;}$$
This is not a fit; it is the single derivative $d\theta/dk$ read three equivalent ways (all
verified): **(a)** as the surprisal slope above; **(b)** as the per-shell log-decay of the time ray,
$-d\ln T/dk=-d(-\theta)/dk=1/\varphi$; and **(c)** as the one-way leg of the detailed-balance
affinity. From note 05 the advanced/retarded weight ratio is exactly thermal — the flow-reversal
lattice $1/(1+\cos^2 2k\ln\varphi)$ is even in $k$ and cancels —
$$\frac{\kappa(+k)}{\kappa(-k)}=e^{-2k/\varphi}=e^{-2\theta}\quad(\text{residual }5.6\times10^{-17}),$$
so the affinity $A(k)=\ln[\kappa(+k)/\kappa(-k)]=-2\theta$ is the **round trip** (out on the
forward leg, back on the gravity leg), and one leg is $-\tfrac12\,dA/dk=1/\varphi$. The branch
entropy at the now is maximal, $S_{\rm br}(0)=\ln2=0.693147$ (note 05 §5): the now is the
zero-rapidity, maximum-branch-entropy fixed point from which both rays descend.

**Honest comparison.** The rate $1/\varphi$ here is the *constant* accumulation slope of the forward
surprisal — it has no textbook counterpart and does not vanish at the now. Established thermodynamics
fixes only the second-law *inequality*, which in this framework is carried by a **different**
quantity: the flow-entropy production $\sigma$ of §2 (sign-definite, $=0$ only at $\theta=0$). We
*recover that inequality as a theorem* there, and the *value* of the rate (i) is the framework's own
golden number; this is structure recovered, not a forced agreement. The two must be kept distinct —
see the Verdict.

## 2. The second law as a sign, and why gravity *increasing* entropy is consistent

The entropy-production rate along the flow is the antisymmetric part of the one kernel,
$\sigma(k)=-G_{\rm flow}=\sinh(\theta)/(1+\cos^2 2k\ln\varphi)\ge0$ for $\theta>0$, vanishing only
at the now (note 05 §3). So the second law is just **$\sigma$ has the sign of $\theta$**. But
black holes are maximum-entropy objects, and gravity is the *advanced* ($+1$, growing) ray — its
naive "time-reverse" reading would *decrease* entropy. The resolution is note 05 §6, sharpened
here: descending the gravity ray drives the two-state **branch** entropy
$$S_{\rm br}(k)=\ln\!\big[2\cosh\theta\big]-\theta\tanh\theta:\quad
\ln2\;\xrightarrow{\;+\theta\;}\;0\ \text{(verified monotone, }S_{\rm br}(50)=0\text{)},$$
i.e. gravity **orders** the local two-branch system (ln 2 $\to$ 0), while simultaneously the
**flow** entropy $\sigma\sim\sinh\theta$ grows without bound. Gravity is the engine that *consumes
branch entropy and dumps flow entropy* — it crystallizes local order (bound states, the mass
ordinals) precisely by exporting disorder down the forward channel. The exported disorder is
banked on the horizon. At the truncation depth $n_H$ (note 15) the conformal entropy is the bare
shell count,
$$S_{\rm CFT}=n_H\ln\varphi=\ln\frac{r_s}{\ell_P}=88.10\quad(c=3,\ \text{exact}),$$
and the Bekenstein entropy $S_{\rm BH}=\pi(r_s/\ell_P)^2=1.05\times10^{77}$ for $M_\odot$, at
$n_H=183.08$ shells. **This is the textbook solar-mass value, recovered *by construction* of the
radius map $r_n=\ell_P\varphi^{\,n}$** (the horizon is *placed* at $r_s$), so it is a consistency
check, not a derivation; honestly, $\ln S_{\rm BH}=\ln\pi+2n_H\ln\varphi=177.35$ — note the $\ln4$
distinction from $\ln(A/\ell_P^2)=178.73$. The compensation (branch order up, horizon entropy up)
is **structural** — the Penrose picture that gravitational collapse orders matter locally while
horizon entropy dominates the net — and is $O(1)$ per chronon against $10^{77}$ on the area; it
does not balance per-chronon and we do not claim it does. It is the *direction* that is locked.

## 3. Common origin: arrow and gravity are one sign — and exactly what that *is*

Here is the structural claim, stated at its true strength — neither inflated nor undersold. The flow
entropy and the net force are **both built from the same single $\sinh\theta$** generated by the one
boost $K$:
$$\sigma(k)=-G_{\rm flow}=\frac{\sinh\theta}{1+\cos^2 2k\ln\varphi}=\mathrm{osc}(k)\,\sinh\theta,
\qquad \mathcal F(k)=G-T=2\sinh\theta,\qquad
\frac{\sigma(k)}{\mathcal F(k)}=\frac{\mathrm{osc}(k)}{2}\in\Big[\tfrac14,\tfrac12\Big].$$
They are **not two independently sourced quantities** that happen to agree: both descend from the
$-1$ and $+1$ eigendirections of the *same* generator (note 35), so their ratio is the lattice
factor $\mathrm{osc}/2$, which is strictly positive and **$\theta$-independent in sign**. With the
lattice strictly positive ($\mathrm{osc}\in[\tfrac12,1]$, proved in the Extension) they therefore
carry the identical sign across *all* $\theta$ — including the advanced side $\theta<0$, where
$\sigma<0$ and $\mathcal F<0$ flip **together**. Sampling 800 shells on both sides of the now
confirms numerically what the algebra already guarantees,
$$\boxed{\;\operatorname{sign}\sigma(k)=\operatorname{sign}\mathcal F(k)=\operatorname{sign}\theta
\quad\text{for all }\theta\neq0,\quad\text{with }\sigma=\mathcal F=0\text{ only at the now.}\;}$$
**Honest reading of this identity.** This is an exact *internal* theorem, not an empirical
prediction: $\sigma>0\Leftrightarrow\theta>0$ and $\mathcal F<0\Leftrightarrow\theta<0$, so
"$\sigma$ and $\mathcal F$ share $\operatorname{sign}\theta$" is the tautology that $\theta$ cannot
be simultaneously positive and negative. It says the framework is *self-consistent* — it does not,
and cannot, on its own select which side the universe sits on. The arrow of time (the sign of
entropy production) and the attractiveness of gravity (the sign of the net force) are **one sign**,
the sign of $\theta$ relative to the now-surface; that they are *the same* sign is forced, but the
sign *itself* — the empirical fact that we observe $+\theta$ — is an **input** (the low-entropy
boundary condition / Penrose past hypothesis), not a derivation. The observable universe sits on the
$+\theta$ side: the **time ray is spent forward** ($T=e^{-\theta}$ decaying), entropy is produced
($\sigma>0$), and on those same shells gravity dominates in amplitude ($G>T$, $\mathcal
F=2\sinh\theta>0$). Forward-time and attraction are not "$T$-dominant vs $G$-dominant"
alternatives — they are **one side**, because $T\cdot G=1$ ties the decaying time ray to the growing
gravity ray. The genuine content of the framework, then, is not "the second law is derived" but the
narrower, true statement: *if* a universe is assembled with forward entropy production on a set of
shells, the same generator makes gravity attractive on exactly those shells — the two cannot be
chosen independently. To flow forward in time *is* to fall toward gravity: same side, same $\sinh$,
same $K$.

This does **not** contradict cosmic acceleration. Large-scale repulsion is not a local $\mathcal
F<0$ at positive $\theta$; it is the **outer-horizon depletion** regime (note 08): past the
depletion shell $N_\star=\log_\varphi(R_{\rm H}/\ell_P)=291.88$ the source becomes *interior* and
the same advanced field points *outward* — a sign flip in the **source geometry**, not in the local
force law. At every individual shell $\theta>0$ the sign-lock holds; $\Lambda$ lives at the $N_\star$
boundary, $108$ shells outside the solar horizon $n_H$, where the hierarchy has run out outward.

## Verdict

The cosmological arrow of time and the attractiveness of gravity are **not independently
choosable**: both are read off the single generator $K$, so they share $\operatorname{sign}\theta$
identically — this is an exact internal theorem (§3), and it is what the framework genuinely
delivers. What it does **not** deliver is the arrow itself: which side of the now the universe sits
on ($+\theta$) is an *input* — the low-entropy boundary condition — not a derivation. With that
input supplied, two distinct entropy statements hold and must not be conflated: **(i)** the forward
surprisal accumulates at the *constant* golden rate $dS/dk=1/\varphi=0.618$ per shell (the time-ray
decay rate, derived three independent ways, with *no* textbook value to match — the rate is the
framework's own number; this is nonzero everywhere, including the now); **(ii)** the *flow*-entropy
production $\sigma=\mathrm{osc}\,\sinh\theta$ is sign-definite, $\sigma\ge0$ for $\theta\ge0$ with
$\sigma=0$ *only* at $\theta=0$ — and it is *this* quantity that recovers the second-law inequality
$\sigma\ge0$ as a sign-definiteness theorem (equality only at the now). The constant rate (i) and
the vanishing-at-the-now production (ii) are different measures; the box $dS/dk=1/\varphi$ refers to
(i). The textbook $S_{\rm BH}(M_\odot)=1.05\times10^{77}$ is
reproduced **by construction** at $n_H=183.08$ (the radius map *places* the horizon at $r_s$), with
honest log bookkeeping $\ln S_{\rm BH}=\ln\pi+2n_H\ln\varphi=177.35$ — kept distinct from
$\ln(A/\ell_P^2)=178.73$ by exactly $\ln4$, the $S=A/4$ factor. Gravity *consumes* branch entropy
($\ln2\to0$) while *dumping* flow entropy onto the horizon — the Penrose direction, **structurally**,
$O(1)$ per chronon against $10^{77}$ on the area; we do **not** claim a per-chronon numerical
balance. The hard number is $\boxed{dS/dk=1/\varphi=0.61803}$ per shell, sign-locked to the force
$\mathcal F=2\sinh\theta$ through the shared $\sinh$.

**On falsifiability — stated honestly.** One might write a "falsifier": find a single shell
(one $\theta$) on the forward-time side ($\sigma>0$) that is *also* gravitationally repulsive
($\mathcal F<0$). But this is **unfalsifiable by construction**, and it would be dishonest to
present it otherwise: $\sigma>0\Leftrightarrow\theta>0$ while $\mathcal
F<0\Leftrightarrow\theta<0$, so the "falsifier" asks for a $\theta$ that is *both* positive and
negative — algebraically impossible. Invoking $T\cdot G=1$ "to forbid it" is circular ($T\cdot
G=e^{-\theta}e^{+\theta}=1$ is the same identity). The sign-lock is therefore a **self-consistency
theorem, not an empirical test**. A *genuine* falsifier would require $\sigma$ and $\mathcal F$ to be
**independently sourced** so that they *could* disagree — but in this framework both are
$(\text{positive})\times\sinh\theta$ from the one generator $K$ (their ratio is the lattice factor
$\mathrm{osc}/2\in[\tfrac14,\tfrac12]$, sign-fixed), so the framework offers no such independent
handle. What *is* genuinely testable lives elsewhere — the $1/\varphi$ entropy-rate per shell, the
log-periodic horizon comb of note 15, the $w(0)+1\approx3\times10^{-3}$ of note 08 — quantities with
a number the framework does not get to choose. The sign-lock's role is to certify that those
predictions are *mutually consistent*, not to be a test in its own right.

## Extension — the lattice bound that makes the sign-lock non-vacuous

The §3 sign-lock has exactly one non-trivial moving part, and it is worth isolating because it is
the *only* place the lattice could in principle have spoiled the result. The flow entropy
$\sigma=\mathrm{osc}(k)\,\sinh\theta$ and the force $\mathcal F=2\sinh\theta$ share a sign **iff the
modulating lattice factor $\mathrm{osc}(k)$ never changes sign**. It does not, and the bound is
elementary but worth stating as a theorem:
$$\boxed{\;\mathrm{osc}(k)=\frac{1}{1+\cos^2(2k\ln\varphi)}\in\Big[\tfrac12,\,1\Big]\quad\text{for all }k\in\mathbb R,\;}$$
because $\cos^2\in[0,1]$ forces the denominator into $[1,2]$. The upper bound $\mathrm{osc}=1$ is
attained exactly on the **inversion shells** $k_n=(2n-1)\pi/(4\ln\varphi)$ (there $2k_n\ln\varphi=(2n-1)\pi/2$,
$\cos^2(2k_n\ln\varphi)=0$, $\tau_{\rm Frenet}=0$, the momentary time-reversal-symmetric points of
note 00/05 §3 — where the $\sinh$ flow is *un*modulated); the lower bound $\mathrm{osc}=\tfrac12$ is
attained midway between them, at $k=m\pi/(2\ln\varphi)$ (where $\cos^2=1$). This pins the
$\sigma/\mathcal F$ ratio into a hard, $\theta$-independent window:
$$\frac{\sigma(k)}{\mathcal F(k)}=\frac{\mathrm{osc}(k)}{2}\in\Big[\tfrac14,\,\tfrac12\Big],$$
so the lattice modulates the *magnitude* of entropy production relative to the force by at most a
factor of $2$ — entropy is produced most efficiently per unit force on the inversion shells
($\mathrm{osc}=1$, $\sigma/\mathcal F=\tfrac12$) and least on the midway shells
($\mathrm{osc}=\tfrac12$, $\sigma/\mathcal F=\tfrac14$) — but it can **never flip the sign**, because
the window is strictly bounded away from zero ($\sigma/\mathcal F\ge\tfrac14>0$). The content of the sign-lock is therefore precisely this bound: *the only way
forward-time could coexist with repulsive gravity is if the lattice drove $\mathrm{osc}<0$, and the
golden flow-reversal lattice is structurally incapable of it.* Had the corpus instead used a lattice
that could vanish or change sign — say a bare $\cos(2k\ln\varphi)$ rather than the $1/(1+\cos^2)$
even denominator — the sign-lock would genuinely fail on a measure-nonzero set of shells, and *that*
hypothetical is what makes the present statement carry information rather than being empty. The
sign-lock is non-vacuous exactly to the extent that $\inf_k\mathrm{osc}(k)=\tfrac12>0$ is a
non-trivial fact about the golden lattice. (Verified: $\min\mathrm{osc}=0.5000$,
$\max\mathrm{osc}=1.0000$ over a dense $k$-grid; $\sigma/\mathcal F\in[0.250,0.500]$;
$\operatorname{sign}\sigma=\operatorname{sign}\mathcal F$ everywhere $\theta\neq0$.)
