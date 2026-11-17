# 00 — The Spine: κ as Inverse Temporal Flow

*Foundation note. Everything in this directory builds on the four results below.
All numerics verified to machine precision — see `verify/verify_spine.py`.*

---

## The claim

The κ coupling function and "inverse temporal flow" are not two pillars of the
framework that need to be joined. They are one object — the conserved current of
the base manifold — seen along two axes. This note makes the join structural.

## 1. The temporal axis lives inside the manifold

Base worldline:

$$\mathbf{r}(t) = \left(\sin t,\; \tfrac12\sin 2t,\; \cos t\right), \qquad y = xz.$$

The $x,z$ coordinates ride the unit cylinder — **spatial circulation**. The $y$
coordinate is the *product* $y=xz$ riding the hyperbolic paraboloid. We promote
$y$ to its physical role:

> **$y$ is the temporal axis. Time is the bilinear coupling of the two spatial
> circulations**, not an independent coordinate. The saddle $y=xz$ is the
> statement that time is emergent — as a bilinear form on space.

## 2. Conserved chronon current (exact)

Areal current about the temporal axis:

$$L_y \;\equiv\; \big(\mathbf{r}'\times\mathbf{r}''\big)\cdot\hat{\mathbf y}
\;=\; \dot z\,\ddot x - \dot x\,\ddot z
\;=\; \sin^2 t + \cos^2 t \;=\; 1 \quad\text{identically.}$$

This is conservation of **chronon flux** about the temporal axis — the first
exact conservation law the manifold hands us, and it is conservation of
*temporal flow*, not energy or momentum. The "binormal middle component = 1"
note in the base-manifold file was hiding a Noetherian fact. Define
$j_\chi \equiv L_y$; then $dj_\chi/dt = 0$ is the continuity equation for time.

## 3. Curvature / torsion = gravity / temporal flow

Frenet invariants of the curve ($u = \cos^2 2t$):

$$\kappa_{\text{Frenet}}(t) = \frac{\sqrt{5-3u}}{(1+u)^{3/2}} \in[\tfrac12,\sqrt5],
\qquad
\tau_{\text{Frenet}}(t) = \frac{-3\cos 2t}{5-3u}.$$

By the fundamental theorem of curves, $(\kappa,\tau)$ completely determine the
worldline. Assignment:

- **$\kappa_{\text{Frenet}}$ (in-plane bending) = gravitational / spatial-coupling
  strength.** Everywhere positive. In ordinal-sampled form it *becomes* the
  coupling function $\kappa(r)$.
- **$\tau_{\text{Frenet}}$ (out-of-plane twist) = temporal flow rate $\Phi$, and
  it is *signed*** ($\tau\propto-\cos 2t$):

$$\boxed{\;\Phi(t)\equiv\tau_{\text{Frenet}}(t):\quad
\Phi>0\Rightarrow\text{forward (entropic) flow},\quad
\Phi<0\Rightarrow\text{inverse (gravitational) flow}.\;}$$

The strict complementarity from the manifold file becomes the central dynamical
statement: **$\kappa_{\text{Frenet}}$ is maximal exactly where
$\tau_{\text{Frenet}}=0$** (saddle peaks, $u=0$), and vice versa.

> **"Gravity *is* inverse temporal flow," made precise:** at the saddle peaks the
> net temporal flow $\Phi$ passes through zero while spatial bending hits its
> maximum $\sqrt5$. The conserved unit $L_y=1$ has been fully converted from
> temporal flow into spatial curvature. Gravity is most intense exactly at the
> turning point where forward flow reverses into inverse flow — identical, not
> merely correlated.

## 4. The coupling function inherits the flow — retarded / advanced split

Golden-ordinal sampling $t_k=k\ln\varphi$ gives the parameter-free shell coupling

$$c(k) = \frac{1}{1+\cos^2(2k\ln\varphi)}\,e^{-k/\varphi}.$$

The forward κ we render with is the **retarded** branch ($e^{-k/\varphi}$, the
arrow of time). Inverse temporal flow is the **advanced** branch — the same
kernel continued to negative ordinal, $e^{+k/\varphi}$ — a solution that *grows
toward the source*, the signature of attraction. Even/odd split:

$$G_{\text{sym}}(k)=\tfrac12[\kappa(+k)+\kappa(-k)]
=\frac{\cosh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}
\quad\text{(standing chronon mode / correlation, }G_{\text{sym}}(0)=\tfrac12),$$

$$G_{\text{flow}}(k)=\tfrac12[\kappa(+k)-\kappa(-k)]
=\frac{-\sinh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}
\quad\text{(net temporal flow / gravity, }G_{\text{flow}}(0)=0).$$

Hyperbolic invariant (the shell-space echo of $L_y=1$):

$$G_{\text{sym}}^2 - G_{\text{flow}}^2 = \frac{1}{\big(1+\cos^2(2k\ln\varphi)\big)^2}.$$

**Ordinal depth is rapidity in temporal-flow space**, boost angle
$\theta_k=k/\varphi$. Each shell descended is a fixed hyperbolic boost $1/\varphi$
deeper into inverse flow.

### Flow-reversal lattice

The resonant orbits coincide three ways — verified exactly:

$$k_n=\frac{(2n-1)\pi}{4\ln\varphi}\approx 1.632,\,4.896,\,8.161,\dots$$

are *simultaneously* (i) coupling-factor maxima ($\cos\to0$, factor $\to1$),
(ii) torsion zeros, and (iii) temporal-flow reversals. These are the **inversion
shells** — the gravitational skeleton of the stack. This is why the oscillation
is structural and must never be smoothed: smoothing deletes the flow-reversal
lattice.

## 5. Shell gravitational potential, written in κ

$$V_{\text{grav}}(n) = -\sum_{m<n} G_{\text{flow}}(n-m)\,\rho_m
= \sum_{m<n}\frac{\sinh\!\big((n-m)/\varphi\big)}{1+\cos^2\big(2(n-m)\ln\varphi\big)}\,\rho_m,$$

with $\rho_m$ the chronon density (shell occupation). The $\sinh$ growth toward
the source is the attractive well; the oscillatory denominator imprints the
inversion-shell terraces. Gravity and the rendering kernel emerge from one
expression by a sign choice on a single exponent.

---

## One-line summary

> One conserved current $L_y=1$, partitioned by the saddle into curvature
> (gravity) and signed torsion (temporal flow), sampled into κ where the
> partition becomes the retarded/advanced split: inverse flow
> $=-\sinh(k/\varphi)$, forward correlation $=\cosh(k/\varphi)$, on the shared
> oscillatory flow-reversal lattice $k_n$.

## Open branches (developed in sibling notes)

01 flow continuity · 02 effective metric & Wick rotation · 03 advanced-propagator
gravity · 04 inversion-shell spectroscopy · 05 thermodynamics & arrow of time ·
06 quantum bounce / two-sheeted time · 07 torsion–spin (Einstein–Cartan) ·
08 cosmology & dark flow · 09 transport reciprocity.
