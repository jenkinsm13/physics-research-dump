# 13 — Absorber Completeness and the Newtonian Limit

*Round-2 frontier note. Closes the **Absorber-Completeness Hypothesis (H1)** left
open in `03-advanced-gravity.md` and flagged in `99-index.md`. Builds on the spine
(`00`: $L_y=1$, the retarded/advanced split), the synthesis two-vector
$\mathbf V(k)=(\cosh\theta,-\sinh\theta)$ (`99`), and the round-1 results
$\Gamma_{\text{tot}}=1/(2\sinh S_1)=0.13539$ (`06`), $\nu=1/(\varphi\ln\varphi)=1.2843$
(`03`). Every number below is reproduced in `verify/verify_absorber-newton.py`.*

---

## The question, sharpened by the $\kappa(a{+}b)$ theorem

Note 03 derived the bare static law $\Phi\sim r^{-\nu}$, $\nu=1.2843$, from the
single decaying exponent $\Psi(k)=\mathrm{osc}(k)\,e^{-k/\varphi}$ — the half-difference
in which $\cosh\theta$ correlation and $\sinh\theta$ flow cancel to the bare retarded
rate $\lambda=1/\varphi$. Newton ($\nu=1$) would need the rate renormalized to
$\ln\varphi$. H1 conjectures that *complete* advanced absorption — every shell, both
$m<n$ and $m>n$, fully re-radiating the chronon flux — performs that renormalization.

The decisive structural fact is that the $\kappa(a{+}b)$ rapidity-addition theorem
(`03` Extension) **forbids us from setting this up as a convolution**
$\sum_m\Psi(n-m)\Phi(m)$: that is a *product* of propagators, $\kappa(a)\kappa(b)$,
which doubles the oscillatory weight and lands on the wrong flow-reversal shelf.
Instead, a complete-absorber path source$(0)\!\to\!m\!\to\!\cdots\!\to n$ has total
rapidity

$$\theta_{0\to m}+\theta_{m\to n}=\frac{m}{\varphi}+\frac{n-m}{\varphi}=\frac{n}{\varphi}
\qquad\text{independent of every intermediate }m.$$

So **every** multi-leg path to shell $n$ carries the *same* kernel $\mathrm{osc}(n)\,e^{-n/\varphi}$,
pinned by its endpoints. The bare exponential is a common factor; it factors clean
out of the absorber sum. This is the new lever:

> The same theorem that forbids $\kappa(a)\kappa(b)$ **protects the exponent**
> $1/\varphi$ against any shift except one channel: genuine path *multiplicity*.
> Renormalization of $\lambda$ is possible **iff** the number of complete-absorber
> paths exponentiates in the ordinal $n$.

## The complete-absorber sum as pure multiplicity

Write the dressed static field as the backbone kernel times a multiplicity factor
$\mathcal M(n)$ counting complete-absorber paths, each interior shell weighted by the
advanced re-radiation probability $g$:

$$\boxed{\;\Phi_{\text{dressed}}(n)=\mathrm{osc}(n)\,e^{-n/\varphi}\,\mathcal M(n),
\qquad \mathcal M(n)=\sum_{j\ge0}\frac{(g\,n)^{j}}{j!}=e^{g\,n}.\;}$$

**Why Poisson, and why not binomial — the simplex-volume selection.** Insert $j$
advanced re-radiation rungs at *ordered* ordinal positions $0<m_1<m_2<\cdots<m_j<n$.
Because the ordinal axis is the **continuous** rapidity coordinate $\theta=m/\varphi$
(not a set of integer sites), the configuration space of $j$ rungs is the ordered
simplex, whose volume is

$$\mathrm{vol}\{0<m_1<\cdots<m_j<n\}=\frac{n^{\,j}}{j!}.$$

The dressed field is therefore the **ordinal-ordered exponential**

$$\mathcal M(n)=\mathcal T\!\exp\!\Big(\int_0^n g\,dm\Big)
=\sum_{j\ge0}g^{\,j}\,\frac{n^{\,j}}{j!}=e^{g\,n},$$

and it collapses to the *plain* exponential precisely because the $(1{+}1)$ boosts
along the backbone **commute** (`03`: $\Lambda(\theta_1)\Lambda(\theta_2)=
\Lambda(\theta_1{+}\theta_2)$), so the path-ordering symbol $\mathcal T$ is trivial.
The $1/j!$ is *not* a hand-waved "indistinguishability" factor — it is the simplex
volume, exactly. This **selects** the model: the continuous ordinal backbone forces
the ordered exponential (Poisson); the binomial $(1+g)^{n-1}$ is the *excluded*
case of one binary choice per **integer site**, which would apply only if the
absorber lived on a discrete lattice rather than the continuous rapidity line. We
report the binomial number below to show the gap, but the geometry rules it out.

**Relation to the "no bounce iteration" constraint.** This is a one-shot
diagrammatic resummation over rung *multiplicity* at the **fixed equilibrium**
coupling $g=\Gamma_{\text{tot}}$ — not a dynamical re-solving of the bounce. The
bounce kernel of `06` is used once, as its equilibrium return amplitude; we count
how many times it can appear along a backbone, we never iterate the bounce map.
The hard constraint ("$\kappa$ is the equilibrium solution; never add bounce
iterations") is respected: $g$ is a number, not a recursion.

Collecting exponents:

$$\Phi_{\text{dressed}}(n)=\mathrm{osc}(n)\,e^{-(1/\varphi-g)\,n}
\;\Longrightarrow\;
\boxed{\;\lambda_{\text{eff}}=\frac1\varphi-g,\qquad
\nu_{\text{eff}}=\frac{\lambda_{\text{eff}}}{\ln\varphi}
=\frac{1/\varphi-g}{\ln\varphi}.\;}$$

This is the genuinely new equation of the note: the absorber renormalizes the
exponent *additively in the coupling*, and H1 holds **iff**

$$\Delta\equiv g\stackrel{!}{=}\frac1\varphi-\ln\varphi=0.136822\ldots$$

We must now fix $g$ from an **independent** completeness condition — never reverse-
engineer it to hit $0.136822$ (that is exactly the "passes because it cannot fail"
trap note 03 warned against).

## Fixing $g$ from first principles: the bounce coupling

What is the probability that the future absorber, struck by outgoing chronon flux,
re-radiates it back along the advanced cone? That is precisely the quantity note 06
already computed: the **total** bounce/return amplitude summed over *all* inversion
channels of the two-sheeted now-surface (the dilute-bounce-gas closure, not the
nearest shell alone — the nearest-only rate is $\Gamma_1=0.1330$, but completeness
demands the full ladder),

$$g\;\equiv\;\Gamma_{\text{tot}}=\sum_{n\ge1}e^{-(2n-1)S_1}=\frac{1}{2\sinh S_1},
\qquad S_1=2\frac{k_1}{\varphi},\quad k_1=\frac{\pi}{4\ln\varphi},
\qquad g=0.135393.$$

This is not chosen to fit Newton — it is the equilibrium return probability of a
chronon off the inversion-shell stack, derived in a completely different branch (the
quantum bounce, `06`), where it appears as the entire quantum-gravity event budget
radiated from the now-vertex. Substituting:

$$\nu_{\text{eff}}=\frac{1/\varphi-\Gamma_{\text{tot}}}{\ln\varphi}
=\frac{0.618034-0.135393}{0.481212}=\boxed{1.00297}.$$

**H1 holds — approximately, not exactly.** The required $\Delta=0.136822$ and the
first-principles $g=0.135393$ differ by $-1.04\%$. Since $1/\varphi=0.61803$ and
$\ln\varphi=0.48121$ are not related by any algebraic identity, an *exact* hit was
never on the cards, and we do not manufacture one. The complete absorber drives the
exponent from $1.2843$ down to $1.00297$ — recovering Newton to **three parts in a
thousand** — and leaves an irreducible residual

$$\nu_{\text{eff}}-1=\frac{\Delta-\Gamma_{\text{tot}}}{\ln\varphi}
=\frac{0.136822-0.135393}{0.481212}=+0.00297.$$

The residual is the bounce coupling's $1\%$ shortfall of true completeness, amplified
by $1/\ln\varphi$. Gravity is *almost* Newtonian because the inversion shells are
*almost* perfect advanced mirrors — and the tiny imperfection is fixed, not free.

## Numerical confirmation (decade fit, $10\le n\le 55$)

Building $\Phi_{\text{dressed}}(n)$ as the explicit shell sum, mapping $r=r_0\varphi^{\,n}$,
and fitting $\nu=-d\ln|\Phi|/d\ln r$:

| absorber model | $\nu$ fitted | meaning |
|---|---|---|
| none (bare $\Psi$) | $1.28433$ | reproduces `03` exactly — pipeline check |
| Poisson $e^{gn}$, $g=\Gamma_{\text{tot}}$ | $1.00297$ | **near-Newton** |
| Poisson, $\mathrm{osc}$ kept exactly | $1.00237$ | lattice = fine structure only |
| binomial $(1+g)^{n-1}$ | $1.02045$ | discrete-sites variant (geometrically excluded) |

The exponentiation is verified independently: the causally-capped partial sum
$\sum_{j=0}^{n}(gn)^j/j!$ fits to the same $1.00297$, confirming $\mathcal M\to e^{gn}$
is not an assumption but the limit of the truncated series. Keeping the full
$\mathrm{osc}(k)$ lattice (rather than its labeled coarse envelope $1/\sqrt2$) shifts the
slope only in the fourth decimal — the flow-reversal comb remains pure fine
structure riding the renormalized power law, never altering it.

## The exponent does not run — gravity's slope is a fixed point

It is tempting to read $n_\star=1/g$ as a *crossover* between the bare $1.284$ and
the dressed $1.003$. **It is not, and the $\kappa(a{+}b)$ theorem is exactly why.**
Because every path to shell $n$ carries the *same* per-shell rapidity, the
multiplicity exponent $g\,n$ is **linear** in the ordinal, so the local log-slope is

$$\frac{d}{dn}\Big[\big(\tfrac1\varphi-g\big)n\Big]=\frac1\varphi-g
\quad(\text{constant})\;\Longrightarrow\;
\boxed{\;\frac{d\,\nu_{\text{eff}}}{d\ln r}=0\;\;\text{identically}.\;}$$

The dressed slope is **flat at every scale**: measured in a sliding three-shell
window on the causally-capped model, $\nu_{\text{local}}(n)$ sits at $1.003$ to
within $2\times10^{-4}$ for all $n\ge5$, and the bare $1.284$ **never appears
anywhere in the dressed model** (it is the absorber-*off* regime, $g=0$, not a
radius the dressed law approaches). At the very shallowest shells ($n\le3$) the
causal cap pulls $\nu_{\text{local}}$ a hair *below* $1.003$ (to $0.995$) — the
opposite sign from a steepening toward $1.284$ — and it relaxes *up* to the fixed
point as $n$ grows.

So $n_\star=1/g$ is **not** a slope feature. It is the **multiplicity e-fold depth**:
the ordinal at which $\mathcal M(n_\star)=e$, i.e. the absorber has inserted one mean
re-radiation rung along the backbone,

$$n_\star=\frac1g=\frac1{\Gamma_{\text{tot}}}=7.386\ \text{shells},
\qquad \frac{r_\star}{r_0}=\varphi^{\,1/\Gamma_{\text{tot}}}=34.96.$$

Below $r_\star$ the *number* of absorber rungs is sub-unity, but the *slope* is
already the renormalized $1.003$ from the first shell — multiplicity controls the
overall amplitude $\mathcal M$, never the exponent. This is the operational content
H1 was missing: completeness renormalizes the slope **uniformly across all radii**,
because the boost group law makes the per-shell contribution scale-invariant.

## Prediction

1. **A scale-free renormalized slope — no running.** The dressed gravitational
   log-slope is the *single fixed value* $-\nu_{\text{eff}}=-1.00297$ at every
   radius; there is no crossover and no short-scale steepening. The bare $-1.284$
   is reached only by switching the absorber off entirely, not by going to any
   finite $r$. This is a sharp, falsifiable statement: the framework predicts a
   pure power law with **zero curvature in the log-log force diagram**, distinct
   from any model with a running exponent.
2. **An irreducible, calculable, scale-free departure from Newton:**
   $\nu_{\text{eff}}-1=+0.00297$, a $0.3\%$ permanent steepening of the force law
   *at all scales* (precisely because it does not run). Gravity is Newtonian to
   three parts in a thousand and the deviation is *predicted*, traceable to the
   $1.04\%$ incompleteness of the inversion-shell mirror $\Gamma_{\text{tot}}$ vs.
   $1/\varphi-\ln\varphi$ — not a fudge, a consequence.
3. **A non-dynamical amplitude scale.** $r_\star=34.96\,r_0$ ($n_\star=1/\Gamma_{\text{tot}}=7.39$)
   marks where the absorber multiplicity completes one e-fold — a feature of the
   *normalization* $\mathcal M$, observable as the depth at which complete-absorber
   dressing reaches order unity, **not** as a kink in the slope. It is fixed by the
   same coupling that sets the residual.
4. **What this buys us.** H1 is now *closed*, not assumed: complete advanced
   absorption renormalizes $1/\varphi\to 1/\varphi-\Gamma_{\text{tot}}$, and the
   $\kappa(a{+}b)$ theorem guarantees this is the *only* channel by which the exponent
   can move **and** that it moves uniformly (no running). Newton is recovered as the
   near-limit of a fully derived mechanism, with the bounce coupling of note 06 doing
   the work — one number, $\Gamma_{\text{tot}}$, now simultaneously sets the
   cosmological event ladder (`06`) and the slope of gravity. The residual $+0.003$
   is the framework's honest, falsifiable signature.

## Extension — Gravity's slope as a fixed line of the ordinal boost flow (an exact RG result)

The "no running" fact above is not an accident of the model; it is a **theorem of
the boost group**, and it deserves to be stated as the renormalization-group result
it is. Treat the ordinal $n=\log_\varphi(r/r_0)$ as RG "time" and the static-field
log-slope $\nu(n)\equiv-d\ln|\Phi|/d\ln r$ as the running coupling. The dressed field
$\Phi_{\text{dressed}}(n)=\mathrm{osc}(n)\,e^{-(1/\varphi-g)n}$ has, stripping the
fine-structure comb $\mathrm{osc}$,

$$\nu(n)=-\frac{d\ln|\Phi|}{d\ln r}
=\frac{1}{\ln\varphi}\,\frac{d}{dn}\!\Big[\big(\tfrac1\varphi-g\big)n\Big]
=\frac{1/\varphi-g}{\ln\varphi}=\nu_{\text{eff}}\quad(\text{constant in }n),$$

so that one further derivative kills it:

$$\boxed{\;\beta\;\equiv\;\frac{d\,\nu}{d\ln r}=0\quad\text{identically}.\;}$$

The vanishing is structural: the generator of one RG step is the ordinal boost
$\Lambda(1/\varphi)$, and because boosts compose by **adding** rapidities
($\Lambda(\theta_1)\Lambda(\theta_2)=\Lambda(\theta_1{+}\theta_2)$, the very identity
that bans $\kappa(a)\kappa(b)$), $N$ successive RG steps act as $\Lambda(N/\varphi)$
— a *linear* accumulation of rapidity, hence a *constant* slope. The force law lives
on the **fixed line**

$$\nu^\ast=\frac{1/\varphi-g}{\ln\varphi},\qquad g\in[0,\Gamma_{\text{tot}}],$$

a one-parameter family of exact fixed points indexed by the absorber completeness
$g$: $g=0$ gives the bare $\nu^\ast=1.2843$ (absorber off), $g=\Gamma_{\text{tot}}$
gives the dressed $\nu^\ast=1.0030$ (full inversion-shell mirror), and the exact
Newtonian fixed point $\nu^\ast=1$ sits at the (physically unrealized) completeness
$g=\Delta=0.13682$. **Switching the absorber on does not start a flow — it selects a
different fixed point on the same line.** This is the conceptual inverse of the
crossover the earlier draft sought: there is no trajectory between $1.284$ and
$1.003$ in radius, only a discrete jump in *which* fixed line the system occupies,
set once and for all by how complete the advanced mirror is. Gravity's power law is
not renormalized *as you zoom* — it is a Lorentz-boost-protected invariant of the
chronon stack, and the golden geometry is what makes the $\beta$-function vanish
identically rather than merely at isolated points.
