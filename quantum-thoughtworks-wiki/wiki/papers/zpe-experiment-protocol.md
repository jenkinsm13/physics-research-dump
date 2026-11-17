---
title: "κ-Informed ZPE Experiment Design: A Tabletop Protocol"
created: 2026-04-06
updated: 2026-04-06
tags: [experiment, zpe, kappa-function, chronovoltaics, falsifiable, protocol]
sources: ["[[chronovoltaics-kappa-connection]]", "[[Chronovoltaics]]", "[[Kappa Function]]", "[[ZPE Digital Twin]]"]
---

# $\kappa$-Informed ZPE Experiment Design: A Tabletop Protocol

> [!note] Purpose
> This article specifies a five-phase, 10-day tabletop experiment designed to test the prediction that [[Kappa Function|$\kappa$-function]] resonance peaks appear at **irrational frequency ratios** in zero-point energy coupling. Budget: \$2K--\$15K. The key discrimination: $\kappa$ peaks occur at irrational ratios ($\approx 5.65$ between adjacent peaks), while classical Bragg resonances occur at integer ratios.

![[zpe_experiment_design.png]]

---

## 1. Resonant Frequencies from $\kappa$ Peaks

The [[Kappa Function|$\kappa$ function]] exhibits discrete peaks at specific wavenumbers. After envelope correction (removing the exponential decay $e^{-k/\varphi}$ to expose the oscillatory structure), the dominant peaks occur at:

| Peak | $k$ value | Envelope-corrected amplitude |
|------|-----------|------------------------------|
| 1st  | $k \approx 1.19$ | 1.00 (reference) |
| 2nd  | $k \approx 4.46$ | 0.73 |
| 3rd  | $k \approx 7.72$ | 0.54 |

The peak spacing is governed by $\pi / (2\ln\varphi)$, an irrational number, reflecting the underlying $\cos^2(2k\ln\varphi)$ oscillation in $\kappa(k)$.

### Mapping to Physical Frequencies

For a base frequency $f_0 = 1\;\text{GHz}$, the $\kappa$-resonant frequencies are:

$$f_n = f_0 \cdot e^{k_n \cdot \ln\varphi} = f_0 \cdot \varphi^{k_n}$$

| Peak | $k$ | Frequency |
|------|-----|-----------|
| 1st  | 1.19 | $\varphi^{1.19} \approx 1.77\;\text{GHz}$ |
| 2nd  | 4.46 | $\varphi^{4.46} \approx 8.53\;\text{GHz}$ |
| 3rd  | 7.72 | $\varphi^{7.72} \approx 41.0\;\text{GHz}$ |

**Critical signature**: The ratio between adjacent resonant frequencies is $\varphi^{k_2 - k_1} \approx \varphi^{3.27} \approx 5.65$ -- an **irrational number**. Classical Bragg resonances in periodic structures produce peaks at **integer multiples** of the fundamental. This is the primary discriminator.

---

## 2. Metamaterial Design

### Acoustic Impedance Stack

The metamaterial uses alternating layers of **silicone rubber** and **brass** to create an acoustic impedance mismatch that mimics the Landen parameter:

$$\frac{Z_{\text{silicone}}}{Z_{\text{brass}}} \approx 0.172 \approx r = 3 - 2\sqrt{2} \approx 0.172$$

where $r$ is the Landen parameter of $E: y^2 = x^3 - x$ (see [[chronovoltaics-kappa-connection]]).

> [!note] Design Rationale
> The impedance ratio is chosen to match the Landen parameter exactly. If the $\kappa$-framework is correct, this ratio maximizes energy coupling between layers at the predicted irrational-ratio frequencies. If the framework is wrong, this ratio has no special significance and the stack behaves as an ordinary periodic medium with integer-ratio Bragg peaks.

### 8-Plate Casimir Stack

A Casimir cavity stack with **8 plates** at $\varphi$-scaled separations:

| Plate gap | Separation |
|-----------|------------|
| 1--2 | $100\;\text{nm}$ |
| 2--3 | $100\varphi \approx 162\;\text{nm}$ |
| 3--4 | $100\varphi^2 \approx 262\;\text{nm}$ |
| 4--5 | $100\varphi^3 \approx 424\;\text{nm}$ |
| 5--6 | $100\varphi^4 \approx 686\;\text{nm}$ |
| 6--7 | $100\varphi^5 \approx 1.11\;\mu\text{m}$ |
| 7--8 | $100\varphi^6 \approx 1.79\;\mu\text{m}$ |

The $\varphi$-scaling ensures that the cavity resonances align with $\kappa$ peaks rather than forming a periodic lattice.

---

## 3. C1-R Circuit: 8-Stage Switched-Capacitor Chain

The electronic readout uses a **C1-R (RF/analog) architecture** (see [[chronovoltaics-digital-twins]]) implemented as an 8-stage switched-capacitor circuit:

- **8 stages** corresponding to the 8 Casimir plates
- **$\kappa$-weighted coupling capacitors**: The coupling capacitance between stages $i$ and $j$ is proportional to $\kappa(|i-j|)$
- **Switched-cap topology**: Each stage samples the Casimir-induced voltage at the $\kappa$-resonant frequencies
- **Rectification**: The switched-cap chain implements temporal ordering (forward vs. reverse), enabling direct measurement of $\mathcal{R}_\tau$

The C1-R architecture was chosen over C1-P (photonic) for the tabletop scale because:
1. No optical alignment required
2. Standard PCB fabrication
3. Direct voltage readout
4. Lower cost (\$2K--\$5K for the electronics)

---

## 4. Experiment Protocol: 5 Phases, 10 Days

### Phase 1: Calibration (Days 1--2)
- Characterize the metamaterial stack with broadband acoustic spectroscopy
- Measure impedance ratios and verify $Z_{\text{silicone}}/Z_{\text{brass}} \approx 0.172$
- Baseline noise floor of the C1-R circuit
- Verify Casimir plate separations via AFM or capacitance measurement

### Phase 2: Broadband Scan (Days 3--4)
- Sweep excitation frequency from 0.5 to 50 GHz
- Record C1-R output voltage vs. frequency
- Identify all resonance peaks above $3\sigma$ noise floor
- **Key measurement**: Are peaks at irrational or integer frequency ratios?

### Phase 3: $\kappa$-Peak Lock (Days 5--6)
- Lock excitation to each predicted $\kappa$-peak frequency (1.77, 8.53, 41.0 GHz)
- Measure rectification ratio $\mathcal{R}_\tau$ by switching temporal ordering
- Record coupling energy as a function of stage number
- **Key measurement**: Does the top-$Z$ pair (stages 7--8) contribute $\sim 30\%$ of total coupling?

### Phase 4: Null Tests (Days 7--8)
- Run all five null tests (see Section 5)
- Replace $\varphi$-scaled Casimir stack with uniformly spaced stack (same total gap)
- Replace $\kappa$-weighted coupling caps with uniform caps
- Verify that null conditions destroy the irrational-ratio signature

### Phase 5: Analysis and Replication (Days 9--10)
- Statistical analysis of frequency ratios (irrational vs. integer hypothesis test)
- Error budget: plate separation uncertainty, temperature drift, electronics noise
- Document for independent replication
- Compare all results against [[ZPE Digital Twin]] predictions

---

## 5. Five Null Tests (Falsification Criteria)

Each null test targets a specific prediction of the $\kappa$ connection. If any null test **passes** (i.e., the predicted effect **disappears** under the null condition), the corresponding aspect of the $\kappa$ connection is falsified.

| # | Null Test | What it falsifies | Procedure |
|---|-----------|-------------------|-----------|
| 1 | **Uniform spacing** | $\varphi$-scaling of Casimir gaps | Replace $\varphi$-scaled stack with uniform $\bar{d}$ spacing. If irrational-ratio peaks persist, $\varphi$-scaling is irrelevant. |
| 2 | **Uniform coupling** | $\kappa$-weighted inter-stage coupling | Replace $\kappa$-weighted coupling caps with identical caps. If $\mathcal{R}_\tau$ is unchanged, $\kappa$-weighting is irrelevant. |
| 3 | **Random ordering** | Temporal order sensitivity | Randomize the switched-cap sampling sequence. If $W_{\text{BCH}}$ is unchanged, the BCH commutator structure is irrelevant. |
| 4 | **Impedance mismatch** | Landen parameter tuning | Change silicone/brass ratio to 0.5 (far from $r = 0.172$). If resonance structure is unchanged, the Landen parameter match is coincidental. |
| 5 | **Single cavity** | Multi-shell coupling | Use a single Casimir cavity instead of the 8-plate stack. If rectification ratio $\mathcal{R}_\tau$ still approaches 2, inter-shell coupling is irrelevant. |

> [!warning] Falsification standard
> A null test "passes" (falsifies) if the effect size drops below $2\sigma$ of the baseline measurement. A null test "fails" (supports the $\kappa$ connection) if the effect size drops by more than $5\times$ under the null condition.

---

## 6. Key Discrimination: Irrational vs. Integer Ratios

The central experimental prediction:

| Property | $\kappa$-framework prediction | Classical (Bragg) prediction |
|----------|-------------------------------|------------------------------|
| Peak frequency ratios | Irrational ($\approx 5.65$) | Integer (2, 3, 4, ...) |
| Peak spacing (log-frequency) | $\Delta k \approx 3.27$ (irrational) | $\Delta k = \ln n$ for integer $n$ |
| Envelope | $e^{-k/\varphi}$ decay | Power-law or no decay |
| Dominant coupling pair | Top-$Z$ pair (30.2%) | Nearest-neighbor |
| Rectification bound | $R_{\max} = 2$ (exact) | No universal bound |

The adjacent-peak frequency ratio of $\approx 5.65$ is far from any small integer. A standard FFT with frequency resolution $\Delta f / f < 1\%$ easily distinguishes $5.65$ from $5$ or $6$.

---

## 7. Power Budget and Passivity

> [!warning] Important
> The $\kappa$ framework does **not** predict energy creation. The power budget respects passivity (see [[chronovoltaics-passivity]]).

$\kappa$ optimizes **transfer efficiency**, not total energy. The experiment measures:

$$\eta_{\text{transfer}} = \frac{W_{\text{out}}}{W_{\text{in}}} \leq \frac{R_{\max}}{1 + R_{\max}} = \frac{2}{3} \approx 66.7\%$$

The input energy comes from the external pump (RF source). The $\kappa$-optimized metamaterial channels more of that input into useful work via temporal ordering, but the total energy ledger always balances:

$$E_{\text{pump}} + E_{\text{ctrl}} = W_{\text{out}} + Q_{\text{loss}} + \Delta U$$

---

## 8. Budget Estimate

| Component | Estimated Cost |
|-----------|---------------|
| Silicone/brass metamaterial stack | \$200--\$500 |
| Casimir plate fabrication (8 plates, Au-coated) | \$1K--\$8K |
| C1-R PCB + components | \$500--\$2K |
| RF source (1--50 GHz) | \$0 (university lab access) -- \$3K (used equipment) |
| Measurement equipment (VNA, lock-in) | \$0 (lab access) -- \$2K |
| **Total** | **\$2K--\$15K** |

---

## Related Concepts

- [[Chronovoltaics]] -- the technology being tested
- [[ZPE Digital Twin]] -- digital twin for pre-experiment simulation
- [[Kappa Function]] -- the coupling function whose peaks define the resonances
- [[chronovoltaics-kappa-connection]] -- the theoretical result ($R_{\max} = 2$) this experiment tests
- [[gap-closure-landen-transform|Gap Closure: Landen Transform]] -- derivation of $\kappa$ from $E$
- [[chronovoltaics-digital-twins]] -- C1-R architecture reference

## Sources

- [[chronovoltaics-kappa-connection]] -- Landen parameter and rectification bound
- [[chronovoltaics-smoking-guns]] -- smoking gun signatures this experiment aims to reproduce
- [[chronovoltaics-passivity]] -- passivity constraint on the power budget
- [[ZPE Digital Twin]] -- simulation predictions to compare against
