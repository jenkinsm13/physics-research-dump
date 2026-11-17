# 28 — The Operational GW Template: Ready to Run Against Strain

**Thread:** Note 23 derived the *inversion comb* — an echo train whose delays follow the bounce action $S_n=2k_n/\varphi$ and whose amplitudes fall by $\gamma_{\rm echo}=e^{-S_1}=0.133$. Here we make it **operational**: an explicit matched-filter waveform with concrete numbers for GW150914 and GW190521, the deviation from the GR Kerr quasinormal-mode (QNM) spectrum, the statistical test to run against LIGO strain, and a ruthlessly honest detectability verdict. This is a **template route, not a scale-pinning route** — the absolute-scale keystone (the intercept $b$ in $\ln m=ak+b$) stays open in notes 24/25/26. What we pin here are *spacings and ratios*, fixed by $\varphi$ and $\ln\varphi$ alone, carried on the externally-measured remnant mass **and the measured fundamental ringdown $f_{220}$**. We predict only the *companions* of the measured carrier — the $e^{\pi/2}$ comb ratio and the $\gamma_{\rm echo}$ amplitude law — never the carrier itself. No particle mass is fed in anywhere; there is no scale to pin and we do not pretend to pin one.

---

## 1. The template

Building on the boost-group ladder (note 00) and the absorber-completed Newtonian tail (note 21), the post-merger strain is a coherent sum of delayed, damped copies of the ringdown seed $r(t)$:

$$\boxed{\,h(t)=\sum_{m=0}^{N}\gamma_{\rm echo}^{\,m}\,\Theta(t-t_m)\,e^{-(t-t_m)/\tau}\cos\!\big(2\pi f_0(t-t_m)+\psi+m\,\Delta\psi\big),\quad t_m=t_0\,e^{m\pi/2}\,}$$

with the framework-fixed parameters

$$\gamma_{\rm echo}=e^{-S_1}=0.13305,\qquad S_1=\frac{\pi}{2\varphi\ln\varphi}=2.01749,$$

and the Maslov phase increment $\Delta\psi=\arg(i^{\Delta n})=\pi/2$ per shell crossing (note 23, $i^{\Delta n}$). The delays are **geometric in time** because the ladder is *uniform in rapidity* $\theta=k/\varphi$ (note 00): each rung adds proper interval $1/\varphi$, and Fourier-on-$\ln s$ turns that into a delay ratio $e^{\pi/2}$ (note 23 §3). This is the one structural prediction that distinguishes us from GR: GR echoes (if any) are *uniformly* spaced; ours are *log-uniform*.

The per-echo amplitude drop in decibels:

$$20\log_{10}\gamma_{\rm echo}=20\log_{10}(0.13305)=-17.52\ \text{dB/leg}.$$

The number of observable echoes is set by where the ringdown SNR $\rho_{\rm rd}$ drops below unity along the ladder:

$$N_{\rm obs}=\Big\lfloor \frac{\ln\rho_{\rm rd}}{S_1}\Big\rfloor.$$

---

## 2. The comb in frequency space

Transforming the geometric train gives teeth log-uniform in $f$:

$$\ln f_{p+1}-\ln f_p=\frac{\pi}{2}\quad\Longrightarrow\quad \frac{f_{p+1}}{f_p}=e^{\pi/2}=4.81048.$$

Anchored on the *measured* fundamental ringdown $f_0=f_{220}$ (this is the single external carrier — we predict its *companions*, not its value), the teeth sit at $f_p=f_0\,e^{p\pi/2}$.

---

## 3. GW150914 — concrete numbers

Remnant $M_f\simeq 62\,M_\odot$, measured $f_{220}\simeq 251$ Hz. The fundamental chronon time is the light-crossing time

$$t_0=\frac{GM_f}{c^3}=62\times 4.92549\times10^{-6}\,\text{s}=3.0538\times10^{-4}\,\text{s}=0.3054\ \text{ms}.$$

**First echo delay** (multiplier $e^{S_1}=7.5184$):

$$\Delta t_1=t_0\,e^{S_1}=0.3054\times7.5184=\boxed{2.296\ \text{ms}}.$$

**Overtone comb teeth** (anchor 251 Hz, ratio 4.81):

| tooth $p$ | $f_p$ (Hz) |
|---|---|
| $-1$ | $251/4.81=\mathbf{52.2}$ |
| $0$ | $\mathbf{251}$ (measured anchor) |
| $+1$ | $251\times4.81=\mathbf{1207}$ |

**Detectability — the honest verdict.** The measured ringdown SNR of GW150914 is $\rho_{\rm rd}\approx7$. Then

$$N_{\rm obs}=\Big\lfloor\frac{\ln 7}{2.01749}\Big\rfloor=\big\lfloor 0.965\big\rfloor=\boxed{0}.$$

**No echo is resolvable in GW150914.** The first echo would arrive at $-17.5$ dB, i.e. amplitude $0.133\times$ the ringdown — below the noise. So for this event the echoes are *not* the test. **The live, falsifiable test is the comb spacing**: is there a spectral tooth near **1207 Hz** (and/or **52 Hz**) absent from the GR Kerr spectrum? One needs $\rho_{\rm rd}>e^{S_1}=7.52$ for even a single resolvable echo.

---

## 4. GW190521 — the better target

Remnant $M_f\simeq 142\,M_\odot$ (the heaviest confident detection). Larger mass $\Rightarrow$ longer $t_0$, lower $f_0$, but the *ratios are identical*:

$$t_0=142\times4.92549\times10^{-6}=6.994\times10^{-4}\,\text{s}=0.6994\ \text{ms},$$
$$\Delta t_1=t_0\,e^{S_1}=\boxed{5.259\ \text{ms}}.$$

**Where to anchor the carrier — the honest version.** A naive $f\propto M_f^{-1}$ *at fixed dimensionless spin* gives $f_{220}\approx251\times\tfrac{62}{142}=109.6$ Hz, but this is only a sanity cross-check: GW190521's remnant has a *different* spin from GW150914's, so the simple mass scaling overshoots. The **measured** GW190521 ringdown sits near $f_{220}\approx66$ Hz. Because the comb is a *ratio* prediction, it must ride on the **measured** carrier, not the mass-scaled estimate. The runnable prediction is therefore

$$f_{+1}=e^{\pi/2}\,f_{220}^{\rm meas}=4.81\times66\approx\mathbf{317\ \text{Hz}},\qquad f_{-1}=66/4.81\approx\mathbf{13.7\ \text{Hz}},$$

with the $+1$ tooth at **$\sim$317 Hz** still squarely in LIGO's most sensitive band. (Had we instead trusted the $109.6$ Hz estimate, we would have looked at $527$ Hz — a $\sim$200 Hz miss driven entirely by the spin difference, which is exactly why the carrier must be measured, not scaled.) The longer $5.26$ ms first-echo delay is also more comfortably resolved from the merger than GW150914's $2.30$ ms.

---

## 5. Deviation from the GR Kerr QNM spectrum

This is where the framework is genuinely discriminating. For a Kerr remnant of moderate spin $a\sim0.7$, the first *overtone* of the dominant $(\ell,m)=(2,2)$ mode is **nearly degenerate in frequency** with the fundamental: $f_{221}/f_{220}\sim0.95$–$1.0$, differing mainly in damping (the overtone decays far faster). GR therefore predicts a *cluster* of modes near $f_{220}$, never a companion an octave-plus away.

Our framework predicts a companion at

$$\frac{f_{+1}}{f_0}=e^{\pi/2}=4.81,$$

i.e. a spectral feature at $\sim$**1207 Hz** (GW150914, on measured $f_{220}=251$ Hz) or $\sim$**317 Hz** (GW190521, on measured $f_{220}\approx66$ Hz) that *cannot* be a Kerr overtone, subleading angular mode, or harmonic of the GR spectrum. A detection of power at $f_0\,e^{\pi/2}$ correlated with the ringdown phase would be smoking-gun; its absence at sufficient SNR falsifies the comb.

---

## 6. The statistical test

**Template bank.** Two hypotheses:

- $\mathcal H_{\rm GR}$: Kerr ringdown $h_{\rm GR}(t)=A\,e^{-t/\tau}\cos(2\pi f_{220}t+\psi)$ plus a tightly-spaced overtone.
- $\mathcal H_{\rm comb}$: the §1 template with $\gamma_{\rm echo}=0.133$, $t_m=t_0 e^{m\pi/2}$, $\Delta\psi=\pi/2$ — **zero free shape parameters**; only $(t_0,f_0,\psi,A)$ float, all fixed by the measured remnant.

**Matched filter.** Cross-correlate the post-merger strain $d(t)$ against each template, $\rho=\langle d\,|\,h\rangle/\sqrt{\langle h|h\rangle}$, in the noise-weighted inner product. The echo train carries a coherent SNR boost

$$\sqrt{\textstyle\sum_{m\ge1}\gamma_{\rm echo}^{2m}}=\sqrt{\frac{\gamma_{\rm echo}^2}{1-\gamma_{\rm echo}^2}}=0.1343,$$

so recovering even the *first* echo at SNR 5 requires $\rho_{\rm rd}=5/\gamma_{\rm echo}\approx37.6$, and recovering the *coherently summed* train at SNR 5 requires $\rho_{\rm rd}=5/0.13425\approx37.25$ — both well above any current event. This is why §3's verdict is $N_{\rm obs}=0$ and why the **time-domain echo search is hopeless at today's SNRs**; the frequency-domain comb tooth is the only live channel.

**Bayesian odds.** Compute $\mathcal O=\dfrac{p(d|\mathcal H_{\rm comb})}{p(d|\mathcal H_{\rm GR})}$ with $\ln\mathcal O\approx\tfrac12(\rho_{\rm comb}^2-\rho_{\rm GR}^2)$ over the joint $(t_0,f_0)$ posterior. **Detection threshold:** require $\ln\mathcal O>5$ (decisive) *and* a tooth-SNR $>5$ at $f_0 e^{\pi/2}$. The framework template is parameter-free in shape, so it incurs *no* Occam penalty relative to GR's free overtone amplitudes — a structural advantage if the tooth is there.

**Tie to existing repo material.** This operationalizes note 23's comb and supplies the carrier handle ($t_0=GM_f/c^3$ for the *delays*; the *measured* $f_{220}$ for the *teeth* — the $f\propto M_f^{-1}$ scaling is used only as a labelled cross-check, see §4) needed to fold the framework template against the public LIGO O1/O3 strain for these two events; it inherits $S_1$, $\Gamma_{\rm tot}$, and $\gamma_{\rm echo}$ unchanged from notes 00/21/23 (no new constants introduced).

---

## 7. Honest scope

We did **not** pin an absolute scale here, and we did not try to: the echo *delays* and comb *teeth* both ride on the externally measured $M_f$ and $f_{220}$. What is parameter-free and falsifiable is the **ratio** $e^{\pi/2}=4.81$ and the **amplitude law** $\gamma_{\rm echo}=0.133$ — pure $\varphi$-geometry. No electron mass is computed in this note; the keystone gap is untouched and remains the business of the scale routes.

## Extension — the inversion-comb finesse $F$

A comb is only a comb if its teeth are sharper than their spacing. Two adjacent teeth sit at log-distance $\pi/2$ (the rapidity-uniform rung, note 00); each tooth has fractional linewidth $1/Q_{\rm eff}$, where $Q_{\rm eff}=\pi f_0\tau$ is the quality factor of the ringdown seed $r(t)$. Define the **inversion-comb finesse**

$$\boxed{\,F\;\equiv\;\frac{\text{tooth spacing}}{\text{tooth width}}\;=\;\frac{\pi}{2}\,Q_{\rm eff}\,}$$

and the **resolve-one-tooth floor** — the minimum intrinsic quality at which the $+1$ tooth separates from the carrier rather than blurring into it:

$$\boxed{\,Q_{\min}=\frac{1}{e^{\pi/2}-1}=\frac{1}{3.8105}=0.26244\,}\qquad\text{(pure }\varphi\text{-free geometry, set by }e^{\pi/2}\text{ alone).}$$

This is a *structural* statement with teeth (pun intended). For any astrophysical Kerr remnant the dominant $(2,2,0)$ mode has $Q_{220}\sim3$–$4$ (e.g. $Q_{220}\simeq3.2$ at spin $a\sim0.7$), giving a finesse $F=(\pi/2)(3.2)\simeq5.03$ and $Q_{220}\gg Q_{\min}$ by more than an order of magnitude. The consequence is sharp and falsifiable-by-architecture:

> **The inversion-comb teeth are *always* intrinsically width-resolvable when present. The sole obstruction to detection is SNR, never linewidth.**

This cleanly partitions the null result: a non-detection at $\rho_{\rm rd}<7.52$ is *expected and uninformative* (too faint), whereas a non-detection at $\rho_{\rm rd}>7.52$ with the GR cluster cleanly resolved is *genuinely falsifying* — because $F\gg1$ guarantees a real tooth could not have hidden under its own width. The finesse converts "we didn't see it" into a graded, honest verdict instead of an excuse.

## Prediction

**A spectral tooth at $e^{\pi/2}\,f_{220}^{\rm meas}=4.81\,f_{220}^{\rm meas}$, anchored on the *measured* fundamental — i.e. $\mathbf{1207\pm}$ a few Hz for GW150914 ($f_{220}=251$ Hz) and $\mathbf{\sim317}$ Hz for GW190521 ($f_{220}\approx66$ Hz) — phase-correlated with the ringdown. If a next-generation detector reaches $\rho_{\rm rd}>7.52$ on such an event and finds NO power within $\pm2\%$ of $4.81\,f_{220}^{\rm meas}$ (while the GR Kerr overtone cluster near $f_{220}$ is cleanly resolved), the inversion comb is falsified.**
