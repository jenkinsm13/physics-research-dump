# 15 — Gravitational Waves and the Horizon Shell

*Frontier note. Builds on the spine (`00`): conserved current $L_y=1$, the
$\kappa/\tau$ split, the inversion shells $k_n$. Builds on the synthesis (`99`):
the chronon two-vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$, $\theta=k/\varphi$,
ordinal depth $=$ rapidity. Builds on `03` (redshift saturation
$f(n)=\tanh(n/\varphi)$, terrace ratio $e^{\pi/2}$), `06` (bounce ladder
$e^{-\pi/(\varphi\ln\varphi)}$), `08` ($N_\star=\log_\varphi(R_{\rm H}/\ell_P)$),
and ties to the corpus LIGO re-analysis. Every number below is reproduced in
`verify/verify_gw-horizon.py` to residual $\le10^{-16}$.*

---

## 1. The horizon is the shell where $L_y=1$ has been fully spent

In `03` the redshift envelope is the net-flow fraction

$$f(n)=\frac{|G_{\text{flow}}(n)|}{G_{\text{sym}}(n)}=\tanh\!\frac{n}{\varphi}=\tanh\theta=\beta,$$

the boost velocity of the chronon two-vector $\mathbf V(n)$ in flow-space. The
spine's central statement — gravity *is* the conversion of temporal flow into
spatial curvature, with the unit $L_y=1$ as the conserved budget — becomes, in
two-vector language, the statement that **the boost approaches the light cone**.
At $\theta\to\infty$, $\mathbf V(n)$ becomes null: $G_{\text{sym}}\simeq
|G_{\text{flow}}|$, the time and space components of the flow merge, and
$\beta\to1$. The event horizon is exactly the shell where the unit timelike
worldline of the framework runs into its own light cone:

$$\boxed{\;\text{horizon shell }n_H:\quad \tanh\frac{n_H}{\varphi}=1-\varepsilon,
\qquad n_H=\varphi\,\operatorname{artanh}(1-\varepsilon).\;}$$

A black hole, in this picture, is **the shell stack truncated at $n_H$** — a
Matryoshka tower whose innermost shells have boosted all the way to $\beta=1$, so
that no further temporal flow can be extracted from them. Gravity has eaten all
the time: $G_{\text{flow}}/G_{\text{sym}}\to1$, $\sinh\theta\to\cosh\theta$, the
$\cosh$ correlation and the $\sinh$ flow become indistinguishable on the null
cone. This is the local-collapse twin of the cosmological depletion shell
$N_\star$ of `08`: $N_\star$ is the *outer* horizon where the hierarchy runs out
*outward*; $n_H$ is the *inner* horizon where it saturates *inward*. Both are
loci where $\beta\to1$; both are where a shell sum must be truncated.

## 2. The horizon shell of a solar-mass black hole

Map ordinal to radius by the geometric law $r_n=r_0\varphi^{\,n}$ with the seed at
the Planck length, $r_0=\ell_P$. The horizon sits at the Schwarzschild radius
$r_s=2GM/c^2$, so the horizon-shell *depth* is the pure hierarchy traversal

$$\boxed{\;n_H=\log_\varphi\!\frac{r_s}{\ell_P}
=\frac{\ln(r_s/\ell_P)}{\ln\varphi}.\;}$$

For one solar mass, $r_s=2954\,\text{m}$, $\ell_P=1.6163\times10^{-35}\,\text{m}$,
giving the confirmed number

$$n_H(M_\odot)=183.08\ \text{shells}.$$

This sits cleanly between the lepton-comb depths of `04` and the cosmological
horizon $N_\star=\log_\varphi(R_{\rm H}/\ell_P)=291.88$ of `08` — the *same* law,
$\log_\varphi(\text{radius}/\ell_P)$, evaluated at the Schwarzschild radius
instead of the Hubble radius. A solar-mass black hole is $N_\star-n_H\approx108$
shells *shallower* than the cosmos: gravity has spent $183$ octaves of the
golden hierarchy to reach the null cone, the universe spends $291$. At this depth
the redshift fraction is saturated past machine precision,
$\tanh(n_H/\varphi)=1-\mathcal O(10^{-98})$, and its rate of change is frozen,
$f'(n_H)=\operatorname{sech}^2(n_H/\varphi)/\varphi\approx1.3\times10^{-98}$ — the
two-vector is null to all physical accuracy; the horizon is a fixed point of the
boost flow.

## 3. Entropy of the truncated stack — the CFT $c\simeq3$ area law, exactly

The corpus CFT result $S(\ell)=(c/3)\ln\ell$ with $c\approx2.94\to3$ now acquires
a black hole. Identify the conformal extent of the truncated stack with its
radius in Planck units, $\ell=r_s/\ell_P=\varphi^{\,n_H}$. Then

$$S_{\rm CFT}=\frac{c}{3}\ln\frac{r_s}{\ell_P}\;\xrightarrow{\,c=3\,}\;
\ln\frac{r_s}{\ell_P}=n_H\ln\varphi,$$

an exact identity (residual $0$ in `verify`). The Cardy central charge $c\to3$ is
precisely the "$\approx3$ dimensions" the corpus already extracts from $S(\ell)$ —
here it is what makes the conformal entropy collapse to the bare ordinal depth.
The Bekenstein–Hawking area law is then *not an extra postulate* but a consequence
of the geometric radius map: the horizon area is

$$A=4\pi r_s^2,\qquad \frac{A}{\ell_P^2}=4\pi\Big(\frac{r_s}{\ell_P}\Big)^2
=4\pi\,\varphi^{\,2n_H},\qquad
\ln\frac{A}{\ell_P^2}=2\,n_H\ln\varphi+\ln 4\pi=178.73,$$

so the area grows as $\varphi^{2n_H}$ — *two* powers of the boost depth, one per
spatial dimension transverse to the radial stack — with only the fixed geometric
prefactor $4\pi$ riding on top. Bekenstein entropy
$S_{\rm BH}=A/4\ell_P^2=\pi(r_s/\ell_P)^2$ for $M_\odot$ evaluates to
$1.05\times10^{77}$ (confirmed; the textbook solar-mass value), and its *log* is
$2n_H\ln\varphi+\ln4\pi$ — the radial part is twice the CFT log-entropy,
$\ln S_{\rm BH}=2\,S_{\rm CFT}|_{c=3}+\ln4\pi$. **The CFT log-entropy counts shells
(the radial boost depth $n_H$); the Bekenstein entropy counts shell-pairs on the
transverse area ($\varphi^{2n_H}$).** One truncation depth $n_H$ generates both,
and the $4\pi$ is the only thing the radial stack does not already carry.

## 4. Ringdown terraces are echoes — the golden log-period

In `03` the inversion-shell terraces sit at fixed *multiplicative* radial steps

$$\frac{r_{n+1}}{r_n}=\varphi^{\,\Delta k}=e^{\pi/2}=4.8105,\qquad
\Delta k=\frac{\pi}{2\ln\varphi}=3.26425,$$

the radial images of the torsion-zero / flow-reversal ordinals
$k_n=(2n-1)\pi/(4\ln\varphi)$. A perturbed truncated stack rings down by leaking
chronon flux outward across these terraces. Each terrace is a partial mirror — a
$\beta$-discontinuity in the boost flow — so the ringdown is not a single decay
but a **cavity between terraces**: the late-time signal is a train of echoes, each
the previous pulse advanced one terrace outward. Because terraces are equally
spaced in $\ln r$, the echoes are equally spaced in $\ln(\text{time})$, with the
log-period

$$\boxed{\;\frac{t_{\text{echo},\,m+1}}{t_{\text{echo},\,m}}
=\frac{r_{n+1}}{r_n}=e^{\pi/2}=4.8105,
\qquad \Delta\ln t=\frac{\pi}{2}\ \text{per echo}.\;}$$

This is a *log-periodic* echo comb, the gravitational-wave fingerprint of the
self-similar golden stack — distinct from the linearly-spaced echoes of a hard
wall cavity. In frequency it is identical by $f\sim1/r$: the ringdown spectrum
carries a **discrete golden comb** with adjacent teeth in the ratio

$$\frac{f_{j+1}}{f_j}=e^{\pi/2},\qquad \Delta\ln f=\frac{\pi}{2}=1.5708.$$

## 5. The new equation: the echo amplitude *is* the first-bounce rate of `06`

Each echo advances the pulse one terrace outward — a **single advanced leg** of the
chronon worldline — costing it the static-kernel weight $e^{-\Delta k/\varphi}$ from
$\Psi(k)\propto e^{-k/\varphi}$ (`03`, §2). The terrace spacing is not an arbitrary
ordinal step: it is exactly *twice the first inversion ordinal*,
$\Delta k=2k_1$ (since $k_1=\pi/(4\ln\varphi)$, $\Delta k=\pi/(2\ln\varphi)$;
residual $0$). Therefore the leg rapidity equals the **first-bounce action** of `06`,

$$\frac{\Delta k}{\varphi}=\frac{2k_1}{\varphi}=S_1=\frac{\pi}{2\varphi\ln\varphi}
=2.017418\ldots,$$

and the single-echo amplitude is *the* first-bounce rate $\Gamma_1=e^{-S_1}$, not
merely related to it:

$$\boxed{\;\gamma_{\text{echo}}\equiv\frac{|h_{m+1}|}{|h_m|}
=e^{-\Delta k/\varphi}=e^{-S_1}=\Gamma_1=0.13300\;}
\qquad(-17.52\ \text{dB per echo}).$$

This is the genuinely new lock. In `06` the first bounce fires at rate
$\Gamma_1=e^{-S_1}=0.13300$ and the inter-shell event ladder steps down by the
*ratio* $\Gamma_{n+1}/\Gamma_n=e^{-\pi/(\varphi\ln\varphi)}=e^{-2S_1}=0.017689$.
We find these are the **single advanced leg** and the **round trip** of the same
echo step:

$$\gamma_{\text{echo}}=e^{-S_1}=\Gamma_1\quad(\text{one leg}),\qquad
\gamma_{\text{echo}}^{\,2}=e^{-2S_1}=\frac{\Gamma_{n+1}}{\Gamma_n}\quad(\text{round trip}),
\qquad(\text{residual }3\times10^{-18}).$$

So a classical gravitational-wave echo *is* a quantum bounce event seen at one duty
cycle: the wave reads the worldline once (single advanced leg crossing one terrace,
$\Gamma_1$), the tunneling amplitude reads it twice (the chronon worldline out
through the null vertex and back, $\Gamma_1^2=e^{-2S_1}$ = the ladder ratio). The
ringdown echo comb and the bounce spectrum are one ladder read at two duty
cycles — and the echo rate coincides with the *fundamental* bounce rate, not just
its square. `06` independently meets the same number from its own side: there
$e^{-S_1}=0.1330=\Gamma_1$ resurfaces as the even/odd partition of the bounce gas
(the ratio of even-shell to inversion-shell weight). The GW echo gives that same
$\Gamma_1$ a third reading — as the per-leg amplitude of the ringdown train. A
clean cross-branch lock that was not put in by hand.

## 6. Anchoring to the corpus LIGO re-analysis

The corpus LIGO paper already reports (i) ringdown fundamentals $f_{220}=251\,$Hz
(GW150914), $751\,$Hz (GW151226), $110\,$Hz (GW190521); (ii) phase-transition
timing ratios $t_1/t_2=0.548$; and (iii) a quality factor $Q\simeq3.2$ across
events. The present note sharpens (ii). The natural first reading pairs $0.548$
with $1/\varphi=0.618$ — but that is $12.8\%$ off, and it misreads the *kind* of
quantity. A timing ratio in $[0,1)$ is a **boost velocity** $\beta$, not a rapidity
$\theta=1/\varphi$. The first-shell boost velocity of the chronon two-vector is

$$\beta(1)=\tanh\frac{1}{\varphi}=f(1)=0.5498,$$

which is the *very same* discrete redshift increment $\Delta f(0\!\to\!1)=+0.550$
that `03` already records (line ~152). It sits $0.32\%$ from the observed $0.548$ —
$40\times$ closer than $1/\varphi$. So the corpus number is not "near the golden
ratio"; it is the first shell's flow fraction $\tanh(1/\varphi)$, the boost velocity
at one ordinal step, measured through detector noise. This converts a loose visual
match into the framework's own $f(n)=\tanh(n/\varphi)$ ladder evaluated at $n=1$.
Taking GW150914's $f_{220}=251\,$Hz as the $j=0$ comb
tooth, the golden ringdown comb predicts replica/echo teeth at

$$\dots,\,52.2,\;251,\;1207,\;5808\,\text{Hz},\dots
\qquad(\text{ratio }e^{\pi/2}\text{ between teeth}),$$

and a late-time echo train with delay log-period $e^{\pi/2}$ and amplitude
decrement $0.133$ per echo. With $M_f=62\,M_\odot$ the horizon light-crossing is
$2r_s/c=1.22\,$ms and the fundamental period $1/f_{220}=3.98\,$ms (matching the
corpus $\tau_{220}=4.0\,$ms), setting the absolute scale on which the *dimensionless*
golden log-period rides.

## Extension — the echo envelope is gravity's spatial fall-off, read in time

The echo comb of §4–§5 has a hidden coarse-grained content. The teeth sit at
multiplicative times $t_m=t_0\,e^{m\pi/2}$ (log-period $\Delta\ln t=\pi/2$) with
amplitudes $h_m=h_0\,e^{-mS_1}$ (decrement $\gamma_{\text{echo}}=e^{-S_1}$ per leg,
§5). Eliminate the echo index $m$ between the two — $m=(2/\pi)\ln(t/t_0)$ from the
time law, substituted into the amplitude law — and the discrete comb resolves into a
smooth power-law **envelope** in time:

$$\boxed{\;|h(t)|\;\sim\;t^{-2S_1/\pi}\;=\;t^{-\nu},\qquad
\nu=\frac{2S_1}{\pi}=\frac{1}{\varphi\ln\varphi}=1.2843\ldots\;}$$

(residual $0$: $2S_1/\pi=1/(\varphi\ln\varphi)$ identically, since
$S_1=\pi/(2\varphi\ln\varphi)$). This $\nu$ is **exactly the spatial exponent of
`03`**: gravity's static potential falls as $\Phi(r)\sim r^{-\nu}$, $\nu=1.2843$,
set by the same intrinsic rapidity rate $\lambda=1/\varphi$. The late-time ringdown
*tail in time* carries the identical golden exponent as gravity's fall-off *in
space*. One boost rate $1/\varphi$, one exponent $\nu$, read on two axes the
worldline trades through the saddle: $r^{-\nu}$ radially (the advanced static field,
`03`) and $t^{-\nu}$ temporally (the echo envelope here). This is the space$\leftrightarrow$time
duality of the chronon two-vector made into a measurable power law — and it is
constraint-clean: the comb is *not* smoothed away, it remains the fine structure
riding on the envelope, exactly the coarse/fine dual `03` uses for the terraced
potential. The envelope traces the comb *peaks* $h_m$ (the upper envelope); the
golden teeth at $\Delta\ln t=\pi/2$ are the lattice riding on it.

## Prediction

1. **Log-periodic GW echo train with a golden power-law envelope.** Post-merger
   ringdowns carry echoes at *multiplicative* time spacing $e^{\pi/2}=4.8105$ (not
   the linearly-spaced echoes of exotic-compact-object models), each suppressed by
   $\gamma_{\text{echo}}=e^{-S_1}=e^{-\pi/(2\varphi\ln\varphi)}=0.133$ ($-17.5\,$dB),
   and their peaks lie on the envelope $|h(t)|\sim t^{-\nu}$, $\nu=1/(\varphi\ln\varphi)=1.2843$
   — the *same* exponent as gravity's spatial fall-off $\Phi(r)\sim r^{-\nu}$ (`03`).
   The second echo is down $35\,$dB — at most one or two echoes survive above LIGO
   noise, consistent with their non-detection so far.
2. **Discrete golden comb in the ringdown spectrum.** Adjacent comb teeth in the
   ratio $e^{\pi/2}$; for GW150914 (251 Hz fundamental) the nearest teeth fall at
   $\sim52\,$Hz and $\sim1207\,$Hz. A stacked power spectrum of many events,
   rescaled to each $f_{220}$, should show peaks at $\ln f$ spacing $\pi/2$. The
   first phase-transition timing ratio is the first-shell boost velocity
   $t_1/t_2=\tanh(1/\varphi)=0.550$ (corpus $0.548$, $0.32\%$), *not* $1/\varphi$.
3. **Horizon-shell entropy lock.** Any black hole satisfies
   $S_{\rm CFT}=n_H\ln\varphi=\ln(r_s/\ell_P)$ with $c=3$ *exactly*, and
   $\ln(A/\ell_P^2)=2n_H\ln\varphi$ — the Bekenstein area law is the transverse
   square of the same golden truncation depth ($n_H=183.08$ for $M_\odot$). The
   echo rate is the first-bounce rate of `06`, $\gamma_{\text{echo}}=e^{-S_1}=\Gamma_1$,
   and its square $\gamma_{\text{echo}}^2=e^{-2S_1}=e^{-\pi/(\varphi\ln\varphi)}$ is
   the bounce-ladder *ratio* — tying the classical echo comb to the quantum bounce
   ladder: **one boost step, single leg = $\Gamma_1$, round trip = ladder ratio.**
