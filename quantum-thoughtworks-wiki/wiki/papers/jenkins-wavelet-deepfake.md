---
title: "Summarizing the Jenkins Transform for Wavelet-Based Deepfake Detection"
author: David Stump ASC BVK, Johnathan Banta, Michael C. Jenkins
created: 2026-04-06
updated: 2026-04-06
tags: [paper, jenkins-transform, deepfake-detection, wavelet, continued-fractions, stochastic-analysis]
sources:
  - "raw/LaTeX/jenkins-wavelet.tex"
---

# Summarizing the Jenkins Transform for Wavelet-Based Deepfake Detection

**David Stump ASC BVK, Johnathan Banta, Michael C. Jenkins**

## Overview

This paper explores using the [[Jenkins Transform]] for [[Deepfake Detection|deepfake detection]] through several complementary approaches.

## The Jenkins Transform

$$\mathcal{J}[f](x) = \int_V f(v)g(x, v) \, dv$$

Key properties: linearity, invertibility (under certain conditions), high-dimensional/high-speed computation capability.

## Detection Approaches

### 1. Wavelet-based Kernel Design

**Conjecture.** There exists a Jenkins Transform kernel $g^*$ based on a mother wavelet $\psi_\lambda$ such that $\mathcal{J}[I](x, y) > \tau$ iff $I$ is AI-generated.

### 2. Continued Fraction Representation

**Conjecture.** The Jenkins Transform can be expressed as continued fraction approximations of pixel values, with statistical properties distinguishing natural vs. AI-generated images.

### 3. Matrix Continued Fraction Formulation

**Theorem (Stability with Induced p-Norms).** If submatrices $\{A_i\}$ from the kernel satisfy $\|A_i\|_p \leq \tau_p$ and image perturbation $\|\Delta\|_p < \epsilon_p$, the output variation is bounded by $f_p(\epsilon_p, \tau_p) \to 0$ as $\epsilon_p \to 0$.

### 4. Stochastic Representation

**Proposition.** $\mathcal{J}[I]$ can be represented as a stochastic process $\{X(t), t \in \mathbb{R}^2\}$ capturing local transform behavior.

### 5. Topological Analysis and Persistent Homology

Topological features of the transformed image space provide additional discriminative power.

---

## Related Concepts

- [[Jenkins Transform]]
- [[Deepfake Detection]]
- [[Continued Fractions]]
- [[ai-detection-deepfakes|AI Detection Paper]]
