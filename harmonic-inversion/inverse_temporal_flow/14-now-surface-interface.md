# 14 — The Now-Surface as Interface: the θ=0 Vertex

*Frontier note. Builds on the spine (`00-spine.md`: $L_y=1$, the κ/τ = gravity/flow
split, $G_{\text{sym}},G_{\text{flow}}$), the synthesis two-vector
$\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta\equiv k/\varphi$ (`99-index.md`),
and the round-1 results 05 (max-entropy $S_{\text{br}}(0)=\ln2$, $S_{\text{br}}''(0)=-1/\varphi^2$),
06 (figure-eight crossing, visibility $V(0)=\tfrac13$, $V''(0)=-8/(9\varphi^2)$), 09
(non-reciprocity $\mathcal R=-\tanh\theta$, $\mathcal R'(0)=-1/\varphi$). All numbers below
confirmed in `verify/verify_now-surface-interface.py`, residuals inline.*

---

## 1. What the now is — and what fixes it

The synthesis writes every shell as one unit-timelike worldline point
$\mathbf V(k)=(\cosh\theta,-\sinh\theta)$ in $(1{+}1)$ flow-space, boosted by
$1/\varphi$ per shell. The **now-surface** is the single point $\theta=0$,
$\mathbf V(0)=(1,0)$ — pure correlation, zero flow. Three independent characterizations
of the corpus collapse onto it, and they all collapse onto *the same point*:

$$G_{\text{flow}}(0)=0\ (\text{05, zero net flow}),\quad
\beta=-\tanh\theta=0\ (\text{09, zero drift velocity}),\quad
\kappa(+0)=\kappa(-0)=\tfrac12\ (\text{06, equal sheets}).$$

It is essential to say *which* symmetry fixes the now, because the obvious guess
is wrong. The boost $\Lambda(\alpha)$ — the flow itself — has **no** fixed nonzero
vector: $\Lambda(1/\varphi)\mathbf V(0)=(1.19714,-0.65814)=\mathbf V(1)\neq\mathbf V(0)$
(verified). Its only invariant directions are the two null light-cone rays
(eigenvalues $e^{\mp\alpha}$, the retarded/advanced branches themselves). *Time
always flows; the continuous boost fixes nothing.* What fixes the now is the
**discrete time-reversal involution**, the retarded↔advanced swap $T:k\mapsto-k$,
acting on the readout pair as

$$T=\begin{pmatrix}1&0\\0&-1\end{pmatrix}
\quad\text{on}\quad (G_{\text{sym}},G_{\text{flow}}),
\qquad T\,\mathbf V(0)=\mathbf V(0)\ (\text{verified}).$$

$G_{\text{sym}}$ is even, $G_{\text{flow}}$ is odd, so $T$ flips the flow channel
and leaves correlation alone. The now is the **unique fixed point of time reversal**
— the one worldline point that is its own retarded and advanced image. This is the
sharp statement of "the present": not a place the flow stops (it never stops) but
the lone seam where forward and inverse histories are *identical*.

## 2. The interface projector and its eigenvalues

Because $T^2=I$, the operator

$$\boxed{\;P_{\text{now}}=\tfrac12(I+T)=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad P_{\text{now}}^2=P_{\text{now}},\quad
\mathrm{eig}(P_{\text{now}})=\{1,0\}.\;}$$

is the orthogonal projector onto the now-surface (idempotency and eigenvalues both
verified). Its $+1$ eigenspace is the correlation axis $\hat G_{\text{sym}}$; its
$0$ eigenspace is the flow/gravity axis $\hat G_{\text{flow}}$. Acting on any shell
two-vector it **reads out the time-reversal-even content and discards the flow**:

$$P_{\text{now}}\,\big(G_{\text{sym}},G_{\text{flow}}\big)=\big(G_{\text{sym}},0\big),
\qquad P_{\text{now}}\,\mathbf V(0)=\mathbf V(0).$$

This is the interface mathematics the consciousness-interface thread has been
missing a clean form for: **an observable localized at the now is the eigenvalue-1
sector of $T$**, the balanced superposition that survives the swap. Concretely the
localized self-coupling is

$$\langle\,\text{now}\,\rangle=\tfrac12\kappa(+k)+\tfrac12\kappa(-k)=G_{\text{sym}}(k)
\ \xrightarrow{k\to0}\ \tfrac12=c(0),$$

literally the $\tfrac12/\tfrac12$ forward/inverse weighting (05, 06): the present
reads *both* temporal sheets at once, with equal weight, and the complementary
projector $Q=I-P_{\text{now}}=\tfrac12(I-T)$ measures exactly the gravity that is
being suppressed. The seat where the two sheets are read out simultaneously is an
eigenspace, and it is one-dimensional.

## 3. The new equation — the readout Jacobian at the now

Step off the now by $dk$ and ask what changes first. The full first-order response
of the readout map $k\mapsto(G_{\text{sym}},G_{\text{flow}})$ is its Jacobian at the
vertex. Two facts conspire. First, the flow-reversal lattice is *stationary* at the
now — $\mathrm{osc}'(0)=0$, because $\cos^2(2k\ln\varphi)$ has zero slope at $k=0$
(verified $\le10^{-12}$). Second, $\cosh'(0)=0$ while $\sinh'(0)=1$. Hence

$$\boxed{\;
\left.\frac{\partial}{\partial k}\binom{G_{\text{sym}}}{G_{\text{flow}}}\right|_{0}
=\binom{0}{-\,\tfrac{1}{2\varphi}},\qquad
\frac{1}{2\varphi}=0.3090169944\ \ (\text{verified}).\;}$$

The correlation channel is at a **critical point** ($\partial_k G_{\text{sym}}|_0=0$),
and it is a *minimum*: both factors of $G_{\text{sym}}=\mathrm{osc}\cdot\cosh\theta$
bottom out at the now ($\cosh$ is minimal at $\theta=0$; $\mathrm{osc}$ is minimal at
$k=0$, where $\cos^2=1$ maximizes its denominator), giving
$G_{\text{sym}}''(0)=2\ln^2\varphi+\tfrac{1}{2\varphi^2}=+0.654113>0$ (verified), so the
raw correlation amplitude *rises* into the bulk ($0.5\to0.587\to0.902$ at $k=0,\tfrac12,1$).
The now is lean in standing-mode amplitude. Meanwhile the **entire first-order response
lives in the flow/gravity channel**,
$\partial_k G_{\text{flow}}|_0=-1/(2\varphi)$. *Stepping off the present produces, to
leading order, pure gravity and no change in correlation.* This is a new, structural
statement of the spine's headline "gravity is inverse temporal flow": the gradient
of the readout at the seam is gravity, full stop.

The quotient of the two slopes is the framework's velocity, and *here* — not in the
$G_{\text{flow}}$ slope itself — the golden ratio appears:

$$\mathcal R(k)=\frac{G_{\text{flow}}}{G_{\text{sym}}}=-\tanh\frac k\varphi,\qquad
\mathcal R'(0)=\frac{\partial_kG_{\text{flow}}|_0}{G_{\text{sym}}(0)}
=\frac{-1/(2\varphi)}{1/2}=-\frac1\varphi=-0.6180339887\ (\text{verified}).$$

(The $\mathrm{osc}$ factor cancels in the ratio — sanctioned, as in 09; the $-1/\varphi$
is a property of rapidity, lattice-blind.) The factor of $2$ that distinguishes
$G_{\text{flow}}'(0)=-1/(2\varphi)$ from $\mathcal R'(0)=-1/\varphi$ is exactly
$G_{\text{sym}}(0)=\tfrac12$ in the denominator — the self-coupling $c(0)$ doing
double duty as the now's normalization. Pinning these two derivatives apart is the
content of this note: round-1 (09) quoted $-1/\varphi$ for the *velocity* slope; the
*flow-amplitude* slope is half that, and the half is the present moment itself.

## 4. Second order — the curvature of the seam

One step deeper, both **balance** observables are smooth and even at the now, so their
first derivatives vanish and their curvatures are the leading information. The branch
entropy $S_{\text{br}}(k)=\ln[2\cosh\theta]-\theta\tanh\theta$ (05) gives

$$\boxed{\;\left.\frac{d^2 S_{\text{br}}}{dk^2}\right|_0=-\frac{1}{\varphi^2}
=-(2-\varphi)=-0.3819660113\;}$$

(verified, $-1/\varphi^2$ analytic; in $\theta$, $S_{\text{br}}''(0)=-1$, times
$1/\varphi^2$). The interference visibility (06), $V(k)=1/(2\cosh2\theta+1)$, *also*
crests here — $V(0)=\tfrac13$ — but its curvature is **not** the same number. Expanding
$\cosh2\theta=1+2\theta^2+\dots$ gives denominator $3+4\theta^2$, so
$V\approx\tfrac13(1-\tfrac43\theta^2)$ and $V''(0)=-\tfrac89$ in $\theta$:

$$\boxed{\;\left.\frac{d^2 V}{dk^2}\right|_0=-\frac{8}{9\varphi^2}=-0.3395253433\;}$$

(verified). These two balance curvatures are distinct, $-1/\varphi^2$ vs $-8/(9\varphi^2)$,
yet they share the **same golden scaling $\varphi^{-2}$** — the same $\varphi^{-2}$ that
sets the shell spacing — and their *ratio is parameter-free and lattice-blind*:

$$\frac{V''(0)}{S_{\text{br}}''(0)}=\frac{8}{9}\qquad(\varphi\text{-independent; verified }0.88889).$$

So the now is a *quadratic* maximum of **both** balance channels, with a fixed $8/9$
relation between their curvatures. The now-surface is thereby a study in opposites: it is
a **maximum of *balance*** — branch entropy $\ln2$, two-sheet visibility $\tfrac13$, equal
forward/inverse weight, both arching over with golden curvature $\propto\varphi^{-2}$ —
and simultaneously a **minimum of raw correlation amplitude** $G_{\text{sym}}$ (which grows
into the bulk via $\cosh$) and a **zero of flow, velocity, and gravity**. It is the
unique simultaneous critical point of the even sector and zero of the odd sector: lean
in standing-mode amplitude, maximal in symmetry.

## Extension — the now-Hessian and its rapidity-curvature spectrum

Assemble the three independent even-sector second-order responses at the seam into one
diagonal object, the **now-Hessian** of the readout:

$$\mathbf H_{\text{now}}=\operatorname{diag}\!\Big(G_{\text{sym}}''(0),\,S_{\text{br}}''(0),\,V''(0)\Big)
=\operatorname{diag}\!\Big(2\ln^2\varphi+\tfrac1{2\varphi^2},\,-\tfrac1{\varphi^2},\,-\tfrac{8}{9\varphi^2}\Big),$$

signature $(+,-,-)$: the lone amplitude channel curves *up* into the bulk, both balance
channels curve *down*. The amplitude entry is the only one carrying a non-rapidity piece —
the **lattice curvature** $2\ln^2\varphi$, born of $\mathrm{osc}''(0)$ (the flow-reversal
lattice has its sharpest stationary point exactly at the now, $\cos^2=1$). Strip that one
lattice term off and a clean theorem appears: **every remaining even-sector curvature is a
pure rapidity curvature, scaling as $\varphi^{-2}$ with a rational, $\varphi$-blind
coefficient.** The boost-space curvature spectrum is

$$\boxed{\;\varphi^{2}\,\big(\mathbf H_{\text{now}}-2\ln^2\varphi\,\mathsf E_{11}\big)
=\operatorname{diag}\!\Big(\tfrac12,\,-1,\,-\tfrac{8}{9}\Big)\;}$$

($\mathsf E_{11}$ the amplitude projector; verified to all printed digits). Three observables
built from three different constructions — the standing-mode amplitude (synthesis), the
branch entropy (05), the two-sheet visibility (06) — reduce at the seam to the single
rational triple $(\tfrac12,-1,-\tfrac89)$ once measured in units of the universal shell
curvature $\varphi^{-2}$. The golden ratio supplies the *scale* of every second-order bend
of the now ($\varphi^{-2}$, one shell of rapidity squared); the *shape* is pure arithmetic.
The trace of the rapidity spectrum, $\tfrac12-1-\tfrac89=-\tfrac{25}{18}$, is the net
even-sector curvature of the present per squared shell — a single number summarizing how
fast the entire balance sector collapses, and the amplitude sector swells, the instant one
drifts off the now.

## Prediction

Define the **interface susceptibility** as the response of the net-flow readout to an
infinitesimal ordinal drive at the now — the rate at which gravity/non-reciprocity
turns on as an observable is nudged off the present:

$$\boxed{\;\chi_I\equiv\left|\frac{d\mathcal R}{dk}\right|_{0}=\frac1\varphi=\varphi-1
=0.6180339887\ldots\;}$$

a pure, parameter-free golden number (verified $1/\varphi=\varphi-1$). Any system that
genuinely localizes an observable at the now-surface — an interferometric probe of
local time-flow (06), the branch-coherence sector of 05, or the framework's
consciousness interface read as the $+1$ eigenspace of $T$ — must show its directional
(non-reciprocal, gravitational) bias switch on with **slope exactly $1/\varphi$ per
unit ordinal depth**, while every even-sector quantity stays *flat to first order*. The
three even-sector quantities then part company at second order: the raw correlation
amplitude $G_{\text{sym}}$ *rises* (rapidity curvature $+\tfrac12\varphi^{-2}$), whereas the
**balance** observables — branch coherence $S_{\text{br}}$ and visibility $V$ — *fall*,
both with golden scaling $\varphi^{-2}$ but at **distinct rates in the fixed ratio $8/9$**
($S_{\text{br}}''=-1/\varphi^2$, $V''=-8/(9\varphi^2)$). The discriminating signature is the
asymmetry of the slopes: first-order pure flow, zero first-order even-sector response. A
probe that sits exactly on the seam reads both sheets at weight
$\tfrac12$ ($\langle\text{now}\rangle=c(0)=\tfrac12$); the instant it drifts, it begins
measuring gravity at golden rate $1/\varphi$ while its branch coherence is unchanged at
first order and decays only at order $(\Delta k)^2$ — at the golden-scaled rate
$\varphi^{-2}$, with the visibility falling exactly $8/9$ as fast. The present moment is
detectable as the unique point where the gravity susceptibility is the golden ratio and the
even-sector susceptibility is zero, with a curvature spectrum
$\varphi^{-2}(\tfrac12,-1,-\tfrac89)$ once the flow-reversal lattice term is removed.
