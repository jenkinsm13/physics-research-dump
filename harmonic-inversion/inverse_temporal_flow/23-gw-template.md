# 23 — A Falsifiable GW Template: the Golden Ringdown Comb

*Round-3 note. Turns the qualitative ringdown picture of `15` into a concrete,
matched-filter template with hard numbers. Builds directly on the **closed boost
group** (`10`): the chronon two-vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$,
$\theta=k/\varphi$, with ordinal depth $=$ rapidity and the one-shell boost
$\Lambda(1/\varphi)$. Uses the round-1/2 locks: terrace ratio $e^{\pi/2}$ (`03`,`12`),
echo decrement $\gamma_{\rm echo}=e^{-S_1}=\Gamma_1=0.13300$ (`06`,`15`), golden
envelope exponent $\nu=1/(\varphi\ln\varphi)=1.28433$ (`03`,`15`), horizon shell
$n_H=\log_\varphi(r_s/\ell_P)$ (`08`,`15`). Anchors to the corpus LIGO re-analysis.
Every number below is reproduced in `verify/verify_gw-template.py`. Where a quoted
residual is $\sim10^{-16}$ it is float noise on an algebraic **identity** (flagged as
such, not empirical agreement); the genuine, falsifiable predictions are the
dimensional ones — the echo delay in ms, the overtone ratio, the timing ratio, and the
SNR detectability threshold.*

---

## 1. The template object: a boost-orbit of damped sinusoids

A ringdown in the framework is not one decaying mode plus exotic corrections; it is
the **boost orbit of a single seed pulse** read off the truncated Matryoshka stack.
Each successive echo is the seed advanced one terrace outward — one application of
$\Lambda(\Delta k/\varphi)$ with $\Delta k=\pi/(2\ln\varphi)$ — so the echo train is
the discrete group $\{\Lambda^m\}$ acting on the QNM seed. Two invariants of that
action fix the whole waveform: the **time dilation** per leg (a multiplicative delay
$e^{\pi/2}$, because terraces sit at fixed multiplicative radial steps
$r_{n+1}/r_n=\varphi^{\Delta k}=e^{\pi/2}$, `03`) and the **null weight** per leg
($e^{-\Delta k/\varphi}=e^{-S_1}$, the retarded projection of $\mathbf V$, `15`§5).
The explicit, cross-correlatable template is therefore

$$\boxed{\;h(t)=\sum_{m=0}^{\infty}\gamma_{\rm echo}^{\,m}\;
\Theta(t-t_m)\,e^{-(t-t_m)/\tau}\,\cos\!\big(2\pi f_0\,(t-t_m)+\psi\big),
\qquad t_m=t_0\,e^{m\pi/2}.\;}$$

Three numbers carry everything. $\gamma_{\rm echo}=e^{-S_1}=0.13300$ ($-17.52$ dB
per echo) is the **per-leg null weight** — the same first-bounce rate $\Gamma_1$ of
`06`, not a free parameter. The onset times $t_m=t_0e^{m\pi/2}$ are **log-periodic**,
spacing $\Delta\ln t=\pi/2$ — the boost-group orbit, not a hard-wall cavity's
arithmetic ladder. $(f_0,\tau)$ are the ordinary $\ell{=}2$ QNM fundamental and its
damping, the only event-specific scale.

The $m$-th echo's amplitude is **not** $m$ copies of an amplitude multiplied
together — that would be the forbidden $\kappa(a)\kappa(b)$ chaining. It is the
*single* null weight $e^{-\theta}$ evaluated at the rapidity **added** $m$ times along
the boost orbit, $\theta_m=m\,\Delta k/\varphi=m\,S_1$, so $h_m=e^{-\theta_m}=e^{-mS_1}$:
boosts add, weights of a single $\mathbf V$ are read once at the summed rapidity. This
is the $\Lambda^m$ orbit of `10`, not a product of legs.

A note on what is *checkable* here versus what is *identity*. Eliminating $m$ between
$\log h_m=-mS_1$ and $\log t_m=\log t_0+m\pi/2$ gives the comb-peak slope
$d\log h/d\log t=-2S_1/\pi=-\nu$ **by construction** — this is an algebraic identity,
$S_1\equiv\pi/(2\varphi\ln\varphi)$, *not* a fit that could have come out otherwise; the
verify script's $\sim10^{-16}$ residual is floating-point noise on a tautology, reported
only to confirm the code wires the identity correctly, never as empirical agreement. The
genuinely non-trivial, *predictive* content is that the two locks feeding this identity —
the time log-period $e^{\pi/2}$ (terrace ratio, `03`) and the amplitude decrement
$e^{-S_1}$ (bounce rate, `06`) — were derived on *independent* branches and only here
collide into one envelope exponent. The peak energies fall by
$\gamma_{\rm echo}^2=0.017689$ per echo, which **is** a cross-branch coincidence and not a
tautology: it equals the note-`06` bounce-ladder ratio $e^{-\pi/(\varphi\ln\varphi)}$
(matching to residual $3.5\times10^{-18}$) because $2S_1=\pi/(\varphi\ln\varphi)$ — one
echo amplitude $=\Gamma_1$, one echo *energy* $=$ the quantum ladder step. The template is
a classical waveform whose decrement is a quantum tunneling rate.

## 2. The analytic envelope: gravity's spatial law, read in time

Eliminating the discrete echo index $m=(2/\pi)\ln(t/t_0)$ between the time law
$t_m=t_0e^{m\pi/2}$ and the amplitude law $h_m=h_0e^{-mS_1}$ collapses the comb peaks
onto a power-law upper envelope

$$|h(t)|\sim t^{-2S_1/\pi}=t^{-\nu},\qquad
\nu=\frac{2S_1}{\pi}=\frac{1}{\varphi\ln\varphi}=1.2843283489\ldots$$

(residual $0$: $S_1=\pi/(2\varphi\ln\varphi)$ identically). This is the same exponent
as gravity's static fall-off $\Phi(r)\sim r^{-\nu}$ (`03`, `13`): the late-time
ringdown **tail in time** carries the identical golden exponent as the field's
fall-off **in space**, the space$\leftrightarrow$time duality of the boost two-vector
made into a measurable slope. A matched filter need only fit $(t_0,f_0,\tau)$; the
ratios $e^{\pi/2}$, $\gamma_{\rm echo}$, $\nu$ are *fixed by the group* — a
one-parameter family in the echo sector, far more constrained than free-ECO templates.

## 3. The first-echo delay for GW150914 — honest brackets

GW150914's remnant: $M_f\approx62\,M_\odot$, $a_f\approx0.70$, $f_0=f_{220}=251$ Hz,
$\tau_{220}=4.0$ ms, $Q=\pi f_0\tau=3.15$ (corpus $Q=3.2$, $1\%$). The horizon
light-crossing is $2r_s/c=1.222$ ms ($r_s=1.831\times10^5$ m). The first-echo delay
is the first boost leg, $\Delta t_{\rm echo}=t_0(e^{\pi/2}-1)$, $e^{\pi/2}-1=3.8105$.
The seed scale $t_0$ is where I must be honest — three physically-motivated choices:

| seed $t_0$ | $\Delta t_{\rm echo}=t_0(e^{\pi/2}-1)$ |
|---|---|
| QNM period $1/f_0=3.984$ ms | **15.18 ms** |
| damping time $\tau_{220}=4.0$ ms | **15.24 ms** |
| light-crossing $2r_s/c=1.222$ ms | **4.66 ms** |

The framework's natural seed is the QNM coherence scale $\sim\tau_{220}$ (the pulse
*is* the ringdown), giving $\Delta t_{\rm echo}\approx15$ ms; the conservative
light-crossing seed gives $\approx4.7$ ms. Either way the prediction lands in the
**few-to-15 ms** band. The published echo claim — Abedi–Afshordi (2017),
arXiv:1612.00266 — reported tentative GW150914 echoes at $\Delta t_{\rm echo}\approx
0.2$–$0.3$ s ($\sim$0.99×$t_{\rm merger}$ spacing), i.e. **$\sim200$–$300$ ms**. Our
prediction is **$\sim15$–$60\times$ shorter** than that claim. This is a sharp,
falsifiable split: the golden comb says the *first* echo is early (tens of ms) and
the *spacing* is multiplicative ($\times4.81$ each leg), not the near-constant
$\sim0.3$ s spacing of the Abedi–Afshordi ansatz. Onset times (seed $\tau_{220}$):
$4.0,\,19.2,\,92.6,\,445,\,2142$ ms with amplitudes $1,\,0.133,\,0.0177,\,0.0024,
\,0.0003$. The second echo is already $-35.0$ dB; **at most one echo (the $-17.5$ dB
first leg) plausibly survives LIGO noise**, consistent with the marginal status of
all echo searches to date — and the Extension below turns this into a hard SNR
threshold ($N_{\rm obs}=\lfloor\ln\rho_{\rm rd}/S_1\rfloor$), so it is derived, not
asserted.

## 4. The QNM overtone comb vs the GR Kerr spectrum — the sharpest test

Here the boost group makes a prediction that *qualitatively* breaks from GR. In Kerr,
the $\ell=m=2$ overtones $n=0,1,2,\dots$ are nearly **degenerate in real frequency**:
for $a_f=0.70$ the dimensionless $\mathrm{Re}(M\omega_{22n})=\{0.5326,0.5189,0.4936\}$
(Berti–Cardoso–Will fits), so $f_{221}/f_{220}=0.974$, $f_{222}/f_{221}=0.951$ —
ratios just *below* $1$, the overtones piling near the fundamental while their damping
grows. Converted for $M_f=62\,M_\odot$ these are $\approx277,270,257$ Hz — all within
$10\%$ of each other.

The framework instead reads the overtone ladder as a **terrace-cavity comb**, and the
mechanism is the one `15`§4 already fixed. The truncated stack is not a single potential
well but a nested cavity: each inversion-shell terrace at $r_n=r_0\varphi^{\,n}$ is a
partial mirror — a $\beta$-discontinuity in the boost flow — so the ringdown is the
standing-wave spectrum *of the terrace stack itself*. Cavity resonances live where an
integer number of phase cycles fit between adjacent mirrors; because the mirrors are
equally spaced in $\ln r$ (spacing $\Delta k$ in ordinal, $e^{\pi/2}$ in radius), the
resonant frequencies $f\sim c/r_n$ are equally spaced in $\ln f$. The teeth therefore sit
at the flow-reversal ordinals $k_n=(2n-1)\pi/(4\ln\varphi)$ — the *same* lattice that
carries the torsion zeros (`00`), the bounce shells (`06`), and the potential terraces
(`03`) — and adjacent teeth are in fixed **geometric** ratio

$$\frac{f_{j+1}}{f_j}=\varphi^{\Delta k}=e^{\pi/2}=4.8105.$$

The overtone index is not a radial-quantum-number of one well (which gives Kerr's
near-degenerate cluster) but a **terrace index** of the self-similar stack: stepping one
overtone $=$ stepping one cavity $=$ one boost leg $\Lambda(\Delta k/\varphi)$. That is
why the ratio is the terrace ratio $e^{\pi/2}$ and not a near-unity overtone spacing.

Anchoring $f_0=251$ Hz (the GW150914 fundamental), the golden comb teeth fall at

$$\dots,\,52.2,\;\mathbf{251},\;1207,\;5808\,\text{Hz},\dots$$

So the framework's overtone-frequency ratio is $4.81$ where GR's is $\approx0.95$ — a
**$4.9\times$ discrepancy** in a directly measurable quantity. This is the cleanest
falsifier in the corpus: GR's overtones cluster at one frequency (the recent
black-hole-spectroscopy programmes fit $n=0,1$ at nearly the *same* $f$), while the
golden model predicts the next tooth nearly **five times higher** (or, downward,
$251/4.81=52$ Hz). A stacked, $f_{220}$-rescaled power spectrum of many ringdowns,
plotted in $\ln f$, should show **either** GR's tight overtone cluster **or** the
framework's $\Delta\ln f=\pi/2$ picket fence — never both. One spectrum decides it.

## 5. Tie to the corpus LIGO re-analysis

The corpus LIGO paper reports phase-transition timing ratio $t_1/t_2=0.548\pm0.015$,
loosely matched there to $1/\varphi=0.618$ ($12.8\%$ off). The boost group sharpens
this: a dimensionless ratio in $[0,1)$ is a **boost velocity** $\beta=\tanh\theta$,
not a rapidity. The first-shell velocity is

$$\beta(1)=\tanh\frac1\varphi=0.5498,$$

$0.32\%$ from the *corpus's own re-analysis* value (an internal-consistency match, not an
external-LIGO validation) — **$40\times$ closer** than $1/\varphi$ — and it is the *same*
discrete redshift increment $\Delta f(0\!\to\!1)=+0.550$ already in `03`. The corpus
$Q\simeq3.2$ across all three events ($f_0\tau\pi\approx3.15$) and the $1/M_f$ scaling
of $f_{220}$ ($251,751,110$ Hz for $M_f=62,20.8,142\,M_\odot$, all $\approx10\%$ of
the $a{=}0.7$ Kerr fundamental) are reproduced as sanity checks. The horizon shell
$n_H=183.08$ for $M_\odot$ ($=\log_\varphi(r_s/\ell_P)$, `15`) sets the entropy
$S_{\rm CFT}=n_H\ln\varphi$ at $c=3$; the template here is what that truncated stack
*radiates* when struck.

## Extension — the detectable-echo count is fixed by the dB-per-leg lock

§3 asserted "at most one echo survives LIGO noise." That claim should be *derived*, not
asserted, and the boost group hands it over directly. Each leg costs a fixed
$D_1\equiv-20\log_{10}\gamma_{\rm echo}=20\,S_1/\ln10=+17.52$ dB of amplitude. A ringdown
enters with a finite dynamic range $\mathcal D_{\rm dB}=20\log_{10}(\rho_{\rm rd})$ set by
the ringdown SNR $\rho_{\rm rd}$ (the post-peak coherent SNR, not the full inspiral). The
number of echoes that clear unit SNR is then a pure floor:

$$\boxed{\;N_{\rm obs}=\left\lfloor\frac{\mathcal D_{\rm dB}}{D_1}\right\rfloor
=\left\lfloor\frac{20\log_{10}\rho_{\rm rd}}{20\,S_1\log_{10}e}\right\rfloor
=\left\lfloor\frac{\ln\rho_{\rm rd}}{S_1}\right\rfloor,\qquad S_1=2.01742.\;}$$

The dB ratio collapses to a rapidity ratio because $D_1=20\,S_1\log_{10}e$ exactly: the
dB ledger *is* the rapidity ledger, one boost leg $=$ one $S_1$ of log-amplitude (the
$\log_{10}e$ factors cancel between numerator and denominator). For GW150914's ringdown
$\rho_{\rm rd}\approx7$ (post-merger), $\ln\rho_{\rm rd}=1.95<S_1=2.017$, giving
$N_{\rm obs}=\lfloor0.965\rfloor=0$ — **the first echo itself sits right at the noise
floor**, and the framework predicts the marginal, non-confirmed status of every echo
search to date *as a theorem*, not as an excuse. To see even one clean echo
($N_{\rm obs}\ge1$) requires $\rho_{\rm rd}\ge e^{S_1}=7.52$; for two echoes,
$\rho_{\rm rd}\ge e^{2S_1}=56.53$. A golden-comb echo becomes detectable only for ringdown
SNR above $\sim7.5$ — a sharp, instrument-facing threshold: next-generation detectors
(Cosmic Explorer, Einstein Telescope) reaching $\rho_{\rm rd}\gtrsim60$ on a loud event
should resolve the **first two** golden teeth or rule the comb out.

## Prediction

1. **First-echo delay, GW150914:** $\Delta t_{\rm echo}=t_0(e^{\pi/2}-1)$ with seed
   $t_0\simeq\tau_{220}=4$ ms $\Rightarrow$ **$\Delta t_{\rm echo}\approx15$ ms**
   (conservative light-crossing seed $\Rightarrow$ **4.7 ms**). This is $\sim15$–$60\times$
   shorter than the Abedi–Afshordi (2017) claimed $\sim0.2$–$0.3$ s, and the echo
   spacing is *multiplicative* ($\times4.81$ per leg), not constant.
2. **Echo decrement** $\gamma_{\rm echo}=e^{-S_1}=0.13300$ ($-17.5$ dB/leg, energy
   $\gamma^2=0.0177=$ the note-`06` bounce-ladder ratio); peaks ride the envelope
   $|h(t)|\sim t^{-1.28433}$ — the same $\nu$ as gravity's spatial fall-off.
3. **Overtone comb** $f_{j+1}/f_j=e^{\pi/2}=4.81$ (golden), versus GR Kerr's
   $\approx0.95$ — a $4.9\times$ split. For GW150914 the predicted neighbouring teeth
   are $52$ Hz and $1207$ Hz around the $251$ Hz fundamental.
4. **Timing ratio** $t_1/t_2=\tanh(1/\varphi)=0.5498$ (corpus $0.548$, $0.32\%$ —
   internal-consistency, framework-vs-corpus), the first-shell boost velocity — not
   $1/\varphi$.
5. **Detectability threshold** $N_{\rm obs}=\lfloor\ln\rho_{\rm rd}/S_1\rfloor$: a
   golden echo is invisible below ringdown SNR $\rho_{\rm rd}=e^{S_1}=7.52$, one echo
   visible above it, two above $e^{2S_1}=56.53$. GW150914 ($\rho_{\rm rd}\approx7$) lands
   at $N_{\rm obs}=0$ — the marginal status of all echo searches is a theorem of the
   $17.52$ dB/leg lock, not a fitted excuse.

**Falsifier:** a single high-SNR ringdown whose $f_{220}$-rescaled $\ln f$ spectrum
shows GR's tightly-clustered overtones (ratio $\approx0.95$, all within $\sim10\%$)
and **no** tooth near $5\times$ or $1/5\times$ the fundamental kills the golden comb;
equivalently, a confirmed echo at $\Delta t\sim0.3$ s with *constant* (non-$e^{\pi/2}$)
spacing falsifies the boost-orbit template.
