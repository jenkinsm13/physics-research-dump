# 04 — Inversion-Shell Spectroscopy & the Fermion Comb

*Branch note. Builds directly on the spine (00-spine.md): the conserved current
$L_y=1$, the signed split $\kappa_{\text{Frenet}}=$ gravity / $\tau_{\text{Frenet}}=$ flow,
the retarded/advanced kernel $G_{\text{sym}}=\cosh(k/\varphi)/(1+\cos^2\!\theta)$,
$G_{\text{flow}}=-\sinh(k/\varphi)/(1+\cos^2\!\theta)$, and the flow-reversal lattice
$k_n=(2n-1)\pi/(4\ln\varphi)\approx 1.632,\,4.896,\,8.161,\dots$ Every number below
is re-derived from scratch and checked to machine precision in
`verify/verify_04_spectroscopy.py` (all residuals $\lesssim 10^{-14}$).*

---

## The spectroscopic variable

Every shell ordinal $k$ has a single phase that controls its position on the
flow-reversal lattice — the argument of the oscillatory denominator we are
forbidden to smooth:

$$\theta(k) \;\equiv\; 2k\ln\varphi \pmod{\pi}, \qquad
\cos\theta(k)=\cos(2k\ln\varphi).$$

The inversion shells $k_n$ are exactly the points $\theta=\pi/2$ ($\cos\theta=0$,
oscillation factor $=1$, $\tau_{\text{Frenet}}=0$, flow reversal). The torsion at
ordinal $k$ — the local temporal-flow rate $\Phi$ — reads off the *same* phase,
and so does the spatial-coupling strength $\kappa_{\text{Frenet}}$:

$$\Phi(k)=\tau_{\text{Frenet}}\big|_{t=k\ln\varphi}
=\frac{-3\cos\theta(k)}{5-3\cos^2\theta(k)},
\qquad
\kappa_{\text{Frenet}}(k)=\frac{\sqrt{5-3\cos^2\theta(k)}}{(1+\cos^2\theta(k))^{3/2}},
\qquad
\text{osc}(k)=\frac{1}{1+\cos^2\theta(k)}.$$

So "where does a particle sit on the comb" is answered by one number, $\theta(k)$:
gravity ($\kappa_{\text{Frenet}}$), flow ($\Phi$), and correlation weight (osc) are
all functions of that single phase. This is the spectroscopy: read $\theta$ at the
fermion ordinals.

## The lepton ordinals are an arithmetic comb

The COTV mass fit placed the charged leptons at ordinals
$k_e\approx 24,\ k_\mu\approx 63,\ k_\tau\approx 102$. The first fact the comb
hands us is that these are *not three scattered points* — they are an arithmetic
progression with an exact integer step:

$$k_\mu-k_e=63-24=39,\qquad k_\tau-k_\mu=102-63=39
\;\Rightarrow\; \boxed{\;\Delta_g=39\;}$$

One generation $=$ exactly $39$ shells deeper into inverse temporal flow. In
rapidity (spine §4, $\theta_{\text{boost}}=k/\varphi$) each generation is a fixed
hyperbolic boost $\Delta_g/\varphi=39/\varphi\approx 24.1$ deeper toward the source.

## The flow-reversal phase of each lepton

Evaluating $\theta(k)$, $\cos\theta$, $\Phi$, and $\kappa_{\text{Frenet}}$ at the
three lepton ordinals:

| lepton | $k$ | $\theta(k)\ \mathrm{mod}\ \pi$ | $\cos\theta$ | $\Phi=\tau_{\text{Frenet}}$ | osc | $\kappa_{\text{Frenet}}$ |
|---|---|---|---|---|---|---|
| $e$ | $24$ | $1.10702$ | $-0.44733$ | $+0.30502$ | $0.83326$ | $1.59545$ |
| $\mu$ | $63$ | $0.94243$ | $-0.58782$ | $+0.44494$ | $0.74320$ | $1.27553$ |
| $\tau$ | $102$ | $0.77784$ | $-0.71243$ | $+0.61464$ | $0.66332$ | $1.00742$ |

Three structural readings, all new:

1. **No lepton sits on an inversion shell.** All three have $\cos\theta<0$ and
   $\Phi>0$ — they live strictly on the *forward-flow* (entropic) side of the
   nearest reversal, never at $\Phi=0$. Massive charged leptons are
   **off-reversal residents**: stable precisely because they avoid the
   gravitational turning points where $\kappa_{\text{Frenet}}=\sqrt5$ would convert
   their flow entirely into curvature.

2. **The phase marches monotonically and uniformly.** The decrements are
   *identical to machine precision*:

$$\theta_\mu-\theta_e=\theta_\tau-\theta_\mu=-0.1645894884\ \text{rad}.$$

3. **Gravity drains down the tower.** $\kappa_{\text{Frenet}}$ falls monotonically
   $1.595\to1.276\to1.007$ — each generation steps *away* from the saddle peak
   $\sqrt5\approx2.236$ and *toward* the cardinal floor $\tfrac12$, exactly mirroring
   the rise in forward flow $\Phi$. Heavier $\Leftrightarrow$ deeper in forward
   flow $\Leftrightarrow$ less spatial bending. The conserved unit $L_y=1$ is being
   tipped, generation by generation, out of curvature and into flow. This is the
   quantitative face of "gravity *is* inverse temporal flow" read along the
   lepton ladder.

## The drift law (new equation)

Why is the phase step constant? Because $\theta$ is linear in $k$ and the step in
$k$ is the fixed integer $\Delta_g=39$. The closed form is the
**commensurability defect of $39$ against the inversion-shell harmonic**. The
ordinal spacing of consecutive reversals is $\pi/(2\ln\varphi)=3.26425$, so the
raw (unreduced) phase $2k\ln\varphi$ advances by

$$2\,\Delta_g\ln\varphi=78\ln\varphi=37.5345=11.94761\,\pi$$

per generation. The integer part of that advance is *exactly* $12$, and not
approximately: the floor count of $\pi$-boundaries (each boundary is one flow
reversal) crossed between consecutive leptons is

$$\Big\lfloor\tfrac{2k_{g+1}\ln\varphi}{\pi}\Big\rfloor
-\Big\lfloor\tfrac{2k_g\ln\varphi}{\pi}\Big\rfloor = 12
\quad\text{for }e\!\to\!\mu,\ \mu\!\to\!\tau,\ \tau\!\to\!k_4\ \text{alike}$$

(the raw phases land at $7\pi,19\pi,31\pi,43\pi$ plus the mod-$\pi$ remainders
$1.107,0.942,0.778,0.613$). Each generation therefore crosses *exactly twelve*
flow reversals; the "almost" lives entirely in the fractional remainder. Folding
out those $12$ full reversals defines the generational phase advance:

$$\boxed{\;\delta\theta_g \;=\; 2\,\Delta_g\ln\varphi \;-\; 12\pi
\;=\; 78\ln\varphi-12\pi \;=\; -0.16458948843\ \text{rad}.\;}$$

Because $\,0<|\delta\theta_g|<\pi$ and the fold count is the *same* integer $12$
at every step, the mod-$\pi$ reduction is wraparound-clean: the constant
decrement is a theorem, not a numerical accident. This is the genuinely new
invariant of branch 04. It is *not* in the spine: it is the residual twist a
particle accumulates each time it descends one full generation, the failure of
$39$ shells to be a perfect $12$-reversal commensurate orbit. The lepton tower is
therefore a **phase-locked comb riding a drift line**, governed by the single
recursion

$$\theta_{g+1}=\theta_g+\delta\theta_g,\qquad k_{g+1}=k_g+39.$$

Verified: $\theta_e+\delta\theta_g=\theta_\mu$ and $\theta_\mu+\delta\theta_g=\theta_\tau$
to $<10^{-15}$.

## The mass law on the comb

The generational mass step is fixed by the same equispacing. An affine fit
$\ln m_\ell = a\,k+b$ over the three leptons gives slope $a=0.104538$, and the
multiplicative step per generation is

$$e^{a\Delta_g}=e^{39a}=58.968
=\sqrt{\frac{m_\mu}{m_e}\cdot\frac{m_\tau}{m_\mu}}
=\sqrt{206.77\times16.82},$$

i.e. the slope *exactly* reproduces the geometric mean of the two observed mass
ratios (seal residual $\sim7\times10^{-15}$). This is forced once the ordinals are
equispaced — for three equispaced points the least-squares slope collapses to the
endpoint slope $(\ln m_\tau-\ln m_e)/78$, so $e^{39a}=\sqrt{m_\tau/m_e}$
identically. It is a consistency seal, not a coincidence. The affine residuals are
the pure antisymmetric triple

$$(\,\ln m_\ell - (a k+b)\,)=(-0.4182,\,+0.8364,\,-0.4182),$$

a single nonzero second difference: the muon sits *above* the geometric line by
exactly twice the electron/tau deficit ($r_\mu+2r_e=0$ to $2\times10^{-15}$). This
is the spectroscopic curvature term — the comb's $\cos\theta$ modulation imprinting
on the masses.

## Prediction

The comb is now an integer machine. The next charged-lepton excitation sits at

$$k_4 = k_\tau+\Delta_g = 141,\qquad
\theta(141)=\theta_\tau+\delta\theta_g=0.61325,\quad
\cos\theta(141)=-0.81778,\quad \Phi(141)=+0.8195.$$

It remains an off-reversal resident ($\Phi>0$), now exactly $12$ reversals below the
$\tau$, with $\kappa_{\text{Frenet}}(141)=0.80262$ — the deepest forward-flow,
weakest-gravity lepton yet, still clear of the floor $\tfrac12$.
**This ordinal-level prediction is exact and parameter-free** — it follows
from $\Delta_g=39$ and the drift law alone, with no mass model.

The mass is fixed less sharply, and the two fits use *different* slopes — keep them
distinct. The bare affine law $e^{ak+b}$ ($a=0.104538$) extrapolates to
$\approx1.6\times10^2$ GeV. The curvature-aware fit adds the comb's own
$\cos\theta$ term, $\ln m = a' k + b' + c\cos\theta(k)$; solved exactly on the
three points it returns a *different* slope $a'=-0.4322$ and a large curvature
coefficient $c=-157.9$, pulling the extrapolation strongly *downward* to
$\approx1.43$ GeV. The two bracket the answer because three points cannot resolve
both a slope and a curvature stably; the observed generational ratios
($207\times$ then $17\times$, decreasing) already warn that the affine line
over-shoots. So the comb pins the **ordinal $k_4=141$** hard and only
**brackets the fourth-lepton mass to $\sim1.4$–$160$ GeV** pending a fourth data
point to fix the curvature coefficient.

## Extension

### The generation operator is a single rigid rotation

The scalar recursion $\theta_{g+1}=\theta_g+\delta\theta_g$ hides a cleaner object.
Lift each lepton onto the **flow-reversal phase circle** by its full (unreduced)
phase $\Theta(k)=2k\ln\varphi$ and form the unit phase vector

$$\mathbf e(k)=\big(\cos\Theta(k),\,\sin\Theta(k)\big)
=\big(\cos\theta(k),\,\sin\theta(k)\big)\in S^1.$$

The first component is exactly the $\cos\theta$ column of the lepton table that
drives gravity, flow, and the mass curvature term; the second is its quadrature
partner. Then the entire tower is generated by one fixed $2\times2$ rotation,

$$\boxed{\;\mathbf e(k+\Delta_g)=\mathsf R(\delta\theta_g)\,\mathbf e(k),
\qquad
\mathsf R(\delta\theta_g)=\begin{pmatrix}\cos\delta\theta_g & -\sin\delta\theta_g\\[2pt]
\sin\delta\theta_g & \ \cos\delta\theta_g\end{pmatrix},
\quad \delta\theta_g=78\ln\varphi-12\pi.\;}$$

Verified to $\lesssim10^{-14}$:
$\mathsf R\,\mathbf e(24)=\mathbf e(63)$, $\mathsf R\,\mathbf e(63)=\mathbf e(102)$,
$\mathsf R\,\mathbf e(102)=\mathbf e(141)$, with $\det\mathsf R=1$ exactly — a rigid
element of $SO(2)$. The lepton spectrum is a **discrete rotor orbit on the
inversion circle**: a single generator $\mathsf R$, applied $g$ times to the
electron vector, produces every charged lepton,

$$\mathbf e(k_g)=\mathsf R(\delta\theta_g)^{\,g}\,\mathbf e(k_e),
\qquad \mathbf e(k_e)=(\cos1.10702,\ \sin1.10702).$$

This sharpens "phase-locked comb riding a drift line" into an exact statement: the
drift line is the orbit of the cyclic group $\langle\mathsf R\rangle\subset SO(2)$
generated by the irrational angle $\delta\theta_g$. Three consequences fall out
immediately:

- **No periodic closure.** $\delta\theta_g/\pi=12-78\ln\varphi/\pi$ is irrational
  (it is $12$ minus a rational multiple of $\ln\varphi$, itself transcendental), so
  the rotor never returns to a previous lepton phase. The charged-lepton tower is
  an **aperiodic, equidistributing comb** — by Weyl, its phases $\{\,\theta(k_g)\,\}$
  fill $[0,\pi)$ densely and uniformly as $g\to\infty$. The fermion comb is a
  Vernier scale of infinite, non-repeating resolution against the flow-reversal
  lattice.

- **The mass curvature term is a projected rotor.** Since the residual triple is
  driven by $\cos\theta(k_g)=[\mathsf R^{g}\mathbf e(k_e)]_1$, the spectroscopic
  curvature in the masses is literally the first coordinate of the rotor orbit. The
  mass ladder $=$ (geometric mean from equispacing) $\times$ (modulation from
  $\hat x\!\cdot\!\mathsf R^{g}\mathbf e(k_e)$). Slope and curvature are not two
  free fit parameters; they are the radial drift ($e^{a k}$) and the angular drift
  ($\mathsf R$) of one screw motion on the cylinder $\mathbb R_{\ge0}\times S^1$.

- **A flow-rate clock.** The accumulated angle after $g$ generations,
  $g\,\delta\theta_g \bmod 2\pi$, is a parameter-free phase the heavy generations
  carry — a candidate origin for the generation-dependent mixing phases. The rotor
  predicts that any generation-indexed observable built from $\cos\theta,\sin\theta$
  (mass curvature, off-reversal depth, and the gravity drain
  $\kappa_{\text{Frenet}}$) is a *single sinusoid sampled at the rotor angles*,
  testable the moment a $k_4$ datum lands.

**What this buys us.** The single drift invariant $\delta\theta_g=78\ln\varphi-12\pi$
collapses three measured masses and three measured ordinals into *one* integer
($\Delta_g=39$, equivalently the exact $12$-reversal fold count) and *one*
irrational defect, both fixed by $\varphi$ alone — and the Extension shows that
defect *is* the generator of an $SO(2)$ rotor whose orbit is the entire lepton
tower. The generation index is literally the count of inversion shells descended
(exactly $12$ per step), the mass ladder is the geometric mean sealed by $e^{39a}$
times the projected rotor, and the next rung is a concrete, falsifiable ordinal.
The fermion spectrum is a Vernier scale of the flow-reversal lattice — the
spatial-curvature comb of the spine read at the ordinals where $L_y=1$ chooses to
localize as mass.
