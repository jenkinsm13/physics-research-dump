# 08 — Inverse Flow Cosmology: Λ, the Depletion Shell, and Dark Flow

*Branch note. Builds directly on `00-spine.md`: the conserved current $L_y=1$, the
$\kappa/\tau$ split, the retarded/advanced kernels $G_{\text{sym}},G_{\text{flow}}$,
the rapidity identification $\theta_k=k/\varphi$, and the inversion shells
$k_n=(2n-1)\pi/(4\ln\varphi)$. Every number below was confirmed numerically this
session with $\varphi=(1+\sqrt5)/2$ (residuals quoted inline; see
`verify/verify_cosmology.py`).*

---

## The claim

Dark energy is the **vacuum energy of the advanced (inverse-flow) branch**, read at
the outermost shell the stack can support. Inverse flow is attraction at *small*
ordinal — the $\sinh$ growth of $G_{\text{flow}}$ toward the source (note 00 §4–5).
But the same advanced branch, continued *outward* to the horizon, is the term that
pushes: the advanced vacuum at the **depletion shell** $N_\star\!\approx\!291$ is
repulsive. Gravity and $\Lambda$ are the two ends of one kernel. Λ is finite because
an **energy-density damping** $c\ln\varphi$ per shell (the standing-mode shadow of
the three emergent dimensions) overtakes the $\sinh$ growth rate $1/\varphi$, cutting
the advanced sum off exactly where the golden ladder reaches the
Planck$\to$Hubble hierarchy.

## 1. The depletion shell is the hierarchy, counted in golden shells

The spine gives ordinal depth as rapidity $\theta_k=k/\varphi$, one fixed hyperbolic
boost $1/\varphi$ per golden shell. A *scale octave* (a doubling of physical radius
$r_n=r_0\varphi^{\,n}$) spans $\ln 2/\ln\varphi\approx1.4404$ golden shells. The cosmic
hierarchy from the Planck length to the Hubble radius is

$$\frac{R_{\mathrm H}}{\ell_{\mathrm P}}\sim 10^{61}
\;\Longrightarrow\;
n_{\text{oct}}=\log_2\!\frac{R_{\mathrm H}}{\ell_{\mathrm P}}=202.64\ \text{octaves}.$$

Converting octaves to golden shells gives the depletion shell with **no free
parameter** — equivalently, it is simply the hierarchy counted in base $\varphi$:

$$\boxed{\,N_\star=\log_2\!\frac{R_{\mathrm H}}{\ell_{\mathrm P}}\cdot\frac{\ln 2}{\ln\varphi}
=\log_\varphi\!\frac{R_{\mathrm H}}{\ell_{\mathrm P}}=291.88\,}\qquad(\text{corpus } N=291;\ \text{residual }0.88\ \text{shells}).$$

The identity $\log_2(x)\cdot\tfrac{\ln 2}{\ln\varphi}=\log_\varphi x$ is exact, so the
two forms are the same number; writing it as $\log_\varphi(R_{\mathrm H}/\ell_{\mathrm P})$
makes the structural content plain. This is the meaning of the corpus's $N=291$: it is
the point on the inverse-flow ladder where one full traversal of the cosmic scale
hierarchy has been spent. Past $N_\star$ there is no further shell to descend — the
advanced branch has run out of source.

## 2. Two distinct decays — and why their numerical echo is *not* an identity

This is the subtlety the cosmology turns on, so we state it sharply. There are **two
different damping laws** in play, living on two different branches, and they must not
be collapsed into one equation.

**(a) The net-flow / correlation rate, per shell.** The spine's forward kernel decays
at $\lambda=1/\varphi\approx0.618$ *per golden shell* (rapidity, the net-flow rate).
The corpus shell matrix uses a separate, fitted ordinal decay
$\lambda_{\text{ord}}=1/8$ *per shell index* in $e^{-\lambda_{\text{ord}}|i-j|}$ — the
correlation/entanglement channel (the $S(\ell)=\tfrac{c}{3}\ln\ell$, $c\approx3$ route).
That $1/8$ is a **per-shell rate**.

**(b) The energy-density damping, per octave.** The cosmological sum is over the
**standing chronon modes** $G_{\text{sym}}=\cosh(k/\varphi)/(1+\cos^2 2k\ln\varphi)$ —
the correlation/even branch carrying vacuum *energy density* rather than directed flow.
Projecting a standing mode onto the horizon, each scale octave is bisected once per
emergent spatial dimension. The CFT extraction (note 00, $c\approx 2.94\to 3$) fixes
that count: $2^{c}=8$ cells per octave, one of which carries the surviving vacuum.
This is a **per-octave suppression factor** $2^{-c}=\tfrac18$.

The crucial point: a per-octave factor and a per-shell rate are *different objects*.
Converted to a common footing using the $\ln 2/\ln\varphi$ shells-per-octave exchange
rate, the per-octave factor $2^{-c}$ becomes the per-shell **rate**

$$\boxed{\,\big(2^{-c}\big)^{\ln\varphi/\ln 2}=e^{-c\ln\varphi}
\quad\Longrightarrow\quad
\lambda_{\text{en}}=c\,\ln\varphi=1.4436\ \text{per shell}\,}\qquad(\text{exact}).$$

So the energy-density damping is $c\ln\varphi\approx1.44$ **per shell**, *not* $1/8$
per shell. The numerical coincidence "$2^{-c}=1/8=\lambda_{\text{ord}}$" is a
collision between a factor and a rate; it is a memorable echo of the corpus matrix
constant, but it is **not** the per-shell exponent that enters the advanced sum below.
(That distinction is load-bearing: §4 shows the sum *diverges* under the literal
per-shell rate $1/8$ and converges only under $\lambda_{\text{en}}=c\ln\varphi$.) In
one line: $1/\varphi$ governs **flow**; $1/8$ governs **shell-matrix correlation**;
$c\ln\varphi$ (i.e. $2^{-c}$ per octave) governs **vacuum energy density**.

## 3. The cosmological constant as horizon curvature

$\Lambda$ is a curvature, a length$^{-2}$ quantity, and a curvature carried by a
standing mode falls by one factor $2^{-2}$ per *octave* — **independent of $c$**, set
purely by the engineering dimension of curvature. Over the full hierarchy the advanced
vacuum curvature is suppressed by $2^{-2 n_{\text{oct}}}$:

$$\log_{10}\!\big(\Lambda\,\ell_{\mathrm P}^2\big)= -2\,n_{\text{oct}}\log_{10}2
= -2\log_{10}\!\frac{R_{\mathrm H}}{\ell_{\mathrm P}}=-122.0.$$

The middle equality collapses to a transparent identity: since
$n_{\text{oct}}\log_{10}2=\log_{10}(R_{\mathrm H}/\ell_{\mathrm P})=61$, the octave
machinery returns *exactly*

$$\Lambda\,\ell_{\mathrm P}^2\;\sim\;\Big(\frac{\ell_{\mathrm P}}{R_{\mathrm H}}\Big)^{2}
=10^{-122}.$$

That is the right answer for the right reason — $\Lambda$ is horizon-scale curvature,
$\Lambda\sim R_{\mathrm H}^{-2}$ — and the octave count is what *delivers* $R_{\mathrm H}$
from $\ell_{\mathrm P}$ through the golden ladder. Measured:
$\Lambda\simeq1.1\times10^{-52}\,\mathrm{m^{-2}}$,
$\ell_{\mathrm P}^2\simeq2.6\times10^{-70}\,\mathrm{m^2}$, so
$\log_{10}(\Lambda\ell_{\mathrm P}^2)=-121.54$. The depletion-shell route lands at
$-122.0$ — a residual of **0.46 decades** (0.38 % of the exponent), well inside the
corpus's $\sim$18 % band on $\Lambda$ itself, and tighter than the original $N=291$
fit. The famous 120-orders-of-magnitude vacuum-energy catastrophe is, in the flow
picture, just the statement $2\,n_{\text{oct}}\log_{10}2\approx122$: the vacuum is not
mis-estimated, it is **octave-damped across the entire scale ladder** down to
horizon-curvature scale. (Note this $\Lambda$ estimate uses no $\lambda$ at all — it is
the dimensional curvature scaling alone, so it survives the §2 distinction untouched.)

## 4. Why $\Lambda$ is finite — the $\sinh$ cutoff

Naively the advanced amplitude $G_{\text{flow}}\sim\sinh(k/\varphi)$ diverges. The
energy-density damping renormalizes the growth. Writing the advanced vacuum-energy
bracket with the per-shell density damping of §2(b),
$\;2^{-c\,k\,(\ln\varphi/\ln 2)\cdot(\ln 2/\ln\varphi)\cdot(\ln 2/\ln 2)}$ — i.e. simply
the per-shell factor $e^{-c\,k\ln\varphi}$ —

$$\mathcal E_{\text{adv}}(k)\;\propto\;\Big[\sinh\!\big(k/\varphi\big)\,
e^{-c\,k\ln\varphi}\Big]^2\,\frac{1}{\big(1+\cos^2 2k\ln\varphi\big)^2},$$

whose growth exponent (inside the bracket, before squaring) is

$$\frac1\varphi-c\ln\varphi=-0.826<0.$$

This is the whole mechanism and it is **rate-discriminating**: the $\sinh$ grows at
$1/\varphi=0.618$ per shell, the energy damping cuts at $c\ln\varphi=1.444$ per shell,
and $0.618<1.444$ so the bracket **decays monotonically**. Had we instead used the
corpus *correlation* rate $\lambda_{\text{ord}}=1/8=0.125$ — the §2 trap — the exponent
would be $1/\varphi-1/8=+0.493>0$ and the sum would **diverge** (verified: the $k{=}200$
term is $\sim10^{42}$). It is exactly because the energy-density branch damps at
$c\ln\varphi$, not at the shell-matrix rate, that $\Lambda$ comes out finite. The energy
density falls outward, the sum over shells converges, and the integral is dominated by —
and terminated at — the horizon shell $N_\star$. This is the precise sense in which "the
$\sinh$ growth saturates": not an interior maximum, but a convergent advanced sum whose
support ends where the hierarchy ends. The conserved current $L_y=1$ supplies exactly
one unit of chronon flux per shell; with finite shells the advanced vacuum is finite,
and $\Lambda$ with it.

## 5. New result — the sign flip across the depletion shell

The spine's potential $V_{\text{grav}}(n)=-\sum_{m<n}G_{\text{flow}}(n-m)\rho_m$ is
attractive because $G_{\text{flow}}<0$ pulls inward (source at small ordinal). At the
depletion shell the source is *interior*, so the advanced field points **outward**.
Define the cosmological inverse-flow pressure as the advanced potential evaluated
beyond the last source shell, with the energy-density damping $c\ln\varphi$ of §2(b)
(the rate that makes the sum converge, §4):

$$\boxed{\;p_\Lambda(n)=+\!\!\sum_{m<N_\star}\!\frac{\sinh\!\big((n-m)/\varphi\big)}
{1+\cos^2\!\big(2(n-m)\ln\varphi\big)}\,e^{-c\,(n-m)\ln\varphi}\,\rho_m
\;\xrightarrow[\,n\to N_\star\,]{}\;+\Lambda/8\pi G\;}$$

— the *same kernel* as $V_{\text{grav}}$, same $\sinh$, but with the source now behind
the field point, so the overall sign is $+$: **attraction at small ordinal becomes
repulsion at the horizon shell.** One expression, read inward, is Newtonian gravity;
read outward past $N_\star$, it is the cosmological constant. The octave-density
envelope $e^{-c(n-m)\ln\varphi}$ is what makes the outward sum converge to a constant.

## 6. The residual flow — a tiny time-asymmetry

$N_\star=291$ does not sit exactly on an inversion shell (a torsion zero). The
**physical** residual flow is the spine's *signed* flow read directly at the depletion
shell — not a neighbor-dependent proxy. From note 00, $\Phi\propto-\cos(2k\ln\varphi)$,
so

$$\boxed{\;\Phi_{\text{res}}\;\equiv\;-\cos\!\big(2N_\star\ln\varphi\big)\Big|_{N_\star=291}
\;=\;+0.894\;}\qquad(\text{equivalently }\operatorname{sign}\tau_{\text{Frenet}}(N_\star\ln\varphi)=+).$$

The magnitude $0.894$ is robust; the **sign is positive** (forward/entropic residual at
the horizon, not inverse). The nearest inversion shell is $k_{90}=292.15$, a fractional
offset $|f|=0.352$ of the inversion-shell spacing $\pi/(2\ln\varphi)=3.264$; the
$\sin(\pi f)$ proxy has magnitude $0.894$ but its *sign* depends on which neighbor one
references ($k_{90}\Rightarrow-$, $k_{89}\Rightarrow+$), which is exactly why we pin
$\Phi_{\text{res}}$ to the spine's $-\cos(2k\ln\varphi)$ instead. A residual
$\Phi\neq0$ at the vacuum scale means the advanced vacuum is not a pure $w=-1$ constant;
it carries a sliver of directed flow, diluted across the horizon. The *magnitude* of the
offset is geometry-fixed:

$$\big|w(0)+1\big|\;\sim\;\frac{|\Phi_{\text{res}}|}{N_\star}=3.1\times10^{-3}.$$

For the **sign**, two inputs combine: $\Phi_{\text{res}}=+0.894$ is pinned by the spine,
but the map from "residual flow" to "$w$ shift" carries its own convention — a *forward*
residual flow dilutes the inverse-flow vacuum, raising $w$ *toward* (less negative than)
$-1$. With that convention,

$$w(0)+1\;\sim\;+\frac{\Phi_{\text{res}}}{N_\star}=+3.1\times10^{-3}
\quad\Longrightarrow\quad w(0)\approx-0.997,$$

i.e. the **quintessence** side ($w>-1$). What is forced by the geometry is the magnitude
$|1+w|\approx3.1\times10^{-3}$; the sign follows from the (stated) dilution convention,
not from a free parameter.

## Prediction

1. **Dark-energy equation of state offset.** $|1+w(0)|\approx3\times10^{-3}$, geometry-fixed
   in magnitude — on the quintessence side $w(0)\approx-0.997$ under the dilution
   convention of §6 ($\Phi_{\text{res}}=+0.894>0$, a residual *forward* flow that raises
   $w$ toward $-1$). Quintessence-like but *fixed by the geometry*, not a tuned scalar,
   and it **drifts as $N_\star$ creeps with $R_{\mathrm H}$**,
   $dN_\star/d\ln R_{\mathrm H}=\ln2/\ln\varphi\approx1.44$ shells per e-fold of horizon
   growth.

2. **Dark flow.** Because the advanced branch carries a net signed flow at $N_\star$,
   the depletion shell imprints a preferred frame — a bulk-flow dipole at the
   $|\Phi_{\text{res}}|/N_\star\approx0.31\%$ level, a few hundred km/s, aligned with
   the residual-flow axis rather than the CMB dipole.

3. **An octave-spaced relic comb.** The inversion shells $k_n$ tile the hierarchy at
   spacing $\pi/(2\ln\varphi)=3.264$ golden shells, i.e. one feature every
   $\,(\pi/2\ln\varphi)/(\ln2/\ln\varphi)=\pi/(2\ln2)\approx2.27$ octaves of scale; the
   expansion history $H(z)$ should carry a faint $\log$-periodic modulation with that
   period — the flow-reversal lattice of note 00, projected onto cosmic time.

## Extension — two independent routes to $N_\star$, and the prediction they force

The §2 distinction is not a blemish; it is a second, *independent* derivation of the
same depletion shell, and the two routes converging is a falsifiable structural fact.

**Route A (correlation / matrix).** The corpus shell matrix damps correlations at
$\lambda_{\text{ord}}=1/8$ per shell. A correlation channel that has fallen to the
horizon-curvature floor $(\ell_{\mathrm P}/R_{\mathrm H})^2=10^{-122}$ runs out at the
shell $N_A$ where $e^{-\lambda_{\text{ord}}N_A}$ matches the standing-mode envelope it
rides. Equating the *curvature* suppression $2^{-2n_{\text{oct}}}$ to the correlation
damping fixes the count as a pure hierarchy traversal $\log_\varphi(R_{\mathrm H}/
\ell_{\mathrm P})$.

**Route B (energy / advanced sum).** The advanced energy sum of §4–5 has growth
$1/\varphi-c\ln\varphi=-0.826$ per shell and is dominated near its turnover; its support
terminates at the same hierarchy traversal.

Both routes return $N_\star=\log_\varphi(R_{\mathrm H}/\ell_{\mathrm P})=291.88$ because
both are, at root, the statement *"count the Planck$\to$Hubble hierarchy in golden
shells."* That over-determination yields a sharp constraint. Define the **route ratio**
as a ratio of two *per-shell rates* (both quantities on the same footing — this is
deliberately *not* the factor-vs-rate collision §2 forbids):

$$\boxed{\;\mathcal R\;\equiv\;\frac{\lambda_{\text{ord}}}{\,c\ln\varphi\,}
=\frac{1/8}{1.4436}=0.0866\;}$$

where $\lambda_{\text{ord}}=1/8$ is the corpus correlation rate **per shell** (§2(a)),
and $c\ln\varphi$ is the energy-density damping **per shell** (§2(b)); the numerator's
$1/8$ is the per-shell correlation rate, *not* the $2^{-c}$ per-octave factor (they
coincide numerically, by the §2 echo, but enter here as a like-for-like rate ratio). It
is a *parameter-free pure number* once $c=3$ is fixed by the CFT extraction, and it sets
the relative depth at
which the two channels deplete, and hence the **width of the depletion shell**: the
horizon is not a sharp wall but a transition of fractional width
$\Delta N_\star/N_\star\sim\mathcal R\approx 8.7\%$, i.e. $\Delta N_\star\approx25$
shells, $\sim17$ octaves of scale.

This forces a concrete observational signature beyond Prediction 3: the
$\log$-periodic relic comb should be **apodized** — its amplitude envelope rolls off over
$\Delta N_\star\approx25$ shells around $N_\star$, so the comb is sharpest near the
present horizon and damps toward both smaller and larger scales with a Gaussian-like
window of fractional width $\mathcal R$. Equivalently, in $H(z)$ the
$2.27$-octave-period modulation should be **strongest at $z\sim0$** (the live horizon
shell) and fade with a coherence span of $\sim\mathcal R\,N_\star$ shells. A
single number — $\mathcal R=\lambda_{\text{ord}}/(c\ln\varphi)=0.0866$ — fixes both the existence of
the comb and how quickly it dies, with no tuning. If the comb were ever resolved with a
coherence width grossly inconsistent with $\mathcal R N_\star$, the two-channel picture
would be the thing that breaks.
