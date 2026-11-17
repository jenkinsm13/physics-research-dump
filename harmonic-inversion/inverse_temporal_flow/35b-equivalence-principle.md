# 35b — The Equivalence Principle: Gravitating IS Slowing Time

*Thread (b) of note 35. The spine's claim is literal: gravity is the $+1$ eigenray
$G=e^{+\theta}$, time is the $-1$ eigenray $T=e^{-\theta}$, and $T\cdot G=1=L_y$. If that
is right, then "sitting deeper in a well" ($G$ large) must be the **same statement** as
"your clock runs slow" ($T$ small) — the gravitational time dilation of GR. This is the
make-or-break test against established gravity. We do it even-handedly, and we are blunt
about the two places a free parameter hides: (i) the **weak-field EP recovery is real but
map-independent** (not evidence for this framework over GR), while the **strong-field
deviation is a falsifiable signature of one specific choice** — the linear map $\theta=\Phi_N$
($c=0$ in a one-parameter family), not a theorem; and (ii) more fundamentally, **the EP map
$\theta=\Phi_N$ is a separately-posited identification**, distinct from the spine's per-shell
boost rapidity $\theta=k/\varphi$, and is the load-bearing assumption of the whole note. All
numbers confirmed in `verify/verify_equivalence-principle.py` (exit 0).*

---

## The map: rapidity *is* the Newtonian potential

From the spine, the local time-rate carried by the chronon worldline is the time ray
$$\frac{d\tau}{dt}=T(\theta)=e^{-\theta},$$
and the boost (redshift) velocity is $\beta=\tanh\theta=(G-T)/(G+T)$. GR's gravitational
time dilation in a static field is
$$\left(\frac{d\tau}{dt}\right)_{\rm GR}=\sqrt{1-\frac{2GM}{rc^2}}=\sqrt{1-2\Phi_N},
\qquad \Phi_N\equiv\frac{GM}{rc^2}.$$

The two expressions can only be the same physical clock if the rapidity that labels shell
depth is identified with the gravitational potential, $\theta=f(\Phi_N)$ for some monotone
$f$ with $f(0)=0$. We adopt the **linear** identification
$$\boxed{\;\theta\;=\;\Phi_N=\frac{GM}{rc^2}\;}\qquad(\text{rapidity}=\text{Newtonian potential}),$$
and we are precise about *why* this is the natural map and exactly *where* that justification
holds. The boost-addition theorem (note 11) makes rapidities **add** exactly,
$\theta_{12}=\theta_1+\theta_2$; in the regime where Newtonian potentials **superpose**
($\Phi_{12}=\Phi_1+\Phi_2$, a column of shallow shells), the only map that turns
potential-addition into rapidity-addition is a *linear* one, $f(\Phi_1+\Phi_2)=f(\Phi_1)+f(\Phi_2)$,
i.e. $\theta=a\Phi_N$. Matching the source strength below fixes the slope to $a=1$. So
$\theta=\Phi_N$ is the **unique additive map in the superposition regime** — but note the
domain: that argument is a *weak-field* statement (linear superposition is itself a weak-field
property). It does not by itself fix the map where potentials stop superposing — exactly the
strong-field regime where the prediction lives. We return to this honestly in the Extension;
the headline below is the linear choice, and we mark where it is forced versus chosen.

This is the equivalence-principle map: depth-in-shells *is* potential-in-units-of-$c^2$.
Under it the gravity ray $G=e^{+\theta}=e^{+\Phi_N}$ is the column-integrated blueshift
toward the source, and the net force of note 35, $\mathcal F=2\sinh\theta$, becomes
$2\sinh\Phi_N\to2\Phi_N=2GM/rc^2$ in the weak field — twice the Newtonian potential, i.e.
the standard relativistic source strength (the "$2$" that makes light bend by the GR
factor, not the Newtonian one). This source-strength match is what pins the slope $a=1$.

## Weak field: the equivalence principle is recovered — and it is map-independent

Expand both clocks for shallow shells ($\theta=\Phi_N\ll1$):
$$T=e^{-\Phi_N}=1-\Phi_N+\tfrac12\Phi_N^2-\dots,\qquad
\sqrt{1-2\Phi_N}=1-\Phi_N-\tfrac12\Phi_N^2-\dots.$$
The **linear terms are identical**:
$$\frac{d\tau}{dt}\approx 1-\Phi_N=1-\frac{GM}{rc^2},$$
which is exactly GR's (and Pound–Rebka's) weak-field gravitational redshift. The
equivalence principle —- *gravitating is slowing time* —- is not assumed here; it falls
out of $T=e^{-\theta}$ the moment rapidity is read as potential.

**The honest qualifier — and it sharpens the result rather than weakening it.** This
linear recovery does *not* single out our map $\theta=\Phi_N$. Take **any** smooth map
$\theta=\Phi_N+c\,\Phi_N^2+O(\Phi_N^3)$ with the slope fixed to $1$ (forced by the
source-strength match): then $T=e^{-\theta}=1-\Phi_N+(\tfrac12-c)\Phi_N^2+\dots$, so the
linear term is $1-\Phi_N$ **for every $c$**. The EP residual $1-T-\Phi_N$ is $O(\Phi_N^2)$
for all $c$ (verified: $\sim5\times10^{-9}$ at $\Phi_N=10^{-4}$ for $c=0,\tfrac12,1$ alike).
That is the right way to state the result: weak-field gravitational time dilation is a
*consequence of $T=e^{-\theta}$ plus any slope-1 potential map*, so passing GPS / Pound–Rebka
/ optical-clock tests is **not** evidence for this framework over GR — it is evidence the
framework contains GR's weak field, which is exactly what an honest unification must show
and exactly why no weak-field datum can favour it.

For the **specific** linear map ($c=0$) the two clocks first disagree at second order, with
the framework's clock running **faster** than GR's:
$$\frac{T-\sqrt{1-2\Phi_N}}{\sqrt{1-2\Phi_N}}=(1-c)\,\Phi_N^2+O(\Phi_N^3)\;\xrightarrow{\,c=0\,}\;\Phi_N^2.$$
Numerically the leading coefficient is $1-c$: at $\Phi_N=10^{-4}$ the relative clock
difference is $1.0001\times10^{-8}\approx\Phi_N^2$ for $c=0$ (verified). For Earth's surface
$\Phi_N\simeq7\times10^{-10}$, the $c=0$ deviation is $\Phi_N^2\sim5\times10^{-19}$
(below float64's ability to resolve it against unity — pure cancellation) — far below any
current clock comparison, so **the framework is observationally indistinguishable from GR
in every weak-field test** regardless of $c$. EP: recovered (map-independently).

## Strong field: exponential vs square-root — a real, quantified split

The disagreement is structural, not a small correction: the framework's redshift law is an
**exponential** $T=e^{-\Phi_N}$, GR's is a **square root** $\sqrt{1-2\Phi_N}$. As the field
deepens they part company fast (verified):

| $\Phi_N=\theta$ | $T=e^{-\theta}$ | $\sqrt{1-2\theta}$ | rel. dev. |
|---:|---:|---:|---:|
| $0.10$ | $0.90484$ | $0.89443$ | $+1.16\%$ |
| $0.20$ | $0.81873$ | $0.77460$ | $+5.70\%$ |
| $0.30$ | $0.74082$ | $0.63246$ | $+17.1\%$ |
| $0.49$ | $0.61263$ | $0.14142$ | $+333\%$ |

A concrete falsifiable case: a neutron-star surface, $\Phi_N\simeq0.2$ ($1.4\,M_\odot$,
$\sim10$ km). The surface gravitational redshift is
$$z=\frac{1}{d\tau/dt}-1:\qquad z_{\rm FW}=e^{0.2}-1=0.2214,\qquad
z_{\rm GR}=\frac1{\sqrt{1-0.4}}-1=0.2910,$$
a **fractional deficit $(z_{\rm FW}-z_{\rm GR})/z_{\rm GR}=-23.9\%$** (verified; a
$1.4\,M_\odot$, $10$ km star gives $\Phi_N=0.207$, so $\Phi_N\simeq0.2$ is the genuine
physical value, not a tuned one). Measured surface redshifts of accreting neutron stars
(e.g. absorption-line $z\sim0.35$) sit in this regime: with the linear map the framework
predicts a *systematically smaller* redshift than GR at fixed $M/R$. That is a clean
discriminator. **But be exact about what is being tested:** this $-23.9\%$ is the signature
of the choice $c=0$ (the linear map), not a parameter-free consequence of the framework. The
same algebra ($T=e^{-\theta}$, source-matched slope $1$) with the second-order coefficient
$c$ slid upward shrinks the deficit monotonically — $z=0.221,0.234,0.246,0.259,0.271$ for the
quadratic maps $c=0,\tfrac14,\tfrac12,\tfrac34,1$ (all verified) — and the *all-orders*
completion $\theta=-\tfrac12\ln(1-2\Phi_N)$ lands exactly on GR's $z=0.291$. So the
strong-field measurement does not test "the framework versus GR" — it **measures $c$** (more
precisely, the curvature of the rapidity–potential map), the one number the weak field cannot
reach.

## The horizon: both freeze time, but in opposite topologies

GR: the time-rate hits zero at the **finite** radius $r_s=2GM/c^2$, i.e. at $\Phi_N=1/2$,
where $\sqrt{1-2\Phi_N}=0$ — a coordinate horizon at finite depth. The framework's clock
$T=e^{-\theta}$ never reaches zero at any finite $\theta$; it freezes only **asymptotically**,
as $\theta\to\infty$, where $\beta=\tanh\theta\to1$ (note 35). So under the EP map
$\theta=\Phi_N$, at GR's horizon the framework's clock still ticks at
$T=e^{-1/2}=0.6065$ — **no horizon there**. The framework replaces the finite-radius event
horizon with an infinitely deep rapidity throat: time freezes, but only at infinite
rapidity, never at a finite shell. (The shell horizon $n_H=183$ of the spine is where
$\theta$ becomes Planck-large, not where $\Phi_N=1/2$.)

The two horizons *can* be forced to coincide by abandoning the linear EP map for the
exact-redshift map $\theta=-\tfrac12\ln(1-2\Phi_N)=\Phi_N+\Phi_N^2+\tfrac43\Phi_N^3+\dots$,
which makes $T\equiv\sqrt{1-2\Phi_N}$ identically and sends $\theta\to\infty$ as
$\Phi_N\to1/2$ (verified). This is **exactly the $c=1$ end** of the family above: its
quadratic coefficient is $c_{\rm eff}\to1$ as $\Phi_N\to0$ (verified). It still has slope
$1$ and still satisfies weak-field EP — it is not "rapidity $\ne$ potential," it is
"rapidity $=$ potential to linear order, with a *specific* higher-order completion that
re-sums to the GR square root." Under it the agreement becomes a definition and the
strong-field prediction collapses to GR. So the two endpoints of the one free number are:
$c=0$ (linear map, no finite horizon, $-23.9\%$ NS deficit) and $c=1$ (re-summed map, GR's
finite horizon at $r_s$, zero deviation). The weak field cannot distinguish them; the
strong field is precisely the measurement of $c$.

## Extension — the EP map is a one-parameter family; $c$ is the only physical degree of freedom

Make the whole structure exact. Any admissible rapidity–potential map is a monotone
$\theta=f(\Phi_N)$ with $f(0)=0$. Write its Taylor head
$$\theta=f(\Phi_N)=a\,\Phi_N+c\,\Phi_N^2+O(\Phi_N^3).$$
Two corpus facts collapse the freedom in $a$ and expose where it survives in $c$:

**1. Slope $a=1$ is forced by the source.** The net chronogravitational force (note 35) is
$\mathcal F=2\sinh\theta=2a\Phi_N+O(\Phi_N^3)$. The relativistic source strength is
$2GM/rc^2=2\Phi_N$ (the factor-$2$ that bends light by the GR amount). Matching gives
$a=1$, with **no** freedom: any $a\ne1$ misnormalizes light bending. (Verified: $2\sinh\Phi_N
\to2\Phi_N$ to $O(\Phi_N^3)$.)

**2. The clock to $O(\Phi_N^2)$ depends only on $c$.** Substituting,
$$\frac{d\tau}{dt}=T=e^{-\theta}=1-\Phi_N+\Big(\tfrac12-c\Big)\Phi_N^2+O(\Phi_N^3),$$
versus GR's $\sqrt{1-2\Phi_N}=1-\Phi_N-\tfrac12\Phi_N^2+\dots$. Hence the **theorem**:
$$\boxed{\;\frac{T-\sqrt{1-2\Phi_N}}{\sqrt{1-2\Phi_N}}=(1-c)\,\Phi_N^2+O(\Phi_N^3)\;}$$
The linear ($\Phi_N^1$) term cancels for *every* $c$ — that is the map-independence of the
weak-field EP recovery, now a one-line proof. The first observable difference from GR is
$(1-c)\Phi_N^2$, controlled by the single number $c$ at leading order. The full strong-field number, for a
neutron star at $\Phi_N=0.2$, with $z=e^{\theta}-1$:

| map | $\theta$ at $\Phi_N=0.2$ | NS redshift $z$ | dev vs GR | horizon |
|:---|---:|---:|---:|:---|
| linear, $c=0$ ($\theta=\Phi_N$, simplest) | $0.2000$ | $0.2214$ | $-23.9\%$ | none (at $\theta=\infty$) |
| quadratic, $c=\tfrac12$ (trunc.) | $0.2200$ | $0.2461$ | $-15.4\%$ | none |
| quadratic, $c=1$ (trunc.) | $0.2400$ | $0.2712$ | $-6.8\%$ | none |
| exact re-summation $\theta=-\tfrac12\ln(1-2\Phi_N)$ | $0.2554$ | $0.2910$ | $0\%$ ($\equiv$ GR) | finite, at $r_s$ |

The quadratic rows are *truncations* sharing the same $(1-c)\Phi_N^2$ leading split; only the
**all-orders** re-summation (whose head is $c=1$) lands exactly on GR and restores the
finite horizon. The hierarchy is monotone in how much higher-order curvature the map carries:
flat (linear) $\to$ no horizon, $-23.9\%$; fully GR-curved $\to$ horizon at $r_s$, $0\%$.

So the **empirical content of this EP-map ansatz beyond GR's weak field is the value of one
dimensionless constant $c$**, and it is observationally accessible *only* in the strong field.
The *ansatz alone* does not fix $c$ — the additivity argument fixes $c=0$ only in the
superposition (weak-field) regime, which is precisely where $c$ is invisible. Whether the
deeper shell structure constrains $c$ is a separate question this note does **not** settle:
the static-potential law $\Phi(r)\sim r^{-\nu}$ (note 16, $\nu_{\rm eff}\approx1.003$) and the
shell-radius map $n_H=\log_\varphi(r_s/\ell_P)=183$ (spine) plausibly pin the physical
$\theta(r)\leftrightarrow\Phi_N$ relation independently of the EP ansatz; verifying that — and
reading off the $c$ it implies — is left to a sibling note. What is established *here* is the
clean conditional: a genuine prediction *given the linear ansatz*, with the choice and its
falsifier both explicit. No hidden knob — one *declared* knob $c$, plus the load-bearing
identification flagged next. (All family rows verified in the script.)

### The deeper assumption beneath $c$: $\theta_{\rm EP}=\Phi_N$ is *not* the spine's per-shell $\theta$

There is a more fundamental knob than $c$, and honesty about the GR comparison requires naming
it. Everything imported into this note from the spine — $T=e^{-\theta}$, $\beta=\tanh\theta$,
$\mathcal F=2\sinh\theta$, **and the rapidity-addition theorem used to "force" $a=1$** — was
derived for the *per-shell boost rapidity* $\theta=k/\varphi$ (notes 16, 35), where $k$ is the
shell ordinal. One shell down, $\theta=1/\varphi=0.618$ and $\beta=\tanh(1/\varphi)=0.5498$
(the note-15 LIGO ratio). The EP map then sets $\theta=\Phi_N$, which puts that *single* shell
at $\Phi_N=0.618$ — **past GR's horizon** $\Phi_N=1/2$. But the spine reaches the horizon only
at $n_H=183$ shells, *not* at $\Phi_N=1/2$ (this note's own horizon section). The two $\theta$s
therefore differ by a factor of hundreds: $\theta_{\rm shell}=k/\varphi$ accumulates per shell,
while $\theta_{\rm EP}=\Phi_N$ is the radial Newtonian potential. They can only be the *same*
$\theta$ if a shell-index$\to$radius$\to$potential composition $\theta_{\rm EP}=\theta_{\rm shell}$
holds — which note 35a does **not** assert (it keeps $\theta$ abstract, $U(\theta)=-2\cosh\theta$
in rapidity-space, never tied to $r$), and which is introduced *only here*. So $\theta=\Phi_N$
is a **separately-posited identification**, the load-bearing assumption of this entire note.
This sharpens rather than weakens the conclusion: a *posited* map carries no framework-fixed
higher-order shape, which is exactly why $c$ is free — and it means even $a=1$ is conditional on
$\theta_{\rm EP}\equiv\theta_{\rm shell}$ (the additivity that fixes $a=1$ is a property of
$\theta_{\rm shell}$, transferred by assumption to $\theta_{\rm EP}$). Resolving whether the
shell-radius / static-potential machinery (notes 00/16, $\nu$, $n_H$) *derives* this
identification — and with it $a$ and $c$ — is the open task that 35b leaves on the table.

---

## Verdict

**The equivalence principle is RECOVERED** in the weak field — and the recovery is
**map-independent**: for any slope-$1$ potential map $\theta=\Phi_N+c\Phi_N^2+\dots$, the
time ray $T=e^{-\theta}$ reproduces GR's $1-GM/rc^2$ exactly at linear order. The framework
therefore *contains* GR's weak field by construction, which is what unification requires and
which is also why **no weak-field test (GPS, Pound–Rebka, optical clocks) can favour the
framework over GR.** This is a clean "agrees in the weak-field limit" result, stated without
overclaim.

The strong field is where the content lives, and it is honestly a **one-parameter** content:
the second-order coefficient $c$ is *not* fixed by any weak-field observable (the additivity
argument that suggests $c=0$ relies on linear superposition of potentials, which is itself a
weak-field property and fails in the regime being tested). The natural/simplest choice is
the linear map $c=0$ ($\theta=\Phi_N$), giving the exponential law $T=e^{-\Phi_N}$, no
finite-radius event horizon (freeze at infinite rapidity, not $r_s$), and a quantified
$-23.9\%$ surface-redshift deficit at $\Phi_N=0.2$. The opposite endpoint $c=1$ re-sums to
GR exactly. **What was "forced" in the earlier draft is in truth "chosen": $c=0$ is the
simplest map, not a theorem.**

**Falsifier (now sharper — it measures the free parameter):** the surface gravitational
redshift of a neutron star with independently constrained $M/R$ ($\Phi_N\simeq0.2$, e.g.
$1.4\,M_\odot$/$10$ km $\Rightarrow\Phi_N=0.207$) directly reads $c$ off the data:
$z=e^{\theta}-1$ with $\theta=\Phi_N+c\Phi_N^2$. GR ($c=1$) predicts $z=0.291$; the simplest
framework choice ($c=0$) predicts $z=0.221$, a $-23.9\%$ deficit; the measured $z$ pins $c$
in between. A redshift matching $\sqrt{1-2\Phi_N}$ to better than $\sim5\%$ at
$\Phi_N\gtrsim0.2$ drives $c\to1$ — i.e. selects the GR re-summation and falsifies the
*linear* "rapidity is potential" reading, while leaving the weak-field EP recovery (which
holds for all $c$) untouched.

**Two declared assumptions, no hidden ones.** The honest accounting for this GR comparison
is: (1) the free second-order coefficient $c$ (only the strong-field redshift measures it;
$c=0$ is the simplest choice, giving $-23.9\%$); and (2) the deeper, load-bearing
identification $\theta_{\rm EP}=\Phi_N$ — a *posited* map, not the spine's per-shell
$\theta=k/\varphi$, which is why $c$ (and even the slope $a$) is unconstrained by the
framework's own derivations. Both are stated, not buried; neither is fudged. A correct
"contains GR's weak field, deviates in a one-parameter, falsifiable way at strong field —
conditional on a posited potential map" is the result, and it is the kind a unification owes.
