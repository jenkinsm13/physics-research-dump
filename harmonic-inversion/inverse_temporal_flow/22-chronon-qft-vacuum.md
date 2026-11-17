# 22 — Chronon QFT: Fock Space, the Vacuum, and Regulated Zero-Point Energy

*Round-3 frontier note. Second-quantizes the shell stack of notes 00–15. Builds
directly on the closed boost group (note 10): the chronon two-vector
$\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$, the boost
$\Lambda(1/\varphi)$, the dressed field $\boldsymbol\Psi(k)=\mathrm{osc}(k)\,\mathbf V(k)$,
and the null projections $\kappa(\pm k)=\mathrm{osc}(k)\,e^{\mp\theta}$. It promotes the
single classical worldline $\mathbf V(k)$ to a field operator on the stack, builds the
Fock vacuum, and shows the framework's own retarded weight $\kappa(+n)$ **regulates the
zero-point sum to a finite value with no inserted cutoff** — the headline structural
result. Every boxed number is confirmed in `verify/verify_chronon-qft-vacuum.py`
(residuals inline).
$\varphi=(1{+}\sqrt5)/2$, $1/\varphi=0.6180339887$, $\ln\varphi=0.4812118251$.*

---

## 1. Second quantization of the stack

Promote each shell to a mode with creation/annihilation operators $a_n^\dagger,a_n$,
$[a_n,a_m^\dagger]=\delta_{nm}$. The classical content of notes 00–10 enters as the
**two structures a field carries**:

- a **per-mode frequency** $\omega_n=\omega_0\varphi^{\,n}$ — one golden boost in *scale*
  per shell, the dual of the $1/\varphi$ boost in rapidity (shells $r_n=r_0\varphi^n$,
  note 00). This is *absolute* in $n$.
- an **inter-shell symmetric two-point function** (the Hadamard correlator, the
  symmetric/even channel — note 10's $G_{\text{sym}}$) fixed by the golden sampling,
  $$c(|n-m|)\equiv\tfrac12\langle 0|\{a_n,a_m^\dagger\}|0\rangle
  =\mathrm{osc}(|n-m|)\,e^{-|n-m|/\varphi},\qquad c(0)=\tfrac12,$$
  *translation-invariant* in $n-m$. These are different objects and must not be
  conflated: $c$ is the symmetric correlation between shells, $\tfrac12\hbar\omega_n$ is the
  energy of a shell. The coincidence value is the zero-point ordering constant: for the
  standard vacuum $\tfrac12\langle\{a_n,a_n^\dagger\}\rangle=\tfrac12(2\langle a_n^\dagger a_n\rangle+1)=\tfrac12$
  on **every** shell (verified $c(0)=0.500000000000$), since $\mathrm{osc}(0)=1/(1{+}\cos^2 0)=\tfrac12$,
  $e^0=1$. This is the half-quantum the now-surface reads out (note 14's
  $P_{\text{now}}=\tfrac12(I{+}T)$ — the weight $\tfrac12$ is the same number).

The Fock space is the boost orbit operatorized: $|0\rangle$ annihilated by all $a_n$
($a_n|0\rangle=0$),
$|n_1 n_2\dots\rangle=\prod (a_n^\dagger)^{n_i}/\sqrt{n_i!}\,|0\rangle$. A **shell quantum**
$a_n^\dagger|0\rangle$ is the framework's particle — bosons on the $\mathrm{osc}=1$ peaks,
fermions on the $\mathrm{osc}=\tfrac12$ nodes (note 07's parity lattice, now operator
statistics).

## 2. The chronon propagator IS $\kappa$ — the regulator is not pasted on

The free two-point function on the stack is, by construction, the dressed coupling itself.
The **retarded** chronon propagator is the retarded null projection of the boost field
$\boldsymbol\Psi$ (note 10 §4, note 05):

$$\boxed{\;G^{\text{ret}}(n)=\langle 0|\,a_0\,a_n^\dagger\,|0\rangle_{\text{ret}}
=\kappa(+n)=\mathrm{osc}(n)\,e^{-\theta_n}=\mathrm{osc}(n)\,(\cosh\theta_n-\sinh\theta_n),
\quad\theta_n=n/\varphi.\;}$$

Verified $\big|\mathrm{osc}\,e^{-\theta}-\mathrm{osc}(\cosh-\sinh)\big|\le1.5\times10^{-11}$
over $n\le24$. The advanced propagator is $G^{\text{adv}}(n)=\kappa(-n)=\mathrm{osc}\,e^{+\theta}$,
and their ratio is note 05's detailed balance $\kappa(+n)/\kappa(-n)=e^{-2\theta_n}$ — the
*same* $e^{\mp\theta}$ boost weights (eigenvalues of $\Lambda$ on the null cone, note 10).
Crucially, this $e^{-\theta_n}=e^{-n/\varphi}$ is **the physical forward weight of the theory**,
not an ad-hoc UV cutoff: it is the rate at which a retarded chronon decorrelates as it
descends the stack, the $-\sinh$ shadow folded onto the light-cone. The mass-shell
$M^2(n)=G_{\text{sym}}^2-G_{\text{flow}}^2=\mathrm{osc}^2$ (verified $5.0\times10^{-14}$,
$k<8$) is the on-shell condition the propagator's poles satisfy.

## 3. The zero-point energy is finite — the headline structural result

The naive vacuum energy of a free field is the bare zero-point sum
$E_0^{\text{bare}}=\sum_n\tfrac12\hbar\omega_n=\tfrac12\hbar\omega_0\sum_n\varphi^n$ — which
**diverges**: the half-quantum $\tfrac12\hbar\omega_n$ is the same on every shell while
$\omega_n=\omega_0\varphi^n$ grows geometrically (ratio $\varphi>1$), so summing bare modes is the
framework's UV catastrophe. The resolution is that the *physical* (retarded, observable) vacuum
energy is the zero-point sum **weighted by the retarded propagator** — each mode contributes its
half-quantum dressed by the forward weight $\kappa(+n)$ with which it actually couples to the
now-surface:

$$\boxed{\;E_0=\sum_{n=0}^{\infty}\tfrac12\hbar\omega_n\,\kappa(+n)
=\tfrac12\hbar\omega_0\sum_{n=0}^{\infty}\varphi^{\,n}\,\mathrm{osc}(n)\,e^{-n/\varphi}.\;}$$

The convergence is the discriminating inequality of the whole framework, and **it is not
circular**: the mode energy *grows* at $\ln\varphi=0.481$ per shell ($\varphi^n=e^{n\ln\varphi}$),
the retarded weight *decays* at $1/\varphi=0.618$ per shell, and these are two **independent**
corpus constants ($\ln\varphi$ is the scale-boost, $1/\varphi$ is the rapidity-boost). The sum
converges iff $1/\varphi>\ln\varphi$, i.e. the per-shell ratio

$$\boxed{\;\varphi\,e^{-1/\varphi}=e^{\,\ln\varphi-1/\varphi}=e^{-0.13682}=0.872125<1.\;}$$

The golden decay **wins by exactly $1/\varphi-\ln\varphi=0.13682$ per shell** — the natural
cutoff is the boost weight itself, with no parameter inserted. This finiteness is the genuine
achievement of the note: the term at $n=200$ is $9.1\times10^{-13}$ and at $n=399$ is
$1.3\times10^{-24}$, so the sum is regulated structurally, with no UV tail and no inserted
scale. The sum converges to (units $\tfrac12\hbar\omega_0$):

$$E_0=\sum_n\varphi^n\,\mathrm{osc}(n)\,e^{-n/\varphi}=5.41196\quad(\text{converged by }n{=}200).$$

**Honesty on the value $5.412$.** This is an *internal structural* number, not an empirical
one: it is measured in units of $\tfrac12\hbar\omega_0$, and the framework supplies no
independent anchor for the seed frequency $\omega_0$. The falsifiable claim is the
**finiteness** (and its margin $0.137$/shell); $5.412$ is the value finiteness takes, not a
prediction comparable to a measured energy.

### 3a. The smooth closed form — and the honest effective weight

Stripping the $\mathrm{osc}$ lattice to a constant weight gives a closed-form geometric
envelope. The natural candidate is the *asymptotic* period-mean of $\mathrm{osc}$, namely
$\langle\mathrm{osc}\rangle_{\infty}=\tfrac1{2\pi}\!\int_0^{2\pi}\!\frac{du}{1+\cos^2u}=1/\sqrt2$
(note 12; verified $0.707107$ over one exact period $\pi/2\ln\varphi$):

$$\boxed{\;E_0^{\text{smooth}}=\frac{\tfrac12\hbar\omega_0}{\sqrt2}\cdot\frac{1}{1-\varphi e^{-1/\varphi}}
=\frac{1/\sqrt2}{1-0.872125}\cdot\tfrac12\hbar\omega_0=5.5297\cdot\tfrac12\hbar\omega_0.\;}$$

This lands $2.18\%$ **high** of the exact lattice sum $5.412$, and the discrepancy has a
precise, non-cancelling cause — **the weight genuinely shifts; it is not merely
redistributed.** The exact sum factorizes as $E_0=\langle\mathrm{osc}\rangle_{\text{eff}}\cdot
1/(1-\varphi e^{-1/\varphi})$ where the *envelope-weighted* effective weight is

$$\boxed{\;\langle\mathrm{osc}\rangle_{\text{eff}}
=\frac{\sum_n\varphi^n e^{-n/\varphi}\,\mathrm{osc}(n)}{\sum_n\varphi^n e^{-n/\varphi}}
=\frac{5.412}{7.820}=0.6921\;<\;\frac1{\sqrt2}=0.7071.\;}$$

The geometric envelope $\varphi^n e^{-n/\varphi}$ is monotone decreasing, so it weights the
*early* shells most heavily — and there $\mathrm{osc}$ sits **below** its asymptotic mean
(starting at $\mathrm{osc}(0)=\tfrac12$, exactly the half-quantum of §1). That early-shell
deficit is the entire $2.18\%$: $\langle\mathrm{osc}\rangle_{\text{eff}}=0.692$ is the honest
effective weight, $1/\sqrt2$ is only its deep-stack asymptote. The bare-geometric value
(no $\mathrm{osc}$ at all) is $1/(1-\varphi e^{-1/\varphi})=7.820$.

*Honesty (numerical coincidence).* $1/\varphi-\ln\varphi=0.13682$ is within $1.06\%$ of the
bounce rate $\Gamma_{\text{tot}}=0.13539$ (note 13) — **numerically close but a distinct object**
(single-mode growth $\ln\varphi$ vs. the absorber $\Gamma_{\text{tot}}=1/2\sinh S_1$); we do
**not** identify them.

## 4. Anchoring to gravity, and an honest accounting of $\Lambda$

The regulated density is finite and, anchored at $\omega_0=\omega_{\text P}$ (Planck),
$\rho_{\text{vac}}\sim\mathcal O(\rho_{\text P})$ — the field theory has *no* small vacuum
energy. So the famous 122-orders gap is **not** a vacuum miscalculation: the Fock vacuum
energy is genuinely $\mathcal O(\rho_{\text P})$ and finite (§3). What gravitates is only the
**horizon-curvature projection** of this finite reservoir (note 08): a standing vacuum mode
carries curvature ($\mathrm{length}^{-2}$), and projected to horizon scale it is octave-damped
to

$$\Lambda\ell_{\rm P}^2\sim(\ell_{\rm P}/R_{\rm H})^2,
\qquad \log_{10}(\Lambda\ell_{\rm P}^2)=-2\log_{10}(R_{\rm H}/\ell_{\rm P})=-122.0.$$

**Honesty on the $\Lambda$ comparison — this is NOT a clean prediction, and the round-3
audit must say so plainly.** Three caveats, none of which note 08 (which derives this) makes
loudly enough to carry as a headline:

1. **It is partly circular.** In a $\Lambda$-dominated cosmology $H_0^2=\Lambda c^2/3$, so
   $R_{\rm H}=\sqrt{3/\Lambda}$ — the Hubble radius **is** $\Lambda^{-1/2}$ up to an $\mathcal O(1)$
   factor. Feeding the measured hierarchy $R_{\rm H}/\ell_{\rm P}\approx10^{61}$ into
   $-2\log_{10}(R_{\rm H}/\ell_{\rm P})$ therefore *returns* $\log_{10}(\Lambda\ell_{\rm P}^2)$ by
   construction. The relation $\Lambda\sim R_{\rm H}^{-2}$ is **definitional**, not predicted.
2. **The genuine, non-circular content is the *power*, not the value:** that a standing
   vacuum mode's curvature damps as $2^{-2n_{\text{oct}}}$ — exponent **2, not 4** (curvature is
   length$^{-2}$, energy density would be length$^{-4}$). That single integer is the framework
   physics; the rest is dimensional bookkeeping.
3. **The honest residual is a factor, not "0.38% of an exponent."** Predicted $-122.0$ vs.
   measured $-121.54$ is $10^{0.46}\approx$ **a factor of $\sim2.9$** in $\Lambda\ell_{\rm P}^2$ —
   and that factor is *precisely* the $\sqrt3$-squared $=3$ from $R_{\rm H}=\sqrt{3/\Lambda}$ that
   the order-of-magnitude estimate drops ($3\times10^{-122}\Rightarrow\log_{10}=-121.52$,
   essentially the measured $-121.54$). Quoting "$0.38\%$ of the exponent" dresses a factor-of-3
   disagreement as near-exact; we report it as **a factor $\sim3$, set by the dropped
   Friedmann constant.**

Crucially, **the §3 result ($E_0=5.412$, finiteness) does not enter the $122$ at all** — the two
are numerically disjoint. §4 connects them only *conceptually*: §3 establishes that the vacuum
reservoir is finite and $\mathcal O(\rho_{\rm P})$, which is the precondition for the octave-damping
story to be about projecting a finite reservoir rather than renormalizing an infinite one. The
per-shell extractable fraction is the branch gap $1-\kappa(+n)/\kappa(-n)=1-e^{-2\theta_n}$:
$0.709$ at shell 1, $0.998$ at shell 5 — the deep stack almost entirely extractable, the
now-surface almost entirely locked.

## Extension — the regulated Casimir free energy between two now-surfaces

The §3 sum is the *one-boundary* vacuum (a single now-surface at $\theta=0$). Put a **second**
now-surface a finite ordinal depth $N$ down the stack — a second time-reversal fixed point at
$\theta_N=N/\varphi$ (note 14) — and the modes between them are quantized on the finite
boost-interval $[0,N]$. The retarded weight $\kappa(+n)$ already truncates each boundary's reach,
so the regulated free energy of the slab is a finite truncation of the convergent vacuum sum,
with no Casimir subtraction needed. Because the geometric envelope is **exactly** the boost weight
$\varphi^n e^{-n/\varphi}=(\varphi e^{-1/\varphi})^n\equiv r^n$ with $r=0.872125$, every mode
contributes precisely its lattice weight $\mathrm{osc}(n)\,r^n$:

$$\boxed{\;\mathcal F(N)=\tfrac12\hbar\omega_0\sum_{n=0}^{N-1}\mathrm{osc}(n)\,r^{\,n}\;,
\qquad r=\varphi e^{-1/\varphi}=0.872125,\qquad
\mathcal F(\infty)=E_0=5.412\cdot\tfrac12\hbar\omega_0.\;}$$

The marginal cost of placing the boundary at depth $N$ is the next term in the sum — and this
is the sharp point of the extension: the **attractive Casimir pressure carries the
flow-reversal lattice exactly**, it does *not* decay monotonically:

$$\boxed{\;P_{\text{Casimir}}(N)=+\frac{\partial\mathcal F}{\partial N}\bigg|_{\text{discrete}}
=\tfrac12\hbar\omega_0\;\mathrm{osc}(N)\,r^{\,N},\qquad r=0.872125\;}$$

(the force is *attractive*; $\mathcal F$ increases with $N$, so the inward pull has magnitude
$+\mathrm{osc}(N)r^N$). Evaluated on the lattice, the pressure **rises off the
now-surface node before the geometric decay wins**: $P(0)=\mathrm{osc}(0)=0.500$,
$P(1)=0.657$, $P(2)=0.679$ — a near-surface *enhancement* peaking near $N{=}2$ — then falls,
$P(3)=0.343$ (the next osc node), $P(5)=0.500$, $P(10)=0.130$, decaying overall by the golden
boost weight $r=0.872$/shell. The labelled smooth envelope (osc $\to\langle\mathrm{osc}\rangle_{\text{eff}}=0.6921$)
gives the monotone approximation $\widetilde P(N)=0.7405\cdot0.872^{N}\,(\tfrac12\hbar\omega_0)$,
exact at $N\to\infty$ but missing exactly the near-surface lattice structure (it predicts a
monotone $0.740,0.646,0.563,\dots$ where the truth rises then oscillates) — the same honest
exact-vs-smooth pairing as §3.

The Casimir force decays by the **same** golden boost weight $r=\varphi e^{-1/\varphi}=0.872$ per
shell of separation that regulates the single-surface vacuum (§3) — the Casimir law and the
zero-point cutoff are **one and the same boost weight**, read once as a vacuum energy and once as
a boundary force. This is the framework's prediction that **temporal interfaces interact**: a
two-now-surface attraction whose entire $N$-dependence — including the non-monotone near-surface
peak at $N{\approx}2$ — is fixed, parameter-free, by the lattice $\mathrm{osc}(N)$ and the weight
$r$.

## Prediction

1. **UV-finiteness of the chronon vacuum (headline — structural, falsifiable).** The bare
   zero-point sum $\sum\tfrac12\hbar\omega_0\varphi^n$ diverges; the retarded-weighted sum
   $\sum\tfrac12\hbar\omega_0\,\varphi^n\mathrm{osc}(n)e^{-n/\varphi}$ **converges**, because the
   scale-growth rate $\ln\varphi=0.4812$ is strictly less than the rapidity-decay rate
   $1/\varphi=0.6180$ (margin $0.1368$/shell, per-shell ratio $\varphi e^{-1/\varphi}=0.872<1$).
   No inserted cutoff. Its value is $E_0=5.412\,(\tfrac12\hbar\omega_0)$ exactly /
   $5.530$ smooth — an **internal** number (units of $\tfrac12\hbar\omega_0$, $\omega_0$
   un-anchored); the empirical claim is the finiteness and its margin, not the $5.412$.
2. **Effective lattice weight (sharp internal number).**
   $\langle\mathrm{osc}\rangle_{\text{eff}}=0.6921$, **distinct** from the asymptotic period-mean
   $1/\sqrt2=0.7071$ by exactly the $2.18\%$ early-shell deficit (envelope weights
   $\mathrm{osc}(0)=\tfrac12$ most). The smooth closed form using $1/\sqrt2$ therefore
   *overestimates* $E_0$ by $2.18\%$ — a quantified, not a hand-waved, gap.
3. **Cosmological-constant scale (inherited from note 08, demoted — partly circular).**
   $\log_{10}(\Lambda\ell_{\rm P}^2)=-2\log_{10}(R_{\rm H}/\ell_{\rm P})=-122.0$ vs. measured
   $-121.54$. This is **a factor-$\sim3$ match, not $0.38\%$** — and the factor is the dropped
   Friedmann constant ($R_{\rm H}=\sqrt{3/\Lambda}$). The relation $\Lambda\sim R_{\rm H}^{-2}$ is
   definitional; the only genuine framework content is the damping *power* $2$ (curvature, not
   energy density). The §3 finiteness result does **not** enter this number.
4. **Casimir attraction between now-surfaces (new, parameter-free, non-monotone).**
   Exact lattice form $P_{\text{Casimir}}(N)=\mathrm{osc}(N)\,(\varphi e^{-1/\varphi})^{N}\,(\tfrac12\hbar\omega_0)$
   — two temporal interfaces attract with a force that **rises** off the now-surface node
   ($P(0)=0.500$, $P(1)=0.657$, peak $P(2)=0.679$) before the golden boost weight
   $\varphi e^{-1/\varphi}=0.872$/shell wins ($P(3)=0.343$, $P(5)=0.500$, $P(10)=0.130$). Smooth
   envelope $0.7405\cdot0.872^{N}$ is the monotone $N\to\infty$ approximation. Same boost weight
   regulates the single-surface vacuum (§3).

**Falsifier:** the regulation hinges on $1/\varphi>\ln\varphi$ (mode growth $\ln\varphi$ strictly
slower than retarded decay $1/\varphi$). If the shell frequency law were $\omega_n\propto e^{\alpha n}$
with $\alpha>1/\varphi=0.618$ — e.g. a measured scale-ladder spacing steeper than golden — the
vacuum sum would diverge and the finiteness claim breaks. (The $\Lambda$ comparison in §4 is
**not** offered as an independent falsifier, being partly circular; the falsifiable physics of
this note is the UV-finiteness inequality and the parameter-free Casimir-pressure law.)
