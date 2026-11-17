# 01 — Base Manifold

## The curve

$$\mathbf{r}(t) = \left(\sin t,\; \tfrac{1}{2}\sin 2t,\; \cos t\right)$$

### Constraint surfaces

- Unit cylinder: x² + z² = sin²t + cos²t = 1.
- Hyperbolic paraboloid: y = ½ sin 2t = sin t · cos t = x · z.
- The curve is (cylinder) ∩ (saddle). Closed, topologically S¹, figure-eight in projection to the xz-plane.

### Cardinal points

t ∈ {0, π/2, π, 3π/2}: r = (0,0,1), (1,0,0), (0,0,-1), (-1,0,0). All on the unit sphere.

t ∈ {π/4, 3π/4, 5π/4, 7π/4}: |y| = 1/2, distance √5/2 from origin.

## Derivatives

$$\mathbf{r}'(t) = (\cos t,\; \cos 2t,\; -\sin t)$$
$$\mathbf{r}''(t) = (-\sin t,\; -2\sin 2t,\; -\cos t)$$

### Speed squared

$$|\mathbf{r}'|^2 = \cos^2 t + \cos^2 2t + \sin^2 t = 1 + \cos^2 2t$$

With u = cos(2t), this is 1 + u². Already has the structure of a κ denominator: 1/(1 + β u^γ) with β = γ = 1.

### Cross product

$$\mathbf{r}' \times \mathbf{r}'' = \big(-\cos t(1 + 2\sin^2 t),\; \mathbf{1},\; -\sin t(1 + 2\cos^2 t)\big)$$

Middle component is identically 1. Binormal y-component is constant across the whole curve.

### Cross product magnitude

$$|\mathbf{r}' \times \mathbf{r}''|^2 = 2 + 3\sin^2 2t = 5 - 3\cos^2 2t$$

## Frenet-Serret

With u = cos²(2t):

$$\kappa_{\text{Frenet}}(t) = \frac{\sqrt{5 - 3u}}{(1 + u)^{3/2}}$$

$$\tau_{\text{Frenet}}(t) = \frac{-3\cos(2t)}{5 - 3u}$$

### Ranges

- κ ∈ [1/2, √5]. Min at u = 1 (cardinal points). Max at u = 0 (saddle peaks).
- τ vanishes at u = 0 (where κ peaks). |τ| is max at u = 1.

### Complementarity

κ and τ are strictly complementary. Max bending-in-plane coincides with zero twisting. Max twisting coincides with min bending.

### Period doubling

Both depend on cos(2t). Period π, not 2π. Curvature/torsion complete two cycles per parametric period.

## Factorization

$$\kappa_{\text{Frenet}}(t) = \underbrace{\frac{1}{(1 + \cos^2 2t)^{3/2}}}_{\text{bare propagator}} \times \underbrace{\sqrt{5 - 3\cos^2 2t}}_{\text{source modulation}}$$

Bare propagator is κ(r) with β = 1, γ = 2, r = cos(2t), λ = 0. Source modulation is the cross-product magnitude — intrinsic deviation from geodesic.

Full transport:

$$\kappa_{\text{transport}}(r) = \kappa_{\text{manifold}}(t) \cdot e^{-\lambda r}$$

Geometry provides oscillating base. Material provides exponential decay.

## √3 discrepancy

Hand-derived version has √(15 − 9 cos²(2t)) in the numerator = √3 × √(5 − 3 cos²(2t)). Candidate explanations:

1. Algebra slip that doubled a factor.
2. Geodesic curvature on a specific surface or norm of second fundamental form.
3. √(dim) = √3 normalization to Riemannian norm.

The √3 is a constant multiplier on κ₀. Functional form unchanged.

## Frenet frame export

```typescript
interface FrenetFrame {
  position:  [x, y, z];
  tangent:   [x, y, z];  // T = r' / |r'|
  normal:    [x, y, z];  // N = T' / |T'|
  binormal:  [x, y, z];  // B = T × N, y-component always > 0
  curvature: number;     // κ(t)
  torsion:   number;     // τ(t)
}
```

## Figure-eight projection

Projecting along y gives a figure-eight in the xz-plane. Crossings at t = π/2 and t = 3π/2 where y = 0 and (x, z) repeats.

## Ordinal sampling

Sample at t_k = k · ln φ, k ∈ ℤ₊:

$$u_k = \cos^2(2 k \ln\varphi)$$

$$c(k) = \frac{1}{1 + \cos^2(2 k \ln\varphi)} \cdot e^{-k/\varphi}$$

Parameter-free. Both constants derived from φ.

### Self-coupling

c(0) = 1/(1 + 1) = 1/2. Base manifold never reaches coupling 1.

### Resonant peaks

cos(2k ln φ) = 0 at k ln φ = π/4 + nπ/2:

- k₁ = π/(4 ln φ) ≈ 1.631
- k₂ = 3π/(4 ln φ) ≈ 4.893
- k₃ = 5π/(4 ln φ) ≈ 8.155
- k₄ = 7π/(4 ln φ) ≈ 11.418

At these separations the oscillatory factor hits local max above the exponential envelope. Coupling is not monotone in ordinal distance.

## Numerical constants

| Constant | Value |
|---|---|
| φ | 1.6180339887 |
| ln φ | 0.4812118251 |
| 1/φ | 0.6180339887 |
| c(0) | 0.5 |
| k₁ | 1.6310 |
| k₂ | 4.8930 |
| k₃ | 8.1550 |
| κ_Frenet min | 0.5 |
| κ_Frenet max | √5 ≈ 2.2361 |

## Code

```python
import numpy as np

PHI = (1 + np.sqrt(5)) / 2
LN_PHI = np.log(PHI)

def curve(t):
    return np.array([np.sin(t), 0.5*np.sin(2*t), np.cos(t)])

def kappa_frenet(t):
    u = np.cos(2*t)**2
    return np.sqrt(5 - 3*u) / (1 + u)**1.5

def tau_frenet(t):
    u = np.cos(2*t)**2
    return -3*np.cos(2*t) / (5 - 3*u)

def c_shell(k):
    return 1.0 / (1 + np.cos(2*k*LN_PHI)**2) * np.exp(-k/PHI)
```

```glsl
float kappa(float k) {
    float u = cos(2.0 * k * 0.4812118);
    return 1.0 / (1.0 + u*u) * exp(-k * 0.6180340);
}
```
