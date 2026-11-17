# 01 — Flow Continuity & the Chronon Noether Current

*Branch note. Builds directly on `00-spine.md`: the exact identity $L_y=1$, the
$\kappa_{\text{Frenet}}/\tau_{\text{Frenet}}$ split, the even/odd kernel halves
$G_{\text{sym}},G_{\text{flow}}$, and the inversion shells $k_n$. All numerics
re-verified this session; residuals embedded below.*

---

## 1. From a conserved number to a conserved current

The spine handed us a *number*: $L_y=(\mathbf r'\times\mathbf r'')\cdot\hat{\mathbf y}=1$.
We now promote it to a *current*. Define the chronon density on the shell stack
as the shell occupation $\rho_\chi(n,t)=E_n(t)$ (chronon energy resident in shell
$n$) and the chronon flux $j_\chi(n,t)$ as the net transfer crossing the
interface between shell $n$ and $n{+}1$. The discrete continuity equation we
demand is

$$\boxed{\;\partial_t\,\rho_\chi(n,t)+\big(\nabla\!\cdot j_\chi\big)(n,t)=0,\qquad
\big(\nabla\!\cdot j_\chi\big)(n)\equiv j_\chi(n)-j_\chi(n{-}1).\;}$$

The claim of this branch: the turbulence-application shell energy law

$$\frac{dE_n}{dt}=T_{n-1\to n}-T_{n\to n+1}-2\nu k_n^2 E_n+R_n(t)
\tag{1}$$

*is* this continuity equation, with the cascade transfers $T$ playing the role of
$-\nabla\!\cdot j_\chi$, the viscous term the only genuine sink, and the resonance
term $R_n$ the **advanced ($G_{\text{flow}}$) re-injection from depth**. The
conserved charge of the symmetry is exactly $L_y$.

## 2. The Noether symmetry: rotation of the hodograph

What symmetry produces $L_y$? Not a spatial rotation of $\mathbf r(t)$ — the
saddle $y=xz$ breaks that. It is a rotation of the **velocity's $xz$-projection**.
The hodograph component is

$$(\dot x,\dot z)=(\cos t,\,-\sin t),\qquad \dot x^2+\dot z^2=1\ \text{identically.}$$

The velocity's spatial part sweeps the **unit circle at unit angular rate** — a
manifest $U(1)$ symmetry about the temporal axis $\hat{\mathbf y}$. Its conserved
areal charge is precisely the binormal-$y$ component,

$$L_y=(\mathbf r'\times\mathbf r'')\cdot\hat{\mathbf y}
=\dot z\,\ddot x-\dot x\,\ddot z=\sin^2 t+\cos^2 t=1.$$

Verified: $\max|\dot x^2+\dot z^2-1|=2.22\times10^{-16}$, $\max|L_y-1|=2.22\times10^{-16}$,
and the hodograph charge holds at $+1.000000$ across the period. This is the
Noether statement: **uniform phase advance of the spatial circulation $\Leftrightarrow$
conservation of chronon flux about time.** Time is the angle conjugate to that
circulation; $L_y=1$ says the angle advances at unit rate — the clock never
stalls, never doubles. That is *why* time has a fixed local tick: it is a Noether
charge, not an external parameter.

## 3. Telescoping = continuity (the cascade is a divergence)

Write the transfer as an antisymmetric interface flux,
$T_{n\to n+1}=j_\chi(n)=g\sqrt{E_nE_{n+1}}$. Then the two cascade terms in (1) are
exactly $T_{n-1\to n}-T_{n\to n+1}=j_\chi(n{-}1)-j_\chi(n)=-(\nabla\!\cdot j_\chi)(n)$.
This is not an approximation: with the convention $j_\chi(-1)=j_\chi(N{-}1)=0$ at
the boundaries (no flux escapes the top or bottom of the stack), the discrete
divergence of the interface flux **is** the cascade term, sign-for-sign. Summing
the conservative part over the whole stack telescopes term-by-term:

$$\frac{d}{dt}\sum_n E_n=\underbrace{\sum_{n=0}^{N-1}\big[j_\chi(n{-}1)-j_\chi(n)\big]}_{=\,j_\chi(-1)-j_\chi(N-1)=0}
-\,2\nu\sum_n k_n^2E_n+\sum_n R_n(t).
\tag{2}$$

The bracketed sum collapses to a single boundary difference, which vanishes
identically by the no-flux condition — this is *why* the conservative part is a
pure divergence and can store no charge, independent of the state, the coupling
$g$, or the shell spacing. Integrating the **inviscid, unforced** stack
($\nu=0,\,R=0$) by RK4 over $N=12$ golden shells $k_n=\varphi^{\,n}$ confirms it
numerically:

$$\Big|\textstyle\sum_n E_n(T)-\sum_n E_n(0)\Big|=5.33\times10^{-15}
\quad(T=20,\ \Delta t=10^{-3}),\qquad \textstyle\sum_n(\nabla\!\cdot j_\chi)(n)=0\ \text{exactly.}$$

So the cascade moves chronon flux *between* shells without creating or destroying
it — the lattice analogue of $\partial_t\rho_\chi+\nabla\!\cdot j_\chi=0$. The
conserved $\sum_n E_n$ is the macroscopic descendant of the microscopic $L_y=1$:
**one conserved chronon charge, refined from the worldline to the whole stack.**

## 4. The resonance term is the advanced ($G_{\text{flow}}$) piece

Now restore $R_n$. The spine's $G_{\text{flow}}(d)=-\sinh(d/\varphi)/(1+\cos^2(2d\ln\varphi))$
is the *advanced* branch — it grows toward the source ($\sinh$), the signature of
attraction, and it is the **antisymmetric** half of $\kappa$. The cascade transfer
$T$, by contrast, is the *retarded/decaying* branch ($\propto e^{-\lambda|i-j|}$,
the arrow of time). These are the odd and even halves of the *one* kernel; we
never chain $\kappa(a)\kappa(b)$ — the depth simply adds in the argument.

Crucially, the spine's gravitational potential carries an **explicit minus sign** on
$G_{\text{flow}}$: $V_{\text{grav}}(n)=-\sum_{m<n}G_{\text{flow}}(n-m)\rho_m=
+\sum\sinh(\cdot)/(1+\cos^2(\cdot))\,\rho_m>0$, the attractive well. The
re-injection inherits that same sign so that "pump from depth" is a genuine
*source*, not a drain:

$$\boxed{\;R_n=-\,r\!\sum_{m\neq n}\!G_{\text{flow}}(|n-m|)\,E_m
=\,r\!\sum_{m\neq n}\frac{\sinh(|n-m|/\varphi)}{1+\cos^2(2|n-m|\ln\varphi)}\,E_m.\;}$$

**No explicit phase is attached.** An earlier draft of this branch multiplied each
term by $\cos(\omega_{nm}t)$ with $\omega_{nm}=|n-m|\ln\varphi$; that is forbidden.
The flow-reversal lattice is *already encoded* in $G_{\text{flow}}$ through its
denominator $1+\cos^2(2|n-m|\ln\varphi)$ — a function of separation living on the
$\ln\varphi$ grid. Tacking on a second $\cos(\omega_{nm}t)$ built from the *same*
$\ln\varphi$ grid re-introduces a phase the dressed propagator has already
absorbed (HARD CONSTRAINT: $\kappa$ is a dressed propagator, never add $e^{ikr}$).
The depth-dependence belongs in the argument of $\kappa$, not in a separate
oscillator. Removing it leaves the lattice exactly where it should be — inside the
kernel — and has a clean payoff: the advanced weight $-G_{\text{flow}}$ is
**positive for every $d=|n-m|>0$** (verified: $-G_{\text{flow}}(1..5)=
\{0.496,1.407,1.608,3.730,10.86\}$), so $R_n$ is now *unconditionally* a source,
shell by shell, with no in-phase caveat. $R_n$ is literally the advanced
propagator acting as a re-injection between shells.

For a definite, reproducible check take the seeded state
$E_m=\text{Uniform}[0.5,1.5]$ (NumPy default RNG, seed 0), $\nu=10^{-3}$,
$r=0.05$, $N=12$, $k_n=\varphi^n$. The verified instantaneous balance is

$$\frac{d}{dt}\sum_n E_n=-\underbrace{104.11}_{\text{dissipation }2\nu\sum k_n^2E_n}
+\underbrace{136.20}_{\text{advanced injection }\sum R_n}=+32.09,$$

while the conservative transfer contribution is $0$ to floating point (Sec. 3),
and every individual $R_n>0$ (verified). The arrow of time is the *net* sign:
retarded dissipation drains forward, advanced $R_n$ pumps backward from depth. For
this state the pump wins ($+32.09$); deeper or colder states ($\nu k_n^2$ large)
let dissipation win. The "now" is wherever they cross — the sign of the net is the
only thing that distinguishes forward from inverse time, and it is a *dynamical*
output, not an input.

## 5. The now-surface: where forward and inverse flow exchange

Forward flow is $\Phi=\tau_{\text{Frenet}}>0$; inverse flow is $\Phi<0$. They
exchange exactly where $\Phi=0$, i.e. $\cos 2t=0$ — the saddle peaks where
$\kappa_{\text{Frenet}}=\sqrt5$ is maximal. Mapped to ordinal time these are the
inversion shells

$$k_n=\frac{(2n-1)\pi}{4\ln\varphi}\approx 1.6321,\,4.8964,\,8.1606,
\qquad \Delta k=\frac{\pi}{2\ln\varphi}=3.264251,$$

verified to carry $\cos(2k_n\ln\varphi)\sim10^{-16}$ (torsion zero) and oscillation
factor $1/(1+\cos^2)=1.0$ exactly. The **now-surface is the flow-reversal lattice
itself**: a periodic comb of $L_y$-conserving turning points, equally spaced by
$\Delta k=\pi/(2\ln\varphi)$ in rapidity $\theta=k/\varphi$. At each comb tooth the
conserved unit $L_y=1$ is fully held as spatial curvature (gravity), momentarily
neither flowing forward nor back — the instant of "now," replicated down the stack.
At those teeth the spine's hyperbolic invariant tightens to
$G_{\text{sym}}^2-G_{\text{flow}}^2=1$ exactly (verified at $k_1$: $1.000000$),
the shell-space echo of $L_y=1$ standing at full strength precisely on the
now-surface.

## What this buys us

The arrow of time stops being an axiom and becomes a **balance condition**:
$\frac{d}{dt}\sum_n E_n = -2\nu\sum_n k_n^2 E_n + \sum_n R_n$, retarded drain
versus advanced pump on a shared golden lattice. **Prediction:** at any shell the
local time-arrow reverses sign precisely on the comb $k_n$, so a chronon-density
probe scanning ordinal depth should register a periodic flow-reversal signature
with fixed spacing $\Delta k=\pi/(2\ln\varphi)\approx3.2643$ — a measurable
golden-ratio fingerprint of the now-surface, independent of $\nu$, $r$, and the
shell amplitudes.

## Extension — the second Noether moment: a Green–Kubo chronon diffusivity

The first moment of the chronon current is $L_y=1$ (a charge). The *second*
moment turns the continuity law into a **transport law**. Model descent through
the stack as a random walk whose step weights are the forward (retarded) kernel
$c(k)=e^{-k/\varphi}/(1+\cos^2(2k\ln\varphi))$ — the only causal half, since the
advanced half $G_{\text{flow}}$ cannot set a finite correlation length (its
$\cosh$/$\sinh$ growth would diverge). Define the **chronon correlation length**
and the **stack diffusivity** as the normalised moments of $c$:

$$\tau_\chi=\frac{\int_0^\infty c(k)\,dk}{c(0)},\qquad
D_\chi=\tfrac12\,\operatorname{Var}_c(k)=\tfrac12\big(\langle k^2\rangle_c-\langle k\rangle_c^2\big),
\qquad \langle f\rangle_c\equiv\frac{\sum_k f(k)\,c(k)}{\sum_k c(k)}.$$

We use the **central** second moment — the variance of the step distribution — as
befits a random-walk diffusivity (the raw moment $\tfrac12\langle k^2\rangle_c$
would double-count the drift $\langle k\rangle_c$). Because $c(0)=\tfrac12$ exactly
(corpus self-coupling) these are pinned to the framework's own constants. Verified
numerically:

$$\int_0^\infty c(k)\,dk=1.109004,\qquad \tau_\chi=2.218008,\qquad
\langle k\rangle_c=1.34408,\quad \langle k^2\rangle_c=4.38479,\quad
\operatorname{Var}_c(k)=2.57824,\quad D_\chi=1.28912.$$

The oscillatory denominator leaves a clean fingerprint here too. Its period-mean
is $\langle 1/(1+\cos^2)\rangle=1/\sqrt2=0.707107$ exactly, so the flow-reversal
lattice **suppresses** the bare envelope integral $\int_0^\infty e^{-k/\varphi}dk=\varphi$
toward $\varphi/\sqrt2=1.14412$ (the measured $1.10900$ sits just below, the
residual coming from the $e^{-k/\varphi}$ weighting toward small $k$ where the
oscillation factor is nearer $1$). In one line:

$$\boxed{\;\int_0^\infty\!\frac{e^{-k/\varphi}}{1+\cos^2(2k\ln\varphi)}\,dk
\;\approx\;\frac{\varphi}{\sqrt2}\;=\;1.144,
\qquad D_\chi=\tfrac12\operatorname{Var}_c(k)=1.289.\;}$$

This is a **Green–Kubo relation for time itself**: the diffusivity of chronon
charge down the stack is fixed by the autocorrelation of the very kernel we render
with. It hands branch 09 (transport reciprocity) a ready-made Onsager
coefficient — $L_y=1$ sets the conserved current, $D_\chi=1.289$ sets how that
current spreads — and it gives the Sec.-5 prediction a *magnitude* to go with its
spacing: the flow-reversal comb is sharp on the scale $\tau_\chi\approx2.22$, just
under one inversion-shell gap $\Delta k\approx3.26$, so each "now" tooth is
resolved as a distinct event rather than washed into its neighbours.

The next branch (02) Wick-rotates this continuity law into an effective metric,
turning the conserved $L_y$ into the lapse function of emergent time and $D_\chi$
into the diffusion constant of the emergent proper-time coordinate.
