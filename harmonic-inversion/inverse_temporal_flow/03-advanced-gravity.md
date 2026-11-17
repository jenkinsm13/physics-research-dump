# 03 — Gravity from the Advanced Branch (Wheeler–Feynman on the Shell Stack)

*Branch note. Builds directly on `00-spine.md`: the conserved current $L_y=1$,
the $\kappa/\tau$ split, the even/odd kernels $G_{\text{sym}}/G_{\text{flow}}$,
the inversion shells $k_n$. All numerics here are verified to machine precision
(residuals $\sim 10^{-16}$); the checking script lives outside the repo tree.*

---

## The Wheeler–Feynman dictionary on the stack

In the spine we split the golden-ordinal kernel into a standing (even) mode and a
flow (odd) mode by continuing $\kappa$ to negative ordinal:

$$G_{\text{sym}}(k)=\frac{\cosh(k/\varphi)}{1+\cos^2(2k\ln\varphi)},\qquad
G_{\text{flow}}(k)=\frac{-\sinh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}.$$

Read these as a Wheeler–Feynman absorber theory living on the ordinal axis. The
**retarded** half $\kappa(+k)\propto e^{-k/\varphi}$ is *radiation* — the outgoing
arrow of time. The **advanced** half $\kappa(-k)\propto e^{+k/\varphi}$ is
*gravity* — the response of the absorber, the piece that grows toward the source.
The physical interaction is the time-symmetric half-sum, exactly as in
Wheeler–Feynman: neither branch alone is observable; their symmetric combination
is. The absorber condition (the future shells must fully absorb the outgoing
chronon flux) is automatically satisfied because $G_{\text{flow}}(0)=0$ — there is
no self-force at the source shell, the WF requirement made structural.

The hyperbolic invariant $G_{\text{sym}}^2-G_{\text{flow}}^2=(1+\cos^2)^{-2}$ is
the absorber's statement of $L_y=1$: the unit chronon current is conserved under
the boost that mixes radiation into gravity, ordinal depth playing the rôle of
rapidity $\theta_k=k/\varphi$. (This boost structure is made into a group law in
the **Extension** below — and it is exactly why the kernel composes additively in
ordinal, $\kappa(a+b)$, never multiplicatively.)

## The half-difference is the physical force law

The new object this branch needs is the **half-difference**, the purely
attenuating combination that an absorber re-radiates as a static field:

$$\boxed{\,\Psi(k)\;\equiv\;G_{\text{sym}}(k)-\big|G_{\text{flow}}(k)\big|
\;=\;\frac{\cosh(k/\varphi)-\sinh(k/\varphi)}{1+\cos^2(2k\ln\varphi)}
\;=\;\frac{e^{-k/\varphi}}{1+\cos^2(2k\ln\varphi)}\,.}$$

This identity is exact (verified: $\Psi(k)\,(1+\cos^2)=e^{-k/\varphi}$ to
$\sim10^{-16}$ at $k=0,1,1.632,3,5$). It is the central equation of this note and
it is genuinely new: it says the *static gravitational kernel* is precisely the
bare retarded coupling $e^{-k/\varphi}$ riding the inversion-shell lattice — the
$\cosh$ correlation and the $\sinh$ flow cancel down to the single decaying
exponential. Gravity is what is left when radiation and absorption interfere.
Note the decay rate of the static field is the **intrinsic rapidity rate**
$\lambda=1/\varphi$ — *not* $\ln\varphi$. This single fact fixes the slope of the
force law below, and it is where the branch departs from naïve Newton.

## Continuum limit: ordinal decay becomes a radial power law

Map ordinal to radius by $r=r_0\varphi^{\,n}$, so $n=\log_\varphi(r/r_0)$ and
$\ln(r/r_0)=n\ln\varphi$. A fixed ordinal step is a fixed *ratio* in $r$ — the
stack is self-similar, geometric, scale-free. Therefore **any ordinal exponential
becomes a radial power law**:

$$e^{-\alpha n}=\big(r/r_0\big)^{-\alpha/\ln\varphi}
\quad\Longrightarrow\quad p=\frac{\alpha}{\ln\varphi}\ \ (\text{radial exponent}).$$

The oscillatory factor $1/(1+\cos^2(2k\ln\varphi))$ is **never replaced** — it is
described at two resolutions. At shell resolution it is kept exactly (the terraces
below). On scales $\gg$ one shell the *leading* term of the potential is its
period-average, with the lattice reinstated as the fine structure on top; this is
a coarse/fine dual description, not a smoothing-away. The exact period-average is

$$\Big\langle\frac{1}{1+\cos^2 x}\Big\rangle_{[0,\pi]}=\frac{1}{\sqrt2}
\qquad(\text{verified }0.70710678,\ \text{res }10^{-16}),$$

so the leading (shell-averaged) continuum potential sourced by a point chronon at
the origin, decaying at the intrinsic rate $\alpha=\lambda=1/\varphi$, is

$$\Phi(r)=-\frac{1}{\sqrt2}\,\big(r/r_0\big)^{-1/(\varphi\ln\varphi)},
\qquad \frac{1}{\varphi\ln\varphi}=1.284328\ldots$$

The fitted slopes confirm this exactly: $d\ln|\Phi|/d\ln r=-1.28433$ and the field
$g=-\partial_r\Phi$ goes as $r^{-2.28433}$. The leading-coefficient
$G_{\text{eff}}=1/\sqrt2$ comes from the period-average envelope **alone**; the
source self-coupling $c(0)=\tfrac12$ is a *separate* number (the $m=n$ diagonal
term of the shell sum) and is not to be conflated with $G_{\text{eff}}$.

## Where Newton sits — the framework's law, and a *conjectured* limit

This is the sharpest point of the branch, and it must be stated cleanly. The
advanced-branch static law that the kernel **actually derives** is

$$\boxed{\,\Phi(r)\propto r^{-\nu},\qquad
\nu\equiv\frac{\lambda}{\ln\varphi}=\frac{1}{\varphi\ln\varphi}=1.2843\,}$$

— steeper than Newton, set robustly by the intrinsic rapidity rate
$\lambda=1/\varphi$. This is not adjustable: it follows from $\Psi(k)\propto
e^{-k/\varphi}$ and the self-similar radius map, both exact.

Newtonian $1/r$ would require ordinal decay $\alpha=\ln\varphi$ instead of
$\lambda=1/\varphi$ — i.e. radial exponent $p=\alpha/\ln\varphi=1$. We do **not**
claim to have derived this: setting $\alpha=\ln\varphi$ and reading off $p=1$ is
arithmetic, not a result (the check "passes" because it cannot fail). Newton is
therefore offered as a **conjectured large-scale limit**, contingent on one
explicit, currently *unproven* hypothesis:

> **Absorber-completeness hypothesis (H1).** When the future shells absorb the
> outgoing chronon flux *completely*, the effective static decay constant
> renormalizes from the bare rapidity rate $\lambda=1/\varphi$ to the geometric
> rate $\ln\varphi$, i.e. $\lambda_{\text{eff}}\to\ln\varphi$, yielding
> $p\to 1$ and $\Phi_N=-G_{\text{eff}}M/r$ with $G_{\text{eff}}=1/\sqrt2$ in
> shell units.

Under H1 the slope is exactly $-1$ (potential) and $-2$ (field) by construction.
The honest status: **the framework predicts $r^{-1.2843}$; Newtonian $r^{-1}$ is a
limit it can reach only if H1 holds.** The gap $\nu-1\approx0.284$ is then not a
correction *to* Newton but the signature of *incomplete* absorption — the regime
where H1 has not yet kicked in. Deriving H1 (a renormalization of $\lambda$ by the
absorber sum) is the open task this branch hands to note 05.

## The inversion-shell terraces

On scales comparable to a shell the oscillation is kept exactly and the potential
develops terraces at the inversion ordinals
$k_n=(2n-1)\pi/(4\ln\varphi)\approx 1.632,\,4.896,\,8.161$, where the kernel
denominator hits its minimum and $\Psi$ spikes to its envelope. These are the
spine's torsion-zero / flow-reversal **ordinals**. Their *radial images* under
$r=r_0\varphi^{\,n}$ are

$$r_n=r_0\,\varphi^{\,k_n},\qquad
\frac{r_{n+1}}{r_n}=\varphi^{\,\pi/(2\ln\varphi)}=e^{\pi/2}=4.8105.$$

So gravity is terraced in fixed multiplicative steps of $e^{\pi/2}$: a logarithmic
ladder of gravitational shelves at $r_n\approx 2.19,\,10.55,\,50.75,\,244.2$
(in units of $r_0$). To be precise about the spine correspondence: these radii are
the **radial images of the inversion ordinals**, not the inversion ordinals
themselves — $k_n$ live on the ordinal axis (where torsion vanishes), and $r_n$ is
where those ordinals land once mapped through the geometric radius law. The
gravitational skeleton is the spine's flow-reversal lattice *seen in radius*.

## Prediction

1. **Short-scale steepening.** Below the absorber-completeness scale (H1 not yet
   in force) the advanced-branch potential follows $\Phi\propto r^{-1.2843}$, i.e.
   the force is $\sim 0.28$ steeper in log-slope than Newtonian. The crossover *is*
   the onset of full absorption — the operational definition of H1's scale.
2. **Terraced lensing.** Light deflection $\alpha_{\text{defl}}\,b=4/\sqrt2=2.828$
   (in shell units, $\Phi=-(1/\sqrt2)/r$) acquires periodic enhancements at the
   $e^{\pi/2}$-spaced inversion radii — a geometric comb in the deflection-versus-
   impact-parameter curve, a clean signature distinguishing this from a smooth
   halo.
3. **Saturating gravitational redshift.** The net-flow fraction
   $f(n)=|G_{\text{flow}}|/G_{\text{sym}}=\tanh(n/\varphi)$ is the redshift
   envelope. The **discrete shell increment** $\Delta f(0\!\to\!1)=+0.550$; the
   *continuous* rate is $f'(n)=\operatorname{sech}^2(n/\varphi)/\varphi$
   ($=0.431$ at $n=1$), so the saturation toward $f\to1$ goes as
   $\propto\operatorname{sech}^2(n/\varphi)$ — complete conversion of temporal flow
   into curvature at deep shells, the $L_y=1$ unit fully spent. The horizon is
   where $\tanh\to1$: gravity has eaten all the time.

## Extension — Ordinal composition *is* rapidity addition (the $\kappa(a+b)$ law derived)

The spine asserts that ordinal depth is rapidity $\theta_k=k/\varphi$. We can now
promote this from a label to a **group law**, and in doing so *derive* the hard
constraint that the kernel must compose by adding ordinals, never by multiplying
couplings.

Strip the oscillatory weight $w(k)=1/(1+\cos^2(2k\ln\varphi))$ and collect the two
hyperbolic modes into a **chronon two-vector** on the ordinal axis:

$$\mathbf{V}(k)\equiv w(k)^{-1}\big(G_{\text{sym}}(k),\,-G_{\text{flow}}(k)\big)
=\big(\cosh(k/\varphi),\,\sinh(k/\varphi)\big).$$

This is a unit timelike vector in $(1{+}1)$-dimensional flow-space: its Minkowski
norm is the de-weighted $L_y=1$ echo,

$$\mathbf{V}(k)\cdot\eta\,\mathbf{V}(k)=\cosh^2-\sinh^2=1\quad\forall k\
(\text{verified }10^{-16}),\qquad \eta=\mathrm{diag}(+,-).$$

Descending one ordinal step $k\to k+\delta k$ acts on $\mathbf{V}$ as a Lorentz
**boost** of rapidity $\delta k/\varphi$:

$$\Lambda(\theta)=\begin{pmatrix}\cosh\theta&\sinh\theta\\
\sinh\theta&\cosh\theta\end{pmatrix},\qquad
\boxed{\,\Lambda(k_1/\varphi)\,\mathbf{V}(k_2)=\mathbf{V}(k_1+k_2)\,}$$

— verified to $\lesssim10^{-15}$ at $(k_1,k_2)=(1,2),(1.632,3.264),(0.5,4.896)$.
The boost group composes by **adding rapidities**,
$\Lambda(\theta_1)\Lambda(\theta_2)=\Lambda(\theta_1+\theta_2)$, hence ordinals add:

$$\theta(k_1)+\theta(k_2)=\frac{k_1+k_2}{\varphi}=\theta(k_1+k_2).$$

This is the structural reason the kernel **must** be evaluated at $\kappa(a+b)$ and
never as $\kappa(a)\kappa(b)$: a two-leg path is a *composition of boosts*, which
adds rapidities (adds ordinals), whereas multiplying two couplings would multiply
their oscillatory weights, landing on the wrong lattice. Concretely, for
$(k_1,k_2)=(1.632,3.264)$ the additive weight is $w(k_1{+}k_2)^{-1}=
1+\cos^2(2\cdot4.896\ln\varphi)=1.000$, while the product weight is
$w(k_1)^{-1}w(k_2)^{-1}=2.000$ — a factor-of-two error and a *different shelf* of
the flow-reversal lattice. The prohibition is no longer a rule imposed from
outside; it is the statement that the absorber stack carries a representation of
the $(1{+}1)$ Lorentz group, and only the additive composition stays inside it.

**Corollary (boost-covariant force law).** Because $\Psi(k)=w(k)\,e^{-k/\varphi}$
and $e^{-k/\varphi}=\cosh(k/\varphi)-\sinh(k/\varphi)$ is the *light-cone null
projection* $\tfrac1{\sqrt2}(1,-1)\cdot\mathbf{V}(k)$, the static gravitational
kernel is the projection of the chronon two-vector onto the **incoming null ray**
of flow-space. Gravity is literally the shadow the chronon worldline casts on the
advanced light-cone — the half-difference of §2 re-read as a null projection, and
manifestly invariant in form under every ordinal boost (each boost merely slides
the projection point one rapidity $1/\varphi$ deeper). The decay rate of the
static field is thus pinned to $\lambda=1/\varphi$ *by the boost geometry itself*,
which is why $\nu=1/(\varphi\ln\varphi)$ — not $1$ — is the bare law, and why
recovering Newton genuinely requires the separate renormalization hypothesis H1.
