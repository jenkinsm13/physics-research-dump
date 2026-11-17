---
title: "A Wavefunction Formalism for Photons: Toward a Unified Quantum-Mechanical Description of Light"
author: Michael C. Jenkins
affiliation: Quantum Thoughtworks
created: 2026-04-06
updated: 2026-04-06
tags: [paper, photon, wavefunction, quantum-optics, QED, multi-photon, entanglement]
sources:
  - "raw/Chrotonics/ClaudeCode/framework-documents/PhotonWavefunction.tex"
  - "raw/100-patent-challenge/background/_photon_wavefunction.tex"
---

# A Wavefunction Formalism for Photons: Toward a Unified Quantum-Mechanical Description of Light

**Michael C. Jenkins** -- Quantum Thoughtworks

## Abstract

We present a novel formulation for describing single-photon states within a wavefunction framework. By expressing the photon's state as $\Psi_{\text{photon}}(x,t) = \psi(x)\cdot \tau(t)$ and introducing a corresponding equation of motion $i\hbar \frac{\partial}{\partial t}\Psi_{\text{photon}}(x,t) = (H + T^{(t)})\Psi_{\text{photon}}(x,t)$, we provide a conceptual bridge between the canonical operator formalism of quantum electrodynamics and a more familiar Schrodinger-like picture. We extend this approach to multi-photon states via tensor products, enabling the direct treatment of entanglement and interference within a spatial-temporal wavefunction language.

---

## Motivation

Photons, despite their ubiquity and fundamental importance, lack a direct wavefunction description analogous to that for non-relativistic massive particles. Traditional QFT treats photons as excitations created by field operators on the vacuum. While accurate, this lacks the direct intuition of wavefunction-based approaches.

Key motivations:

1. **Conceptual Unification**: Common language for massless and massive quantum particles
2. **Intuition and Computation**: Direct spatial probability amplitudes simplify multi-photon interference calculations
3. **Link to Experiments**: Detection events are inherently position/time-dependent

---

## Theoretical Framework

### Defining the Photon Wavefunction

$$\Psi_{\text{photon}}(x,t) = \psi(x)\cdot\tau(t)$$

where $\psi(x)$ encodes spatial amplitude distribution and $\tau(t)$ governs time evolution.

### Equation of Motion

$$i\hbar\frac{\partial}{\partial t}\Psi_{\text{photon}}(x,t) = (H + T^{(t)})\Psi_{\text{photon}}(x,t)$$

where:

- $H = \hbar c|\hat{\mathbf{k}}|$ is the free-space Hamiltonian (linear dispersion $\omega = c|\mathbf{k}|$)
- $T^{(t)}$ enforces transversality ($\nabla\cdot\mathbf{E}=0$) and gauge invariance

### Relation to Standard QED

The spatial part relates to standard creation operators via Fourier transform:

$$\boldsymbol{\psi}(x) = \sum_{\lambda}\int \frac{d^3k}{(2\pi)^3} f_{\mathbf{k},\lambda}(x) a^\dagger_{\mathbf{k},\lambda}|0\rangle$$

### Transversality Enforcement

The operator $T^{(t)}$ introduces the transverse projector $\mathcal{P}_\perp = \mathbb{I} - \nabla(\nabla\cdot)^{-1}$:

$$T^{(t)} = i\hbar\frac{\partial}{\partial t}\mathcal{P}_\perp - \mathcal{P}_\perp H$$

This vanishes for already transverse states and corrects any longitudinal components.

### Temporal Relativity Perspective

A speculative "temporal relativity" viewpoint imagines the photon's reference frame as an evolving structure of time itself -- a beating, hourglass-shaped capsule of temporal flow. The photon's propagation is reinterpreted as "stationary" with respect to this dynamically shifting temporal reference, even though it remains forever in motion spatially.

---

## Multi-Photon States

### Tensor Product Structure

Two-photon joint state:

$$\Psi_{\text{total}} = \sum_{i,j} c_{ij}\,\Psi_i(x_i,t_i)\otimes \Psi_j(x_j,t_j)$$

Joint probability:

$$P(x_1,x_2,t_1,t_2) = |\Psi_{\text{total}}(x_1,x_2,t_1,t_2)|^2$$

### Symmetrization (Bosonic)

$$\Psi_{\text{total}}(x_1,x_2,t_1,t_2) = \Psi_{\text{total}}(x_2,x_1,t_2,t_1)$$

This leads naturally to Hong-Ou-Mandel interference and photon bunching.

### Entanglement

$$\Psi_{\text{entangled}}(x_1,x_2,t_1,t_2) = \frac{1}{\sqrt{2}} \left[\Psi_A(x_1,t_1)\Psi_B(x_2,t_2) + \Psi_B(x_1,t_1)\Psi_A(x_2,t_2)\right]$$

---

## Applications

- Linear optical quantum computing and Boson sampling
- Quantum walks of photons
- Error analysis and state characterization in photonic quantum devices

---

## Related Concepts

- [[Matryoshka-Chronon Framework]]
- [[Temporal Shells]]
- [[DivideByZero]]
