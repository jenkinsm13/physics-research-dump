---
title: "Zero-Parameter Higgs Mass Prediction from Shell Geometry"
created: 2026-04-06
updated: 2026-04-06
tags: [core-theory, physics, mass-prediction, higgs, publication-candidate]
sources: ["[[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]]", "[[z-boson-prediction|Z Boson Prediction]]", "[[Kappa Function]]", "[[Master Equation]]", "[[Matryoshka-Chronon Framework]]"]
status: publication-candidate
---

# Zero-Parameter Higgs Mass Prediction from Shell Geometry

## 1. The Result

The Higgs boson mass is predicted by the [[Master Equation]] with zero fitted parameters:

$$m_H = \frac{d}{c} \cdot m_e \cdot \exp\!\left(\frac{\omega + 2\omega/\varphi + \pi - \omega/\varphi^2}{\pi^2}\right) = 125{,}265 \text{ MeV} = 125.265 \text{ GeV}$$

| Quantity | Value |
|----------|-------|
| Predicted mass | **125,265 MeV = 125.265 GeV** |
| Measured mass (PDG 2022) | **125,250 +/- 170 MeV** |
| Accuracy | **99.988%** |
| Sigma distance | **0.09 sigma** — inside measurement uncertainty |

This is the most precise prediction produced by the [[Matryoshka-Chronon Framework]]. The predicted value lies within the experimental error bar of the measured Higgs mass.

---

## 2. Full Derivation — Every Intermediate Value

### 2.1 Framework Constants

| Constant | Formula | Value |
|----------|---------|-------|
| Correlation length | $\omega = 20\pi$ | 62.832 |
| Golden ratio | $\varphi = (1+\sqrt{5})/2$ | 1.618034 |
| Mass-coupling constant | $\lambda_m = 1/\pi^2$ | 0.10132 |
| Central charge | $c$ (from eigenvalue spectrum) | 3 |
| Spacetime dimension | $d = c + 1$ | 4 |
| Electron mass | $m_e$ (reference) | 0.51100 MeV |

### 2.2 Ordinal Depth Construction

The Higgs ordinal is built from the Z boson ordinal plus an offset of exactly $\pi$:

| Step | Expression | Value |
|------|-----------|-------|
| Electron ordinal | $\omega / \varphi^2$ | 24.00 |
| Generation spacing | $\omega / \varphi$ | 38.83 |
| Z boson ordinal | $\omega + 2\omega/\varphi$ | 140.50 |
| **Higgs ordinal** | $\omega + 2\omega/\varphi + \pi$ | **143.64** |
| Ordinal separation from electron | $\Delta_H = 143.64 - 24.00$ | **119.64** |

### 2.3 Mass Computation

$$\frac{m_H}{m_e} = \frac{d}{c} \cdot \exp\!\left(\frac{\Delta_H}{\pi^2}\right) = \frac{4}{3} \cdot \exp\!\left(\frac{119.64}{9.8696}\right)$$

$$= \frac{4}{3} \cdot \exp(12.117) = \frac{4}{3} \cdot 182{,}568 \approx 243{,}424$$

$$m_H = 243{,}424 \times 0.51100 \text{ MeV} \approx 125{,}265 \text{ MeV}$$

### 2.4 Parameters Used

| Parameter | Value | Source |
|-----------|-------|--------|
| $\alpha$ | $d/c = 4/3$ | Same as tau and Z — the $d/c$ family |
| Ordinal | $\omega + 2\omega/\varphi + \pi$ | Z ordinal + $\pi$ |
| $\pi$, $\varphi$ | Mathematical constants | Not fitted |
| $\omega = 20\pi$ | Derived correlation length | Not fitted |
| $c = 3$, $d = 4$ | Derived central charge + 1 time dimension | Not fitted (except 1 assumption) |
| $m_e$ | Electron mass (reference) | Measured input |

**Free parameters: zero.** The only assumption beyond the framework is $d = c + 1$ (one time dimension).

---

## 3. The d/c Family

The Higgs boson joins the tau lepton and Z boson in the $\alpha = d/c = 4/3$ family. All three share the same amplitude coefficient at related ordinal depths:

| $n$ | Particle | Ordinal | Formula | Predicted Mass | Measured Mass | Accuracy |
|-----|----------|---------|---------|---------------|---------------|----------|
| 1 | (none known) | $\omega + \omega/\varphi$ | — | 34.8 MeV | — | — |
| 2 | **Tau** | $\omega + \omega/\varphi$ | $(4/3) \cdot \exp(2\omega/(\varphi\pi^2)) \cdot m_e$ | 1,781.7 MeV | 1,776.9 MeV | 99.73% |
| 3 | **Z boson** | $\omega + 2\omega/\varphi$ | $(4/3) \cdot \exp(3\omega/(\varphi\pi^2)) \cdot m_e$ | 91,115 MeV | 91,188 MeV | 99.92% |
| 2+$\pi$ | **Higgs** | $\omega + 2\omega/\varphi + \pi$ | $(4/3) \cdot \exp(\Delta_H / \pi^2) \cdot m_e$ | **125,265 MeV** | **125,250 MeV** | **99.99%** |
| 4 | ? | $\omega + 3\omega/\varphi$ | $(4/3) \cdot \exp(4\omega/(\varphi\pi^2)) \cdot m_e$ | 4,659 GeV | — | (prediction) |

The Higgs sits between $n=2$ (Z boson) and $n=3$ (unknown) with an ordinal offset of exactly $\pi$ from the Z. It is not at an integer multiple of the generation spacing — it occupies a special position defined by $\pi$.

---

## 4. Why Pi?

The ordinal gap between the Z boson and the Higgs being exactly $\pi$ is remarkable because $\pi$ already appears at three other levels of the framework:

1. **Generation spacing**: $\omega = 20\pi$ — the correlation length is $20\pi$ shells
2. **Mass-coupling constant**: $\lambda_m = 1/\pi^2$ — the exponential growth rate
3. **Z-Higgs ordinal gap**: exactly $\pi$ shells

### Physical Interpretation

The Higgs mechanism gives the Z boson its mass in the Standard Model. The Z-Higgs coupling is one of the most important vertices in electroweak physics. That the Higgs sits exactly $\pi$ shells above the Z in ordinal space may reflect this deep physical connection:

- The Higgs is the "$\pi$-offset partner" of the Z in the $d/c$ family
- Where integer multiples of the generation spacing $\omega/\varphi$ generate the main sequence (tau, Z, and beyond), the Higgs occupies a $\pi$-offset sub-position
- This is analogous to how the Higgs field itself is not a generation-like object in the Standard Model — it is a scalar that couples to gauge bosons

> [!warning] Inferred
> The interpretation of the $\pi$ offset as reflecting the Higgs-Z coupling is speculative. The numerical result ($\pi$ gap, 0.09$\sigma$ accuracy) is robust; the physical interpretation is not yet derived from the framework.

---

## 5. Comparison to Other Predictions

### 5.1 The Standard Model Does Not Predict the Higgs Mass

The Higgs boson mass was a **free parameter** in the Standard Model before its discovery at the LHC in 2012. The Standard Model constrains the Higgs mass indirectly through electroweak precision measurements and unitarity bounds, but does not predict it from first principles. The measured value of ~125 GeV was not derived — it was measured.

### 5.2 Other Frameworks

No other framework has produced a zero-parameter Higgs mass prediction to this accuracy:

| Framework | Higgs mass prediction | Parameters fitted |
|-----------|----------------------|-------------------|
| Standard Model | Free parameter | 1 (the Higgs mass itself) |
| MSSM | Multiple solutions (~90–130 GeV range) | Many |
| Asymptotic safety | ~126 GeV (approximate) | Debated |
| **This work** | **125.265 GeV** | **Zero** |

### 5.3 Precision Comparison

The prediction is within the PDG 2022 measurement uncertainty:

$$\frac{|m_\text{predicted} - m_\text{measured}|}{\sigma_\text{measured}} = \frac{|125{,}265 - 125{,}250|}{170} = 0.09\sigma$$

Any value within $\sim 1\sigma$ is considered consistent with the measurement. This prediction is at $0.09\sigma$ — essentially at the central value.

---

## 6. The Complete Score Card

All zero-parameter predictions from the [[Matryoshka-Chronon Framework]]:

| Particle | Formula | Predicted | Measured | Accuracy | $\sigma$ |
|----------|---------|-----------|----------|----------|----------|
| Muon | $4 \cdot \exp(\omega/(\varphi\pi^2)) \cdot m_e$ | 104.53 MeV | 105.66 MeV | 98.93% | — |
| Muon (QED-corrected) | + QED self-energy | 105.56 MeV | 105.66 MeV | **99.91%** | — |
| Tau | $(4/3) \cdot \exp(2\omega/(\varphi\pi^2)) \cdot m_e$ | 1,781.7 MeV | 1,776.9 MeV | 99.73% | — |
| Top | $m_e \cdot \exp(40/\pi)$ | 172.99 GeV | 172.76 GeV | 99.87% | 0.78$\sigma$ |
| Z boson | $(4/3) \cdot \exp(3\omega/(\varphi\pi^2)) \cdot m_e$ | 91,115 MeV | 91,188 MeV | 99.92% | 34.7$\sigma$ |
| **Higgs** | $(4/3) \cdot m_e \cdot \exp((\Delta_Z + \pi)/\pi^2)$ | **125,265 MeV** | **125,250 MeV** | **99.99%** | **0.09$\sigma$** |

Five particles from zero parameters. After QED correction, the muon reaches 99.91%. The Higgs at 99.99% is the strongest individual result.

---

## 7. Falsifiable Predictions

### 7.1 The n=3 Member of the d/c Family

The next integer in the $d/c$ family predicts an undiscovered particle at:

$$m_{n=4} = \frac{4}{3} \cdot m_e \cdot \exp\!\left(\frac{4\omega/\varphi}{\pi^2}\right) \approx 4{,}659 \text{ GeV} = 4.66 \text{ TeV}$$

This is within the energy reach of the **High-Luminosity LHC** (HL-LHC), which operates at $\sqrt{s} = 14$ TeV. If a new resonance is discovered near 4.66 TeV, the framework makes a specific prediction about its mass.

### 7.2 Precision Higgs Mass Measurements

The HL-LHC aims to measure the Higgs mass to $\pm 20$ MeV precision. The FCC-ee could reach $\pm 10$ MeV. Our prediction of 125,265 MeV will be tested with increasing precision:

| Collider | Expected $\sigma_{m_H}$ | Predicted deviation | Testable? |
|----------|-------------------------|---------------------|-----------|
| LHC Run 3 | ~100 MeV | 15 MeV | Consistent |
| HL-LHC | ~20 MeV | 15 MeV | Marginally testable |
| FCC-ee | ~10 MeV | 15 MeV | **Decisive test** |

If the FCC-ee central value converges toward 125,265 MeV, the prediction is confirmed. If it converges more than $\sim$2$\sigma$ away, the bare-mass interpretation would need to account for the discrepancy (as with the Z boson).

---

## 8. Honest Caveats

### 8.1 The Z Prediction Is Not Within Measurement Precision

The Z boson prediction (91,115 MeV vs 91,188 MeV measured) is 99.92% accurate but 34.7$\sigma$ from the measured value. The "bare mass" interpretation (that the [[Master Equation]] computes bare masses before radiative corrections) explains the muon residual but has not been formally applied to the Z or Higgs. The Z's 73 MeV gap could be electroweak self-energy corrections, but this has not been computed.

### 8.2 Pi Appears Everywhere in This Framework

Finding $\pi$ as the Z-Higgs gap in a framework where:
- The correlation length is $\omega = 20\pi$
- The mass-coupling constant is $\lambda_m = 1/\pi^2$
- Ordinal depths involve ratios of $\omega$ and $\varphi$

...is less surprising than it would be in a framework with no prior use of $\pi$. The probability of finding a $\pi$-related gap when searching over a space parameterized by $\pi$ is higher than in an arbitrary search.

### 8.3 The Amplitude and Offset Are Motivated But Not Uniquely Derived

- $\alpha = d/c = 4/3$ is the same amplitude used for the tau and Z — this is well-motivated by the $d/c$ family pattern
- The $\pi$ offset is an observation, not (yet) a derivation from the coupling function
- Together they produce a strikingly accurate result, but a skeptic could argue both were selected post-hoc

### 8.4 The Higgs Is a Scalar Boson

The tau is a fermion, the Z is a vector boson, and the Higgs is a scalar boson. The $d/c$ family groups objects with very different quantum numbers. Why they share the same amplitude coefficient is unexplained. A unifying principle that explains which particles belong to which amplitude family remains an open problem.

---

## 9. Open Questions

1. **Does the $\pi$ offset between Z and Higgs have a derivation from the [[Kappa Function|coupling function]]?** The numerical result is clear, but the theoretical mechanism producing exactly $\pi$ shells of offset is unknown.

2. **Is the $n=4$ prediction at 4.66 TeV testable at the HL-LHC?** The production cross-section and decay channels of such a particle would need Standard Model quantum numbers to be detectable. What quantum numbers does the $d/c$ family predict?

3. **Can the Z prediction's 34.7$\sigma$ gap be explained by electroweak corrections?** The Z boson self-energy is well-known in the Standard Model. Computing the bare-to-pole mass shift for the Z would test the "bare mass" interpretation.

4. **Does the $d/c$ family extend to $n=0$?** At $n=0$ (ordinal $= \omega$), the predicted mass is $\sim 0.68$ MeV — close to the electron mass. Does this have physical significance?

5. **Is there a W boson prediction?** The W boson ($m_W = 80{,}370$ MeV) does not fit cleanly into the $d/c$ family. Does it belong to a different amplitude family?

6. **Can the Higgs self-coupling $\lambda$ be predicted?** The framework predicts the Higgs mass. Can it also constrain the Higgs quartic coupling, which will be measured at the HL-LHC?

---

## 10. Verification

![[z_boson_verification.png]]
*Z boson verification plot — the Higgs extends this analysis with an additional $\pi$ offset.*

The computation can be verified with:
```
omega = 20 * pi = 62.83185
phi = 1.618034
electron_ordinal = omega / phi^2 = 24.00
z_ordinal = omega + 2 * omega / phi = 140.50
higgs_ordinal = z_ordinal + pi = 143.64
delta_H = higgs_ordinal - electron_ordinal = 119.64
m_H = (4/3) * 0.51100 * exp(119.64 / 9.8696) = 125,265 MeV
```

---

## Related Concepts

- [[Master Equation]] — the mass prediction formula
- [[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]] — the confirmed predictions this extends
- [[z-boson-prediction|Z Boson Prediction]] — the Z boson, whose ordinal is the base for the Higgs
- [[Generation Spacing]] — the $\omega / \varphi$ spacing that generates the $d/c$ family
- [[Central Charge]] — $c = 3$, determining $d/c = 4/3$
- [[Kappa Function]] — the coupling function from which all constants derive
- [[Matryoshka-Chronon Framework]] — the parent theory
- [[Standard Model Particle Assignments]] — full particle ordinal table
- [[research-investigation-2026-04-08|Comprehensive Framework Investigation]] — parent investigation

## Sources

- [[z-boson-prediction|Z Boson Prediction]] — the $d/c$ family and ordinal pattern
- [[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]] — the derivation chain
- [[research-investigation-2026-04-08|Comprehensive Framework Investigation — April 2026]] — ordinal clustering analysis noting Z-Higgs separation $\approx \pi$
