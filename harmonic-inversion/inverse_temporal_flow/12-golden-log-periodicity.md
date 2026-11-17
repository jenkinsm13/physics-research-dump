# 12 — Golden Log-Periodicity: One Comb from Leptons to H(z)

*Round-2 frontier note. Builds on the spine (`00-spine.md`): the conserved current
$L_y=1$, ordinal depth as rapidity $\theta_k=k/\varphi$, and the flow-reversal
lattice $k_n=(2n-1)\pi/(4\ln\varphi)$ with fixed ordinal spacing
$\Delta k=\pi/(2\ln\varphi)=3.26425$. Builds on the synthesis (`99-index.md`): the
chronon two-vector $\mathbf V(k)=(\cosh\theta,-\sinh\theta)$ dressed by
$\mathrm{osc}(k)=1/(1+\cos^2 2k\ln\varphi)$, and on round-1 results 03 (terraces
$r_{n+1}/r_n=e^{\pi/2}$), 04 (lepton step $\Delta_g=39$, drift
$\delta\theta_g=78\ln\varphi-12\pi$), 08 ($N_\star=\log_\varphi(R_{\rm H}/\ell_{\rm P})=291.88$,
$H(z)$ comb at $\approx2.27$ octaves). Every number below is checked to machine
precision in `verify/verify_golden-log-periodicity.py`.*

---

## The claim

The inversion comb $\Delta k$ is laid down **once**, in ordinal, by the saddle
geometry. It appears at lepton scale, at terrace scale, and at cosmic scale not as
three coincidences but as **one comb read through three different exponential maps
from ordinal to physical scale**. The conversion factor between any two axes is a
single dimensionless constant, and that constant is forced by $\varphi$ alone.

## 1. The master identity — the comb tooth is $e^{\pi/2}$, exactly

The lattice spacing $\Delta k$ and the rapidity rate $\ln\varphi$ are reciprocal in
the sharpest possible way. From the definition,

$$\boxed{\;\Delta k\cdot\ln\varphi=\frac{\pi}{2\ln\varphi}\cdot\ln\varphi=\frac{\pi}{2}\quad\text{(exact).}\;}$$

This single line is the whole note. Physical radius grows as $r_n=r_0\varphi^{\,n}$
(geometry, exact: $d\ln r/dn=\ln\varphi$), so the radial multiplier across **one comb
tooth** is

$$\Lambda_\varphi\;\equiv\;\varphi^{\,\Delta k}\;=\;e^{\Delta k\ln\varphi}\;=\;e^{\pi/2}\;=\;4.810477381\ldots,$$

verified to $0$ residual. This is **not a new number** — it is *exactly* note 03's
terrace ratio $r_{n+1}/r_n=e^{\pi/2}$. The terraces, the inversion shells, and the
comb teeth are the same objects: one flow-reversal per $e^{\pi/2}$ of scale.

$\Lambda_\varphi=e^{\pi/2}$ is the **golden log-periodicity constant**. It is the
discrete-scale-invariance (DSI) factor of the entire framework: every observable
that lives on the flow-reversal lattice is invariant under $s\to\Lambda_\varphi\,s$
in its scale variable, not under arbitrary dilations.

## 2. The new equation — DSI log-frequency and complex scaling dimensions

A scale-covariant observable $F(s)$ on the lattice satisfies the Weierstrass-type
discrete renormalization $F(\Lambda_\varphi\,s)=\mu\,F(s)$ for some multiplier $\mu$.
The general solution is a power law dressed by a $\ln s$-periodic modulation,

$$F(s)=s^{-D}\,\mathcal P\!\left(\frac{\ln s}{\ln\Lambda_\varphi}\right),\qquad
\mathcal P(\xi+1)=\mathcal P(\xi),$$

so the spectrum of the dilation generator is $D+i\,\omega_\varphi n$, $n\in\mathbb Z$,
with **fundamental log-frequency**

$$\boxed{\;\omega_\varphi\;=\;\frac{2\pi}{\ln\Lambda_\varphi}\;=\;\frac{2\pi}{\pi/2}\;=\;4\quad\text{(exact, residual }0\text{).}\;}$$

The framework's discrete scale invariance carries an **integer** log-frequency
$\omega_\varphi=4$ — the only place a bare integer falls out of $\varphi$-geometry,
and it does so because $\ln\Lambda_\varphi=\pi/2$ rationalizes the $2\pi$ of the
Fourier-on-$\ln s$ dual.

The two pieces of $F(s)=s^{-D}\mathcal P$ are not free — they are **exactly the two
factors of the dressed chronon two-vector** (synthesis 99). The retarded null
projection is $\kappa(+k)=\mathrm{osc}(k)\,e^{-\theta}$ with $\theta=k/\varphi$, and
on the radial axis $k=\log_\varphi(r/r_0)$ turns the rapidity factor into the power
law

$$e^{-k/\varphi}=(r/r_0)^{-1/(\varphi\ln\varphi)}\quad\Longrightarrow\quad
D=\frac{1}{\varphi\ln\varphi}=1.28433,$$

which is note 03's static-law exponent $\nu=1.2843$, verified to $4\times10^{-5}$.
So the $SO(1,1)$ rapidity boost of $\mathbf V(k)$ **is** the envelope $s^{-D}$, and
the flow-reversal weight $\mathrm{osc}(k)$ **is** the log-periodic part
$\mathcal P(\ln s/\ln\Lambda_\varphi)$.

### 2a. Why $\mathrm{osc}$ *is* the $\omega_\varphi=4$ modulation — proved, not asserted

The identification is not a relabelling; it is an arithmetic theorem about the
harmonic content of $\mathrm{osc}$, and it is the rigorous version of the rule that
forbids us to smooth it. On the radial axis $2k\ln\varphi=2\ln(r/r_0)$, so the
flow-reversal weight is *literally* a function of $\ln r$ with a single bare
frequency hidden in the square:

$$\mathrm{osc}(r)=\frac{1}{1+\cos^2\!\big(2\ln(r/r_0)\big)}
=\frac{2}{3+\cos\!\big(4\ln(r/r_0)\big)},$$

using $\cos^2 x=\tfrac12(1+\cos 2x)$. The angular frequency of the *only* cosine
that appears is exactly $4$ in $\ln r$ — i.e. **the leading (and fundamental)
Fourier harmonic of $\mathrm{osc}$ is $\omega_\varphi=4$, identically**, with zero
content at any other base frequency. Because $\mathrm{osc}$ is *exactly*
$\ln\Lambda_\varphi=\pi/2$–periodic in $\ln r$ (period $\Delta k$ in ordinal), its
**entire** Fourier tower lands on the integer multiples $\{4n\}_{n\in\mathbb Z}$ —
nothing off-lattice. The harmonic spectrum of the un-smoothed flow-reversal weight
is therefore *identical* to the DSI complex-dimension lattice $D_n=D+4in$. That is
the precise content of "osc is $\mathcal P$": the thing we may not smooth is the
periodic part $\mathcal P$ of the Weierstrass solution, and its spectral support is
forced onto the $\omega_\varphi=4$ comb by the saddle geometry alone. (Verified by
FFT to $<3\times10^{-16}$ in `verify/`.)

The complex scaling dimensions are therefore

$$D_n=D+4\,i\,n,\qquad n\in\mathbb Z,$$

and the observable $\Re\!\big[s^{-D_n}\big]=s^{-D}\cos\!\big(4n\ln s+\phi_n\big)$ is a
pure log-cosine comb. This is the genuinely new object of note 12: the chronon
two-vector's boost group $SO(1,1)$ (synthesis 99), reduced modulo the reversal
lattice, leaves a residual **$\mathbb Z$ of log-harmonics with spacing $\omega_\varphi=4$**.

## 3. The conversion — one comb, three axes

Each physical axis maps ordinal $n$ to its own scale variable through a per-shell
log-rate; the comb spacing $\Delta k$ in ordinal is fixed, so the *observed* period
on each axis is $\Delta k$ times that axis's rate.

| Axis | per-shell log-rate | one comb tooth | round-1 tie |
|---|---|---|---|
| radial $r$ | $\ln\varphi$ (exact) | $r\!\times\!e^{\pi/2}=\Lambda_\varphi$ | 03 terraces $e^{\pi/2}$ |
| cosmic (octaves) | $\ln\varphi/\ln2=0.69424$ | $\log_2\Lambda_\varphi=\dfrac{\pi}{2\ln2}=2.26618$ oct | 08 "$\approx2.27$ oct" |
| lepton $\ln m$ | $a=0.104538$ (empirical, 04) | $e^{a\,\Delta k}=1.4067$ | model-dependent |

The radial and cosmic teeth are **geometry-exact**; the cosmic identity
$\log_2 e^{\pi/2}=\pi/(2\ln2)=2.26618$ reproduces note 08's "$2.27$ octaves" to
$4\times10^{-16}$ — it was always the *same* tooth, not a numerical echo. The lepton
tooth rides the *measured* slope $a$ and is therefore a projection of the comb
through data, not a pure prediction.

## 4. The lepton generation step is six comb periods — and the $0.44\%$ is $\delta\theta_g$

The raw oscillation $\cos(2k\ln\varphi)$ has full period $P=2\Delta k=\pi/\ln\varphi=6.5285$
(two reversals per period). Note 04's generation step $\Delta_g=39$ is therefore

$$\Delta_g\;\approx\;6P\;=\;12\,\Delta k\;=\;39.17101,\qquad
\frac{12\,\Delta k}{39}-1=+0.439\%.$$

**Six full log-periods per generation** (equivalently twelve flow reversals — exactly
note 04's "twelve $\pi$-boundaries crossed per generation"). The $0.44\%$ is not slop:
it is round-1's drift invariant in disguise. The mismatch in ordinal units is

$$12\,\Delta k-39\;=\;\frac{12\pi-78\ln\varphi}{2\ln\varphi}\;=\;-\frac{\delta\theta_g}{2\ln\varphi}\;=\;+0.171016\ \text{shells},$$

verified equal to $-\delta\theta_g/(2\ln\varphi)$ to $3\times10^{-15}$. The lepton
comb's failure to close on the generation step **is** the rotor angle
$\delta\theta_g=78\ln\varphi-12\pi$ of note 04, now read as the incommensurability of
the integer step $\Delta_g$ against six golden log-periods. The Vernier offset and
the log-period defect are one quantity.

On the mass axis the per-generation multiplier follows from the same six teeth:
$e^{39a}=58.967$, which is note 04's $\sqrt{m_\tau/m_e}$ (to $58.973$). One comb tooth
on $\ln m$ multiplies mass by $e^{a\,\Delta k}=1.407$; six teeth give one generation.

## 5. Why all three are literally the same comb

Write the universal log-periodic structure once, in ordinal, then pull it back to
each axis by that axis's exponential map $s_X(n)=s_{X,0}\exp(\rho_X\,n)$ with rate
$\rho_X\in\{\ln\varphi,\ \ln\varphi/\ln2,\ a\}$:

$$F_X(s)=\Big(\tfrac{s}{s_{X,0}}\Big)^{-D}\,\mathcal P\!\Big(\frac{\ln(s/s_{X,0})}{\rho_X\,\Delta k}\Big),
\qquad \rho_X\,\Delta k=\rho_X\cdot\frac{\pi}{2\ln\varphi}.$$

For the radial axis $\rho_r\Delta k=\frac{\pi}{2}$ so the period in $\ln r$ is
$\pi/2$ and $\Lambda_\varphi=e^{\pi/2}$. For cosmic scale the period in $\log_2$ is
$\pi/(2\ln2)$. For mass it is $a\,\Delta k$. **All three share the same dimensionless
log-frequency $\omega_\varphi=4$** when each is plotted against
$\ln s/(\rho_X\Delta k)$ — that common abscissa is the proof that one comb underlies
all of them. The conversion between any two axes $X,Y$ is the pure ratio of rates,

$$\frac{\text{period}_X}{\text{period}_Y}=\frac{\rho_X}{\rho_Y},$$

independent of $\Delta k$ — the comb cancels, leaving only the axis-to-axis exchange.

## Extension — the comb amplitudes are set by the *silver* ratio

Section 2a fixed where the teeth sit ($\omega_\varphi=4n$, golden); it did not say how
tall they are. Both fall out in closed form. Writing $\psi=4\ln(r/r_0)$ so that
$\mathrm{osc}=2/(3+\cos\psi)$, the Gradshteyn–Ryzhik series for $1/(a+b\cos\psi)$ with
$a=3,\ b=1$ gives the **exact** log-cosine comb of the flow-reversal weight:

$$\boxed{\;\mathrm{osc}(r)=\frac{1}{\sqrt2}\left[1+2\sum_{n=1}^{\infty}(-1)^n\,
\delta_S^{-2n}\,\cos\!\big(4n\ln(r/r_0)\big)\right],\qquad
\delta_S^{-2}=3-2\sqrt2=(\sqrt2-1)^2.\;}$$

This single equation carries the whole content of the note in spectral form, and it
is exact — not a smoothing, but the convergent Fourier representation of the
un-smoothed weight, verified coefficient-by-coefficient to machine precision
($n=1$: $-0.242641$; $n=2$: $+0.041631$; $n=3$: $-0.007143$; residuals $<3\times10^{-16}$).

Three things are forced by it, and the third is new:

1. **The $n=0$ mode is $1/\sqrt2$.** The DC term of the exact comb is precisely the
   period-mean $\langle\mathrm{osc}\rangle=1/\sqrt2$ that the framework already blesses
   as the legitimate coarse-grained envelope. We do not *assume* that envelope; it is
   *derived* here as the zeroth Fourier harmonic, with every higher tooth an explicit
   correction on top of it.

2. **The teeth sit at $4n$** — the golden $\omega_\varphi$ comb of §2a, now with
   amplitudes attached.

3. **The amplitudes decay as the silver ratio.** Each successive tooth is suppressed by
   the universal factor $\delta_S^{-2}=(\sqrt2-1)^2=0.171573$, where
   $\delta_S=1+\sqrt2$ is the **silver ratio** (the metallic mean satisfying
   $\delta_S=2+1/\delta_S$, just as $\varphi=1+1/\varphi$). So the comb is a *two-metal*
   object: **the golden ratio sets the tooth spacing** ($\Lambda_\varphi=e^{\pi/2}$,
   $\omega_\varphi=4$) **and the silver ratio sets the tooth amplitudes**
   ($\delta_S^{-2}$ per harmonic). The effective number of resolvable teeth is the
   silver decay length $\sim 1/\ln\delta_S^{2}\approx0.567$ — meaning the $n=1$ tooth
   already carries $97\%$ of the AC power, so every prediction below is dominated by the
   single golden tooth, with a small, sign-alternating silver tail.

The Schottky-style harmonic ladder of note 05 and the boost tower of note 99 thus close
on a clean arithmetic: $\varphi$ in the exponent (where teeth are), $\delta_S$ in the
amplitude (how loud teeth are), and the bare integer $4$ tying them. The two metallic
means that bracket the saddle — golden from the $\sqrt5$ of $\kappa_{\rm Frenet}$,
silver from the $\sqrt2$ of the period-mean — are the spacing and the loudness of one
and the same comb.

## Prediction

A **single dimensionless log-periodicity constant** $\Lambda_\varphi=e^{\pi/2}=4.8105$
(equivalently $\omega_\varphi=4$, exact) must imprint a log-cosine comb on every
scale-covariant spectrum the framework touches:

1. **$H(z)$ / cosmic expansion.** Log-periodic modulation in $(1+z)$ with period
   $\Lambda_\varphi=4.81$ per cycle $=2.2662$ octaves, **apodized** over
   $\Delta N_\star\approx25$ shells ($\mathcal R=(1/8)/(3\ln\varphi)=0.0866$, note 08):
   sharpest at $z\sim0$, fading by $z\sim$ few. Falsifiable spacing: residuals of
   $H(z)$ about $\Lambda$CDM should peak at $\ln(1+z)$ separations of $\pi/2$ in
   natural-log units (factor $4.81$ in $1+z$).

2. **Lepton tower.** Generation step $=6$ comb periods $=39.17$ shells; the next
   charged lepton at $k_4=141$ (note 04), with the $0.44\%$ closure defect fixed to
   $\delta\theta_g$. Mass tooth $e^{a\Delta k}=1.407$.

3. **QPO / accreting compact objects.** Twin-peak and harmonic QPO frequencies should
   prefer ratios near $\Lambda_\varphi^{1/m}$ for small integer $m$ (the comb seen at
   finer ordinal sampling): consecutive log-comb teeth at $\nu_{n+1}/\nu_n=4.81$,
   half-teeth at $\sqrt{\Lambda_\varphi}=2.193$, and **quarter-teeth at
   $\Lambda_\varphi^{1/4}=1.481$** — strikingly close to the observed $3{:}2=1.5$
   twin-peak HFQPO ratio.

4. **CMB acoustic comb.** A faint $\ell$-space log-periodic ripple with golden ratio
   $\ell_{n+1}/\ell_n=\Lambda_\varphi=4.81$ riding atop the harmonic acoustic series.

5. **Sphaleron / electroweak.** The same $\omega_\varphi=4$ log-frequency should
   appear in any RG flow that crosses a golden shell — a $4$-fold log-periodic
   correction to running couplings near scale boundaries.

The constant to refute the framework with is one number: **$\Lambda_\varphi=e^{\pi/2}$,
$\omega_\varphi=4$.** Find a clean scale-covariant spectrum whose log-comb spacing is
not $e^{\pi/2}$ (within the apodization width $\mathcal R$ where applicable), and the
one-comb hypothesis breaks. The deepest content is the exact arithmetic:
$\Delta k\,\ln\varphi=\pi/2$ makes the discrete scale invariance carry the integer
log-frequency $4$, tying leptons, terraces, and $H(z)$ to a single tooth.
