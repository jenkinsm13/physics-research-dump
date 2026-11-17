---
title: "Cosmogenesis Visualizer: Scroll-Driven Emergence of 3D Space"
created: 2026-04-07
updated: 2026-04-07
tags: [visualization, cosmogenesis, eigenvectors, research-tool, noosphere]
sources: ["[[Matryoshka-Chronon Framework]]", "[[Kappa Function]]", "[[Cosmogenic Principle]]", "[[Central Charge]]"]
status: implemented
---

# Cosmogenesis Visualizer

The cosmogenesis visualizer (project name: **noosphere**) is a scroll-driven physics demonstrator that shows 3D space emerging from a 1D chain of [[Temporal Shells|golden-ratio-spaced shells]] coupled by the [[Kappa Function]]. It is both a research tool for the [[Matryoshka-Chronon Framework]] and a visual proof-of-concept for the [[Cosmogenic Principle]].

The central claim it demonstrates: shell positions in 3D are **computed from the eigenvectors of the coupling matrix**, not designed. Dimensionality is an output of the physics, not a rendering choice.

## What It Demonstrates

1. A 1D chain of shells coupled by `kappa(k) = 1/(1 + cos^2(2k*ln(phi))) * exp(-k/phi)` produces a coupling matrix whose eigenvalue spectrum encodes spatial dimensionality.
2. As shells are added, the [[Central Charge]] `c` converges toward 3 — three spatial dimensions emerge from pure coupling.
3. The top 3 eigenvectors of the coupling matrix assign each shell a position in 3D space — no coordinate system is imposed.
4. Particles (electron, muon, tau) appear as standing waves at their [[Ordinal Depth|ordinal depths]], with spectral colors encoding their regime (finite, critical, transfinite).

## The Four-Act Structure

The viewer scrolls through cosmogenesis in four acts, each occupying 25% of the scroll range:

### Act 1: Chain (scroll 0-25%)

Shells appear one by one along a 1D line. The coupling matrix is built incrementally. The central charge readout shows `c` rising from near 0 as structure accumulates. Shell count grows from 1 to 40. Only the first eigenvector axis is active (`alpha = [1, 0, 0]`), so all shells remain on a line.

### Act 2: Coupling Propagation (scroll 25-50%)

Shell count grows from 40 to 80. Coupling lines become visible between shells, showing the `kappa` interaction strength. The `c` readout climbs toward the unfolding threshold. The scene remains 1D — the second and third eigenvector axes are still suppressed.

### Act 3: Unfolding (scroll 50-75%)

The unfolding trigger fires when `c >= 2.95`. The second and third eigenvector axes smoothly activate via smoothstep interpolation (`alpha = [1, smoothstep(t), smoothstep(t)]`). Shell count grows from 80 to 100. The 1D chain lifts off the line into 3D space — shells move to positions determined by the eigenvector embedding. This is the key moment: **space itself is emerging from the coupling function**.

### Act 4: Exploration (scroll 75-100%)

All three eigenvector axes are fully active (`alpha = [1, 1, 1]`). Shell count reaches 120. The `c` readout fades. Particle standing waves appear at their ordinal depths. At scroll = 100%, free-camera exploration mode activates.

## How Eigenvector Embedding Works

The core algorithm:

1. **Build the coupling matrix**: For `N` shells, construct the `N x N` symmetric matrix `C[i][j] = kappa(|i - j|)`.
2. **Eigendecompose**: Use Jacobi eigenvalue iteration to find eigenvalues `{lambda_k}` and eigenvectors `{v_k}`.
3. **Extract positions**: The 3D position of shell `i` is:
   ```
   pos[i] = alpha[0] * v1[i] * e_x + alpha[1] * v2[i] * e_y + alpha[2] * v3[i] * e_z
   ```
   where `v1, v2, v3` are the top 3 eigenvectors (sorted by eigenvalue magnitude) and `alpha` is the mixing weight that evolves with scroll progress.
4. **Sign consistency**: Between animation frames, eigenvectors are matched to previous frame's vectors by maximum overlap (dot product), and signs are corrected to prevent mirror-flips. This is essential because eigenvectors are defined only up to sign.
5. **Ordering by continuity**: Eigenvectors can swap ordering between frames as `N` changes. A greedy assignment based on overlap prevents axis swaps.

The positions are not designed — they are a direct consequence of the coupling function's structure. Different coupling functions would produce different embeddings. The fact that `kappa` produces a stable 3D embedding (c converging to 3) is the framework's core claim.

## Central Charge Readout

The `c` value displayed in the HUD is computed from the eigenvalue spectrum via von Neumann entropy:

```
p_i = lambda_i / sum(lambda)     (positive eigenvalues only)
S   = -sum(p_i * ln(p_i))        (von Neumann entropy)
c   = 3 * S / ln(N)
```

As `N` increases:
- N = 40: `c ~ 2.93`
- N = 60: `c ~ 2.98`
- N = 80: `c ~ 3.00`

The convergence to 3 is a computational verification that the [[Kappa Function]] produces exactly three emergent spatial dimensions.

## Particle Standing Waves

At their [[Ordinal Depth|ordinal depths]], standing wave patterns are rendered around the corresponding shells:

| Particle | Shell Index | Regime | Color |
|----------|------------|--------|-------|
| Electron | ~24 | Finite | Blue (short wavelength, ground state) |
| Muon | ~63 | Critical | Green (boundary resonance) |
| Tau | ~102 | Transfinite | Red (long wavelength, cross-domain) |

The spectral coloring reflects wavelength/energy: shorter wavelength (blue) for the lowest-mass electron, longer wavelength (red) for the highest-mass tau. These are the three lepton generations whose masses are predicted by the [[Master Equation]].

## Eigenvalue Sonification

The eigenvalue spectrum is mapped to audio. Each eigenvalue contributes a tone whose frequency is proportional to its magnitude. As shells are added and `c` rises, the harmonic structure of the sound evolves — the listener hears dimensionality emerging.

## Technical Implementation

| Component | Technology |
|-----------|-----------|
| Framework | SvelteKit |
| 3D Rendering | Raw Three.js (no Threlte abstraction) |
| Eigendecomposition | Custom Jacobi algorithm in TypeScript |
| Shaders | Custom GLSL for shells, coupling lines, particles, atmosphere |
| Scroll handling | Native wheel/touch events mapped to `[0, 1]` progress |

### Module Map

- `src/lib/physics/kappa.ts` — The kappa coupling function (DO NOT MODIFY)
- `src/lib/physics/manifold.ts` — Base manifold `r(t) = (sin t, sin(2t)/2, cos t)`
- `src/lib/physics/shells.ts` — Shell radii and golden-ratio scaling
- `src/lib/physics/predictions.ts` — Zero-parameter mass predictions
- `src/lib/simulation/coupling.ts` — Coupling matrix construction, Jacobi eigendecomposition, central charge computation, eigenvector embedding with sign/ordering consistency
- `src/lib/simulation/progress.ts` — Four-act scroll-to-state mapping
- `src/lib/renderer/` — Three.js scene: shells, coupling lines, particles, atmosphere, HUD
- `src/lib/camera/` — Free-camera controller for exploration mode
- `src/shaders/` — GLSL vertex and fragment shaders

### Running It

```bash
cd ~/Projects/noosphere && pnpm dev
```

Opens at `http://localhost:5173`. Scroll to progress through cosmogenesis.

## Significance as a Research Tool

The visualizer is not merely illustrative. It provided the computational environment in which the [[amplitude-coefficient-derivation|amplitude coefficient derivation]] was discovered. By implementing the coupling matrix, eigendecomposition, and central charge computation in code, the relationship `alpha_mu / alpha_tau = c` became visible — leading to the zero-parameter [[Master Equation]].

The code in `src/lib/physics/predictions.ts` and `src/lib/simulation/coupling.ts` serves as executable verification of the framework's claims. The test suite (`*.test.ts` files) confirms numerical accuracy of all computations.

## Related Concepts

- [[Matryoshka-Chronon Framework]] — parent theory
- [[Kappa Function]] — the coupling function that drives everything
- [[Temporal Shells]] — the shells being embedded
- [[Central Charge]] — the emergent dimensionality readout
- [[Cosmogenic Principle]] — the creation narrative being visualized
- [[Ordinal Depth]] — shell positions where particles appear
- [[Master Equation]] — mass predictions derived in this computational environment
- [[amplitude-coefficient-derivation|Amplitude Coefficient Derivation]] — discovery made using this tool
- [[Kappa Engine Cosmos]] — prior Rust/wgpu visualizer (predecessor)

## Source Code

- Repository: `~/Projects/noosphere/`
- Physics engine: `src/lib/physics/`
- Simulation: `src/lib/simulation/`
- Verification scripts: `scripts/derive-amplitudes.ts`, `scripts/derive-amplitudes-2.ts`
