# 31c — Mechanism C — Damping Lifetime / Stability Threshold

**Question addressed.** This note tests whether a *lifetime / stability threshold* built
from the dispersion of the unified field equation (note 16) can answer the desert-depth
problem (note 30): does any parameter-free survival criterion **cap the charged tower** at a
deepest stable mode near $n_e = \log_\varphi(E_P/m_e) = 107.08$? This is a **termination**
question (split (b) of the reframing), with a side glance at placement (a). I work in the
absolute Planck-anchored ordinal where $n_e=107.08$, and flag where the rotor ordinal
($k_e=24$, offset by the Planck-to-electron intercept $b$ of $\ln m = ak+b$) would enter.

> **Adversarial knob-hunt (this revision).** The original note already reached a clean
> *negative*; this pass attacked it rather than re-confirming it, and the verdict stands and
> is now *sharper*: **negative**. Three things were added and reproduced in
> `verify/verify_lifetime-stability.py`: (1) a **non-perturbative Floquet theorem** that
> closes the one real loophole — the frozen-mass approximation — by proving $\tau=\varphi$ is
> *exact*, not adiabatic; (2) the **true knob** of a lifetime mechanism, the inner product
> that *defines* "lifetime", with a D4 alternative that is depth-blind from a *different*
> direction; (3) an **ordinal-hygiene** argument that a rotor-shell rate cannot in principle
> locate an absolute-ordinal depth. (Numerical hygiene note: the comb spacing
> $\Delta k=\pi/(2\ln\varphi)=3.26425$ is correct — $k_1=\pi/(4\ln\varphi)=1.6321$ and
> $\Delta k=2k_1$; I checked this explicitly rather than assume it.)

## The dispersion and its lifetime

From note 16 the boost-covariant equation $(D_k^2+M^2)\Psi=0$ with
$D_k^2=\partial_k^2-(2/\varphi)K\partial_k+(1/\varphi^2)I$, $M^2=\mathrm{osc}^2(k)$,
$\mathrm{osc}(k)=1/(1+\cos^2(2k\ln\varphi))$, yields in the frozen-mass (adiabatic) limit
$$\omega(k)=\pm\,\mathrm{osc}(k)\;-\;i\,\frac{s}{\varphi},\qquad s=\pm1 .$$
The imaginary part is set entirely by the rotor term $-(2/\varphi)K\partial_k$: it is
$\mathrm{Im}\,\omega=-s/\varphi$, **independent of $k$**. The retarded ($s=-1$) branch
decays as $e^{-k/\varphi}$, so the e-fold lifetime is
$$\boxed{\;\tau=\frac{1}{|\mathrm{Im}\,\omega|}=\varphi\;\text{shells}\;}$$
exactly $\varphi$ for *every* mode at *every* depth (note 16: $G_R\propto e^{-k/\varphi}$,
e-fold $=\varphi$).

The natural "stability" diagnostics one would build from this are:
$$Q(k)=\frac{\varphi\,\mathrm{osc}(k)}{2}\in\Big[\tfrac{\varphi}{4},\tfrac{\varphi}{2}\Big]
=[0.405,\,0.809],\qquad
N_{\rm osc}(k)=\mathrm{osc}(k)\,\tau=\varphi\,\mathrm{osc}(k)\in[0.809,\,1.618].$$
$Q$ is the quality factor (oscillations per radian of decay); $N_{\rm osc}$ is the number of
coherent real oscillations within one e-fold. Both are **bounded and periodic** in $k$ with
the comb period $\Delta k=\pi/(2\ln\varphi)=3.26425$ — they repeat identically every
$3.26$ shells and have **no monotone trend with depth**. The verify script confirms the
osc-envelope on $[0,\Delta k]$ equals that on $[100,100+\Delta k]$ to machine precision.

**Immediate consequence.** Any criterion of the pure form "mode is stable iff $Q\ge Q_c$"
or "iff $\tau\ge\tau_c$" or "iff $N_{\rm osc}\ge N_c$" returns the **same verdict at every
shell**: either all comb modes pass or all fail. A depth-blind rule cannot select a *deepest*
depth. This is the structural verdict and it is fatal to the mechanism as stated.

## The one real loophole, and why it does not save the mechanism (Floquet)

A reviewer could object that $\tau=\varphi$ is read off the **frozen-mass / adiabatic**
dispersion, and that note 16/31b *themselves* admit the carrier is **never adiabatic**
($R=\mathrm{osc}''+\mathrm{osc}^3$ is $O(1)$, RMS $0.66$; $Q<1$ everywhere). If the periodic
mass $\mathrm{osc}^2(k)$ pumped the mode parametrically, the *true* decay rate could acquire
depth structure (a Floquet/Lyapunov exponent), and the depth-blindness above would be an
artifact of the approximation. This is the only place a hidden knob — or a genuine selection —
could live, so it must be settled non-perturbatively, not waved away.

Settle it. The full retarded channel is
$\chi''+\tfrac2\varphi\chi'+(\tfrac1{\varphi^2}+\mathrm{osc}^2(k))\chi=0$. The substitution
$\chi=e^{-k/\varphi}u$ is **exact** and removes the friction algebraically (it is a
constant-coefficient first-order term — a similarity transform), leaving the **Hill equation**
$$u''+\mathrm{osc}^2(k)\,u=0,\qquad \mathrm{osc}^2\in[\tfrac14,\,1]\ \text{strictly positive, $\Delta k$-periodic.}$$
The decay of $\chi$ is therefore the **exact prefactor $e^{-k/\varphi}$ multiplied by whatever
$u$ does**, and the question reduces to: does $u$ grow (real Floquet exponent) or stay bounded?
Computing the one-period monodromy matrix $M$ by RK4 (`verify`, no scipy dependency):
$$\det M=1.0000000000\ (\text{symplectic, Wronskian}=1),\qquad |\mathrm{tr}\,M|=1.5696<2,\qquad
|\text{multipliers}|=1.0000000000,$$
$$\boxed{\;\max\mathrm{Re}(\text{Floquet exponent of }u)=9\times10^{-16}\ \text{per shell}\;\approx 0.\;}$$
$|\mathrm{tr}\,M|<2$ places the Hill equation **inside a stable band** (Lyapunov-stable,
bounded-oscillatory $u$); a strictly positive bounded periodic potential cannot drive a
parametric instability here. (Mathieu/parametric resonance would require the pump frequency
$2\pi/\Delta k=1.925$/shell near $2/n$ times the natural frequency
$\sqrt{\langle\mathrm{osc}^2\rangle}=0.728$/shell; the ratio is $2.64$, far from any tongue.)

**Conclusion of the Floquet test (an upgrade, not a rescue):** the only decay in $\chi$ is the
*exact* $e^{-k/\varphi}$; the periodic mass merely modulates the *phase* of $u$, never its
amplitude. So $\tau=\varphi$ is **non-perturbatively exact**, not an adiabatic accident. The
"frozen-mass is uncontrolled" objection is closed — and the closing makes the negative
*stronger*: the decay rate is depth-constant as a theorem, not an approximation, so periodicity
cannot manufacture the depth structure a termination would need.

## The only escape: a finite stack — and where it leads

Depth-dependence can be smuggled in only via the **finite stack length**: UV at the Planck
shell $k=0$ (note 24, the single dimensionful anchor $\omega_0=E_P$) and IR floor at
$N_\star=291.88$ (notes 24/30). Then "survival to the floor" becomes depth-dependent. The
defensible candidates, all parameter-free *given* $N_\star$:

| rule | $K_\star$ | value |
|---|---|---|
| survive $\ge1$ e-fold to floor | $N_\star-\varphi$ | $290.26$ |
| $\ge1$ coherent oscillation to floor (worst $\mathrm{osc}=\tfrac12$) | $N_\star-2\varphi$ | $288.64$ |
| stack midpoint | $N_\star/2$ | $145.94$ |
| **soft attractor (note 30)** | $N_\star/\varphi^2$ | $\mathbf{111.49}$ |

Every "survive to the IR floor" rule lands near $290$ — the cutoff is the floor itself,
because $\tau=\varphi$ is tiny compared to the $\sim292$-shell stack, so essentially *all*
modes "survive" in the same trivial sense and the boundary is just $N_\star$. None lands at
$107$. The **only** finite-stack expression that lands in the target region is
$N_\star/\varphi^2=111.49$ — which is exactly the **pre-registered failure flag (D5)**. It
is $111$, not $107$ (a $4.4$-shell, $\sim4\%$ miss), and per note 30 I treat it as the
soft-attractor failure mode, **not** as "close to $107$".

Note carefully: this $N_\star/\varphi^2$ is *imported* — it is the cross-scale closure of
**Mechanism E** (note 31e), not an output of the lifetime mechanism itself. The lifetime
mechanism's own object ($\tau$) produces **no number at all**; it touches $111$ only by
borrowing E's finite-stack rule. This is why 31c is a clean *negative* (it selects nothing)
while 31e is *failure-flag-111* (its own only in-range output is $111.5$). Keeping the two
distinct matters: 31c does not even reach the attractor without E's machinery.

To actually hit $107$ from the lifetime picture one must demand a *specific* e-fold count
from the Planck anchor: $K_\star=n_{\rm ef}\cdot\varphi=107\Rightarrow n_{\rm ef}=66.1$.
There is **no** intrinsic $66$ in the dispersion; it is a pure knob.

## The actual knob of a *lifetime* mechanism: the inner product (D4, re-derived)

The note's D4 (below) varies the *finite-stack threshold*. But the defining choice of a
*lifetime* mechanism is upstream of any threshold: it is the **inner product / functional
space in which "lifetime" is measured**. The operator is non-Hermitian, so there is no
canonical norm, and the headline $\tau=\varphi$ is silently committed to one choice — the
**single-channel modulus** $|e^{i\omega k}|=e^{-k/\varphi}$ of the retarded eigendirection
on $G_R\in L^1(\mathbb R_{\ge0})$ with the indefinite $\eta$-pairing.

Take the equally-defensible alternative: measure decay in the **conserved $\eta$ Noether
charge** of note 16 §6. The carrier is $\Psi=\mathrm{osc}\cdot\mathbf V$,
$\mathbf V(\theta)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$, and
$$\langle\mathbf V,\mathbf V\rangle_\eta=\cosh^2\theta-\sinh^2\theta=1=L_y\qquad
\text{(an \emph{analytic} identity, exact for all $k$; note 16 §6).}$$
(Numerically this is $1$ to machine precision for $\theta\lesssim12$ and then succumbs to
float cancellation as $\cosh\theta,\sinh\theta$ both overflow toward the same value — so the
conservation is an *exact identity*, not a clean wide-range numerical residual, and the verify
script checks it only in the cancellation-free window $k\lesssim40$.) Under this norm the
doublet charge is **exactly conserved**, so the "lifetime" is **infinite** — no decay, no
finite cutoff at any depth. The decay $\tau=\varphi$ is what you get by projecting onto the
single decaying channel and *discarding* the growing advanced channel; the $\eta$-symmetric
(CPT-paired) bookkeeping that keeps both restores the conservation law.

**The strongest counter, answered.** A skeptic will say: the $\eta$-norm gives $\tau\to\infty$
*only* because it keeps the growing advanced channel; a *particle* is physically the decaying
retarded channel, so the single-channel modulus is the right choice and $\tau=\varphi$ stands.
That is the best objection, and the reply is decisive: the point is **not** that the $\eta$-norm
is *more* correct. It is that **neither defensible choice selects a depth** — single-channel
modulus $\Rightarrow\tau=\varphi$ (constant in $k$); conserved $\eta$-charge $\Rightarrow\tau=\infty$
(no cutoff). Both horns are depth-blind. The mere *existence* of the inner-product knob is what
forecloses any *claim* of a parameter-free, depth-selecting lifetime — regardless of which horn
one prefers, the answer to "which depth?" is "none." There is no third, physically defensible
inner product that yields a *finite, depth-dependent* lifetime; the friction $1/\varphi$ is
$k$-constant by construction (it is the flat $SO(1,1)$ connection), so no norm can read a depth
out of it.

## Ordinal hygiene: a rate cannot locate an absolute offset

One more structural reason, independent of all the above. $\tau=\varphi$ is a rate measured in
**rotor shells** ($k$), and it is **intercept-free** — it knows nothing of the Planck-to-electron
offset $b$ in $n=k+b$ (notes 04/24). The target $n_e=107.08$ lives in the **absolute** ordinal.
A depth-constant *rate* in rotor units carries zero information about the absolute offset $b$,
so it cannot in principle point at $107$ even before any of the dynamical objections bite. The
lifetime mechanism is the wrong *kind* of object to answer a placement/termination question
posed in the absolute ordinal.

## Pre-registered disownment test (D1–D5)

- **D1 — NO FREE KNOB.** *Fail.* The pure-dispersion form has no knob but also no depth
  selection. Forcing a depth requires either the threshold $\tau_c/Q_c/N_c$ (a chosen real)
  or the e-fold count $n_{\rm ef}=66.1$ (chosen to land on $107$). Deeper than that: the very
  *definition* of "lifetime" is a knob (single-channel modulus vs conserved $\eta$-charge),
  and the latter gives $\tau\to\infty$. The stack length $N_\star=291.88$ is an external input
  (notes 24/30), and the rule $N_\star/\varphi^2$ is precisely the flagged attractor — imported
  from Mechanism E.
- **D2 — MANDATORY CROSS-CHECK (decisive).** *Fail.* A genuine mechanism must reproduce the
  muon ($\approx63$), proton ($\approx92$), or tau ($\approx102$) with the *same* rule. But a
  lifetime criterion yields **one cutoff $K_\star$, not a ladder** of stable depths. With
  $\tau=\varphi$ identical for all modes (now proven exact by Floquet, §Floquet), the rule
  assigns the *same* lifetime to the muon, proton, tau, and electron — it cannot distinguish
  them, let alone order them. Independently re-derived: $1/\tau=1/\varphi=0.6180$ at depths
  $63,92,102,107$ alike. It predicts no second depth, so the cross-check returns nothing to
  match. This alone is disqualifying.
- **D3 — CONSISTENCY WITH THE TOWER.** A boundary at $\sim107$ would (correctly) leave the
  tau (102) and muon (63) inside the allowed region — but only because $107>102$ by accident
  of *which knob* was chosen. The $N_\star/\varphi^2=111$ and $N_\star-\varphi=290$ variants
  also keep the tower alive, but for the trivial reason that they sit far below the floor.
  No version *derives* the tower ordering (electron shallow $24\to$ tau deep $102$); the
  criterion is depth-blind, so placement (a) is unexplained too.
- **D4 — ROBUSTNESS.** *Fail loudly, two ways.* (i) *Inner product:* the headline $\tau=\varphi$
  becomes $\tau\to\infty$ (no cutoff) under the conserved $\eta$-Noether norm — the number does
  not shift to $95$ or $120$, it dissolves; and both norms are depth-blind. (ii) *Threshold:*
  $K_\star=N_\star-\theta\varphi$ swings over $\{291.1,290.3,289.5,288.6\}$ as
  $\theta\in\{0.5,1,1.5,2\}$; $N_\star/2=145.9$, $N_\star/\varphi^2=111.5$,
  $N_\star/\varphi^3=68.9$ — wherever the knob is placed, ranging across the entire tower. The
  knob is fully exposed.
- **D5 — N⋆/φ²=111.5 FAILURE FLAG.** *Triggered, but imported.* The only near-target number
  reachable from this note is $N_\star/\varphi^2=111.49$ — and it is borrowed from Mechanism E's
  finite-stack closure, not produced by $\tau$ itself. I explicitly call it the soft-attractor
  failure mode, not a hit on $107.08$.

### Three traps
(i) **Bloch/periodicity:** $\mathrm{osc}^2$ is periodic $\Rightarrow$ infinitely many comb
modes; the lifetime $\tau=\varphi$ is *also* periodic-invariant (and, by Floquet, the periodic
part contributes *no* amplitude growth at all), so finiteness cannot come from the lattice. It
would have to come from the envelope/boundary $N_\star$ — i.e. the input, not the dynamics.
(ii) **$N_\star/\varphi^2$ attractor:** hit and disowned above (and flagged as imported from E).
(iii) **Non-Hermitian "stability":** the operator is non-Hermitian ($\mathrm{Im}\,\omega\ne0$).
I make **no** bound-state/normalizability claim. "Lifetime" here is strictly
$1/|\mathrm{Im}\,\omega|$ on the retarded Green's function $G_R\in L^1(\mathbb{R}_{\ge0})$
with the indefinite $\eta$-pairing — and §"the actual knob" shows that even *this* choice is
not forced: the conserved $\eta$-charge gives an infinite lifetime. There is no positive inner
product hosting a stable bound state, so any "deepest stable mode" language is unsupported by
the functional space.

## Verdict

**negative.** The damping lifetime is the depth-constant $\tau=\varphi$, now established
**non-perturbatively** (Hill/Floquet: $|\mathrm{tr}\,M|=1.57<2$, multipliers on the unit
circle, decay is the exact prefactor $e^{-k/\varphi}$), and $Q,N_{\rm osc}$ are bounded and
periodic. The mechanism is depth-independent at its core and selects no depth. Its headline
number is itself inner-product-dependent — under the conserved $\eta$-Noether norm the lifetime
is infinite — and *both* defensible norms are depth-blind. Forcing a depth needs a hand-tuned
threshold or e-fold count; the only intrinsic finite-stack number, $N_\star/\varphi^2=111.5$,
is *imported from Mechanism E* and is the disowned attractor, not $107.08$. Cross-check D2 fails
outright — the rule yields one cutoff, never a ladder hitting $63/92/102$. And as a rotor-shell
*rate* it cannot, even in principle, locate an absolute-ordinal *offset*. This is why 31c is a
clean **negative** (selects nothing), distinct from 31e's **failure-flag-111** (whose own only
output is the attractor).

**Falsifier (that would have rescued it):** if $\mathrm{Im}\,\omega$ had carried genuine
$k$-dependence — e.g. a Hill potential that *did* sit in an instability tongue, giving a real
Floquet exponent $\propto\mathrm{osc}'(k)/\mathrm{osc}(k)$ and hence a *monotone* lifetime that
crossed a parameter-free critical $Q=1$ at one depth — **AND** that depth independently
reproduced the muon at $63$ under the same rule, the mechanism would be genuine. The Floquet
computation shows the potential is in a stable band, so this rescue does not exist.

## Extension — the precise structural ingredient that *would* select 107

The knob-hunt makes the missing ingredient sharp. A lifetime mechanism can select a depth
only if $\mathrm{Im}\,\omega(k)$ is **monotone in $k$** and crosses a **parameter-free
critical value** *once*. Two requirements, both absent here, would have to be supplied:

1. **A symmetry-breaking term that makes the friction depth-dependent.** The current friction
   $2/\varphi$ is the flat $SO(1,1)$ connection $A_k=\tfrac1\varphi K$ (note 10), constant by
   construction. Only a *curved* connection — $A_k=f(k)K$ with $f'\neq0$ — gives
   $\mathrm{Im}\,\omega=-s\,f(k)$ with depth structure. Such an $f(k)$ would have to descend
   from a genuine geometric source (e.g. a running of the rapidity ladder against the
   cosmological depletion $N_\star$), not be posted; nothing in notes 10–16 curves the
   connection, so the friction is rigidly constant.

2. **A self-consistent (non-frozen, non-linear) mass.** If $M^2$ depended on the *amplitude*
   of $\Psi$ (a $\Psi^4$ self-coupling), the Hill equation would become a nonlinear
   parametric oscillator whose stable band *can* collapse at a critical amplitude — and the
   advanced channel's $e^{+k/\varphi}$ growth would reach that critical amplitude at a *single*
   depth set by the UV seed. That depth would be genuinely dynamical. Crucially, it would have
   to be cross-checked: the *same* $\Psi^4$ coupling, fed the muon and tau seeds, must
   reproduce $63$ and $102$. That is the one route by which a future note could turn this
   negative into a result — and it requires new physics (a curved boost connection or a
   self-interaction), not a re-reading of the existing linear, flat-connection field equation.
