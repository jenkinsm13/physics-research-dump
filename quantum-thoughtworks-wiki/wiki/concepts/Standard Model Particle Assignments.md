---
title: Standard Model Particle Assignments
created: 2026-04-06
updated: 2026-04-08
tags: [core-theory, physics, standard-model, particles, derivation, mass-prediction]
sources: ["[[Matryoshka-Chronon Framework]]", "[[Kappa Function]]", "[[Kappa Engine Cosmos]]", "[[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]]", "[[z-boson-prediction|Z Boson Prediction]]", "[[research-investigation-2026-04-08|Comprehensive Framework Investigation]]"]
---

# Standard Model Particle Assignments

In the [[Matryoshka-Chronon Framework]], every Standard Model particle is a **standing wave mode** (spherical harmonic $Y_l^m$) at a specific [[Ordinal Depth]] in the [[Temporal Shells|shell hierarchy]]. Particles are not point-like objects with arbitrary quantum numbers -- they are resonant excitations of the shell structure, and their properties (mass, spin, generation) are determined entirely by their ordinal address and angular momentum mode.

## Particle Table

### Leptons (Charged)

| Particle | Ordinal | $l$ | Mass (MeV) | Generation |
|----------|---------|-----|------------|------------|
| Electron ($e^-$) | 24 | 1 | 0.511 | 1st |
| Muon ($\mu^-$) | 63 | 2 | 105.66 | 2nd |
| Tau ($\tau^-$) | 102 | 3 | 1,776.86 | 3rd |

### Quarks (Up-type)

| Particle | Ordinal | $l$ | Mass (MeV) | Generation |
|----------|---------|-----|------------|------------|
| Up ($u$) | 20 | 1 | 2.16 | 1st |
| Charm ($c$) | 55 | 2 | 1,270 | 2nd |
| Top ($t$) | 95 | 3 | 172,760 | 3rd |

### Quarks (Down-type)

| Particle | Ordinal | $l$ | Mass (MeV) | Generation |
|----------|---------|-----|------------|------------|
| Down ($d$) | 22 | 1 | 4.67 | 1st |
| Strange ($s$) | 58 | 2 | 93.4 | 2nd |
| Bottom ($b$) | 98 | 3 | 4,180 | 3rd |

### Bosons

| Particle | Ordinal | $l$ | Mass (MeV) |
|----------|---------|-----|------------|
| $W^\pm$ | 88 | 1 | 80,379 |
| $Z^0$ | 90 | 1 | 91,188 |
| $H^0$ (Higgs) | 92 | 0 | 125,100 |

### Neutrinos

| Particle | Ordinal | $l$ | Mass (MeV) |
|----------|---------|-----|------------|
| $\nu_e$ | 110 | 1 | ~0.000001 |

## Generation Structure

The angular momentum quantum number $l$ increases with generation:

| Generation | $l$ | Particles |
|-----------|-----|-----------|
| 1st | 1 | electron, up, down |
| 2nd | 2 | muon, charm, strange |
| 3rd | 3 | tau, top, bottom |

This means particles are literally **spherical harmonic modes** at specific radial depths. First-generation particles are $l=1$ dipole modes, second-generation are $l=2$ quadrupole modes, third-generation are $l=3$ octupole modes. The generation spacing in ordinal depth is $\Delta i = \omega/\varphi \approx 38.83$, as derived in [[Ordinal Depth]].

> [!note] Why three generations
> There are exactly three generations because the shell structure supports exactly three geometric regimes relative to the correlation length $\omega \approx 20\pi \approx 62.83$: finite ($i < \omega$), critical ($i \sim \omega$), and transfinite ($i > \omega$). A fourth generation would require a fourth geometric regime, which the shell mathematics does not admit.

## Mass Predictions from the Master Equation

> [!warning] Correction (April 2026)
> The $\varphi^{39}$ mass ratio formula documented previously was an early approximation. The correct formula is the [[Master Equation]], which derives absolute mass predictions (not just ratios) with zero free parameters. See [[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]] for the full derivation.

### The Master Equation

$$\frac{m}{m_e} = \alpha \cdot \exp\!\left(\frac{\Delta}{\pi^2}\right)$$

where $\Delta$ is the ordinal depth separation from the electron, $\pi^2$ is the inverse mass-coupling constant, and $\alpha$ is a regime-dependent amplitude coefficient derived from the [[Central Charge]] $c = 3$ and spacetime dimension $d = c + 1 = 4$.

### Confirmed Predictions

| Particle | $\alpha$ | $\Delta$ | Predicted | Measured | Accuracy |
|----------|----------|----------|-----------|----------|----------|
| Muon | $d = 4$ | $\omega/\varphi$ | 104.53 MeV | 105.66 MeV | **98.93%** |
| Tau | $d/c = 4/3$ | $2\omega/\varphi$ | 1,781.7 MeV | 1,776.9 MeV | **99.73%** |
| Top | $1$ | $2\omega$ | 172.99 GeV | 172.76 GeV | **99.87%** |

The muon residual of 1.07% is explained by QED self-energy corrections — the Master Equation predicts **bare masses**. After QED correction, the muon accuracy improves to 99.91%. See [[research-investigation-2026-04-08|Comprehensive Framework Investigation]].

### Z Boson Candidate

| Particle | $\alpha$ | $\Delta$ | Predicted | Measured | Accuracy |
|----------|----------|----------|-----------|----------|----------|
| Z boson | $d/c = 4/3$ | $3\omega/\varphi$ | 91,115 MeV | 91,188 MeV | **99.92%** |

The Z boson uses the tau's amplitude at the next integer multiple of $\omega/\varphi$. See [[z-boson-prediction|Z Boson Prediction]] for details.

### The $d/c$ Family

The tau and Z boson form a family sharing $\alpha = d/c = 4/3$ at integer $n$ multiples of $\omega/\varphi$:

$$m_n / m_e = \frac{4}{3} \cdot \exp\!\left(\frac{n \cdot \omega/\varphi}{\pi^2}\right)$$

| $n$ | Mass | Particle |
|-----|------|----------|
| 2 | 1,781.7 MeV | Tau (99.73%) |
| 3 | 91,115 MeV | Z boson (99.92%) |
| 4 | 4,659 GeV | (prediction) |

### Amplitude Coefficients

| Regime | $\alpha$ | Derivation | Particles |
|--------|----------|------------|-----------|
| Critical ($i \sim \omega$) | $d = 4$ | Spacetime dimension | Muon |
| Transfinite ($i > \omega$) | $d/c = 4/3$ | Dimension ratio | Tau, Z boson |
| Pure ($i = 2\omega$) | $1$ | No correction | Top quark |

Key identity: $\alpha_\mu / \alpha_\tau = 4 / (4/3) = 3 = c$. The amplitudes differ by exactly the central charge.

### Ordinal Clustering (April 2026)

Quarks and leptons cluster in ordinal space:

- **Strange $\leftrightarrow$ Muon**: 1.22 shells apart
- **Charm $\leftrightarrow$ Tau**: 3.31 shells apart
- **W/Z/Higgs/Top**: tight cluster at ordinals $\sim$142--150
- **Z--Higgs separation**: $\approx \pi$ ($0.993\pi$)

> [!warning] Honest Boundary
> Down-type quarks (down, strange, bottom), the W boson, and the Higgs are NOT predicted by the current framework. Systematic searches can achieve $>99\%$ for any particle with sufficiently ad hoc parameters, but this is likely overfitting. The framework's genuine predictive domain is leptons + top quark + possibly Z boson. See [[research-investigation-2026-04-08|Comprehensive Framework Investigation]].

## Particles as Spherical Harmonics

Since particles are $Y_l^m$ modes at specific ordinal depths, they can be visualized as **displacement-mapped spheres**. The Noosphere web visualizer renders these using custom GLSL vertex shaders:

- $l=1$ modes (1st generation): dipole distortion of the sphere (like a peanut)
- $l=2$ modes (2nd generation): quadrupole distortion (like a clover)
- $l=3$ modes (3rd generation): octupole distortion (more complex lobed structure)

The $m$ quantum number within each $l$ distinguishes particles within a generation (e.g., $m$ values separate up-quark from down-quark within $l=1$).

## Computational Verification

The [[Kappa Engine Cosmos]] visualizer computes these assignments at startup:

1. Constructs the $N \times N$ coupling matrix from the $\kappa$ function
2. Performs eigendecomposition (Jacobi eigensolver) to extract 3D positions from the eigenvectors
3. Maps eigenvalues to particle masses via the ordinal-to-mass relation
4. Logs all mass ratio predictions for verification

Key observation: in **exact $\kappa$ mode** ($\kappa_\text{exact}$ with the $\cos^2$ resonance term), particles line up more neatly in the eigenvector embedding than in general $\kappa$ mode. The resonance structure of the exact function organizes the eigenspace -- the periodic $\cos^2$ peaks create preferred positions that correspond to physical particle ordinals.

## Relationship to Higgs Mechanism

In the standard formulation, the Higgs field gives particles mass through spontaneous symmetry breaking. In the shell framework, the Higgs boson at ordinal 92 ($l=0$) is the **radial breathing mode** of the shell system -- the unique spherically symmetric ($l=0$) excitation that couples to all other modes. Its mass (125.1 GeV) is determined by its ordinal position, not by a free parameter.

The Higgs ordinal of 92 sits between the $Z^0$ (90) and top quark (95), consistent with its role as a mediator between the electroweak sector and the heaviest fermion.

## Related Concepts

- [[Matryoshka-Chronon Framework]] -- parent theory
- [[Ordinal Depth]] -- the ordinal address system
- [[Kappa Function]] -- shell coupling that determines mass ratios
- [[Master Equation]] -- the zero-parameter mass prediction formula
- [[Central Charge]] -- $c = 3$ determining amplitude coefficients
- [[Generation Spacing]] -- the universal $\omega / \varphi$ spacing
- [[Scale Invariance of Shell Structure]] -- same structure at all scales
- [[Fine-Structure Constant Derivation]] -- $\alpha$ from $\kappa$ coupling ratios
- [[Temporal Shells]] -- the shell hierarchy
- [[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]] -- confirmed mass predictions
- [[z-boson-prediction|Z Boson Prediction]] -- Z boson candidate
- [[research-investigation-2026-04-08|Comprehensive Framework Investigation]] -- April 2026 investigation
- [[standard-model-implementations]] -- Python implementations (SymPy)
- [[tts-tower]] -- numerical mass-mixing fitting
- [[Kappa Engine Cosmos]] -- Rust/wgpu cosmos visualizer with particle mode

## Open Questions

- Can the full CKM and PMNS mixing matrices be derived from the coupling between quark/neutrino ordinal positions?
- What determines the specific ordinal of the Higgs (92) from first principles?
- Are there predictions for particles beyond the Standard Model at higher ordinals?
- Can the $m$ quantum number assignments be derived rather than inferred?
- Is there a unified amplitude formula generating $\alpha = d$, $d/c$, and $1$ from a single expression?
- Why does the Z boson (a boson) share the tau's (a fermion) amplitude $d/c = 4/3$?
- Can QCD color factors explain the quark-lepton ordinal clustering?
- Does the $d/c$ family's $n = 4$ prediction (4,659 GeV) correspond to a real particle?

## Sources

- Kappa-engine cosmos visualizer: `~/Projects/kappa-engine` -- `cosmos/particles.rs`
- [[Ordinal Depth]] -- generation spacing derivation
- [[standard-model-implementations]] -- `higgs_mechanism.py`, `matryoshka_part3.py`
