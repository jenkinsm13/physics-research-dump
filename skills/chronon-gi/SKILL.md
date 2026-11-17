---
name: chronon-gi
description: Unified light transport using the chronon coupling function κ(r). Use when implementing global illumination, rendering, path tracing, or any light transport system. The coupling function IS the Green's function derived from the Matryoshka-Chronon temporal shell framework—it encodes ALL transport in ONE evaluation. Replaces separate calculations for direct light, indirect bounces, shadows, caustics, SSS, and volumetrics. Triggers on requests for GI implementations, real-time rendering, path tracers, or physically-based light transport.
---

# Chronon-GI: Unified Coupling Transport

## Core Principle

The coupling function κ(r) IS the Green's function derived from the temporal shell framework. It encodes the **equilibrium solution** to light transport—ALL multi-bounce correlation is already baked in.

$$\kappa(r) = \frac{\kappa_0}{1 + \beta r^\gamma} \cdot e^{-\lambda r}$$

This emerges from the shell propagator:
$$c_{ij} = \frac{c_0}{1 + \beta |i-j|^\gamma} \cdot e^{-\lambda \cdot \text{ord}(|i-j|)}$$

For any point P, radiance is:

$$L(P) = \int L_{\text{source}}(Q) \times \kappa(d_{\text{optical}}(P, Q)) \times V(P,Q) \, dQ$$

**One integral. One κ evaluation per path. No iteration.**

## Critical Constraints

**DO NOT:**
- Chain κ×κ for multi-leg paths (double-counts decay)
- Add separate phase terms ($e^{ikr}$) — κ already encodes equilibrium
- Add "bounce" iterations — κ IS the equilibrium solution
- Add wave optics machinery (FFT propagation, Fresnel integrals)
- Confuse refraction (ray direction) with optical distance (coupling strength)

**DO:**
- Trace rays WITH refraction (Snell's law changes direction at interfaces)
- Accumulate optical distance along the refracted path
- ONE κ evaluation per complete path
- Let caustics emerge from refraction geometry + κ weighting
- Let spectral effects emerge from wavelength-dependent λ parameter

## Parameters

| Parameter | Symbol | Default | Role |
|-----------|--------|---------|------|
| Base coupling | κ₀ | 1.0 | Contact coupling strength |
| Power-law amplitude | β | 1.0 | Transition to power-law regime |
| Power-law exponent | γ | 1.5 | 1=Coulomb, 2=dipole |
| Exponential decay | λ | 0.15 | Far-field cutoff rate |

**CFT-derived alternative:** β=0.2, γ=1.0, λ=0.5 produces central charge c≈3.

**Spectral variation:** λ can depend on wavelength for dispersion effects. Materials with λ(λ_light) create chromatic behavior without explicit wave optics.

## Regime Behavior

1. **r → 0:** κ(r) → κ₀ (contact coupling)
2. **β^(-1/γ) ≪ r ≪ λ⁻¹:** κ(r) ≈ κ₀/(βr^γ) (power-law regime)  
3. **r ≫ λ⁻¹:** κ(r) → 0 exponentially (cutoff regime)

The power-law provides **long-range correlation** (color bleeding from distant surfaces). The exponential provides **locality** (eventual cutoff). Pure exponential forces a tradeoff; this form achieves both.

## Why κ Encodes Everything

The coupling function is the **dressed propagator** from the temporal shell framework. It's not a bare 1/r² falloff—it's the solution that already accounts for:

- All orders of scattering between shells
- The equilibrium distribution of energy
- Correlation decay with distance

When you evaluate κ(total_path_length), you're reading off the equilibrium coupling between endpoints. The intermediate bounces are already summed.

## Refraction vs Optical Distance

**These are different things:**

- **Refraction** → changes RAY DIRECTION (Snell's law at interfaces)
- **Optical distance** → changes COUPLING STRENGTH (κ evaluation)

You need both:

1. **Trace the geometric path** with proper refraction (rays bend at interfaces)
2. **Accumulate optical distance** along that path: $d_{optical} = \sum_i n_i \cdot d_{geometric,i}$
3. **Evaluate κ once** on the total optical distance

### Why Both Matter

For a ray passing through a glass sphere:
- Refraction determines the ray EXITS at a different angle than it entered
- Optical distance determines how MUCH the coupling is attenuated

Caustics emerge because:
- Refraction FOCUSES many geometric paths to the same point
- Each path is weighted by κ(its optical length)
- Many paths arriving → large sum → bright caustic

### Implementation

```
1. Trace ray from P in direction D
2. At interface: apply Snell's law, get new direction D'
3. Continue tracing along D'
4. Accumulate: optical_length += segment_length × local_IOR
5. When path complete: contribution = emission × κ(total_optical_length)
```

## Architecture

```
1. Sample ray directions from receiver P
2. Trace ray with REFRACTION (Snell's law at interfaces)
3. Find source point Q (emitter or scatterer that sees light)
4. Compute optical distance along the ACTUAL refracted path
5. Contribution = emission(Q) × κ(optical_distance) × visibility
```

Refraction is geometric (determines path shape). κ is energetic (determines coupling strength).

### Indirect Illumination

For path P → Q → L (receiver ← scatterer ← light):
- Trace P→Q with refraction if passing through media
- Trace Q→L with refraction if passing through media  
- Total optical path = optical(P→Q) + optical(Q→L)
- **Correct:** κ(total_optical_path) — one evaluation
- **Wrong:** κ(optical_PQ) × κ(optical_QL) — double-counts decay

### Caustics

Caustics require knowing WHERE refracted light lands:
1. Trace rays from light through refractive geometry (with Snell's law)
2. Rays bend and potentially focus
3. At receiver P, many paths may arrive from different directions
4. Each path contributes: emission × κ(that_path's_optical_length)
5. Sum is large where paths focus → caustic

The refraction determines the GEOMETRY of focusing. κ determines the STRENGTH of each contribution.

## Materials

Per-material parameters modify how κ behaves:

| Material | λ | Effect |
|----------|---|--------|
| Air | ~0 | No attenuation |
| Glass | 0.01-0.05 | Transparent, refractive |
| Dense media | 0.5+ | Opaque |
| Translucent (SSS) | 0.05-0.1 | Light penetrates |

**Spectral materials:** λ(wavelength) varies → chromatic dispersion without explicit wave optics.
- Skin: λ_red < λ_green < λ_blue (red penetrates deeper)
- Glass: λ varies via Cauchy equation → prismatic separation

## Implementation References

See `references/` for platform-specific guidance:
- `glsl.md` — WebGL/GLSL shaders
- `compute.md` — HLSL/WGSL compute shaders
- `cpu.md` — C++/Rust path tracers

## Common Mistakes

1. **Chaining κ:** Using κ(a) × κ(b) instead of κ(a+b). This double-counts decay.

2. **Adding bounces:** Iterating "bounces" when κ already encodes equilibrium. Creates recursive reflection artifacts.

3. **Separate shadow rays:** Visibility V is binary. κ handles all falloff. Don't multiply by additional distance factors.

4. **Adding phase terms:** Don't bolt on $e^{ikr}$. If wave effects are needed, they emerge from wavelength-dependent parameters, not explicit phase.

5. **Treating κ as 1/r²:** The power-law prefactor is not inverse-square. It's the dressed propagator from shell coupling.
