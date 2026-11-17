# 06 — COTV (Call-of-Void) Potential

Double-Gaussian radial potential. Generates Standard Model fermion masses as bound-state eigenenergies of the radial Schrödinger equation in this potential.

## Form

$$W_{\text{void}}(r) = -V_1 \exp\left(-\frac{(r - R_1)^2}{2\sigma_1^2}\right) + V_2 \exp\left(-\frac{(r - R_2)^2}{2\sigma_2^2}\right)$$

Six parameters per particle: V₁, R₁, σ₁, V₂, R₂, σ₂.

- **Attractive Gaussian (−V₁):** gravitational-like attraction at R₁
- **Repulsive Gaussian (+V₂):** short-range core preventing collapse; analog of zero-point repulsion
- **Equilibrium:** bound state at the radial position where forces balance

## Mass-COTV identity

Two descriptions of the same phenomenon at different scales.

**Matryoshka paper:** mass causes shell distortions
$$\Delta r_i(x) = -\frac{G m}{c^2} \cdot \frac{1}{|x - x_m|} \cdot e^{-\lambda |i - i_m|}$$

**Chronon framework:** the distortion is the COTV potential

Attractive component shows up macroscopically as gravitational mass. Repulsive component shows up as zero-point / quantum pressure.

Emergent mass integral over the manifold:
$$m \propto \int_\mathcal{M} (V_1 \sigma_1^3 - V_2 \sigma_2^3) \, d\mathcal{M}$$

## Fermion mass fitting

### Procedure

1. Solve the radial Schrödinger equation
   $$\psi''(r) + \tfrac{2}{r}\psi'(r) + 2[E - W_{\text{void}}(r)]\,\psi(r) = 0$$
   via shooting method from r = 0 outward.
2. Scan E for bound states (asymptotic ψ(r → ∞) = 0).
3. Optimize six COTV parameters with Nelder-Mead to match the observed mass: |E_bound| c² = M_obs c².
4. Loss: L = [ln(M_calc) − ln(M_obs)]². Log because masses span four orders of magnitude (electron 0.511 MeV to bottom 4180 MeV).
5. Convergence: L < 10⁻¹⁰.

### Initial guess

$$V_1 \approx 2 M_{\text{obs}}, \quad R_1 \approx 1, \quad \sigma_1 \approx 0.5$$
$$V_2 \approx M_{\text{obs}}, \quad R_2 \approx 0.5, \quad \sigma_2 \approx 0.1$$

Natural units, ℏ = c = 1.

### Outcome

Convergent fits for nine fermions: electron, up quark, down quark, strange quark, muon, charm quark, tau lepton, bottom quark.

Non-convergent: top quark (173.1 GeV). Nelder-Mead does not find parameters producing a stable bound state at that mass. Two candidate explanations — (a) top is at or above a stability limit inherent to the COTV form; (b) Nelder-Mead is local and the fit may exist in an unexplored region of parameter space.

### Claimed shell positions from fits

- Electron: ordinal ~24
- Muon: ordinal ~63
- Tau: ordinal ~102

Positions are outputs of the fit, not independent predictions.

## Toroidal geometry argument

Separate structural claim: toroidal topology of the shell structure forces half-integer spin representations via spin-statistics, implying Fermi-Dirac statistics:

$$\{\Psi_\alpha(x), \Psi_\beta^\dagger(y)\} = \delta_{\alpha\beta}\delta^3(x - y)$$

The "toroidal topology imposes causality" step is load-bearing.

## Relation to κ

COTV is not κ. Different object:

- **κ(r):** transport strength between shells as function of separation
- **COTV W(r):** potential energy well at a specific shell with bound states inside

They interact: κ determines how the COTV-induced distortion propagates to nearby shells, creating the effective mass field that other particles feel as gravity. Full model requires both.

## Dark-sector extensions

Proposed mechanisms in the same framework:

**Dark matter** — excitations in dark shells with suppressed coupling to SM shells:
$$c_{DM-SM} = c_{\text{normal}} \cdot e^{-\xi (i-j)^2}$$
Gaussian suppression in ordinal distance. Mass scale estimate ~1 TeV.

**Dark energy** — vacuum energy in the depletion shell at ordinal ~291. Gives Λ ≈ 1.1 × 10⁻⁵² m⁻², within ~18% of observed.

## Code

```python
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

def cotv_potential(r, V1, R1, sig1, V2, R2, sig2):
    return -V1 * np.exp(-(r - R1)**2 / (2 * sig1**2)) \
           + V2 * np.exp(-(r - R2)**2 / (2 * sig2**2))

def radial_rhs(r, y, E, params):
    """y = [ψ, ψ']. Radial Schrödinger in natural units."""
    psi, dpsi = y
    if r < 1e-9:
        r = 1e-9
    W = cotv_potential(r, *params)
    d2psi = -2.0/r * dpsi + 2.0 * (W - E) * psi
    return [dpsi, d2psi]

def shoot(E, params, r_max=20.0):
    r_span = (1e-3, r_max)
    sol = solve_ivp(radial_rhs, r_span, [1e-6, 0.0],
                    args=(E, params), t_eval=np.linspace(*r_span, 2000),
                    rtol=1e-10, atol=1e-12)
    return sol.y[0, -1]

def find_bound_E(params, E_range=(-10, 0), steps=200):
    """Scan for zero-crossing of asymptotic ψ. Bisect to refine."""
    Es = np.linspace(E_range[0], E_range[1], steps)
    vals = np.array([shoot(E, params) for E in Es])
    crossings = np.where(np.diff(np.sign(vals)))[0]
    if len(crossings) == 0:
        return None
    idx = crossings[0]
    # bisection refinement
    lo, hi = Es[idx], Es[idx+1]
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if shoot(mid, params) * shoot(lo, params) < 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)

def fit_mass(M_obs):
    def loss(params):
        E = find_bound_E(params)
        if E is None:
            return 1e6
        M_calc = abs(E)
        return (np.log(max(M_calc, 1e-12)) - np.log(M_obs))**2
    guess = [2*M_obs, 1.0, 0.5, M_obs, 0.5, 0.1]
    return minimize(loss, guess, method='Nelder-Mead',
                    options={'xatol': 1e-10, 'fatol': 1e-10, 'maxiter': 50000})
```
