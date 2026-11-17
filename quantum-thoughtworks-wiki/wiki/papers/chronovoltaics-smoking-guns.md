---
title: "Chronovoltaics Smoking Guns"
created: 2026-04-06
updated: 2026-04-06
tags: [paper, chronovoltaics, experimental-evidence, validation]
sources: ["[[Chronovoltaics]]"]
---

# Chronovoltaics -- Smoking Gun Evidence

Three decisive, reproducible signatures that **time-structure is converted to work**. This evidence package accompanies the [[chronovoltaics-nobel-paper]] and is distributed as a self-contained repo with code, data, and figures.

## The Three Laws

![[plot1_W_vs_C_orders.png]]
*Ordering law: delivered work $W_{\text{out}}$ vs commutator-mass proxy $\mathcal{C}$ across ordering choices.*

### 1. Ordering Law
Delivered work $W_{\text{out}}$ rises with the commutator-mass proxy $\mathcal{C}$, and forward points sit above reverse across ordering choices.

![[plot2_dW_vs_Ipred.png]]
*Information law: chrono gain vs predictive information across input families.*

### 2. Information Law
Chrono gain $W_{\text{out}} - W_0$ increases with predictive information $I_{\text{pred}}$ across input families (AR, chirps, mixtures, noise).

![[plot3_Rtau_vs_R_two_chains.png]]
*Limit law: rectification $\mathcal{R}_\tau$ vs truncation radius R for two cofinal chains.*

### 3. Limit Law
Rectification $\mathcal{R}_\tau$ grows with truncation radius $R$ and diverges for two cofinal chains, isolating the $\omega$-signal.

![[plot4_W_decomposition.png]]
*Work decomposition: $W_{\text{BCH}}$, $W_{\text{chrono}}$, and $W_\omega$ contributions isolated by ablation.*

## Numerical Results (Reference Run)

| Metric | Value |
|--------|-------|
| Base $W_{\text{out}}$ (forward, increasing) | 112,871,344.440 arb. units |
| $I_{\text{pred}}$ (Gaussian MI) | 0.0081 nats |
| $W_{\text{BCH}}$ | 5,476.734 |
| $W_{\text{chrono}}$ | 101,375,564.857 |
| $W_\omega$ | 424,377.083 |

## Statistical Details (from `smoking_guns_summary.json`)

### Order Sensitivity
- Spearman $\rho = -0.921$ ($p = 1.6 \times 10^{-15}$), confirming strong ordering dependence
- Mean gap: 400.74

### Predictive MI (5 families)
- Families tested: AR(0.6), AR(0.85), AR(0.97), chirp, mixed
- $\Theta = 3.74 \times 10^{-8}$ (chrono-voltage)
- Spearman $\rho = 0.6$ ($p = 0.28$) -- directional but small sample

> [!warning] Expanded Predictive MI
> The expanded 12-family test ($\Theta = -1.84 \times 10^{-7}$, $\rho = 0.224$, $p = 0.48$) and the "strong" variant ($\Theta = -35.49$, $\rho = 0.0$) show weaker or null results at larger scale. This is an area requiring further investigation.

### Omega Signal
- Slope: $1.71 \times 10^{-7}$ with $R \in [6, 54]$
- Fraction positive: 88.9% (8/9 sign wins, $p = 0.020$)
- Permutation $p = 0.064$ -- marginally significant

## Version History

Three zip versions exist (`chronovoltaics_smoking_guns.zip`, `2.zip`, `3.zip`). All contain the same structure with identical summary JSON, differing only in plot regeneration timestamps.

## Related Articles

- [[Chronovoltaics]] -- concept overview
- [[chronovoltaics-nobel-paper]] -- formal theory
- [[chronovoltaics-digital-twins]] -- twin implementations that generate this data

## Sources

- `raw/SBIR:QT/SMOKING_GUN.md`
- `raw/SBIR:QT/chronovoltaics_smoking_guns*.zip` (3 versions)
- `raw/SBIR:QT/smoking_guns_summary.json`
- `raw/SBIR:QT/metrics_cv.txt`
