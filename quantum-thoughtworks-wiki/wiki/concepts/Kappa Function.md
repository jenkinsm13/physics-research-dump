---
title: Kappa Function
created: 2026-04-06
updated: 2026-04-06
tags: [core-theory, physics, rendering, mathematics]
sources: ["[[Chronon Flux GI]]", "[[Matryoshka-Chronon Framework]]"]
---

# Kappa Function

The kappa function `kappa(r)` is the **coupling function** that describes how [[Chronons|chronon flux]] decays between two points separated by distance `r`. It is central to both the theoretical physics and the rendering applications of the [[Matryoshka-Chronon Framework]].

## Definition

**Exact form (with resonance structure):**

$$\kappa(k) = \frac{1}{1 + \cos^2(2k \ln\varphi)} \cdot \exp\!\left(-\frac{k}{\varphi}\right)$$

This has two components:
- **Resonance term** $\frac{1}{1 + \cos^2(2k \ln\varphi)}$ -- creates periodic peaks where shells couple strongly
- **Decay envelope** $\exp(-k/\varphi)$ -- exponential falloff scaled by the [[Golden Ratio]]

**General form (simplified):**
`kappa(r) = kappa_0 / (1 + beta * r^gamma) * exp(-lambda * r)`

**Scale-invariant form (used in rendering):**
`kappa(r) = exp(-alpha * r)`

## Why Exponential?

The exponential form is not arbitrary -- it is the **unique solution** forced by requiring scale invariance in the flux field:

If `Phi(lambda*p, lambda*t) = lambda^Delta * Phi(p, t)`, then the coupling must satisfy `kappa(lambda*r) = kappa(r)^lambda`, whose only continuous solution is the exponential.

![[calibration_pattern.png]]
*Calibration pattern showing kappa coupling decay across shell distances.*

## Role in Physics

Kappa encodes the equilibrium solution for all inter-shell interactions:
- **Gravity**: Emerges from gradients in the kappa field
- **Quantum entanglement**: Described by kappa coupling between shells
- **Information transfer**: Bounded by kappa decay rates

## Role in Rendering

In [[Chronon Flux GI]], kappa serves as the **Green's function for light transport**. One kappa evaluation per path replaces all traditional rendering computations:

| Traditional | Kappa Replaces |
|------------|---------------|
| Direct lighting | Single kappa evaluation |
| Indirect illumination | Already encoded |
| Caustics | Emergent from kappa |
| Subsurface scattering | Distance-weighted kappa |
| Ambient occlusion | Local shell density via kappa |

This is the key insight of the [[Chronon Flux GI]] project: correct physics produces correct images as a byproduct.

## Parameters

| Parameter | Symbol | Effect |
|-----------|--------|--------|
| Shell Scale | `alpha` | Coupling decay rate (high = tight/sharp, low = soft/spread) |
| Base Coupling | `kappa_0` | Maximum coupling strength |
| Power Index | `gamma` | Controls near-field behavior |
| Exponential Decay | `lambda` | Far-field falloff rate |

## Scale Invariance

The kappa function governs coupling at **every scale** -- from electron orbitals to galaxy clusters. The same $\cos^2$ resonance peaks that organize Standard Model particles also produce bokeh rings in camera lenses and acoustic peaks in the CMB. See [[Scale Invariance of Shell Structure]] for the full cross-scale analysis and [[Optical Shell Equivalence]] for the optics connection.

## Fine-Structure Constant

The fine-structure constant emerges directly from the ratio of nearest-neighbor to self-coupling: $\alpha = \kappa(1)^2 / (4\pi \cdot \kappa(0)^2) \approx 1/137.04$. See [[Fine-Structure Constant Derivation]].

## Related Concepts

- [[Chronon Flux GI]]
- [[Temporal Shells]]
- [[Chronons]]
- [[OpenPBR Implementation]]
- [[Scale Invariance of Shell Structure]]
- [[Optical Shell Equivalence]]
- [[Standard Model Particle Assignments]]
- [[Fine-Structure Constant Derivation]]
- [[Kappa Engine Cosmos]]
- [[dimensional-emergence-from-kappa-coupling|Dimensional Emergence from Kappa Coupling]]

## Sources

- `raw/Chrotonics/flux-splatting/chronon-flux-gi/README.md`
- `raw/Chrotonics/flux-splatting/README.md`
- Kappa-engine: `~/Projects/kappa-engine/src/kappa.rs`
