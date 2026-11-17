---
title: "Investigation Status: 2026-04-07"
created: 2026-04-07
updated: 2026-04-07
tags: [meta, status, original-research]
sources: ["[[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]]", "[[quark-mass-exploration|Quark Mass Exploration]]"]
status: active-investigation
---

# Investigation Status: 2026-04-07

## What Was Confirmed

- **The mass predictions are independently verified.** Three particle masses (muon, tau, top quark) predicted from the electron mass with zero fitted parameters at 98.93%, 99.73%, and 99.87% accuracy. The numbers are real and reproducible.
- **The derivation chain is traceable:** manifold → κ → ω → Δi → mass. Each step follows from the previous.
- **The central charge c extrapolates to 3.02 ± 0.006** from the coupling matrix eigenvalue spectrum. Consistent with c = 3.
- **Three eigenvalues dominate at particle-physics scales** (N ~ 100), consistent with three spatial dimensions emerging from the coupling.
- **The amplitude coefficient ratio alpha_mu/alpha_tau = c** was discovered computationally. This reduced two fitted parameters to zero.
- **The top quark mass formula m_top = m_e × exp(40/π)** was discovered. The simplest prediction in the framework — no amplitude correction, just the exponential.

## What Was Challenged

- **No spectral gap at large N.** Dimensional emergence is scale-dependent, not absolute. The three dominant eigenvalues don't separate from the rest by a gap — they are smoothly the largest.
- **φ is not special for eigenvalues** — any scaling base produces similar coupling matrices with similar eigenvalue spectra. But φ IS critical for the mass predictions via ω/φ generation spacing. The golden ratio matters for ordinal geometry, not for the eigendecomposition itself.
- **V_void helps the spectral gap but not entropy-based c.** The von Neumann entropy formula `c = 3S/ln(N)` may not be the right metric for extracting dimensionality. The formula gives the right answer (c ~ 3) but the derivation path is debatable.
- **Down-type quarks are unpredicted.** Down (4.67 MeV), strange (93.4 MeV), bottom (4,180 MeV) masses do not fit any clean framework expression. This is an honest failure.
- **Koide formula not automatically satisfied.** The 1% muon residual (predicted 204.6 vs measured 206.8) breaks the Koide relation Q = 2/3 when using predicted rather than measured masses. The Koide formula and the Master Equation are not automatically consistent.
- **CMB direct comparison fails.** Comparing κ(k) to the CMB power spectrum C(ℓ) requires a Boltzmann transport solver (CLASS or CAMB), not simple curve fitting. The mapping ℓ(k) cannot be found by visual overlay — it requires computing the full transfer function through a cosmological model.

## The Open Frontier

The mass predictions work. The question is: **are they a deep truth or an elaborate coincidence?**

The derivation chain from a specific base manifold through κ to ω = 20π to particle masses is either the most important result in theoretical physics or a remarkable numerical accident.

**The way to distinguish:** extend to more particles. If the framework can predict the W, Z, Higgs, and charm masses with the same accuracy, coincidence becomes untenable. If it can't, the three predictions might be numerology.

### Specific Next Steps

1. **W boson mass** (80,370 MeV): can the Master Equation predict it? What ordinal depth and amplitude?
2. **Z boson mass** (91,188 MeV): same question. W and Z are related by the weak mixing angle — the framework should predict both consistently.
3. **Higgs boson mass** (125,250 MeV): the Higgs is the mass-giving mechanism in the Standard Model. If the shell framework predicts its mass from geometry, that's a direct challenge to the Standard Model's Higgs mechanism.
4. **Charm quark** (1,270 MeV): the suggestive 94.8% match at Δi = 2ω/φ should be investigated further. A small amplitude correction might bring it to 99%+.
5. **Down-type quarks**: the hardest problem. May require incorporating QCD/color charge into the shell architecture.

### What Would Make This Conclusive

- **5+ correct predictions at >99% accuracy** from one framework with zero parameters would be extremely difficult to dismiss as coincidence.
- **A single wrong prediction** that clearly contradicts measurements would falsify the specific ordinal depth assignment and constrain the framework.
- **Prediction of an unmeasured quantity** (e.g., a more precise top quark mass that future LHC data confirms) would be the gold standard.

## Files

- [[zero-parameter-mass-predictions|Zero-Parameter Mass Predictions]] — the publication-candidate paper
- [[amplitude-coefficient-derivation|Amplitude Coefficient Derivation]] — alpha = d and d/c
- [[quark-mass-exploration|Quark Mass Exploration]] — quark analysis and negative results
- [[cosmogenesis-visualizer|Cosmogenesis Visualizer]] — interactive demonstration
- All code: `~/Projects/noosphere/`
