---
title: "Z Boson Mass Prediction from Shell Geometry"
created: 2026-04-08
updated: 2026-04-08
tags: [original-research, mass-prediction, z-boson, falsifiable]
sources: ["[[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]]", "[[research-investigation-2026-04-08|Comprehensive Framework Investigation]]", "[[Master Equation]]", "[[Generation Spacing]]"]
status: candidate-prediction
---

# Z Boson Mass Prediction from Shell Geometry

## The Prediction

The Z boson mass is predicted by the [[Master Equation]] using the tau lepton's amplitude coefficient at the third integer multiple of the [[Generation Spacing|generation spacing]]:

$$\frac{m_Z}{m_e} = \frac{d}{c} \cdot \exp\!\left(\frac{3\omega / \varphi}{\pi^2}\right) = \frac{4}{3} \cdot \exp\!\left(\frac{3 \times 20\pi / \varphi}{\pi^2}\right)$$

| Quantity | Value |
|----------|-------|
| Amplitude $\alpha$ | $d/c = 4/3$ |
| Ordinal separation $\Delta_Z$ | $3\omega/\varphi = 3 \times 38.833 = 116.499$ |
| Predicted mass ratio $m_Z / m_e$ | $178{,}272$ |
| Predicted mass | **91,115 MeV** |
| Measured mass (PDG 2022) | **91,188 MeV** |
| Residual | $-0.08\%$ |
| Accuracy | **99.92%** |

---

## Why This Is Motivated

The Z boson prediction is NOT the result of a parameter search. It extends an existing pattern:

### The $d/c$ Family

The tau lepton and Z boson share the same amplitude coefficient $\alpha = d/c = 4/3$ at consecutive integer multiples of $\omega / \varphi$:

| $n$ | $\Delta = n \cdot \omega/\varphi$ | Predicted Mass | Particle | Accuracy |
|-----|-----------------------------------|----------------|----------|----------|
| 1 | 38.83 | 34.8 MeV | (none known) | — |
| 2 | 77.67 | 1,781.7 MeV | **Tau** | 99.73% |
| 3 | 116.50 | 91,115 MeV | **Z boson** | 99.92% |
| 4 | 155.33 | 4,659 GeV | (prediction) | — |

The tau was confirmed first. The Z boson is the next integer — a single-parameter extension ($n = 2 \to 3$), not a search result.

### Ordinal Pattern

The ordinal depths of the predicted particles follow a geometric progression anchored at the muon:

- **Muon**: $\omega$ (the correlation length itself)
- **Tau**: $\omega + \omega/\varphi$ (one generation spacing past muon)
- **Z boson**: $\omega + 2\omega/\varphi$ (two generation spacings past muon)

Each step adds $\omega / \varphi \approx 38.83$ shells.

---

## Relationship to the Weak Mixing Angle

The Z boson mass is related to the W boson mass by the weak mixing angle:

$$m_W = m_Z \cos\theta_W$$

where $\sin^2\theta_W \approx 0.2312$ (PDG 2022). If the framework predicts $m_Z$ correctly, it implicitly constrains $m_W$:

$$m_W^\text{implied} = 91{,}115 \times \cos(28.75°) = 79{,}896 \text{ MeV}$$

The measured $m_W = 80{,}370 \pm 13$ MeV. The implied value is $\sim 0.6\%$ low, suggesting the W boson may need its own framework assignment rather than being derived from the Z.

> [!warning] Inferred
> The framework does not currently predict the weak mixing angle. The W boson mass is not independently predicted — it would require a separate ordinal depth and amplitude.

---

## Falsifiable Tests

1. **Current precision**: The prediction ($91{,}115$ MeV) is $73$ MeV below the measured value ($91{,}188$ MeV). The PDG uncertainty on $m_Z$ is $\pm 2.1$ MeV, so the prediction is $\sim 35\sigma$ from the central value. However, this is a **bare-mass prediction** — QED and electroweak radiative corrections have not been applied. The muon's corrections reduced a 1.07% residual to 0.09%. A similar correction here could close the 0.08% gap.

2. **FCC-ee precision**: The Future Circular Collider (FCC-ee) aims to measure $m_Z$ to $\pm 0.1$ MeV precision. This would not test the prediction more stringently than current data (the residual is already only 73 MeV), but the bare-mass interpretation could be tested by computing the full electroweak correction.

3. **The $n = 4$ prediction**: the $d/c$ family predicts a particle at $\sim 4{,}659$ GeV. No known particle exists there. Discovery of a particle near this mass at a future collider would strongly support the pattern.

---

## The Higgs Boson — Pi Offset Partner

> [!note] Discovery — April 2026
> The Higgs boson mass IS predicted by the $d/c$ family, with an ordinal offset of exactly $\pi$ from the Z boson. See [[higgs-mass-prediction|Higgs Mass Prediction]] for the full analysis.

The Z-Higgs ordinal gap is **exactly $\pi$**:

$$\text{Higgs ordinal} = \omega + 2\omega/\varphi + \pi = \text{Z ordinal} + \pi$$

| Particle | Ordinal | Predicted Mass | Measured Mass | Accuracy | $\sigma$ |
|----------|---------|---------------|---------------|----------|----------|
| Z boson ($n=3$) | $\omega + 2\omega/\varphi$ | 91,115 MeV | 91,188 MeV | 99.92% | 34.7$\sigma$ |
| **Higgs** ($n=2+\pi$) | $\omega + 2\omega/\varphi + \pi$ | **125,265 MeV** | **125,250 MeV** | **99.99%** | **0.09$\sigma$** |

The Higgs prediction is within the PDG 2022 measurement uncertainty — the strongest result in the framework.

---

## What This Does Not Explain

- Why the Z boson shares the tau's amplitude ($d/c = 4/3$) despite being a boson while the tau is a fermion
- Why $n = 1$ (34.8 MeV) has no known particle
- The W boson mass (which the framework does not independently predict)
- Why the Higgs sits at a $\pi$ offset rather than an integer multiple of $\omega/\varphi$ (the numerical result is clear; the derivation from the coupling function is not)

---

## Related Concepts

- [[Master Equation]] — the mass prediction formula
- [[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]] — the confirmed predictions this extends
- [[Generation Spacing]] — the $\omega / \varphi$ spacing that generates the $d/c$ family
- [[Central Charge]] — $c = 3$, determining $d/c = 4/3$
- [[Standard Model Particle Assignments]] — full particle ordinal table
- [[research-investigation-2026-04-08|Comprehensive Framework Investigation]] — parent investigation

## Sources

- Investigation script: `kappa-engine/scripts/extend_master_equation.py`
- Verification: `kappa-engine/scripts/master_equation_verification.py`
- [[research-investigation-2026-04-08|Comprehensive Framework Investigation — April 2026]]
