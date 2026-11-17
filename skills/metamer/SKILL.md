---
name: metamer
description: Michael C. Jenkins' unified research corpus — the κ (kappa) coupling function, the base manifold r(t)=(sin t, sin(2t)/2, cos t), Matryoshka-Chronon temporal shells, Jenkins Spectral Conversion (JSC), the Jenkursion transform, Call-of-Void (COTV) potential, and applications across spectral rendering, photometric stereo, shell-model turbulence, and power electronics. Load whenever the user mentions κ, kappa, Matryoshka-Chronon, JSC, Jenkursion, COTV, BP-REX, temporal shells, chronons, golden-ratio shells, or references "the framework" in a physics/rendering context. Load for any work on Prism Shaders or κ-sim.
---

# Metamer

Working reference for the κ framework and everything built on it. The base manifold, the coupling function, its derivation chain, the shell structure, the spectral conversion pipeline, and the applications.

A metamer is a stimulus that matches another despite different underlying composition. The organizing observation: light transport, angular scattering, turbulent cascades, ceramic glaze color, and power converter efficiency are the same mathematical object under different labels. This skill is the reference for that object.

## The one object

$$\kappa(r) = \frac{\kappa_0}{1 + \beta r^\gamma} \cdot e^{-\lambda r}$$

Derived from the Frenet curvature of:

$$\mathbf{r}(t) = \left(\sin t,\; \tfrac{1}{2}\sin 2t,\; \cos t\right)$$

The curve is the intersection of the unit cylinder x² + z² = 1 with the hyperbolic paraboloid y = xz. A closed figure-eight in projection, riding a saddle on a cylinder. From |r'|² = 1 + cos²(2t) the bare κ kernel emerges directly.

Sampled at golden-ratio ordinal spacing t_k = k · ln φ, with exponential decay at rate 1/φ, the manifold produces a parameter-free shell coupling:

$$c(k) = \frac{1}{1 + \cos^2(2k \ln\varphi)} \cdot e^{-k/\varphi}$$

Zero free parameters. This is the canonical form. Everything else in applied work is a coordinate transform of this onto a specific domain.

## Reference map

Load the file relevant to the task. Files are independent.

- `01-base-manifold.md` — the curve, Frenet apparatus, curvature/torsion, figure-eight topology, derivation of the bare kernel from |r'|². Load first when the question is "where does κ come from."
- `02-kappa-function.md` — the function itself, regime behavior, parameter meanings, the various parameter sets in circulation and where each came from.
- `03-shell-framework.md` — Matryoshka-Chronon shells, φⁿ scaling, ordinal distance, the coupling matrix, c ≈ 3 from entanglement entropy on 60 shells.
- `04-jsc.md` — Jenkins Spectral Conversion. Three DX12 variants. Moore-Penrose pseudoinverse. K10 kernel. 81 bands, 380–780 nm.
- `05-jenkursion.md` — the K(t,s) = t + s/t recursion. Matrix formulation. Scale invariance. Connection to continued fractions and Bessel.
- `06-cotv.md` — Call-of-Void double-Gaussian potential. Fermion mass fitting procedure. The mass ≡ COTV potential identity.
- `07-applications.md` — Prism spectral sky and materials, photometric stereo with κ BRDF, ceramic mode, chronon-GI, shell-model turbulence, CMB/GW overlays, BP-REX, unified κ-sim architecture.

## Variable `r` across domains

The single most common confusion. `r` in κ(r) is whatever scalar the application's coupling depends on; that scalar is different in different domains. State the transform explicitly.

| Domain | `r` is |
|---|---|
| Base manifold | cos(2t) or u = cos²(2t), dimensionless |
| Shell coupling | ordinal distance \|i − j\|, dimensionless integer |
| Chronon-GI | optical distance ∫ n(s) ds along refracted path, meters |
| BRDF | angular deviation θ or sin θ, radians |
| CMB | multipole moment ℓ or log ℓ |
| Gravitational waves | log mass ratio or log frequency |
| BP-REX | time offset or phase offset within switching cycle |

## Don't

- Chain κ(a) · κ(b) for a two-leg path. Use κ(a + b). Chaining double-counts decay.
- Add explicit phase terms e^(ikr). κ is a dressed propagator; equilibrium is encoded.
- Add bounce iterations. κ is the equilibrium solution, not a single-scatter kernel.
- Substitute a smooth monotonic function for the oscillatory form 1/(1 + cos²(2k ln φ)). The oscillations are the base manifold's signature and produce resonant orbits at k ≈ 1.63, 4.89, 8.16.
- Use the Jenkursion kernel K(t,s) = t + s/t inside JSC. K diverges for small t. JSC uses the Moore-Penrose pseudoinverse. They share a name root; they are different objects.

## Key constants

- φ = (1 + √5)/2 ≈ 1.6180339887
- ln φ ≈ 0.4812118251
- 1/φ ≈ 0.6180339887
- Self-coupling c(0) = 1/2 (not 1 — base manifold never reaches coupling 1.0)
- Resonant peaks: k ≈ π/(4 ln φ) ≈ 1.631, then 4.893, 8.155, …
- Frenet κ range: [1/2, √5]
- JSC bands: 81 at 5 nm spacing, 380–780 nm
