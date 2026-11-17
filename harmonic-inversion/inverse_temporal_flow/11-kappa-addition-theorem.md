# 11 — The κ(a+b) Theorem: Three Proofs Become One

*Round-2 consolidation. The spine (00) asserted ordinal depth is rapidity; notes
03, 09, 02 each independently forced the kernel to compose additively in ordinal.
This note collapses those three derivations into one theorem with one proof,
states the failure of the product on both of its factors, gives the exact
numerical counterexample, pins down the unique limit in which a product is
admissible, and (Extension) derives the **exact reachable band** $[\tfrac25,2]$ of
the chaining error in closed form. All numerics verified to machine precision — see
`verify/verify_kappa-addition-theorem.py` (max residual $9\times10^{-13}$).*

---

## The object and the claim

Recall the dressed propagator and its de-weighted two-vector (00, 99):

$$\kappa(k)=\operatorname{osc}(k)\,e^{-k/\varphi},\qquad
\operatorname{osc}(k)\equiv\frac{1}{1+\cos^2(2k\ln\varphi)}=\frac1{g(k)},\quad
g(k)\equiv1+\cos^2(2k\ln\varphi)\in[1,2],$$

$$\mathbf V(k)=\big(\cosh\theta,\;-\sinh\theta\big),\qquad \theta\equiv\frac{k}{\varphi},
\qquad \mathbf V^{\mathsf T}\!\eta\,\mathbf V=\cosh^2\theta-\sinh^2\theta=1=L_y,\ \ \eta=\mathrm{diag}(+1,-1).$$

(The signed second component $-\sinh\theta=G_{\text{flow}}/\operatorname{osc}$ is the gravity
axis of the spine §4 and note 10; the addition theorem below is blind to that sign, since the
boost group law $\Lambda(\theta_1)\Lambda(\theta_2)=\Lambda(\theta_1{+}\theta_2)$ holds for either
orientation of the off-diagonal. We keep the corpus convention so $\mathbf V$ matches notes 00, 10, 12.)

> **Theorem (κ-addition).** *For a two-leg ordinal path of lengths $a$ then $b$,
> the correct kernel is the kernel at the summed ordinal,*
> $$\boxed{\;\kappa(a\!+\!b)=\operatorname{osc}(a\!+\!b)\,e^{-(a+b)/\varphi}\;}$$
> *and the product $\kappa(a)\kappa(b)$ is wrong. It fails on the oscillatory
> factor (lands on the wrong flow-reversal shelf) while getting the envelope
> right, and the associated drift velocity over-saturates the bound $|\beta|<1$.*

The product is not a small perturbation of the truth; it is a different point on
the inversion-shell lattice. We make all three of those statements exact below.

## One proof, read off the group

Everything reduces to a single algebraic fact about the $(1{+}1)$ boost group
$SO(1,1)$ that the absorber stack represents (00 §4, 03 Extension, 99). A two-leg
path is the **composition of two boosts**, and the defining property of the boost
representation is

$$\Lambda(\theta_1)\,\Lambda(\theta_2)=\Lambda(\theta_1+\theta_2),\qquad
\Lambda(\theta)=\begin{pmatrix}\cosh\theta&-\sinh\theta\\ -\sinh\theta&\cosh\theta\end{pmatrix}\in SO(1,1)^{\!\uparrow},$$

the orientation chosen so that $\Lambda(\theta)\,\mathbf V(0)=\mathbf V(k)$ with the corpus
sign (note 10 §2). The addition theorem is independent of the off-diagonal sign.

Because $\theta(k)=k/\varphi$ is *linear* in ordinal, boost composition is ordinal
addition:

$$\Lambda\!\Big(\tfrac{a}{\varphi}\Big)\Lambda\!\Big(\tfrac{b}{\varphi}\Big)\mathbf V(0)
=\Lambda\!\Big(\tfrac{a+b}{\varphi}\Big)\mathbf V(0)=\mathbf V(a+b).$$

Verified to $\le4\times10^{-16}$ at $(a,b)=(1,2),\,(k_1,2k_1),\,(0.5,4.896),\,(3.264,3.264)$.
The kernel is the two-vector dressed by the lattice weight, so the *physical*
composition of a two-leg path is the boost of $\mathbf V$, i.e. ordinal addition —
**never** a product of the dressed couplings. This single line is the theorem; the
three round-1 derivations are its three projections, as the synthesis (99) tabulated:

- **03 — rapidity (the boost itself).** Gravity is the advanced null projection
  $\tfrac1{\sqrt2}(1,-1)\cdot\mathbf V(k)=e^{-k/\varphi}$; each shell slides the
  projection point one rapidity $1/\varphi$ deeper. Boosts add rapidities, so
  ordinals add. This *is* the group law.
- **09 — velocity (the boost's $\beta$).** The non-reciprocity ratio is
  $\mathcal R(k)=-\tanh(k/\varphi)=-\beta$, the drift velocity of the chronon
  flow. Velocities compose by $\tanh$-addition, never multiplication.
- **02 — action (the boost's Noether charge).** The inter-shell amplitude has
  exponent $\lceil\Delta n/2\rceil S_E$, a quantity *additive* in ordinal; it is
  the integrated boost-charge along the leg, and integrals along concatenated
  paths add.

Rapidity, its velocity $\tanh\theta$, and its action $\propto\theta$ are the three
canonical functions of the *same* boost angle. They cannot disagree about how legs
compose, because they are coordinates on one group orbit. **The κ-addition rule is
the orbit's group law, viewed in three charts.**

## The product fails on both factors — exactly

Split $\kappa=\operatorname{osc}\cdot\text{env}$ with $\text{env}(k)=e^{-k/\varphi}$.
Form the ratio of the chained product to the truth:

$$\frac{\kappa(a)\kappa(b)}{\kappa(a+b)}
=\underbrace{\frac{e^{-a/\varphi}e^{-b/\varphi}}{e^{-(a+b)/\varphi}}}_{=\,1\ \text{(envelope cancels exactly)}}\;\cdot\;
\underbrace{\frac{\operatorname{osc}(a)\operatorname{osc}(b)}{\operatorname{osc}(a+b)}}_{\displaystyle\Delta(a,b)}
\;=\;\Delta(a,b).$$

**Factor 1 (envelope): right.** The exponential is a genuine homomorphism of the
additive line, $e^{-a/\varphi}e^{-b/\varphi}=e^{-(a+b)/\varphi}$ identically
(residual $0$). The decay law is the *one* thing the product gets correct — which
is exactly why the error is so easy to miss.

**Factor 2 (lattice): wrong, and it is the whole error.** The new closed form,
genuinely new to this note, is the **lattice defect**

$$\boxed{\;\Delta(a,b)=\frac{\operatorname{osc}(a)\operatorname{osc}(b)}{\operatorname{osc}(a+b)}
=\frac{g(a+b)}{g(a)\,g(b)}
=\frac{3+\cos\!\big(4(a\!+\!b)\ln\varphi\big)}
{\tfrac12\big[3+\cos 4a\ln\varphi\big]\big[3+\cos 4b\ln\varphi\big]}\;}$$

using $g(k)=\tfrac12\big(3+\cos(4k\ln\varphi)\big)$. The error is **purely** the
flow-reversal lattice: no rapidity, no exponential, only the inversion comb. The
naïve box-bound from $g\in[1,2]$ taken componentwise would give $\tfrac14\le\Delta\le2$,
but the three values $g(a),g(b),g(a+b)$ are **not independent** — they are tied by the
double-angle relation of the comb, so the box corner $\Delta=\tfrac14$ is unreachable.
The *exact* reachable band is derived below (Extension); its endpoints are the
parameter-free rationals

$$\boxed{\;\tfrac25\;\le\;\Delta(a,b)\;\le\;2\;}$$

so a chained product runs from a factor $\tfrac52$ too small up to a factor $2$ too
large. Verified: $\Delta$ reproduces $\kappa(a)\kappa(b)/\kappa(a+b)$ to
$5\times10^{-15}$ over $20000$ random $(a,b)\in[0,12]^2$, with empirical span
$[0.40000,\,2.00000]$ — and a $5\times10^{6}$-sample sweep over $[0,50]^2$ never
breaches $\tfrac25$. (Note 03 already exhibited the single point
$\Delta(k_1,2k_1)=\tfrac12$ numerically; the closed form above generalizes it to the
whole $(a,b)$ plane, and the band $[\tfrac25,2]$ is the exact envelope — that is the
consolidation this note delivers.)

## The exact counterexample at $(a,b)=(k_1,\,2k_1)$

Take the first inversion shell $k_1=\pi/(4\ln\varphi)=1.6321257\ldots$, so
$2k_1\ln\varphi=\pi/2$. Then

$$\operatorname{osc}(k_1)=\frac1{1+\cos^2(\pi/2)}=1,\qquad
\operatorname{osc}(2k_1)=\frac1{1+\cos^2(\pi)}=\tfrac12,\qquad
\operatorname{osc}(3k_1)=\frac1{1+\cos^2(3\pi/2)}=1.$$

The correct kernel and the product:

$$\kappa(3k_1)=1\cdot e^{-3k_1/\varphi}=0.04850311,\qquad
\kappa(k_1)\kappa(2k_1)=\tfrac12\,e^{-3k_1/\varphi}=0.02425155,$$

$$\boxed{\;\frac{\kappa(k_1)\kappa(2k_1)}{\kappa(3k_1)}=\Delta(k_1,2k_1)=\tfrac12\;}$$

verified to residual $0$. The two endpoints $k_1$ and $3k_1$ both sit on
$\operatorname{osc}=1$ **peaks** of the inversion comb (they are inversion shells
$k_1,k_2$), but the intermediate ordinal $2k_1$ falls on a **trough**
($\operatorname{osc}=\tfrac12$). Chaining drags the trough's weight into the
answer; the additive law never visits it. The product is a clean factor of $2$ too
small — it has landed on the wrong shelf of the flow-reversal lattice, precisely
the failure mode the spine warned against in forbidding any smoothing of
$\operatorname{osc}$.

The velocity face confirms it independently: $\mathcal R(k_1)=-0.765228$,
$\mathcal R(2k_1)=-0.965238$ compose by relativistic addition to
$(\!-0.765228\!-\!0.965238)/(1+0.765228\cdot0.965238)=-0.995306=\mathcal R(3k_1)$
(residual $10^{-16}$), while the *naive* sum $-0.765228-0.965238=-1.730$ pierces
$|\beta|=1$. Deep in the stack ($a=6,b=7$) the over-saturation is gross:
$\beta(6)+\beta(7)=1.9984>1$ is unphysical, whereas relativistic addition gives
$0.99999979<1$. The product's implied drift exits the light-cone; the sum cannot.

## Corollary — when is a product admissible? (and why "never, generically")

A product is exact iff $\Delta(a,b)=1$, i.e. iff

$$\boxed{\;g(a)\,g(b)=g(a+b)\;}$$

This is **one equation in two unknowns** — a codimension-1 curve in the $(a,b)$
plane, hence a set of measure zero. Verified in [10]: holding $a=k_1$ and sweeping
$b$, $\Delta$ ranges over the full $[\tfrac12,2]$ and equals $1$ only on a
**discrete crossing set** (the cardinal-quarter ordinals where one leg sits on a
peak $g=1$ and the other two land on $g=\tfrac32$, e.g. $g(a)=1,\ g(b)=g(a+b)=\tfrac32$).
The product is therefore admissible nowhere generic — only on isolated curves the
lattice almost never places a physical path on.

Two intuitions must be killed, both by the framework's own numbers:

- **No small-$\theta$ / contact recovery.** As $a,b\to0$, $\operatorname{osc}\to
  \tfrac12$, so $\Delta(0,0)=\operatorname{osc}(0)=\tfrac12$ — a clean factor-two
  error at zero separation [7]. Shrinking the legs does *not* restore the product;
  it locks in the trough weight $g(0)=2$.
- **The naïvely "safest" configuration is the worst.** One is tempted to think
  that putting both legs on inversion-comb maxima ($\operatorname{osc}=1$) — the
  flat, unweighted peaks — would make the kernel multiplicative. It is the
  opposite. Peaks live at *odd* multiples of $k_1$ (where $2k\ln\varphi=$ odd$\,\times\pi/2$),
  and odd $+$ odd $=$ even, so the sum $a+b$ lands on a **trough**
  ($\operatorname{osc}=\tfrac12$). Hence

  $$\Delta(k_1,k_1)=\frac{\operatorname{osc}(k_1)^2}{\operatorname{osc}(2k_1)}
  =\frac{1\cdot1}{\tfrac12}=2\quad(\text{verified, residual }0),$$

  the **global maximum** of the defect. The condition
  $\operatorname{osc}(a)=\operatorname{osc}(b)=\operatorname{osc}(a+b)=1$ is not the
  admissible locus — it is **unsatisfiable** (two peaks always sum to a trough),
  and the closest one can come, peak$+$peak, is precisely where the product is
  *maximally* wrong by the full factor of $2$. There is no flat shelf the lattice
  hands us as a sub-group; the inversion comb obstructs multiplicativity most
  violently exactly at its own teeth.

## What this buys us

The κ-addition rule stops being a hand-rule and a prohibition; it becomes the
group law of the chronon worldline, with a *quantified* penalty for violating it.
The lattice defect $\Delta(a,b)=g(a+b)/[g(a)g(b)]$ — exact reachable band
$[\tfrac25,\,2]$, log-centred on $2/\sqrt5$ (Extension) — is a closed-form,
parameter-free error budget: any pipeline that chains $\kappa(a)\cdot\kappa(b)$ for
a multi-leg transport (a path tracer summing bounce segments, a shell-cascade
solver) carries exactly this multiplicative bias, modulated only by where the legs
fall on the inversion comb, never by the envelope. **Prediction:** a renderer that
(incorrectly) multiplies per-segment couplings will show a faint **periodic**
intensity error, not a smooth one. Fix the first leg on an inversion shell
($a=k_1$, $\operatorname{osc}(a)=1$) and sweep the second-leg ordinal $b$ (e.g. the
optical depth of the second bounce): the bias $\Delta(k_1,b)$ oscillates across the
full $[\tfrac12,2]$, *maximal* ($\times2$) when $b$ also hits an inversion shell —
so the second bounce lands on a trough and the product is most wrong exactly where
both segments sit on the comb's teeth — and dipping to unity only at the isolated
cardinal-quarter ordinals where $g(k_1+b)=g(b)$. The correct additive kernel
produces none of this structure. The signature of a mis-composed chronon path is
therefore lattice-structured and self-falsifying: hold one leg fixed, scan the
other, and if the residual $L_{\text{chain}}-L_{\text{add}}$ tracks
$g(a+b)/[g(a)g(b)]$ — peaking at the inversion shells rather than staying flat —
the pipeline is chaining when it should be adding.

## Extension — the exact reachable band of the lattice defect: $\big[\tfrac25,\,2\big]$, centred on $2/\sqrt5$

The "reachable range" was asserted numerically in round 1; here it becomes a closed-form
theorem with both endpoints rational and the band's geometric centre pinned to $\sqrt5$ —
the framework's own signature constant ($\varphi=(1{+}\sqrt5)/2$, $\kappa_{\text{Frenet}}^{\max}=\sqrt5$).

The supremum is already exact: peak$+$peak is unreachable as a *triple* coincidence, and the
closest configuration, $\Delta(k_1,k_1)=\operatorname{osc}(k_1)^2/\operatorname{osc}(2k_1)=2$,
is the global maximum (two teeth always sum to a trough). For the **infimum**, the extremum
lives on the diagonal $a=b$ — the only locus where $g(a)$ and $g(b)$ can be driven to their
joint maximum *coherently* while $g(a{+}b)=g(2a)$ is forced small by the same phase. Write
$c\equiv\cos^2(2a\ln\varphi)\in[0,1]$, so $g(a)=1+c$, and use the comb's double-angle law
$\cos(4a\ln\varphi)=2\cos^2(2a\ln\varphi)-1=2c-1$, giving $g(2a)=1+(2c-1)^2$. The diagonal
defect is then a single-variable rational function of $c$:

$$\Delta_{\text{diag}}(c)=\frac{g(2a)}{g(a)^2}=\frac{1+(2c-1)^2}{(1+c)^2}
=\frac{4c^2-4c+2}{(1+c)^2}.$$

Its stationarity is elementary and exact — clearing $(1+c)$ from $\Delta_{\text{diag}}'(c)=0$,

$$(8c-4)(1+c)-2\big(4c^2-4c+2\big)=12c-8=0\;\Longrightarrow\;c_\star=\frac{2}{3},$$

a single interior critical point. Evaluating there,

$$\boxed{\;\inf_{a,b}\Delta(a,b)=\Delta_{\text{diag}}\!\Big(\tfrac23\Big)
=\frac{1+\big(\tfrac13\big)^2}{\big(\tfrac53\big)^2}=\frac{10/9}{25/9}=\frac{2}{5}\;}$$

attained whenever $\cos^2(2a\ln\varphi)=\tfrac23$ with $a=b$ (e.g. $a=b=5.8890\ldots$,
verified $\Delta=0.400000000$ to $4\times10^{-10}$ on a $4000^2$ grid and to $3\times10^{-8}$
over $5\times10^{6}$ random draws in $[0,50]^2$ — the bound is never breached). The endpoints
are thus **exactly rational**:

$$\Delta\in\Big[\tfrac25,\;2\Big],\qquad
\text{geometric centre }\sqrt{\tfrac25\cdot2}=\sqrt{\tfrac45}=\frac{2}{\sqrt5}=0.894427\ldots,
\qquad \text{log-width }\ln\!\frac{2}{2/5}=\ln5.$$

Three framework-level facts fall out of this one box. **(i)** The multiplicative error budget of
chaining spans exactly a factor $5$ ($\tfrac25\to2$), and its logarithm is $\ln5$ — the same
$5$ that sits under $\kappa_{\text{Frenet}}\in[\tfrac12,\sqrt5]$ and inside $\varphi$; the
inversion comb hands the pipeline an error band whose width is set by the manifold's defining
integer, not by any free parameter. **(ii)** The band is **log-centred on $2/\sqrt5$**, the
reciprocal of the golden mean's surd part, so the "average" multiplicative bias of a blind
chaining step is not $1$ but $2/\sqrt5\approx0.894$ — a systematic $\sim11\%$ deficit per leg,
the coarse-grained shadow of the trough-weighting (consistent with the period-mean envelope
$\langle\operatorname{osc}\rangle=1/\sqrt2$ the constraints permit as a label). **(iii)** The
infimum sits on the diagonal $a=b$: the **worst** under-counting of any multi-leg transport is a
path that revisits the *same* ordinal depth twice — a self-energy / round-trip segment — which
is precisely the configuration a naïve path tracer hits on a back-scatter or a closed shell-cascade
loop. The additive law $\kappa(2a)$ corrects it; the product undercounts it by the maximal $\tfrac52$.
