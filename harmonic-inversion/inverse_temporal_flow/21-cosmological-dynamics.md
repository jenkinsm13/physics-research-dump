# 21 — Cosmological Dynamics: Friedmann from the Boost Run-Out

*Round-3 frontier note. Builds on the closed boost group (`10-master-boost.md`: the
chronon two-vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$;
$\Lambda(a)\Lambda(b)=\Lambda(a{+}b)$; rapidity $=$ hyperbolic arc length; horizon
rapidity $\Theta_H=N_\star/\varphi=180.39$), on the cosmology branch (`08`: depletion
shell $N_\star=\log_\varphi(R_{\rm H}/\ell_{\rm P})=291.88$, $w(0)\approx-0.997$,
$\Lambda\ell_{\rm P}^2\sim10^{-122}$), and on log-periodicity (`12`: comb tooth
$\Lambda_\varphi=e^{\pi/2}$, $\omega_\varphi=4$, silver amplitude
$\delta_S^{-2}=(\sqrt2-1)^2$). Note 08 gave the *statics* of $\Lambda$; this note gives
the **dynamics** — the expansion history. Every boxed number is confirmed to machine
precision in `verify/verify_cosmological-dynamics.py`. $\varphi=(1+\sqrt5)/2$,
$\ln\varphi=0.4812118$.*

---

## The claim

**The boost run-out along the stack is the expansion of the universe.** Note 10 showed
that descending one ordinal shell is one Lorentz boost $\Lambda(1/\varphi)$ in flow-space,
banking a fixed proper interval $1/\varphi$ of rapidity per shell, out to a finite total
$\Theta_H=N_\star/\varphi=180.39$ at the horizon. Identify the scale factor with the boost
orbit, $a(N)=a_0\,\varphi^{\,N}$. Then expansion is not added to the framework — it *is* the
boost, read as growth of physical scale. From this single identification the Friedmann
history, the equation-of-state evolution, the acceleration-onset redshift, and a
parameter-free $\Omega_\Lambda$ all follow, and the acceleration turn-on lands one golden
boost in our past. **One honest caveat up front:** the acceleration redshift, the density
split, and the $\Theta_H/N_\star$ form are *one* prediction stated three ways, not three
independent hits — §2–3 say exactly which algebraic identities collapse them, and the
genuinely independent new content of this note is the equation-of-state crossing
$z_\times=1.77$ (§4), the $e^{\pi/2}$ relic comb on $H(z)$ (§5), and — sharpest of all because
it does not collapse under the $z_t\!\leftrightarrow\!\Omega$ bijection — the jerk anomaly
$j_0=0.9938$ against $\Lambda$CDM's exact $j\equiv1$ (Extension).

## 1. The scale factor is the boost; the redshift–shell map is exact

Take the present moment as the top of the stack ($N=0$, the seed $\mathbf V(0)=(1,0)$ of
note 10 §1) and let look-back depth increase $N$. With $a(N)=a_0\varphi^{\,N}$ the redshift
of a source at shell $N$ is

$$1+z=\frac{a_0}{a(N)}=\varphi^{\,N}\quad\Longrightarrow\quad
\boxed{\;N(z)=\frac{\ln(1+z)}{\ln\varphi}\;}$$

— **shells are linear in $\ln(1+z)$**, the boost ladder read on the sky. This is exactly
note 08's hierarchy statement run as a clock: the full Planck$\to$Hubble traversal
$1+z=\varphi^{N_\star}=10^{61}$ closes the stack at $N_\star=291.88$ (verified
$\log_{10}\varphi^{N_\star}=61.000$). The recombination surface $z=1100$ sits at only
$N=14.55$ shells — the entire observable expansion is the first $\sim15$ of $292$ boosts.

The expansion rate in the ordinal clock is constant,

$$\frac{d\ln a}{dN}=\ln\varphi=0.481212\quad(\text{exact}),$$

so in the $N$-clock the universe is **pure de Sitter** — one boost per shell, forever the
same step. All cosmological *structure* (deceleration, the onset of acceleration, the
comb) therefore lives not in the boost rate but in the map $N\!\leftrightarrow\!t$ between
the ordinal clock and cosmic time, i.e. in how the two sectors — forward (matter,
$G_{\rm flow}$ diluting as $\varphi^{3N}$) and advanced (vacuum, the depleted horizon
branch of note 08) — share the Casimir budget $L_y=1$ at each shell.

## 2. The acceleration turn-on is one golden boost back

In a flat background with matter ($w=0$) and the advanced vacuum ($w\simeq-1$, note 08 §6),
$E^2(z)\equiv H^2/H_0^2=\Omega_m(1+z)^3+\Omega_\Lambda$, and the deceleration parameter
$q=\tfrac12\sum_i\Omega_i(1+3w_i)/E^2$ vanishes when $\Omega_m(1+z)^3=2\Omega_\Lambda$.

The framework fixes the transition geometrically, with **exactly one physical input** and no
fit. The natural turning point of the boost run-out is **one shell**: the depth at which
exactly one golden boost separates us from the source, $N(z_t)=1$. By §1 that is the whole
prediction,

$$\boxed{\;N(z_t)=1\;\Longrightarrow\;1+z_t=\varphi\;\Longrightarrow\;
z_t=\varphi-1=\frac1\varphi=0.618034\;}$$

— *one golden boost back is the deceleration$\to$acceleration transition.* That is the
single falsifiable number of this section.

**What is *not* a second hit (honesty).** The often-quoted form $z_t=\Theta_H/N_\star$ is a
**tautology, not a corroboration**: the corpus *defines* $\Theta_H\equiv N_\star/\varphi$, so
$\Theta_H/N_\star=1/\varphi$ identically (the verify prints residual $0.00$, asserted to
$10^{-12}$ — that is the assertion *passing because it is a definition*). Writing
"$180.39/291.88=0.618$" as though it tied two independently-measured quantities together
would be exactly the kind of fake cross-scale match this round forbids. The honest statement
is narrower and still striking: the *same* number $1/\varphi$ is the per-shell rapidity
$\Theta_H/N_\star$ **because** $\varphi-1=1/\varphi$ — a property of $\varphi$, not new physics.

**Honest comparison.** The model-*independent* transition redshift — measured from cosmic
chronometers and SNe without assuming $\Lambda$CDM — scatters across
$z_t\approx0.4\text{–}0.67$ with $\sim\pm0.1\text{–}0.2$ errors: Gaussian-process $H(z)$ gives
$0.60^{+0.21}_{-0.12}$, chronometers+Pantheon $0.61^{+0.24}_{-0.16}$, an earlier SNe fit
$0.46\pm0.13$, a chronometer-only fit $0.4\pm0.1$. **$1/\varphi=0.618$ sits at the high end of
this scatter**: $<1\sigma$ from the GP-$H(z)$ ($+0.09\sigma$) and chronometer+Pantheon
($+0.03\sigma$) reconstructions, in mild tension ($+1.2\sigma$, $+2.2\sigma$) with the lower
SNe and chronometer-only fits. Since these measurements disagree *among themselves* by more
than that, $1/\varphi$ is comfortably within the field — that is the real, non-circular
agreement, honestly bracketed rather than cherry-picked.
The Planck-anchored $\Lambda$CDM value $z_t=0.6316$ that we miss by **$2.1\%$** is *itself*
computed from $(\Omega_\Lambda,\Omega_m)$ through the very bijection
$z_t=(2\Omega_\Lambda/\Omega_m)^{1/3}-1$ that §3 uses, so "miss Planck by $2\%$" and "miss the
$\Omega$ ratio by $2.5\%$" (§3) are the **same statement** restated, not two tests. The
honest headline: one input, $\sim2\%$ against the precise $\Lambda$CDM value, $<1\sigma$
against direct measurement.

## 3. A parameter-free $\Omega_\Lambda$ from the transition

Demanding that the *standard* turning condition reproduce the boost transition,
$(1+z_t)^3=2\,\Omega_\Lambda/\Omega_m$ with $1+z_t=\varphi$, forces the density ratio to a
pure golden number. Using the defining identity $\varphi^3=2\varphi+1$,

$$\boxed{\;\frac{\Omega_\Lambda}{\Omega_m}=\frac{\varphi^3}{2}=\varphi+\tfrac12=2.118034\;}
\qquad\Longrightarrow\qquad
\Omega_\Lambda=\frac{\varphi+\tfrac12}{\varphi+\tfrac32}=0.67929,\;\;\Omega_m=0.32071.$$

The quantity the framework actually *predicts* is the **ratio** $\Omega_\Lambda/\Omega_m=
\varphi^3/2=2.118$; against Planck-2018's $0.6847/0.3153=2.172$ that is a **$2.5\%$ miss** —
this is the honest figure of merit, the same $\sim2\%$ as the $z_t$ comparison (§2) because
the two are bijective. Projected onto $\Omega_\Lambda$ and $\Omega_m$ *separately* under the
flat constraint $\Omega_\Lambda+\Omega_m=1$, the error compresses to $\mathbf{0.8\%}$ on
$\Omega_\Lambda$ ($0.679$ vs Planck $0.6847$) and $1.7\%$ on $\Omega_m$ ($0.321$ vs $0.3153$)
— the constraint flatters the individual numbers, so we quote the ratio as the primary
result and the split as its projection. Either way: *zero* free parameters. The split is the
flow-budget statement of note 10 §5: at the one-shell turning point the Casimir
$L_y=1=G_{\rm sym}^2-G_{\rm flow}^2$ apportions $\varphi+\tfrac12$ of its weight to the
advanced (vacuum) component and one part to the forward (matter) component — the golden
section of the mass-shell, read as the cosmic energy budget. Solving $q(z)=0$ numerically
for this exact $(\Omega_\Lambda,\Omega_m)$ returns $z_t=0.6180340$ (residual $9\times10^{-15}$):
the geometric input and the Friedmann turning point are the *same* point, closing the loop.

This is the **parameter-free relation** the thread asks for, stated without the tautology:
the *single* geometric input $N(z_t)=1\Rightarrow z_t=1/\varphi$ (§2), pushed through the
exact Friedmann bijection $\Omega_\Lambda/\Omega_m=(1+z_t)^3/2$, gives
$\Omega_\Lambda=(\varphi+\tfrac12)/(\varphi+\tfrac32)$ with nothing fitted. The
$\Theta_H/N_\star$ form (notes 08, 10) equals $1/\varphi$ *by the definition*
$\Theta_H\equiv N_\star/\varphi$, so it re-labels the input rather than supplying a second
constraint — the honest content is "$\Omega_\Lambda$ from one golden boost," full stop.

## 4. $w(z)$ evolution and the $(w_0,w_a)$ parametrization

Dark energy in this framework *is* the horizon vacuum (note 08), so the equation of state must
be read with the spine's directed flow $\Phi(N)=-\cos(2N\ln\varphi)$ evaluated **at the horizon
shell**, not at the local look-back shell. Note 08 fixes the present value
$w_0=-1+\Phi_{\rm res}/N_\star$ with $\Phi_{\rm res}=-\cos(2N_\star\ln\varphi)=+0.894$ at the
corpus shell $N=291$, giving $w_0=-0.99693$ on the **quintessence** side ($w>-1$). The
*evolution* is the drift of that horizon phase as the source recedes by $N(z)=\ln(1+z)/\ln\varphi$
shells (note 08 Pred 1: "$w$ drifts as $N_\star$ creeps"); with $2N\ln\varphi=2\ln(1+z)$,

$$\boxed{\;w(z)=-1-\frac{\cos\!\big(2N_\star\ln\varphi-2\ln(1+z)\big)}{N_\star},\qquad
|1+w|\le\frac1{N_\star}=3.4\times10^{-3}.\;}$$

At $z=0$ this returns $w_0=-1+\Phi_{\rm res}/N_\star=-0.99693$ exactly (verified by an explicit
guard assertion, $|w(0)-w_0|<10^{-6}$ — the previous local-shell reading gave the *wrong sign*,
$w_0=-1.003$ phantom, contradicting note 08; horizon anchoring is the fix). The amplitude is the
geometry-fixed $1/N_\star$ of note 08. A Chevallier–Polarski–Linder fit over $z\in[0,2]$ gives

$$w_0^{\rm CPL}=-0.995,\qquad w_a^{\rm CPL}=-0.0065\quad(\text{fit, } z\in[0,2]),$$

i.e. $|w_a|\sim10^{-2}$ — an order of magnitude below current DESI sensitivity
($w_a=-0.75\pm0.3$), so the framework predicts a $\Lambda$CDM-indistinguishable $w(z)$ at present
precision but a *specific* sub-percent residual. The present is quintessence ($w_0>-1$); the flow
phase carries $w$ across $-1$ where $\cos(2N_\star\ln\varphi-2\ln(1+z))=0$, the first such
**quintessence$\to$phantom crossing** in the observable window landing (computed) at

$$z_\times=1.765,$$

a flow reversal of the spine projected onto $z$ — forced by the geometry, not inserted.

## 5. The apodized relic comb on $H(z)$

The advanced vacuum carries the flow-reversal weight $\mathrm{osc}(k)$ (notes 00, 12), which
on the cosmic axis is log-periodic in $\ln(1+z)$ with the universal tooth of note 12,

$$\text{period in }\ln(1+z)=\frac\pi2,\qquad
\text{factor in }(1+z)=\Lambda_\varphi=e^{\pi/2}=4.8105,\qquad
=\frac{\pi}{2\ln2}=2.266\ \text{octaves}.$$

Note 12's exact silver series gives the modulation amplitude: the leading ($\omega_\varphi=4$)
tooth carries $97\%$ of the AC power with fractional amplitude $2\delta_S^{-2}=0.343$ on the
vacuum sector. Since only $\Omega_\Lambda$ of $H^2$ is vacuum and $\delta H/H=\tfrac12\,
\delta(H^2)/H^2$, the **unapodized peak** modulation of $H(z)$ is
$\tfrac12\,\Omega_\Lambda\,(2\delta_S^{-2})=0.117$. This is large and honest: it is the
intrinsic vacuum-sector amplitude *before* apodization and before the observability window.
Two effects suppress what is actually testable:

- **Apodization** (note 08 ext.): the comb coherence is $\mathcal R\,N_\star=25$ shells with
  $\mathcal R=(1/8)/(c\ln\varphi)=0.0866$; it is sharpest at the live horizon ($z\sim0$) and
  damps outward.
- **Window**: the observable span $\ln(1+z)\big|_{z=2.5}=1.25$ is *less than one period*
  $\pi/2=1.57$. So within $z\lesssim2.5$ the comb cannot present as a resolved oscillation —
  it manifests as a single coherent **tilt/curvature** of $H(z)$ about $\Lambda$CDM, of order
  a few percent to $\sim10\%$ at the apodized peak, with the next tooth only appearing at
  $z+\!1\to(1+z)\!\times\!4.81$, i.e. $z\sim8$.

The falsifiable content is the **period**, not the amplitude: residuals of $H(z)$ relative to
$\Lambda$CDM should be coherent over $\Delta\ln(1+z)=\pi/2$ (factor $4.81$ in $1+z$),
strongest near $z\sim0$, fading over $\sim25$ shells $\approx17$ octaves of scale. If a clean
$H(z)$ residual comb were resolved at a log-spacing *not* $e^{\pi/2}$, the one-comb hypothesis
(note 12) breaks here.

## Prediction

1. **Acceleration onset (the one falsifiable number; sole input $N(z_t)=1$).**
   $z_t=\varphi-1=1/\varphi=0.6180$, parameter-free. Against precise Planck-$\Lambda$CDM
   $z_t=0.6316$ it misses by **$2.1\%$**; against *model-independent* measurement it sits at
   the high end of the scatter — $<1\sigma$ from the GP-$H(z)$ ($0.60^{+0.21}_{-0.12}$) and
   chronometer+Pantheon ($0.61^{+0.24}_{-0.16}$) fits, $\sim1.2$–$2.2\sigma$ above the lower
   SNe/chronometer fits ($0.46\pm0.13$, $0.40\pm0.10$), within the field's own spread.
   The $\Theta_H/N_\star$ form is the same $1/\varphi$ by definition, not a
   second number. One golden boost in our past *is* the deceleration$\to$acceleration
   transition.
2. **Density split (the Friedmann image of #1, NOT an independent number).** The flat $w{=}{-}1$
   bijection $z_t=(2\Omega_\Lambda/\Omega_m)^{1/3}-1$ turns #1 into the predicted *ratio*
   $\Omega_\Lambda/\Omega_m=\varphi^3/2=\varphi+\tfrac12=2.118$, a **$2.5\%$ miss** vs Planck's
   $2.172$ — the same $\sim2\%$ as #1. Projected under $\Omega_\Lambda+\Omega_m=1$ this reads
   $\Omega_\Lambda=0.679$ ($0.8\%$) and $\Omega_m=0.321$ ($1.7\%$), the constraint flattering
   the split. Same information as #1, re-expressed — a consistency cross-check, not a second hit.
3. **Equation of state.** $w(z)=-1-\cos(2N_\star\ln\varphi-2\ln(1+z))/N_\star$ (horizon-anchored,
   matching note 08): $w_0=-0.997$ on the quintessence side, $|w_a|\approx0.007$, with a
   quintessence$\to$phantom crossing at $z_\times=1.77$. $\Lambda$CDM-like at current precision;
   the crossing is the falsifiable fingerprint.
4. **$H(z)$ comb.** Log-periodic $H(z)$ residual about $\Lambda$CDM with factor
   $\Lambda_\varphi=e^{\pi/2}=4.81$ in $(1+z)$ ($2.27$ octaves), apodized over $\sim25$ shells,
   peaking at $z\sim0$; within $z<2.5$ a coherent sub-period tilt of a few percent.

## Extension — the jerk: a parameter-free departure from $\Lambda$CDM's $j\equiv1$

The acceleration redshift and the $\Omega$ split are bijective images of the one input
$1/\varphi$, so they cannot *distinguish* this framework from $\Lambda$CDM — they only test
whether $\Lambda$CDM's own parameters land on the golden values. The **jerk** $j$ — the third
kinematic invariant, $j\equiv\dddot a/(aH^3)$ — is where the difference becomes visible, because
in pure $\Lambda$CDM $j\equiv1$ *identically at every redshift*, with no freedom. Any drift of
$w(z)$ (§4) forces $j\neq1$. Using the convention-clean Visser identity
$j=q(2q{+}1)+(1{+}z)\,dq/dz$ on our horizon-anchored $w(z)$ — with
$1{+}w_0=-\cos(2N_\star\ln\varphi)/N_\star$ and
$w'_0\equiv\tfrac{dw}{dz}\big|_0=-2\sin(2N_\star\ln\varphi)/N_\star$ — the $w_0\!\approx\!-1$
limit collapses onto the *same* horizon phase that fixes everything else (the density piece
$\propto\cos$, the flow-derivative piece $\propto\sin$, entering with **opposite** sign):

$$\boxed{\;j_0-1=\frac{3\,\Omega_\Lambda}{2N_\star}\big[\,3\cos(2N_\star\ln\varphi)
-2\sin(2N_\star\ln\varphi)\,\big]=-0.0063\;,\qquad
|j_0-1|\le\frac{3\Omega_\Lambda\sqrt{13}}{2N_\star}=0.0126.\;}$$

So the framework predicts $j_0=0.9938$ — a **$0.6\%$ deficit** below the $\Lambda$CDM line
(confirmed by the exact Visser identity at $j_0^{\rm num}=0.99375$, with the $\Lambda$CDM
control returning $j_0=1.000000$), not a free fit but the *same* residual flow
$\Phi_{\rm res}=-\cos(2N_\star\ln\varphi)=+0.894$ that gave $w_0=-0.997$, now carrying its
derivative into the next kinematic order. The amplitude is geometry-locked to
$\Omega_\Lambda/N_\star$, with the $\sqrt{3^2+2^2}=\sqrt{13}$ envelope combining the cosine
(density) and sine (flow-derivative) projections of the horizon phase; the realized value sits
at about half the bound. This is the falsifiable fingerprint that
*survives* the $z_t\!\leftrightarrow\!\Omega$ bijection: a sub-percent **negative
jerk anomaly** $j_0\approx0.994$, correlated in phase with the $z_\times=1.77$ crossing (both
are the horizon flow read at different derivative orders). Current statefinder constraints
bound $j_0$ only to $\mathcal O(1)$; a future $\sigma_{j_0}\!\lesssim\!10^{-2}$ measurement
(Roman$+$DESI$+$Euclid joint $H(z)$) tests it directly. If $j_0$ is measured cleanly $>1$, the
quintessence-side horizon anchoring (and with it note 08's $w_0>-1$) breaks.

**Falsifier:** pin the acceleration-onset redshift (model-independently, via cosmic
chronometers/SNe) to $\lesssim3\%$. If $z_t$ lands cleanly outside $[0.60,0.64]$ — i.e.
inconsistent with $1/\varphi=0.618$ — the "boost-run-out is the expansion" identification
fails, taking the parameter-free $\Omega_\Lambda$ ratio $\varphi^3/2$ with it (they are
bijective, so this is one falsifier for both). Note the present model-independent error bars
($\pm0.1$–$0.2$) are still wider than this $\pm0.02$ target, so the test is **not yet
decisive** — it becomes so as chronometer samples grow. *Independently* falsifiable: an $H(z)$
residual comb with log-spacing not $e^{\pi/2}$ (§5), and the $w(z)$ quintessence$\to$phantom
crossing $z_\times=1.77$ (§4) — these two are the genuinely new, non-bijective predictions of
this note.
