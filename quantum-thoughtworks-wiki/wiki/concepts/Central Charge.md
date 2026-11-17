---
title: Central Charge
created: 2026-04-07
updated: 2026-04-07
tags: [core-theory, physics, mathematics, dimensionality]
sources: ["[[Matryoshka-Chronon Framework]]", "[[Kappa Function]]"]
---

# Central Charge

The central charge `c` is the effective dimensionality that emerges from the eigenvalue spectrum of the [[Kappa Function|coupling matrix]] in the [[Matryoshka-Chronon Framework]]. It converges to approximately 3 as the number of [[Temporal Shells]] increases, corresponding to the three spatial dimensions of our universe.

## Definition

Given `N` shells coupled by the [[Kappa Function]], construct the `N x N` coupling matrix `C[i][j] = kappa(|i - j|)` and compute its eigenvalues `{lambda_k}`. The central charge is extracted via von Neumann entropy of the positive eigenvalue distribution:

```
p_i = lambda_i / sum(lambda)        (positive eigenvalues only)
S   = -sum(p_i * ln(p_i))           (von Neumann entropy)
c   = 3 * S / ln(N)
```

The factor of 3 in the definition normalizes `c` so that a perfectly uniform distribution of 3 dominant eigenvalues yields `c = 3`. The `ln(N)` denominator ensures `c` is independent of system size in the large-`N` limit.

## Convergence

The central charge converges to 3 from below as `N` increases:

| N (shells) | c |
|-----------|---|
| 10 | ~2.5 |
| 20 | ~2.76 |
| 40 | ~2.93 |
| 60 | ~2.98 |
| 80 | ~3.00 |
| 100+ | ~3.00 |

This convergence is a computational verification of the framework's core claim: the [[Kappa Function]] — derived from a base manifold with zero free parameters — produces a coupling structure whose intrinsic dimensionality is 3. Three spatial dimensions are not assumed; they emerge from `kappa`.

## Physical Meaning

The coupling function `kappa(k) = 1/(1 + cos^2(2k*ln(phi))) * exp(-k/phi)` has two components:

1. **Resonance structure** (`1/(1 + cos^2(...))`) — creates periodic peaks of strong coupling
2. **Exponential decay** (`exp(-k/phi)`) — suppresses long-range coupling

This combination produces an eigenvalue spectrum with exactly 3 dominant eigenvalues that carry most of the spectral weight. In the language of the framework: the coupling between shells naturally organizes into 3 independent "directions" — these become the three spatial dimensions.

The von Neumann entropy measures how many independent modes carry significant weight. When `c = 3`, exactly three modes dominate — which is why the top 3 eigenvectors of the coupling matrix provide a stable 3D embedding for shell positions (see [[cosmogenesis-visualizer|Cosmogenesis Visualizer]]).

## Connection to Spacetime Dimension

The central charge gives the number of spatial dimensions:

```
c = 3     (spatial dimensions)
d = c + 1 = 4  (spacetime dimensions, assuming one time dimension)
```

The only assumption beyond the framework is `d = c + 1` — that there is exactly one temporal dimension. Everything else is derived.

## Connection to Mass Predictions

The [[amplitude-coefficient-derivation|amplitude coefficient discovery]] revealed that the two previously-fitted parameters in the [[Master Equation]] are determined by `c` and `d`:

```
alpha_mu = d = 4
alpha_tau = d/c = 4/3
```

The ratio of the two amplitude coefficients equals the central charge:

```
alpha_mu / alpha_tau = d / (d/c) = c = 3
```

Measured from the actual lepton masses: `4.0433 / 1.3297 = 3.04`, within 1.4% of 3. This means the central charge — independently computed from the eigenvalue spectrum of the coupling matrix — governs the mass hierarchy of leptons. Two "fitted" parameters reduce to a single quantity that the framework derives.

## Connection to Cosmogenesis

In the [[cosmogenesis-visualizer|cosmogenesis visualizer]], the central charge serves as the "trigger" for the emergence of space. The visualization shows:

1. Shells accumulate on a 1D line (only first eigenvector active)
2. The `c` readout climbs as more shells couple
3. When `c >= 2.95`, the unfolding threshold is reached
4. The second and third eigenvector axes activate
5. The 1D chain lifts into 3D — space emerges

The threshold `c >= 2.95` (rather than exactly 3) allows the visualization to show unfolding before perfect convergence, representing the physical claim that dimensionality emerges gradually.

## Relationship to Conformal Field Theory

The name "central charge" is borrowed from conformal field theory (CFT), where the central charge `c` characterizes the number of degrees of freedom of a 2D conformal field theory. In the Matryoshka framework, the analogy is precise: the central charge characterizes the number of emergent spatial degrees of freedom of the shell coupling system. However, the computation method differs — here it comes from eigenvalue entropy rather than the Virasoro algebra.

## Related Concepts

- [[Matryoshka-Chronon Framework]] — parent theory
- [[Kappa Function]] — the coupling function whose eigenvalue spectrum produces `c`
- [[Temporal Shells]] — the shells whose coupling defines the matrix
- [[Master Equation]] — mass predictions that depend on `c` and `d = c + 1`
- [[amplitude-coefficient-derivation|Amplitude Coefficient Derivation]] — discovery that `alpha_mu/alpha_tau = c`
- [[cosmogenesis-visualizer|Cosmogenesis Visualizer]] — real-time computation and display of `c`
- [[Ordinal Depth]] — particle shell positions within the coupling structure
- [[Generation Spacing]] — the `omega/phi` jump between generations, derived from the same framework
- [[dimensional-emergence-from-kappa-coupling|Dimensional Emergence from Kappa Coupling]] — the landmark result: full eigendecomposition data from N=2 to N=120

## Computational Verification

The central charge computation is implemented and tested in:
- `/Users/jenkinsm/Projects/noosphere/src/lib/simulation/coupling.ts` — `computeCentralCharge()` function
- `/Users/jenkinsm/Projects/noosphere/src/lib/simulation/coupling.test.ts` — numerical verification
