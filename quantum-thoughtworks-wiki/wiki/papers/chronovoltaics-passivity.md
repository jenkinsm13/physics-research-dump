---
title: "Chronovoltaics Passivity Paper"
created: 2026-04-06
updated: 2026-04-06
tags: [paper, chronovoltaics, passivity, energy-conservation]
sources: ["[[Chronovoltaics]]"]
---

# Predictive Control for Energy Harvesting from Temporally Correlated Sources: A Passivity-Based Framework

This paper provides the rigorous energy conservation proof for [[Chronovoltaics]], ruling out any violation of conservation laws. It establishes that chronovoltaic devices **time the intake of externally supplied energy** -- they do not create energy from nothing.

## Key Results

### System Model

A plant with switching modes $\sigma(t) \in \{1, \dots, M\}$:
$$\dot{x}(t) = A_{\sigma(t)} x(t) + b\,u(t), \quad y(t) = c^\top x(t)$$
where every $A_i$ is Hurwitz. A latched diode connects a resistive load $R > 0$ when forecasts indicate favorable future output. Per-switch energy cost: $\varepsilon > 0$.

### Global Energy Balance (Main Theorem)

For any $T > 0$:
$$\boxed{W_{\text{out}} + E_{\text{ctrl}} \le E_{\text{in}} + V_{\sigma(0)}(x(0))}$$

This proves that the sum of output work and control energy never exceeds input energy plus initial storage. If $u \equiv 0$ and $x(0) = 0$, then $W_{\text{out}} = E_{\text{ctrl}} = 0$ -- the device cannot generate energy without source input.

### Passivity Certificate

For each mode $i$, Lyapunov functions $V_i(x) = \frac{1}{2}x^\top P_i x$ with $P_i \succ 0$ satisfy:
$$A_i^\top P_i + P_i A_i \preceq -Q_i$$

Storage jumps at mode switches are covered by the control budget: $E_{\text{ctrl}} \ge \Sigma_{\text{jump}}$.

### Predictive Gating Algorithm

An implementable predictive latch that converts forecast skill into higher harvested work while staying within the input energy budget:
1. Compute score $s_t = \hat{y}_{t+h}$ from kernel ridge predictor (random Fourier features)
2. Latch on if $g(t^-) = 0$ and $s_t > \theta_{\text{on}}$
3. Latch off if $g(t^-) = 1$ and $s_t < \theta_{\text{off}}$

### Experimental Validation

Work uplift $\Delta W = W_{\text{out}}^{(\text{pred})} - W_{\text{out}}^{(\text{base})}$ is monotonically increasing with forecast AUC across diverse input families (AR, chirps, mixtures, noise). Every run's energy ledger satisfies the balance inequality within numerical tolerance.

## Significance

This paper is the **thermodynamic safety proof** for chronovoltaics. It demonstrates:
- Information shapes **when** to absorb energy; it does not **create** energy
- Gains arise from reduced chatter and better alignment with future-positive intervals
- Nonlinear plants fit the same passivity template with storage beyond quadratic

## Related Articles

- [[Chronovoltaics]] -- concept overview
- [[chronovoltaics-nobel-paper]] -- companion theory paper
- [[chronovoltaics-digital-twins]] -- C1P/C1R implementations

## Sources

- `raw/SBIR:QT/chronovoltaics_passivity_paper.zip`
