# 02 — The κ Coupling Function

## Canonical form

$$\kappa(r) = \frac{\kappa_0}{1 + \beta r^\gamma} \cdot e^{-\lambda r}$$

Rational prefactor × exponential envelope. This is the Green's function / dressed propagator structure.

## Parameter roles

| Symbol | Role |
|---|---|
| κ₀ | Contact coupling. Value at r = 0. |
| β | Power-law onset. Crossover scale from contact to algebraic. |
| γ | Power-law exponent. 1 = Coulomb-like, 2 = dipole-like. |
| λ | Exponential decay rate. Inverse correlation length. |

## Regime structure

Separated by scales β^(−1/γ) and 1/λ.

**Contact (r → 0):** κ → κ₀.

**Power-law (β^(−1/γ) ≪ r ≪ 1/λ):** κ ≈ κ₀ / (β r^γ). Algebraic long-range correlation.

**Cutoff (r ≫ 1/λ):** κ → 0 exponentially. Locality.

Combination of power-law and exponential gives long-range correlation with eventual truncation. Pure exponential lacks correlation; pure power-law diverges integrals.

## Parameter sets in active use

### Set A — Bare manifold

κ₀ = 1/2, β = 1, γ = 2, λ = 0, r = cos(2t).

Direct reading of 1/(1 + cos²(2t)) from the Frenet curvature denominator. No exponential because this is the pure manifold.

### Set B — Ordinal sampled with golden-ratio decay

κ₀ = 1/2, β = 1, γ = 2, λ = 1/φ, r = cos(2k ln φ).

Gives c(k) = 1/(1 + cos²(2k ln φ)) · exp(−k/φ). Parameter-free. Both constants from φ.

### Set C — CFT extraction (linearized)

κ₀ = 1, β = 0.2, γ = 1, λ_ord = 0.5.

60-shell matrix with this coupling, entanglement entropy S(ℓ) = (c/3) ln(ℓ) + const yields c ≈ 2.94 ± 0.03, R² = 0.9999. Smoothed linear envelope of Set B that discards the oscillation.

### Set D — Cosmological constant

α = 0.8, λ_ord = 0.125 = 1/8, N = 291 shells, β_global = 5×10⁵⁸.

Reproduces observed Λ to within ~18%. λ_ord = 1/8 from octave symmetry argument. Mapping to Set B's λ = 1/φ not written in closed form.

### Set E — Chronon-GI rendering defaults

κ₀ = 1.0, β = 1.0, γ = 1.5, λ = 0.15.

Ranges used in working v5–v8: β ∈ [0.3, 2.5], γ ∈ [1.0, 2.5], λ ∈ [0, 120]. Material-dependent.

### Set F — BRDF fit on photometric data

Single-tile fit example: κ₀ free, β = 19.71, γ = 0.80, λ = 13.18.

Large β and λ reflect the Jacobian of the ordinal-to-angular coordinate transform. On MERL database, κ with 4 fitted parameters wins 99.9% of materials over GGX; mean RMS 0.3469 vs 0.3922.

## `r` across domains

| Domain | `r` is | Units |
|---|---|---|
| Bare manifold | cos(2t) or u = cos²(2t) | dimensionless |
| Shell coupling | \|i − j\| | dimensionless integer |
| Chronon-GI | ∫ n(s) ds along refracted path | meters |
| BRDF | θ or sin θ | radians |
| CMB | multipole ℓ | dimensionless |
| GW | log mass or log frequency | dimensionless |
| BP-REX | time / phase offset | seconds / radians |

## Constraints

### Single evaluation per path

For path P → Q → R with optical lengths a and b, use κ(a + b), not κ(a) · κ(b). Chaining multiplies decay factors and double-counts.

### No explicit phase

κ is a dressed propagator. Phase is encoded. Additional e^(ikr) double-counts.

### No bounce iteration

κ is the equilibrium solution. Iterating "bounces" on top creates recursive artifacts.

### Oscillatory form is structural

1/(1 + cos²(2k ln φ)) has local maxima at k ≈ 1.63, 4.89, 8.16. Smoothing to monotonic decay removes the manifold signature and the resonant orbits. Keep the oscillation in layout physics and anywhere resonance structure matters.

## Wavelength dependence

λ = λ(λ_light) produces chromatic behavior from a single scalar per wavelength.

| Material | λ(wavelength) |
|---|---|
| Air | λ ≈ 0 |
| Clearcoat | λ nearly constant across visible (IOR 1.50–1.55) |
| Glass | Cauchy dispersion, λ rises toward blue |
| Skin | λ_red < λ_green < λ_blue |
| Dense media | λ ≥ 0.5 |
| Translucent (SSS) | λ ∈ [0.05, 0.1] |

## Code

```python
import numpy as np

def kappa(r, kappa0=1.0, beta=1.0, gamma=1.5, lam=0.15):
    return kappa0 / (1 + beta * np.power(np.abs(r), gamma)) * np.exp(-lam * np.abs(r))

def kappa_base(k):
    PHI = (1 + np.sqrt(5)) / 2
    return 1.0 / (1 + np.cos(2*k*np.log(PHI))**2) * np.exp(-k/PHI)
```

```glsl
float kappa(float r) {
    return 1.0 / (1.0 + pow(r, 1.5)) * exp(-0.15 * r);
}

// Set B — bare manifold
float kappa_base(float k) {
    float u = cos(2.0 * k * 0.4812118);
    return 1.0 / (1.0 + u*u) * exp(-k * 0.6180340);
}
```

```hlsl
float kappa(float r, float kappa0, float beta, float gamma, float lam) {
    return kappa0 / (1.0 + beta * pow(abs(r), gamma)) * exp(-lam * abs(r));
}
```
