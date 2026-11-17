# CMB Power Spectrum vs Kappa Coupling Function

**Date:** 2026-04-06
**Status:** Initial analysis complete
**Related:** [[Scale Invariance of Shell Structure]], [[Kappa Function]], [[Matryoshka-Chronon Framework]]

---

## Motivation

The [[Matryoshka-Chronon Framework]] predicts that the coupling function:

$$\kappa(k) = \frac{1}{1 + \cos^2(2k \cdot \ln\varphi)} \cdot e^{-k/\varphi}$$

governs interactions between nested shells at ALL scales, from subatomic to cosmological. If this is true, the angular correlations measured in the Cosmic Microwave Background (CMB) should reflect the same coupling structure.

This analysis compares the Planck 2018 CMB TT angular power spectrum $D_\ell = \ell(\ell+1)C_\ell / 2\pi$ against $\kappa(k)$ to test this prediction.

## What Was Compared

**CMB Angular Power Spectrum $D(\ell)$:**
- Source: Planck 2018 release (COM_PowerSpect_CMB-TT-full_R3.01)
- 2507 multipoles, $\ell = 2$ to $\ell = 2508$
- Characteristic features: first acoustic peak at $\ell \approx 220$ ($D \approx 5800\ \mu K^2$), damping tail falling to near zero by $\ell \approx 2500$

**Kappa Coupling Function $\kappa(k)$:**
- Zero free parameters (everything derived from $\varphi$)
- Computed for $k = 0.01$ to $k = 200$
- Single prominent resonant peak at $k \approx 1.21$
- Dominated by exponential decay envelope $e^{-k/\varphi}$ with superimposed $\cos^2$ oscillation

## The Unknown: The Mapping Function

The central challenge is that $\kappa(k)$ operates on ordinal separation $k$ (integer distance in the shell chain) while the CMB spectrum operates on multipole moment $\ell$ (angular frequency on the sky). There is no a priori derivation of the mapping $\ell = f(k)$.

Five mapping families were tested:

| Mapping | Form | Free Parameters |
|---------|------|:-:|
| Linear | $\ell = ak + b$ | 2 |
| Logarithmic | $\ell = a\ln(k+1) + b$ | 2 |
| Power law | $\ell = ak^n + b$ | 3 |
| Phi-scaled | $\ell = a\varphi^{k/10} + b$ | 2 |
| Phi-power | $\ell = a\varphi^{k/c} + b$ | 3 |

## Results

### Correlation by Mapping

| Mapping | Pearson $r$ | $p$-value | Points Used | $\ell$ Range |
|---------|:-----------:|:---------:|:-----------:|:------------:|
| Phi-power | **0.990** | $2.5 \times 10^{-35}$ | 42 | 1209--2465 |
| Logarithmic | 0.983 | $1.1 \times 10^{-8}$ | 12 | 1013--2469 |
| Power law | 0.976 | $4.1 \times 10^{-22}$ | 33 | 491--2397 |
| Phi-scaled | 0.790 | $1.5 \times 10^{-51}$ | 236 | 1460--2502 |
| Linear | 0.530 | $2.2 \times 10^{-145}$ | 2000 | 292--905 |

The best-fit mapping is $\ell = 263.5 \cdot \varphi^{k/1.13} + 944.5$ with $r = 0.990$.

### Key Observations

1. **The high correlations are misleading.** The best mappings (phi-power, logarithmic, power law) achieve $r > 0.97$ but use only 12--42 data points out of 2507. They map the small-$k$ regime of $\kappa(k)$ (where the function is monotonically decaying) onto the high-$\ell$ damping tail of the CMB (which is also monotonically decaying). **Two monotonically decreasing functions will always correlate strongly** --- this is not a meaningful physical match.

2. **The acoustic peaks are not reproduced.** The CMB's defining feature --- the series of acoustic peaks at $\ell \approx 220, 546, 800$ --- has no counterpart in $\kappa(k)$. The kappa function has only one detectable resonant peak at $k \approx 1.21$, and the $\cos^2$ oscillation period ($\pi / (2\ln\varphi) \approx 3.26$ in $k$-space) does not match the CMB peak spacing under any tested mapping.

3. **The linear mapping covers the most data but fits worst.** When the full $k$ range maps onto the acoustic peak region ($\ell \approx 290$--$905$), the correlation drops to $r = 0.53$. This is the most honest test, and it shows that the oscillatory structure of $\kappa(k)$ does not match the CMB oscillatory structure.

4. **Peak structure mismatch.** Only 1 kappa peak and 2 CMB peaks were detected with sufficient prominence, making direct peak-position comparison impossible. The CMB has at least 7 well-resolved acoustic peaks; $\kappa(k)$ has effectively one before the exponential decay kills the signal.

### Plots

![[cmb_comparison.png]]
*Top: Planck 2018 CMB TT power spectrum with acoustic peaks marked. Middle: $\kappa(k)$ coupling function showing the single resonant peak and exponential decay. Bottom: Overlay under the best-fit phi-power mapping --- the high correlation comes from matching two decaying functions in the damping tail, not from reproducing the acoustic peak structure.*

![[cmb_peak_analysis.png]]
*Left: $\kappa(k)$ on log scale showing the oscillation superimposed on exponential decay. Right: Peak position correspondence (too few peaks detected for meaningful comparison).*

## Falsifiability Assessment

This comparison **does not constitute a falsifiable prediction** for the following reasons:

1. **The mapping is not predicted.** The framework does not derive $\ell = f(k)$ from first principles. Searching over 5 mapping families with 2--3 free parameters each is curve fitting, not prediction. Any smooth function can be made to correlate with another smooth function given enough mapping freedom.

2. **The physical mechanisms differ fundamentally.** The CMB acoustic peaks arise from baryon-photon fluid oscillations at the sound horizon scale ($\sim 150$ Mpc comoving). The kappa function's oscillation arises from $\cos^2(2k\ln\varphi)$. These are different physical processes with different characteristic scales.

3. **The match is in the wrong region.** The high correlations occur in the damping tail ($\ell > 1000$), where both functions are simply decaying. The physically interesting region --- the acoustic peaks --- is where the match breaks down.

## What This Means for the Framework

**The kappa coupling function in its current form does not predict the CMB angular power spectrum.** This does not necessarily invalidate the Matryoshka-Chronon framework, but it constrains how the framework might connect to cosmological observables:

- If $\kappa(k)$ governs inter-shell coupling, the CMB power spectrum may not be a direct observable of that coupling. The CMB integrates over the entire photon-baryon interaction history, not just pairwise shell coupling.
- The framework might need a **transfer function** analogous to the standard cosmological transfer function that converts primordial power spectrum to observed $C_\ell$. The raw $\kappa(k)$ would then be an input to such a calculation, not a direct prediction of $D(\ell)$.
- Alternatively, $\kappa(k)$ might manifest in the **primordial power spectrum** $P(k)$ rather than the angular power spectrum $C(\ell)$. Testing against the reconstructed primordial spectrum would be a different (and potentially more appropriate) comparison.

## Next Steps

1. **Derive the mapping from first principles.** If the framework predicts $\kappa(k)$ appears at cosmological scales, it must specify HOW ordinal separation maps to angular scale. This is the critical missing piece.
2. **Compare against the primordial power spectrum** rather than the processed $C(\ell)$. The primordial spectrum has fewer acoustic features and might be a more natural comparison target.
3. **Test the oscillation period.** The kappa function predicts oscillations with period $\Delta k = \pi/(2\ln\varphi) \approx 3.26$. Does any cosmological observable show oscillations at a $\varphi$-related frequency?
4. **Compute the CMB spectrum FROM the framework.** Rather than matching $\kappa(k)$ to $D(\ell)$ directly, use $\kappa(k)$ as an input to a Boltzmann solver (like CAMB or CLASS) and compute the predicted $C(\ell)$. This would be a genuine prediction.

## Data and Code

- Script: `kappa-engine/scripts/cmb_comparison.py`
- Planck data: `kappa-engine/data/planck_tt_spectrum.txt`
- Results JSON: `kappa-engine/output/cmb_comparison_results.json`
- Run: `uv run --with numpy --with matplotlib --with scipy scripts/cmb_comparison.py`
