# 29 — The Golden Ringdown Comb vs Real Data: An Honest Test

*Task 3 of the post-corpus program: run the GW overtone-comb prediction (notes
15/23/28) against real gravitational-wave strain. This sandbox has no outbound
network, so a literal GWOSC fetch + matched filter could not be executed here; the
runnable pipeline is committed (`gw_test/run_gwosc_test.py`) for any networked
machine. What CAN be settled offline — the comparison of the framework's
prediction against the established GR Kerr overtone spectrum and published ringdown
results — is settled here, with the verdict stated plainly. Numbers reproduced by
`gw_test/predict_teeth.py`.*

---

## The prediction, made concrete

The framework makes two distinct GW claims, and they must be tested separately
because they live in different domains:

1. **A frequency overtone comb.** Ringdown spectral teeth at ratio
   $\Lambda_\varphi=e^{\pi/2}=4.8105$, i.e. $f_{m}=f_{220}\,e^{m\pi/2}$.
2. **A time-domain echo train.** Post-merger echoes at $t_m=t_0\,e^{m\pi/2}$ with
   per-echo amplitude decrement $\gamma_{\text{echo}}=e^{-S_1}=0.133$ ($-17.5$ dB/leg)
   and envelope $|h(t)|\sim t^{-1.2843}$.

For the two loudest suitable events:

| Event | $M_f$ | $f_{220}$ | tooth $m{=}{-}1$ | tooth $m{=}{+}1$ | GR $(2,2,1)$ overtone |
|---|---|---|---|---|---|
| GW150914 | $62\,M_\odot$ | $251$ Hz | $52.2$ Hz | $1207$ Hz | $\approx 242$ Hz ($0.96\,f_{220}$) |
| GW190521 | $142\,M_\odot$ | $66$ Hz | $13.7$ Hz (sub-band) | $317$ Hz | $\approx 64$ Hz ($0.97\,f_{220}$) |

## The decisive discriminant

This is the crux, and it does not need new data:

$$\frac{f_{+1}}{f_{220}}\bigg|_{\text{framework}} = e^{\pi/2} = 4.81
\qquad\text{vs}\qquad
\frac{f_{221}}{f_{220}}\bigg|_{\text{GR Kerr}} \approx 0.95 .$$

GR Kerr overtones are **near-degenerate in frequency** — the $(2,2,1)$ real
frequency sits a few percent *below* the fundamental, while its *damping* roughly
triples. The framework, read as an overtone comb, instead places its next tooth a
**factor $\sim5$** away (a $\sim$1 kHz separation for GW150914, $\sim$250 Hz for
GW190521). These are not subtle alternatives; they are unmistakably different
spectra.

## Verdict

**As a frequency overtone comb: disfavored by existing data.** Ringdown overtone
analyses of GW150914 (and the broader catalog) find the first overtone at a
frequency *consistent with GR's near-degenerate $(2,2,1)$*, not at $4.81\,f_{220}$.
A tooth at $1207$ Hz (GW150914) or $317$ Hz (GW190521) carrying the predicted
$-17.5$ dB relative weight is not what the standard analyses report. If the golden
comb's teeth are QNM overtones, the prediction is already in tension with the data.

**As a time-domain echo train: not excluded, but not yet a test.** The framework's
own detectability theorem (note 28) gives
$N_{\text{obs}}=\lfloor \ln\rho_{\text{rd}}/S_1\rfloor=0$ for the ringdown SNRs of
these events ($\rho_{\text{rd}}\sim7<e^{S_1}=7.52$). So the echo interpretation
predicts **no detectable echo** at current sensitivity — consistent with the
(contested, largely null) echo searches in the Abedi–Afshordi vein, and crucially
*distinct* from those searches because it predicts **multiplicative** $e^{\pi/2}$
spacing rather than the constant $\sim0.2$–$0.3$ s spacing they assumed.

**Net honest status.** The cleanest, immediately falsifiable channel — the
$e^{\pi/2}$ *frequency* comb — runs against the grain of established Kerr
phenomenology and looks disfavored. The framework's survivable reading pushes the
signal into the *time-domain echo* regime, where it is self-consistently below
current detectability and awaits either (a) a much louder ringdown
($\rho_{\text{rd}}>7.5$ for one echo, $>56$ for two) or (b) a dedicated search
templated on **multiplicative** $e^{\pi/2}$ spacing with the fixed $-17.5$ dB/leg
decrement, which existing constant-spacing echo searches did not use.

## What runs where there is network

`gw_test/run_gwosc_test.py` (needs `gwpy`, `gwosc`, `scipy`) fetches H1/L1 strain
for both events, whitens and bandpasses, and performs:
- the **overtone test** — post-merger spectral power at the golden teeth
  $f_{220}e^{\pm\pi/2}$ versus at the GR overtone $0.95\,f_{220}$ (the discriminant
  above, now against real spectra), and
- the **echo test** — a matched filter for the golden echo train
  ($t_m=t_0e^{m\pi/2}$, $\gamma=0.133$) versus a time-reversed null control,
  expected to return null at these SNRs.

## Prediction / falsifier

- **Falsified now** if a dedicated overtone search confirms (as the literature
  indicates) that the only ringdown overtone is GR's near-degenerate $(2,2,1)$ and
  sets an upper limit on any $4.81\,f_{220}$ tooth below the predicted $-17.5$ dB.
- **Supported** only if a future loud ringdown ($\rho_{\text{rd}}\gtrsim7.5$) shows
  a post-merger echo at $t_0e^{\pi/2}$ with the fixed golden decrement — a signature
  no constant-spacing search is tuned to find.
