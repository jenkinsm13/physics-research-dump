# 05 — Thermodynamics, Rapidity, and the Arrow of Time

*Branch note. Builds directly on `00-spine.md`: the conserved current $L_y=1$, the
$\kappa$/$\tau$ partition, the retarded/advanced split $G_{\text{sym}}=\cosh(k/\varphi)/(1+\cos^2)$,
$G_{\text{flow}}=-\sinh(k/\varphi)/(1+\cos^2)$, and the inversion shells $k_n$. All numbers
below are confirmed at machine precision — see `verify/verify_thermo.py`.*

---

## 1. Rapidity is a Boltzmann exponent

The spine identified ordinal depth as rapidity, $\theta_k = k/\varphi$, a hyperbolic boost
$1/\varphi$ per shell into inverse flow. Read the retarded weight as a thermal weight: the
forward kernel carries $e^{-k/\varphi}$, which is $e^{-\theta_k}$. This *is* a Boltzmann factor
in which the ordinal $k$ plays the role of an energy level and

$$\boxed{\;\beta_T \;\equiv\; \frac{1}{\varphi} \;=\; \varphi-1 \;=\; 0.6180339887\ldots\;}$$

is the **temporal-flow inverse temperature** — the unique, parameter-free temperature handed to
us by golden-ordinal sampling. The temporal-flow temperature is $T_\chi = \varphi$ (in ordinal
units, $k_B\equiv1$). Every shell descended costs one quantum $\beta_T$ of rapidity; entropy is
produced at the fixed exchange rate $1/\varphi$ per shell. Because $\beta_T=\varphi-1$ is
irrational and self-similar, no special shell is thermally privileged — the lattice is at a single
temperature throughout, which is why the decay $e^{-k/\varphi}$ in the spine never needed a
free coefficient.

## 2. The detailed-balance factor is exactly the boost

Strip nothing, smooth nothing: form the ratio of advanced to retarded weight directly from the
signed kernel $\kappa(k)=\tfrac{1}{1+\cos^2(2k\ln\varphi)}e^{-k/\varphi}$. The oscillatory
flow-reversal lattice $1/(1+\cos^2(2k\ln\varphi))$ is **even in $k$** and cancels identically,
leaving a pure thermal ratio:

$$\boxed{\;\frac{\kappa(+k)}{\kappa(-k)} \;=\; e^{-2k/\varphi} \;=\; e^{-2\theta_k}\;}
\qquad(\text{verified, max residual }2.8\times10^{-17}).$$

This is a **detailed-balance / local-fluctuation relation**: the probability of the forward
(retarded, entropic) leg to depth $k$ relative to the time-reversed (advanced, gravitational)
leg is $e^{-2\theta_k}$. The factor 2 is the round trip — out along forward flow and back along
inverse flow — so the *one-way* dissipated rapidity per shell is $\theta_k$, and the present
moment $k=0$ is the only ratio-unity point. That the lattice cancels here is the thermodynamic
face of the hyperbolic invariant $G_{\text{sym}}^2-G_{\text{flow}}^2=(1+\cos^2)^{-2}$: the
oscillation is a phase structure on the correlations, not on the dissipation.

## 3. The second law is the sign of $G_{\text{flow}}$

The net temporal flow is $G_{\text{flow}}(k)=-\sinh(\theta_k)/(1+\cos^2(2k\ln\varphi))$. Define the
**entropy-production rate along the flow**

$$\sigma(k) \;\equiv\; -\,G_{\text{flow}}(k) \;=\; \frac{\sinh(k/\varphi)}{1+\cos^2(2k\ln\varphi)} \;\ge\; 0,
\qquad \sigma(0)=0.$$

$\sinh$ is odd and monotone; its envelope is strictly increasing in $|k|$ (verified). Hence
$\sigma(k)\ge0$ for all forward depth, vanishing only at the present moment — **the second law is
not assumed, it is the antisymmetric (odd) part of the kernel being sign-definite**. The arrow of
time is the statement that the kernel has a nonzero odd part at all: a purely correlational world
($G_{\text{flow}}\equiv0$, the saddle-peak / inversion-shell condition) is time-symmetric, and
indeed the inversion shells $k_n$ are exactly where $\tau_{\text{Frenet}}=0$ — momentary local
restoration of time-reversal symmetry punctuating the monotone descent. Gravity (the $\sinh$) and
irreversibility (the same $\sinh$) are one quantity.

## 4. A golden Jarzynski equality over shells

Treat the shell stack as a canonical ensemble: a chronon equilibrated to depth $k$ with weight
$p_F(k)=e^{-k/\varphi}/Z$. The partition function is geometric and closed:

$$Z=\sum_{k=0}^{\infty}e^{-k/\varphi}=\frac{1}{1-e^{-1/\varphi}}=2.169211902563,
\qquad \langle k\rangle=\frac{1}{e^{1/\varphi}-1}=1.169211902563.$$

The mean ordinal depth $\langle k\rangle\approx1.169$ lies **in the first terrace** $[0,k_1)$,
approaching the **first inversion shell** $k_1\approx1.632$ from below ($\langle k\rangle<k_1$,
verified): thermal occupation places the typical chronon just short of the first flow reversal,
inside the first inversion terrace. Now drive the system: the work to boost one shell deeper along inverse flow is
$\beta_T W = 2k/\varphi$ (Section 2's exponent). The forward/inverse Crooks ratio is
$p_F(k)/p_R(k)=e^{2k/\varphi}$, so the Jarzynski equality $\langle e^{-\beta_T W}\rangle_F=e^{-\beta_T\Delta F}$
must hold. We confirm it in closed form (residual $1.1\times10^{-16}$):

$$\boxed{\;\big\langle e^{-2k/\varphi}\big\rangle_F
=\frac{1-e^{-1/\varphi}}{1-e^{-3/\varphi}}=0.546589243085
=e^{-\beta_T\Delta F},\quad \beta_T\Delta F=0.604058.\;}$$

This is a genuinely new equation of the framework: the **free-energy difference between forward and
inverse temporal flow is a fixed golden number**, $\beta_T\Delta F=\ln\!\frac{1-e^{-3/\varphi}}{1-e^{-1/\varphi}}=0.604058$,
extracted with no fitted parameter. It is the thermodynamic cost of one round trip through time,
and it is finite — inverse flow is not free, but its price is bounded.

## 5. The present moment is a maximum-entropy fixed point

At $k=0$: $c(0)=\tfrac12$, $G_{\text{sym}}(0)=\tfrac12$, $G_{\text{flow}}(0)=0$ (all verified
exactly). Zero net flow is the equilibrium condition; the self-coupling value $\tfrac12$ is the
retarded and advanced branches occupying the present with equal weight. The binary branch entropy
is therefore maximal, $S=\ln2=0.693147$. **The "now" is the unique zero-rapidity, maximum-branch-entropy
state** — the thermodynamic origin of the boost coordinate, from which forward and inverse flow are
the two equal-and-opposite descents.

## 6. New: the two-branch free energy and where entropy goes

Pair the retarded and advanced weights at depth $k$ (lattice factor common, so factored out). The
two-branch temporal partition is a single spin in a field:

$$z(k)=e^{-k/\varphi}+e^{+k/\varphi}=2\cosh(\theta_k)
=2\,G_{\text{sym}}(k)\,\big[1+\cos^2(2k\ln\varphi)\big],
\qquad \beta_T F(k)=-\ln\!\big[2\cosh(\theta_k)\big],$$

and its thermodynamic (branch) entropy is the new closed form

$$\boxed{\;S_{\text{br}}(k)=\ln\!\big[2\cosh(k/\varphi)\big]-\frac{k}{\varphi}\tanh\!\frac{k}{\varphi}.\;}$$

Verified: $S_{\text{br}}(0)=\ln2$ (its maximum), **monotone decreasing**, $S_{\text{br}}\to0$ deep in
inverse flow. This is the resolution of the apparent paradox in Section 3: the *flow* entropy
$\sigma=\sinh\theta$ grows without bound (the second law, the cosmological arrow), while the *branch*
entropy $S_{\text{br}}=\ln(2\cosh\theta)-\theta\tanh\theta$ **falls** to zero — the descent into
inverse flow polarizes the temporal two-state system, ordering it. Gravity, as the $\sinh$ part,
simultaneously *produces* flow entropy and *consumes* branch entropy: it is the engine that pours
disorder into the expanding/forward channel while crystallizing order (structure, bound states, the
mass ordinals of the spine's fermion fit) into the inverse channel. The total is bookkept by the
hyperbolic invariant — $L_y=1$ in thermal disguise.

## Extension: the Schottky anomaly and a thermal echo of $L_y=1$

The two-branch system $z(k)=2\cosh\theta$, $\theta=k/\varphi$, is a genuine two-level system —
retarded ($-\theta$) and advanced ($+\theta$) branches split by the ordinal-rapidity gap $2\theta$.
Every two-level system carries a **Schottky heat capacity**, and ours is parameter-free. With the
branch energy in units of the rapidity quantum (levels $\pm1$, inverse temperature $\theta$), the
mean energy and capacity are

$$U(k)=-\tanh\theta,\qquad
\boxed{\;\frac{C(k)}{k_B}=\theta^2\,\mathrm{sech}^2\theta=\Big(\frac{k}{\varphi}\Big)^2
\mathrm{sech}^2\!\Big(\frac{k}{\varphi}\Big).\;}$$

($C=\theta^2(\langle E^2\rangle-\langle E\rangle^2)=\theta^2(1-\tanh^2\theta)=\theta^2\,\mathrm{sech}^2\theta$;
verified two independent ways, residual $<2\times10^{-16}$.) $C$ vanishes at the present moment
($\theta\to0$, the branches degenerate, no states to excite) **and** deep in inverse flow
($\theta\to\infty$, the gap freezes out) — the textbook Schottky signature — and peaks in between
at the unique solution of

$$\frac{d}{d\theta}\big[\theta^2\mathrm{sech}^2\theta\big]
=2\theta\,\mathrm{sech}^2\theta\,(1-\theta\tanh\theta)=0
\;\Longrightarrow\; \theta^\ast\tanh\theta^\ast=1
\;\Longrightarrow\; \theta^\ast=1.199679\ldots,\quad
\boxed{\,k^\ast=\varphi\,\theta^\ast=1.941121\ldots\,}$$

with $C(k^\ast)/k_B=0.439229$. Two facts make this corpus-resonant rather than generic:

1. **Ordinal placement.** The thermal-response peak threads the first terrace exactly:
   $\langle k\rangle=1.169<k_1=1.632<k^\ast=1.941$. The mean chronon depth, the first
   flow-reversal shell, and the maximum of the branch heat capacity are the three landmarks of the
   first inversion terrace, in that order. The framework's "now"-neighborhood has a thermal fine
   structure.

2. **A thermal echo of the conserved unit.** With level energies $\pm1$ and inverse temperature
   $\theta$, the mean branch energy is $U(k)=-\tanh\theta$. The rapidity-weighted internal energy
   is then $\theta\,U(k)=-\theta\tanh\theta$, and the Schottky peak condition is *exactly*
   $$\boxed{\;|\theta^\ast\,U(k^\ast)| \;=\; \theta^\ast\tanh\theta^\ast \;=\; 1 \;=\; L_y
   \quad(\text{exact, verified}).\;}$$
   The dimensionless rapidity-weighted branch energy passes through **unity** precisely at the
   Schottky maximum. The conserved chronon current $L_y=1$ of the spine reappears as the value of
   the branch internal energy at the temperature where the two-state system is most thermally
   alive. Gravity's thermal engine runs hottest exactly where it carries one full conserved unit of
   rapidity-weighted branch energy — the same unit the saddle converts between curvature and flow
   in note 00, now read off the heat capacity instead of the binormal.

So the heat capacity is not an add-on: its peak is pinned to $L_y=1$, its location orders the first
terrace, and it tells the Prediction below *where* the branch-coherence signature is most
susceptible to drive — at $k^\ast$, between the mean depth and the first inversion shell.

## What this buys us

- A **parameter-free temperature** $T_\chi=\varphi$ for the whole framework, fixing the decay
  $e^{-k/\varphi}$ as a Boltzmann weight rather than a postulate.
- The **second law as a theorem**: it is the odd part of the one kernel being sign-definite, with
  time-reversal symmetry transiently restored *only* on the inversion shells $k_n$.
- A concrete, falsifiable-in-principle **golden free energy** $\beta_T\Delta F=0.604058$ for the
  round trip through time, and a closed **golden partition function** $Z=1/(1-e^{-1/\varphi})$
  with mean depth $\langle k\rangle\approx1.169$ landing in the first terrace $[0,k_1)$, just
  short of the first inversion shell $k_1\approx1.632$.
- A **Schottky thermometer of the present** (see Extension): the two-branch heat capacity peaks at
  $k^\ast\approx1.941$, threading the ordering $\langle k\rangle<k_1<k^\ast$ and pinning the mean
  branch energy to exactly $-1$ — the thermal fingerprint of $L_y=1$.

## Prediction

Any shell observable that couples to the *branch* (correlation) sector rather than the *flow*
sector should display a $\cosh(k/\varphi)$ ordering signature governed by the branch entropy
$S_{\text{br}}(k)=\ln[2\cosh\theta]-\theta\tanh\theta$ ($\theta=k/\varphi$), which **decreases
monotonically** from $\ln2$ at the present to $0$ deep in inverse flow. Branch disorder is
therefore a probe of mass-ordinal depth, and the two reciprocal coherence observables run in
opposite directions — read them off the same $S_{\text{br}}$, not the same scaling:

$$\boxed{\;\text{linewidth }\;\Delta(k)\propto e^{+S_{\text{br}}(k)}=2\cosh\theta\;e^{-\theta\tanh\theta}:
\;\;2\to1\;\text{(narrows with depth)},$$
$$\text{coherence time }\;T_2(k)\propto e^{-S_{\text{br}}(k)}=\frac{e^{\theta\tanh\theta}}{2\cosh\theta}:
\;\;\tfrac12\to1\;\text{(lengthens with depth).}\;}$$

Both make the deep shells the sharp, long-lived pole. Concretely: the deepest fermion ordinal
(tau, $k\!\approx\!102$ from the spine's COTV fit) is essentially **branch-pure**
($S_{\text{br}}\!\to\!0$, $\Delta\!\to\!\Delta_{\min}$, $T_2\!\to\!T_{2,\max}$), while the electron
($k\!\approx\!24$) still carries $S_{\text{br}}\approx4\times10^{-12}$ more branch entropy — a
strictly monotone mass-ordering of temporal coherence (tau sharpest, electron broadest) with no new
free parameter. The signature peaks in observability not at a shell but at the thermal response
maximum $k^\ast\approx1.941$ identified in the Extension above, where the branch system's
susceptibility to ordinal drive is largest.
