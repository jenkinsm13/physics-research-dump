---
title: "The Fragility of Temporal Coherence in Quantum Systems"
author: Michael C. Jenkins
created: 2026-04-06
updated: 2026-04-06
tags: [paper, temporal-coherence, quantum-entanglement, IBM-quantum, temporal-inequality, decoherence, dividebyzero]
sources:
  - "raw/LaTeX/photon-wavefunction/dividebyzero/examples/temporal-inequality.tex"
  - "raw/100-patent-challenge/dividebyzero/examples/temporal-inequality.tex"
---

# The Fragility of Temporal Coherence in Quantum Systems: Experimental Evidence and Implications

## Abstract

This paper investigates temporal coherence in quantum systems, focusing on how delays between successive circuit executions influence time-like quantum correlations. Using IBM quantum backends, we demonstrate that even minor interruptions degrade measured temporal entanglement, quantified by a custom temporal inequality metric $K$. These results provide experimental evidence for the fragility of time-like coherence and suggest that quantum temporal correlations depend on unbroken temporal continuity.

## Temporal Inequality Metric

$$K = Q_{\text{avg}}^2 - Q_{\text{avg}}$$

where $Q_{\text{avg}}$ is the average expectation value of a binary observable measured across different temporal pressures.

A standard Leggett-Garg inequality was also tested:

$$K_{\text{LG}} = C_{12} + C_{23} + C_{34} - C_{14}$$

## Key Results

| Condition | $K$ Value | $Q_{\text{avg}}$ |
|-----------|:---------:|:-----------------:|
| Continuous execution | $-0.25$ (strong) | ~0.96 |
| Interrupted execution | $-0.04$ (weak) | ~0.90 |

The decay is exponential, consistent with decoherence times ($T_1$, $T_2$) of the backend qubits.

## Implications

- **Time as substrate**: When time is treated as continuous flow, the system retains coherence. Fragmenting time disrupts quantum correlations.
- **Quantum neural networks**: Preserving unbroken temporal flow in QNN architectures could enhance robustness for time-dependent tasks.
- **Philosophical**: Supports the [[Matryoshka-Chronon Framework]] view of time as a fundamental substrate for quantum correlations.

---

## Related Concepts

- [[DivideByZero]]
- [[Temporal Shells]]
- [[Matryoshka-Chronon Framework]]
- [[Chronons]]
