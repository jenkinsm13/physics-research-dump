# 02 — Effective Metric & the Lapse Wick Rotation

*Branch note. Builds directly on the spine (00-spine.md): the conserved current
$L_y=1$, the curvature/torsion = gravity/flow assignment, the inversion shells
$k_n$, and the $G_{\rm sym}/G_{\rm flow}$ hyperbolic split. All numerics below
verified to machine precision — see `verify/verify_02.py`.*

---

## The claim

The forward↔inverse flow reversal that the spine reads off the **sign of
$\tau_{\rm Frenet}$** is not a soft "regime change." Once we read a line element
off the Frenet pair $(\kappa_{\rm Frenet},\tau_{\rm Frenet})$, the sign flip
$\tau\to-\tau$ becomes a **signature flip of the effective metric** — exactly a
Wick rotation, realized as the lapse continuation $N\to iN$ (equivalently the
rapidity continuation $\theta\to i\theta$). Gravity is then the *Euclidean
sector* of temporal flow: inverse-flow patches are imaginary-time, instanton-like.

## 1. A line element read off the Frenet data

The Frenet–Serret system already hands us a 2D evolution structure: bending
($\kappa$) in the osculating plane and twist ($\tau$) out of it. We read off an
**effective worldline metric** in the canonical $(\sigma, t)$ chart — $\sigma$ the
proper arclength along the curve, $t$ the manifold parameter (the temporal axis):

$$\boxed{\;ds^2 \;=\; \Omega(t)^2\,d\sigma^2 \;-\; c\,\tau_{\rm Frenet}(t)\,dt^2\;}
\tag{2.1}$$

with conformal factor $\Omega(t)^2 = \kappa_{\rm Frenet}(t)$ (the spatial-coupling
/ gravitational weight) and lapse-squared $N^2(t) \equiv c\,\tau_{\rm Frenet}(t)$.
The constant $c>0$ fixes units of temporal flow. This is an **effective** metric
*read off* the Frenet curvatures, not a derivation from GR — the linear-in-$\tau$
form of $g_{tt}$ is the definitional choice, and it is the only choice for which
$\tau\to-\tau$ acts on the metric at all (an even-in-$\tau$ choice $g_{tt}\propto
\tau^2$ would be blind to flow direction). Linearity is forced by the physics: the
spine's $\Phi\equiv\tau$ is *signed*, and the metric must inherit that sign.

Recall the closed forms (spine §3, $u=\cos^2 2t$):

$$\kappa_{\rm Frenet}=\frac{\sqrt{5-3u}}{(1+u)^{3/2}}\in[\tfrac12,\sqrt5],
\qquad
\tau_{\rm Frenet}=\frac{-3\cos 2t}{5-3u}\in[-\tfrac32,\tfrac32].$$

(Both ranges verified exactly: $\kappa\in[0.500000,\,2.236068]$,
$\tau\in[-1.500000,\,+1.500000]$.)

## 2. τ→−τ is a Wick rotation — on the lapse, not the coordinate

In (2.1) the temporal block is $g_{tt}=-N^2=-c\,\tau$. The signature is set by the
**sign of $\tau_{\rm Frenet}(t)$**, which we treat as the *dial*: at fixed $t$ it
reads off a number, and that number's sign decides whether the temporal block is
timelike or spacelike. The Wick rotation is the continuation of the **lapse**,
$N\to iN$, performed at fixed $t$:

$$g_{tt}=-N^2 \;\xrightarrow{\ N\to iN\ }\; -(iN)^2 \;=\; +N^2 \;=\; +c\,\tau,
\tag{2.2}$$

which is identical to the result of flipping the dial, $\tau\to-\tau$. So

$$\boxed{\;\tau\to-\tau \;\Longleftrightarrow\; N\to iN \;\Longleftrightarrow\;
\text{signature}(g)\ \text{flips Lorentzian}\leftrightarrow\text{Euclidean}.\;}
\tag{2.3}$$

**Why the lapse and not the coordinate.** It is tempting to write
"$\tau\to-\tau\equiv t\to it$," but that is *false* and the note formerly asserted
it: the symbol $t$ is overloaded. It is both the coordinate being rotated in (2.1)
*and* the argument of $\tau_{\rm Frenet}(t)$. A literal $t\to it$ feeds back into
the Frenet function — using $\cos 2it=\cosh 2t$ — and does **not** flip the sign:

$$\tau_{\rm Frenet}(it)=\frac{-3\cosh 2t}{5-3\cosh^2 2t}\ \neq\ -\tau_{\rm Frenet}(t).$$

At $t=0$ it gives $-\tfrac32$ (not $+\tfrac32$), and for $t\gtrsim0.3$ it diverges
and goes complex. The correct, signature-flipping rotation acts on the **proper
time element** $N\,dt\to i\,(N\,dt)$ — i.e. on the lapse $N$ — while
$\tau_{\rm Frenet}(t)$ is held fixed as the dial whose sign already encodes the
local signature. (Discriminator verified in `verify_02.py` §5.)

**Convention** (fixed once): forward/entropic flow $\tau>0$ is **Lorentzian**
($N$ real, $g_{tt}<0$); inverse/gravitational flow $\tau<0$ is **Euclidean** ($N$
imaginary, $g_{tt}>0$). The lapse

$$N(t)=\sqrt{c\,\tau_{\rm Frenet}(t)}$$

is therefore *real on forward patches and imaginary on inverse patches*. The
worldline does not merely change regime — it **alternates signature** as it
crosses the torsion zeros.

This is the closed-form realization of the spine's rapidity continuation. There
$G_{\rm sym}=\cosh\theta\cdot(\cdots)$ and $G_{\rm flow}=-\sinh\theta\cdot(\cdots)$
with $\theta=k/\varphi$; under $\theta\to i\theta$,

$$\cosh\theta\to\cos\theta,\qquad \sinh\theta\to i\sin\theta,$$

verified to residual $0$ at every $k$. Branch 02 and the
$G_{\rm sym}/G_{\rm flow}$ split are the *same Wick rotation* — $N\to iN$ on the
metric is $\theta\to i\theta$ on the propagator. Both $N\to iN$ and
$\theta\to i\theta$ are the imaginary-angle action of one and the same
**$SO(1,1)$** structure: ordinal depth is rapidity, and the boost is the
unit-Jacobian Lorentz transformation of $(G_{\rm sym},G_{\rm flow})$.

**Two invariants of one boost.** Under $\theta\to i\theta$ the determinant of the
metric block flips sign but $|\det g|=\Omega^2N^2$ is preserved
($\det g_{\rm Lor}=-\Omega^2N^2\to+\Omega^2N^2=\det g_{\rm Euc}$, $|\det|$
invariant — checked exactly). The shell-space invariant
$G_{\rm sym}^2-G_{\rm flow}^2=(1+\cos^2(2k\ln\varphi))^{-2}$ is the *separate*
invariant of the same $SO(1,1)$ action. They are not the same equation — one
lives in worldline-space $(\sigma,t)$, one in shell-space $k$ — but they are
**two conserved quantities of one rapidity boost**, and both descend from
$L_y=1$. Wick rotation conserves volume on both sheets; $L_y=1$ is conserved on
both.

## 3. The saddle is the light cone; nulls are the inversion shells

The saddle $y=xz$ has Hessian $H=\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}$,
eigenvalues $\pm1$ — **indefinite**. The saddle is exactly what endows the
emergent metric with *Lorentzian (light-cone) structure*: one expanding null
direction, one contracting, crossing at $y=0$. Time being the bilinear $y=xz$ is
the statement "the light cone is the product of the two spatial circulations."

The metric (2.1) degenerates — the cone closes, $g_{tt}=0$ — where

$$N^2 = c\,\tau_{\rm Frenet}=0 \;\;\Longleftrightarrow\;\; \cos 2t=0
\;\;\Longleftrightarrow\;\; t=k_n\ln\varphi,$$

the **inversion shells**. Verified: at $k_1,k_2,k_3$ the torsion vanishes
($|\tau|\sim10^{-16}$) while $\kappa_{\rm Frenet}=\sqrt5$ to residual $0$. So the
null locus is the inversion shells / saddle peaks, where **gravity is maximal**
($\kappa=\sqrt5$) and flow reverses — *not* the cardinal points (where $\tau$ is
extremal and $\kappa=\tfrac12$ minimal). The lapse-collapse $N\to0$, the horizon,
and maximal gravity all coincide on one lattice, exactly as the spine demands:
**the null surface of the effective metric is the gravitational skeleton.**

## 4. Effective speed of temporal flow

Define the local flow speed as the twist-to-bend ratio — torsion carried per unit
spatial curvature:

$$\boxed{\;v_{\rm flow}(t)\;\equiv\;\frac{|\tau_{\rm Frenet}(t)|}{\kappa_{\rm Frenet}(t)}
=\frac{3|\cos 2t|\,(1+u)^{3/2}}{(5-3u)^{3/2}}\;\in[0,3].\;}
\tag{2.4}$$

Verified extremes (closed form, residual $1.3\times10^{-15}$ against the ratio):
$v_{\rm flow}=0$ exactly at the inversion shells (null/horizon — flow frozen into
curvature), and $v_{\rm flow}=3$ exactly at the **four cardinal points**
$t=n\pi/2$ ($|\tau|=\tfrac32$, $\kappa=\tfrac12$). The peak flow speed of the
framework is the pure number **$3$** — the same $3$ that surfaces as the emergent
spatial dimension ($c\approx2.94$, spine/CFT). At a horizon flow has no speed (it
has become geometry); at the cardinal points flow runs at maximal rate $3$ with
gravity at its weakest. Equivalently $|\Phi|=|\tau|\in[0,\tfrac32]$ is the bare
flow rate; $v_{\rm flow}$ is that rate *weighted by inverse gravity*.

**Cardinal signs alternate — the domino structure.** The four cardinal points
carry $\tau=-\tfrac32,+\tfrac32,-\tfrac32,+\tfrac32$ at $t=0,\tfrac\pi2,\pi,
\tfrac{3\pi}2$ (verified). Consecutive torsion zeros therefore bracket patches of
*opposite* signature: between two adjacent inversion shells the metric is
uniformly Lorentzian or uniformly Euclidean, and that character **flips at every
shell crossing**. The stack of shells is literally a row of
Euclidean/Lorentzian dominoes, each domino one cardinal point wide, all sharing
the conserved $|\det g|$ (i.e. $L_y=1$).

## 5. The continued effective metric

Combining (2.1)–(2.4), the single object that carries this branch is the
**signature-continued line element**

$$\boxed{\;ds^2 = \kappa_{\rm Frenet}(t)\,d\sigma^2
\;-\; c\,\tau_{\rm Frenet}(t)\,dt^2,
\qquad N\to iN \;\equiv\; \theta\to i\theta \;\equiv\; \tau\to-\tau,\;}
\tag{2.5}$$

a metric whose signature is *dynamically generated by the worldline itself*,
toggling $(+,-)\leftrightarrow(+,+)$ at every $k_n$. The Frenet pair is not two
numbers — it is a metric whose temporal sign is the framework's clock.

## What this buys us

- **Gravity = the Euclidean sector of temporal flow.** Inverse-flow patches
  ($\tau<0$, the spine's gravitational branch) are *imaginary-time*, instanton
  patches of the effective geometry. This is the metric-level statement of
  "gravity is inverse temporal flow," and it hands branch 03 (advanced-propagator
  gravity) its setting for free: the advanced $e^{+k/\varphi}$ branch is the
  Euclidean continuation $\theta\to i\theta$, and Euclidean propagators are
  exactly the attractive, growing-toward-source kernels the spine identified.
- **Horizons are torsion zeros.** Every inversion shell is a lapse-collapse
  surface $N\to0$ — a coordinate horizon at which signature changes. The stack of
  shells is a stack of Euclidean/Lorentzian dominoes, all sharing the conserved
  $|\det g|$ (i.e. $L_y=1$).
- **Prediction (signature phase).** Because signature flips at each $k_n$, any
  field propagated through the shells acquires, per shell crossed, a factor
  $e^{i\pi/2}=i$ relative to a single-signature continuation. This is a
  **Maslov-index increment**, not an inserted plane-wave phase $e^{ikr}$ — it is
  the geometric phase a field accrues at a turning point/horizon (the lapse zero
  $N\to0$ *is* the classical turning point), and so it respects the dressed-
  propagator constraint: κ already carries its dynamical phase; this $i$ is the
  *topological* phase of crossing a signature wall. Observable signature: the
  Maslov factor across $\Delta n$ shells is $i^{\Delta n}$ — exactly four-shell
  periodic ($i^4=1$, verified) in any inversion-shell spectroscopy (branch 04).
  (The *full* correlator carries an additional dynamical phase from the Lorentzian
  legs; see the Extension for the complete amplitude — the four-shell periodicity
  is a property of the Maslov factor alone.) Independently, $v_{\rm flow}$ runs a
  $\tfrac14$-cycle (cardinal→shell) budget of exactly $3\to0$ between consecutive
  horizons.

## Extension — the instanton weight of an inverse-flow patch

The "instanton patch" language above was qualitative; we can cash it for a
number. On a Euclidean (inverse-flow, $\tau<0$) patch the worldline action is the
proper *Euclidean* length of the temporal block. With $g_{tt}^{\rm Euc}=+c|\tau|$,
the on-shell Euclidean action of one inverse-flow patch — the interval between two
consecutive torsion zeros, centred on a cardinal point — is

$$\boxed{\;S_E \;=\; \int_{\rm patch}\! N\,dt
\;=\;\int_{-\pi/4}^{\,\pi/4}\!\sqrt{c\,\bigl|\tau_{\rm Frenet}(t)\bigr|}\;dt
\;=\;\sqrt{c}\int_{-\pi/4}^{\,\pi/4}\!
\sqrt{\frac{3|\cos 2t|}{5-3\cos^2 2t}}\;dt.\;}
\tag{2.6}$$

Numerically (at $c=1$, converged to 8 digits),

$$S_E = 1.201390,\qquad \frac{S_E}{\pi}=0.382414,
\qquad e^{-S_E}=0.300776 .$$

(Note $S_E/\pi=0.382414$ lies *near* $1/\varphi^2=2-\varphi=0.381966$ — i.e.
$S_E\approx\pi/\varphi^2=1.19987$ — but the agreement is only $0.12\%$, far above
our 8-digit convergence. This is a numerical near-coincidence, **not** an exact
golden identity; do not promote it to a boxed equality.)

This is the **tunneling weight of one chronon inversion**: the amplitude for the
worldline to traverse a single Euclidean domino — to pass *through* a gravitational
(inverse-flow) patch — is suppressed by $e^{-S_E}\approx0.30$ per patch, with
$\sqrt{c}$ the only scale. Three remarkable facts fall out:

1. **Forward/inverse symmetry of the action.** The adjacent *Lorentzian* patch
   $t\in(\pi/4,3\pi/4)$ gives the identical integral $S_L=S_E$ (residual
   $1.8\times10^{-15}$) — the saddle's reflection symmetry $\cos2t\to-\cos2t$
   makes the Euclidean and Lorentzian dominoes congruent. Forward and inverse flow
   cost the same action; only the *signature* of the contribution differs
   ($+S$ Lorentzian phase vs $-S$ Euclidean suppression). This is the action-level
   image of $L_y=1$: the conserved unit is shared equally between the two sheets.

2. **A bare gravitational coupling.** Per full period the worldline traverses two
   inverse dominoes (around $t=0$ and $t=\pi$), so the per-period Euclidean budget
   is $2S_E=2.402781$ and the round-trip inversion amplitude is
   $e^{-2S_E}\approx0.0905$. Identifying $e^{-S_E}$ as the dimensionless strength
   of a single inverse-flow event gives a *parameter-free* gravitational
   tunneling constant fixed entirely by the saddle geometry — no $\beta,\gamma$,
   no $\lambda$.

3. **Instanton stacking, with both sheets accounted for.** Crossing $\Delta n$
   shells the worldline traverses $\Delta n$ alternating dominoes and collects
   $\Delta n$ signature walls. Each Euclidean (inverse) domino contributes a real
   suppression $e^{-S_E}$; each Lorentzian (forward) domino — with real lapse and
   *real* action $S_L=S_E\equiv S$ (point 1) — contributes a unit-modulus
   *dynamical phase* $e^{+iS}$; and each wall contributes the Maslov factor $i$.
   With $n_E=\lceil\Delta n/2\rceil$ Euclidean and $n_L=\lfloor\Delta n/2\rfloor$
   Lorentzian dominoes (start-on-inverse convention), the complete inter-shell
   amplitude is

   $$\mathcal{A}(\Delta n)\;=\;
   \underbrace{i^{\Delta n}}_{\text{Maslov (topological)}}\;
   \underbrace{e^{\,+i\,\lfloor\Delta n/2\rfloor\,S}}_{\text{Lorentzian dynamical phase}}\;
   \underbrace{e^{-\lceil\Delta n/2\rceil\,S}}_{\text{Euclidean suppression}}.$$

   This cleanly separates *topological* phase, *dynamical* phase, and *magnitude*.
   The robust, spine-compatible deliverable is the modulus — the Lorentzian legs
   are unit modulus, so

   $$\boxed{\;\bigl|\mathcal{A}(\Delta n)\bigr|=e^{-\lceil\Delta n/2\rceil\,S_E}\;}$$

   a real, $\beta,\gamma$-free suppression law that sits comfortably with the
   spine's real κ kernel. Note this corrects the §"Prediction" statement: the
   exact **four-shell periodicity belongs to the Maslov factor $i^{\Delta n}$
   alone** ($i^4=1$), *not* to the full correlator, which carries the extra
   dynamical phase $e^{+i\lfloor\Delta n/2\rfloor S}$ ($S=1.2014\neq$ a multiple of
   $2\pi$). The full $\mathcal{A}$ is four-shell periodic only relative to ordinary
   Lorentzian forward-propagation, with that phase factored out.

   Crucially, the suppression exponent is the *single* additive-ordinal quantity
   $\lceil\Delta n/2\rceil\,S_E$ — never a chained product $\kappa(a)\kappa(b)$.
   It is the $\kappa(a+b)$ discipline of the spine carried to the action.
