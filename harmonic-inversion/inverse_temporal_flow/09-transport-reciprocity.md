# 09 — Transport Reciprocity: What the Advanced Branch Means for Light

*Builds directly on the spine (note 00). The retarded κ is the kernel we render
with; here we read the **advanced** branch physically and show that Helmholtz
reciprocity is nothing but the even ($G_\text{sym}$) part of the spine split,
while the odd ($G_\text{flow}$) part is the exact, quantified measure of
non-reciprocity. Numerics confirmed to machine precision — script run in `/tmp`,
not committed; confirmed numbers embedded below.*

---

## 1. Source↔camera swap *is* the ±k exchange

A renderer can be run two ways. **Forward (light) transport** propagates radiance
from the source to the eye; **adjoint (importance) transport** propagates
*importance* from the eye back to the source — this is the path-from-the-camera
that every backward path tracer actually computes. The spine already gave us the
two branches of one kernel:

$$\kappa(k)=\frac{e^{-k/\varphi}}{1+\cos^2(2k\ln\varphi)},\qquad
\kappa(-k)=\frac{e^{+k/\varphi}}{1+\cos^2(2k\ln\varphi)}.$$

The identification is structural, not analogical:

$$\boxed{\;\text{light flows }+k\ (\text{retarded, source}\to\text{eye}),\qquad
\text{importance flows }-k\ (\text{advanced, eye}\to\text{source}).\;}$$

The source↔camera swap of light-transport theory is *exactly* the
retarded↔advanced exchange $k\leftrightarrow-k$ of the temporal-flow framework.
Because $\kappa$ is already the **equilibrium (dressed-propagator) solution**, the
adjoint transport is not a new computation: it is the *same kernel evaluated at
$-k$*. No new machinery, no inserted phase $e^{ikr}$, no bounce iteration — the
intermediate scattering is summed once and the swap is a single sign flip on the
ordinal-depth exponent (the rapidity $\theta=k/\varphi$).

## 2. Helmholtz reciprocity = evenness = $G_\text{sym}$

Helmholtz reciprocity states the BRDF is symmetric under swapping incoming and
outgoing directions: $f_r(\omega_i\to\omega_o)=f_r(\omega_o\to\omega_i)$. In our
kernel that swap is $k\to-k$, so the reciprocal content is the **even** part:

$$G_\text{sym}(k)=\tfrac12[\kappa(k)+\kappa(-k)]
=\frac{\cosh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}
\quad(\text{even, }G_\text{sym}(0)=\tfrac12).$$

The standing chronon mode *is* the reciprocal kernel: $G_\text{sym}(-k)=G_\text{sym}(k)$
identically, so any transport built from $G_\text{sym}$ alone satisfies Helmholtz
reciprocity exactly. The familiar textbook reason — "optical distance
$d(P,Q)=d(Q,P)$ is symmetric, so $\kappa(d)$ is reciprocal" — is just the *spatial
shadow* of this evenness. The temporal reading is the deeper one: reciprocity is
the statement that the net chronon flow about the time axis vanishes, i.e. that we
sit on the $L_y=1$ standing mode with no drift.

## 3. The odd part is the *exact* non-reciprocity

The piece that breaks the swap is the **odd** $G_\text{flow}$:

$$G_\text{flow}(k)=\tfrac12[\kappa(k)-\kappa(-k)]
=\frac{-\sinh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}
\quad(\text{odd, }G_\text{flow}(0)=0).$$

This is the equilibrium-violating, non-reciprocal current. It vanishes identically
in equilibrium ($k=0$) — and **that is why thermal/equilibrium light transport is
reciprocal**: detailed balance kills the odd branch. Non-reciprocity is not put in
by hand; it is precisely the advanced–retarded asymmetry of the chronon flow.

## 4. New result — the lattice-free non-reciprocity ratio

The genuinely new equation of this note. Form the *fractional* non-reciprocity by
dividing the odd by the even part. The oscillatory denominator
$D(k)\equiv1/(1+\cos^2 2k\ln\varphi)$ is common to *both* branches —
$G_\text{sym}=D\cosh(k/\varphi)$, $G_\text{flow}=-D\sinh(k/\varphi)$ — so it
**cancels exactly** in the ratio (this is analytic, not a numerical coincidence):

$$\boxed{\;\mathcal{R}(k)\equiv\frac{G_\text{flow}(k)}{G_\text{sym}(k)}
=-\frac{\sinh(k/\varphi)}{\cosh(k/\varphi)}=-\tanh\!\frac{k}{\varphi}.\;}$$

Three consequences, all confirmed numerically (max residual
$1.11\times10^{-16}$ over inversion shells $k_n$, cardinal points, and generic
ordinals — every test point agrees with $-\tanh(k/\varphi)$ to the last bit):

1. **The non-reciprocity ratio is independent of the flow-reversal lattice.**
   Even at an inversion shell $k_1=(2{\cdot}1-1)\pi/(4\ln\varphi)=1.6321$ where the
   oscillatory factor $D$ is maximal ($=1$) and at the cardinal ordinals
   $k=m\pi/(2\ln\varphi)$ where it is minimal ($=\tfrac12$), $\mathcal{R}$ takes
   the *same* value as the smooth $-\tanh$ of rapidity. Verified at the *exact*
   shells (not the rounded $1.632$): at $k_1=1.6321$,
   $\mathcal{R}=-0.765228=-\tanh(k_1/\varphi)$ to residual $0$; at $k_2=4.8964$,
   $\mathcal{R}=-0.995306$ to $1.11\times10^{-16}$. The lattice modulates
   *amplitude* (correlation strength $D$) but not the *degree of non-reciprocity*.
   Reciprocity is a property of rapidity alone.

2. **$\mathcal{R}=-\tanh(\theta)$ is the relativistic velocity↔rapidity relation**
   with $\theta=k/\varphi$. The fractional non-reciprocity *is* the drift velocity
   $\beta=v/c$ of the net chronon flow. The small-ordinal slope is *exactly*

   $$\left.\frac{\mathrm d\mathcal{R}}{\mathrm dk}\right|_0
   =-\frac1\varphi\operatorname{sech}^2(0)=-\frac1\varphi=-0.618034,$$

   no approximation: each shell descended adds a fixed boost $1/\varphi$ in
   rapidity, exactly the spine's "ordinal depth = rapidity."

3. **Limits tie to the physics, analytically.** $\mathcal{R}$ is *odd*, so
   $\mathcal{R}(0)=0$ identically — perfect reciprocity at the self-cell, locking
   to the self-emission term $c(0)=\tfrac12$: own-cell coupling is purely a
   standing mode, light and importance agree exactly. And
   $\mathcal{R}(k)\to-1$ as $k\to\infty$ (confirmed $-1.00000000$ already at
   $k=50$): deep advanced transport is **fully** non-reciprocal — pure attraction
   toward the source, the gravitational/inverse-flow regime.

Equivalently, the absolute reciprocity *defect* is also lattice-free:

$$\frac{|\kappa(k)-\kappa(-k)|}{\kappa(k)+\kappa(-k)}=\Big|\tanh\frac{k}{\varphi}\Big|,$$

confirmed exactly (e.g. $k=3$: defect $0.952131$ vs $|\tanh(3/\varphi)|=0.952131$,
residual $0$). And the forward/adjoint pair reconstructs from the shared kernel,
$\kappa(\pm k)=G_\text{sym}(k)\pm G_\text{flow}(k)$, to $\sim6\times10^{-15}$.

## 5. What an "inverse-time render" computes

Running the kernel at $-k$ is the importance/adjoint pass. Concretely:

$$L_\text{fwd}(P)=\int L_\text{src}(Q)\,\kappa\big(+d_\text{opt}(P,Q)\big)\,V(P,Q)\,\mathrm dQ,
\qquad
W_\text{adj}(Q)=\int W_\text{eye}(P)\,\kappa\big(-d_\text{opt}(P,Q)\big)\,V(P,Q)\,\mathrm dP.$$

The visibility $V$ and optical distance $d_\text{opt}$ are geometric and symmetric
(reciprocal by construction); the only directional content is the sign of the
ordinal exponent. The advanced kernel $\kappa(-k)=e^{+k/\varphi}/(1+\cos^2)$ *grows
toward the source* — which is exactly what importance must do: it concentrates on
the paths that reach the light, the adjoint of attraction. Forward and adjoint
estimators are guaranteed consistent because they are one $L_y=1$ standing mode
($G_\text{sym}$) plus an antisymmetric drift ($G_\text{flow}$) that integrates to
the same measured radiance — bidirectional path tracing is the empirical statement
that $G_\text{sym}$ is shared and $G_\text{flow}$ cancels on a closed light↔eye
loop.

## Extension — non-reciprocities compose by relativistic velocity addition

The note above *names* the rapidity structure ($\mathcal{R}=-\tanh\theta$,
$\theta=k/\varphi$) but stops short of its sharpest consequence: a **composition
law**. Rapidities are additive over ordinal depth (the spine's $\kappa(a+b)$ rule:
a two-leg ordinal path of depths $a$ then $b$ is one kernel at depth $a+b$). Since
$\tanh$ does *not* add but composes by the relativistic addition formula, the
non-reciprocities of consecutive ordinal segments compose as velocities:

$$\boxed{\;\mathcal{R}(k_a+k_b)
=\frac{\mathcal{R}(k_a)+\mathcal{R}(k_b)}{1+\mathcal{R}(k_a)\,\mathcal{R}(k_b)}.\;}$$

This is the velocity-addition law $\beta=(\beta_a+\beta_b)/(1+\beta_a\beta_b)$ for
the chronon drift, and it follows in one line from
$\tanh(\theta_a+\theta_b)=(\tanh\theta_a+\tanh\theta_b)/(1+\tanh\theta_a\tanh\theta_b)$
with $\theta=k/\varphi$. Verified to machine precision (max residual
$1.11\times10^{-16}$): e.g. $\mathcal{R}(1)=-0.549758$ and $\mathcal{R}(2)=-0.844330$
compose to

$$\frac{-0.549758-0.844330}{1+(-0.549758)(-0.844330)}=-0.952131=\mathcal{R}(3),$$

and the inversion-shell pair composes too — $\mathcal{R}(k_1)=-0.765228$ with the
next-resonance gap gives the deeper shell's ratio exactly.

**This *derives* the hard constraint.** The framework forbids chaining
$\kappa(a)\cdot\kappa(b)$ for a two-leg path and mandates $\kappa(a+b)$. Here is
*why*, physically: the directional (non-reciprocal) content of transport is a
drift velocity, and drift velocities **add relativistically** — they do not
multiply. A product $\kappa(a)\kappa(b)$ would impose the relativistically *wrong*
composition (multiplying $\beta$'s, which over-saturates and breaks the $|\beta|<1$
bound), whereas $\kappa(a+b)$ enforces exactly the $\tanh$-addition the geometry
demands. The forbidden-product rule is not a bookkeeping convention; it is the
chronon-drift velocity-addition theorem. Two contact-scale segments
($\beta\approx k/\varphi$ each) add to $\approx(k_a+k_b)/\varphi$ at leading
order — reciprocity defects accumulate *linearly* in the near field and only
saturate toward $\beta\to1$ in the deep (gravitational) shells, precisely the
monotone deepening of §"What this buys us."

## What this buys us

- **A reciprocity dial with a closed form.** The non-reciprocity defect at ordinal
  depth $k$ is exactly $|\mathcal{R}(k)|=\tanh(k/\varphi)$, and it grows
  *monotonically* with depth. At the self-cell ($k=0$) it is zero — transport is
  perfectly reciprocal. In the near field ($k\!\lesssim\!1$) it rises *linearly*,
  $|\mathcal{R}|\approx k/\varphi$, so own-cell and first-neighbour transport are
  reciprocal to first order. It reaches $\tanh(1/\varphi)\approx0.55$ by $k=1$ and
  saturates to full non-reciprocity ($\to1$) only in the deep, multiply-scattered
  (gravitational) shells. This is a free correctness check on a path tracer:
  measure $L_\text{fwd}-W_\text{adj}$; it must scale as $k/\varphi$ at small ordinal
  separation and approach the symmetric-part magnitude as $k$ grows.

- **Prediction.** Build a bidirectional renderer on the chronon kernel and deliberately
  drop $G_\text{flow}$ (use $G_\text{sym}$ only): the image is *exactly* Helmholtz-
  reciprocal and lattice-modulated, but it will be missing precisely the
  $\tanh(k/\varphi)$-weighted directional bias that shows up as a faint, monotonic
  brightening of light-facing surfaces relative to eye-facing ones — strongest in
  the deep multiply-scattered (high-$k$) regime, vanishing at contact. That bias is
  the optical fingerprint of inverse temporal flow inside a rendered scene, and its
  magnitude is fixed with no free parameters: $-\tanh$ of the rapidity $k/\varphi$.
