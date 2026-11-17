# 05 — Jenkursion Transform

Recursive kernel operator from Mike's study of continued fractions and Lentz-style matrix methods for Bessel functions. Mathematically independent of JSC and of the κ coupling function. All three share a surname root; different objects.

## Core kernel

$$K(t, s) = t + \frac{s}{t}, \quad t \neq 0$$

## Recursive definition

$$J_0(t, s) = K(t, s) = t + s/t$$
$$J_n(t, s) = J_{n-1}(K(t, s), s)$$

Explicit expansion:

```
J_1 = t + s/t
J_2 = (t + s/t) + s / (t + s/t)
J_3 = J_2 + s / J_2
```

## Matrix formulation

For matrix applications, two coupled sequences:

```
P[0] = I
Q[0] = 0

P[n] = A ⊗ P[n-1] + B ⊗ Q[n-1]
Q[n] = A ⊗ Q[n-1] + B ⊗ P[n-1]
```

A, B are transformation matrices, ⊗ is matrix multiplication.

Distinction from Lentz / Kacha-Gozeri-Belhroukia matrix continued fractions: the Q equation uses P[n-1] (not P[n-2]). This asymmetric recursion is the novel structural element.

## Properties

### Approximate scale invariance

$$J_n(\lambda t, \lambda s) \approx \lambda \cdot J_n(t, s) \quad \text{as } n \to \infty$$

At n = 1: J_1(λt, λs) = λt + λs/(λt) = λt + s/t. Not exactly λ · J_1(t, s) — the s/t term becomes s/(λt) after rescaling. As recursion deepens, the normalized quantity converges. Verified numerically across scales {1, 10, 100, 1000}.

### Stability region

For s/t² < 1, iterations stay bounded. For s/t² > 1, they diverge. Stable set in the (t, s) plane:

$$\{(t, s) : t > 0, |s/t^2| < 1\}$$

Near-zero t makes s/t² large and blows up. This is why K is not used in JSC — spectral bands near zero would diverge.

### Fractal behavior

Applying J_n in the complex plane (z = x + iy, t = |z|, s = arg z) produces self-similar patterns in |J_n(z)|. Resembles generalized Newton fractal.

### Connection to φ

Iterating K(t, 1) from t₀ = 1 diverges. Iterating fixed-s recursions with other initial conditions produces golden ratio as a limit. Cross-reference with shell-framework motivation for φⁿ spacing.

## Applications

### Continued fractions and Bessel functions

Original motivation. Lentz's method for ratios of Bessel functions uses a matrix continued fraction. Jenkursion variant converges faster on certain complex-plane regions.

### Quantum evolution toy model

P[n] / Q[n] recursion analogous to discrete time-evolution operators. Toy model for self-similar quantum states.

### Heat equation

Recursive generation of self-similar solutions to the 1D heat equation via the matrix sequences.

### Gravitational wave analysis on GWTC-4.0

182 events from GWTC-4.0 analyzed with Jenkursion transformation on mass ratios. Measured quantities:

- 34 of 182 events (18.7%) cluster within a chosen window around φ on mass-ratio distribution
- Scale invariance preservation under Jenkursion transform: 98.4%
- Power-law fit: α ≈ 0.66, R² = 0.929
- One event with M₁ = 137 M☉ (shell 137 candidate)
- One event GW240109 at 0.08% from φ

Null hypothesis in the original analysis is uniform on mass ratios; astrophysical prior is strongly non-uniform, and look-elsewhere corrections are not applied. The p-values quoted in the original write-up are sensitive to both of these. For confirmation-grade claims, re-run with: realistic astrophysical prior, trials correction across shell candidates tried, held-out validation split.

## Distinctions

| Object | Definition | Used where |
|---|---|---|
| Jenkursion kernel K | t + s/t | Matrix continued fractions, toy recursions |
| JSC | Moore-Penrose pseudoinverse of CMF matrix + optional K10 | Prism spectral conversion |
| κ coupling | κ₀ / (1 + β r^γ) · exp(−λ r) | Chronon-GI, shell framework, BRDF |
| κ Frenet | √(5 − 3u) / (1 + u)^(3/2), u = cos²(2t) | Base manifold curvature |
| κ base coupling | 1 / (1 + cos²(2k ln φ)) · exp(−k/φ) | Parameter-free shell coupling from manifold |

All share a surname root. All are different mathematical objects.

## Code

```python
import numpy as np

def jenkursion_scalar(t, s, depth):
    """J_n(t, s) via direct recursion."""
    if depth == 0:
        return t + s / t
    return jenkursion_scalar(t + s / t, s, depth - 1)

def jenkursion_iterative(t, s, depth):
    """Iterative form — safer for large depth."""
    x = t
    for _ in range(depth + 1):
        x = x + s / x
    return x

def jenkursion_matrix(A, B, depth):
    """P[n], Q[n] matrix recursion."""
    I = np.eye(A.shape[0])
    P = I.copy()
    Q = np.zeros_like(A)
    for _ in range(depth):
        P_new = A @ P + B @ Q
        Q_new = A @ Q + B @ P
        P, Q = P_new, Q_new
    return P, Q
```
