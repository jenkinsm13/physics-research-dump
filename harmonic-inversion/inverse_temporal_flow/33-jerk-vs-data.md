# 33 — The Cosmic Jerk and $w(z)$ vs Survey Data

*Confronting the framework's cosmological predictions (note 21) with current DESI DR2
(2025) dark-energy constraints. The honest headline is a **negative**: the framework
predicts near-$\Lambda$CDM dark energy, and DESI now disfavors near-$\Lambda$CDM in
favor of evolving dark energy at $2.8$–$4.2\sigma$. The jerk — the corpus's cleanest
"distinct from $\Lambda$CDM" number — is real but **not yet testable**. All framework
internals reproduced by `verify/verify_jerk-vs-data.py` (exit 0); all DESI numbers
independently web-verified.*

---

## What the framework predicts

From the horizon-anchored equation of state (note 21 §4),
$$w(z)=-1-\frac{\cos\!\big(2N_\star\ln\varphi-2\ln(1+z)\big)}{N_\star},\qquad N_\star\approx291.88,$$
the realized today-values are
$$w_0=-0.9969,\qquad |1+w_0|\le 1/N_\star=3.4\times10^{-3},\qquad
(w_0,w_a)_{\rm CPL}=(-0.995,\,-0.0065),$$
a phantom crossing at $z_\times=1.77$, and the **cosmic jerk**
$$j_0-1=\frac{3\Omega_\Lambda}{2N_\star}\big[3\cos(2N_\star\ln\varphi)-2\sin(2N_\star\ln\varphi)\big]=-0.0062
\;\Rightarrow\; j_0=0.9938,$$
versus $\Lambda$CDM's exact $j\equiv1$. The defining feature: the framework's dark
energy is **a hair off $\Lambda$CDM** — $|1+w_0|\sim10^{-3}$, $|w_a|\sim10^{-2}$.

## What DESI DR2 (2025) measures

DESI DR2 BAO + CMB + SNe prefers *evolving* dark energy in the quadrant $w_0>-1$,
$w_a<0$, and **excludes $\Lambda$CDM** at (web-verified):

| Combination | $w_0$ | $w_a$ | excludes $\Lambda$CDM |
|---|---|---|---|
| DESI+CMB (no SN) | — | — | $3.1\sigma$ |
| DESI+CMB+Pantheon+ | $\approx-0.86$ | $\approx-0.6$ | $2.8\sigma$ |
| DESI+CMB+DES-SN5YR | $\approx-0.82$ | $\approx-0.73$ | $4.2\sigma$ |
| DESI+CMB+Union3 | $\approx-0.66$ | $\approx-1.15$ | $3.8\sigma$ |

*(DESI DR2 BAO: arXiv:2503.14738; evolving-DE SN combinations: arXiv:2508.10514. The
$2.8/3.8/4.2\sigma$ exclusions and the $3.1\sigma$ DESI+CMB figure are confirmed
against the published results.)*

## The comparison — honest and decisive

The framework sits essentially **on the $\Lambda$CDM point** in DESI's parameter space:
$$\frac{|w_{0,\rm fw}-(-1)|}{\sigma_{w_0}}=0.08\sigma,\qquad
\frac{|w_{a,\rm fw}-0|}{\sigma_{w_a}}=0.03\sigma\quad(\text{DESY5 errors}).$$
So whatever DESI says about $\Lambda$CDM, it says about the framework. And DESI
**disfavors** $\Lambda$CDM:

| Combination | framework vs DESI mean, $w_0$ | $w_a$ | inherited verdict |
|---|---|---|---|
| Pantheon+ | $2.4\sigma$ | $2.4\sigma$ | disfavored |
| DES-SN5YR | $3.0\sigma$ | $2.8\sigma$ | disfavored |
| Union3 | $3.7\sigma$ | $3.5\sigma$ | disfavored |

**Verdict on $w(z)$: DISFAVORED at $\sim2.4$–$3.7\sigma$**, the same significance at
which DESI excludes $\Lambda$CDM. The one qualitative point in the framework's favor —
it *does* predict a quintessence-side $w_0>-1$ with a phantom crossing, matching the
*direction* of DESI's preference — is outweighed by the *magnitude*: DESI wants a
crossing near $z_\times\approx0.3$–$0.4$ and a large $|w_a|\sim1$, while the framework's
crossing is at $z_\times=1.77$ with $|w_a|\sim0.006$, two orders too small. Right sign,
wrong size.

## The jerk: real but not yet a test

The jerk deficit $|j_0-1|=0.0062$ is far below current cosmographic resolution. Model-
independent jerk fits carry $\sigma(j_0)\sim0.1$–$1$ (truncation-dependent), and DESI
DR2 cosmography finds $j_0=1$ comfortably within $2\sigma$. To resolve $0.9938$ from
$1$ needs $\sigma(j_0)\ll0.0062$ — more than $15\times$ tighter than the best current
bound. **Verdict on the jerk: NOT YET TESTABLE**; $j_0=0.9938$ is presently
indistinguishable from $\Lambda$CDM. It remains the corpus's cleanest *in-principle*
discriminator (a Roman+DESI+Euclid joint $H(z)$ could reach $\sigma_{j_0}\sim10^{-2}$,
still short), but it is not a near-term win.

## One knob, named honestly

The $w(z)$ formula evaluates the oscillatory phase at the *integer* shell $N=291$ while
using the *continuous* $N_\star=291.88$ for the amplitude (verify-script docstring). This
is a genuine convention ambiguity: putting $291.88$ inside the cosine shifts
$\Phi_{\rm res}$ from $+0.894$ to $+0.257$, hence $w_0\to-0.9991$ and $j_0\to0.9982$.
**This knob does not change either verdict** — every choice keeps $w(z)$ within
$|1+w|\lesssim10^{-3}$ of $\Lambda$CDM (so still disfavored by DESI's evolving-DE
preference) and keeps $|j_0-1|\lesssim0.006$ (so still untestable). The framework's
near-$\Lambda$CDM character is robust to the convention; only the third decimal moves.

## Verdict

- **$w(z)$:** *disfavored* at $\sim2.4$–$3.7\sigma$. The framework is observationally
  $\Lambda$CDM-like, and DESI DR2 now prefers evolving dark energy over $\Lambda$CDM at
  that significance. Right direction (quintessence, $w_0>-1$, a crossing), wrong
  magnitude ($|w_a|$ two orders too small).
- **Jerk $j_0=0.9938$:** *not yet testable* — $15\times$ below current cosmographic
  resolution; indistinguishable from $\Lambda$CDM today.

**Falsifier / watch:** if future BAO+SNe drive $(w_0,w_a)$ *further* from $\Lambda$CDM
(larger $|w_a|$), the near-$\Lambda$CDM framework is falsified outright. If instead the
evolving-DE signal *weakens* back toward $\Lambda$CDM as systematics are controlled
(the SN-calibration sensitivity is real), the framework returns to consistency — and the
jerk becomes the only remaining discriminator, awaiting $\sigma_{j_0}\lesssim10^{-3}$.

**Sources:** [DESI DR2 BAO (arXiv:2503.14738)](https://arxiv.org/abs/2503.14738) ·
[Evolving DE after DESI DR2 (arXiv:2508.10514)](https://arxiv.org/abs/2508.10514) ·
[On DESI's DR2 exclusion of ΛCDM (arXiv:2504.15336)](https://arxiv.org/abs/2504.15336).
