---
title: WJ Lentz Algorithm
created: 2026-04-06
updated: 2026-04-06
tags: [mathematics, continued-fractions, numerical-methods]
sources: ["[[Continued Fractions]]", "[[Jenkins Transform]]"]
---

# WJ Lentz Algorithm

The WJ Lentz algorithm is a numerical method for evaluating **generalized continued fractions** efficiently and stably. It is named after William J. Lentz, who published the method for computing continued fractions that arise in special functions.

## Algorithm

The Lentz algorithm converts the evaluation of a continued fraction:

$$f = b_0 + \cfrac{a_1}{b_1 + \cfrac{a_2}{b_2 + \cfrac{a_3}{b_3 + \cdots}}}$$

into a forward recurrence that avoids the numerical instability of computing large intermediate numerators and denominators. It works by tracking ratios rather than absolute values, making it particularly well-suited for continued fractions that converge slowly or have terms that grow rapidly.

### Key Properties

- **Forward evaluation**: Unlike backward recurrence, Lentz's method evaluates from the first term forward, allowing truncation at any point
- **Numerical stability**: Avoids overflow/underflow by working with ratios
- **Tiny value substitution**: Replaces zero denominators with a small epsilon to maintain convergence
- **Convergence detection**: Naturally provides a convergence criterion at each step

## Connection to the Research

The Lentz algorithm appears in the [[Continued Fractions]] research as a key computational tool. A dedicated paper in `raw/LaTeX/WJ Lentz/` explores the relationship between the [[Jenkins Transform]] and the Lentz algorithm, showing how the Jenkins Transform's kernel function can be expressed and evaluated using modified Lentz iteration.

The paper (`jenkins_transform_lentz.tex`) presents a comprehensive overview of the Jenkins Transform with connections to continued fraction evaluation via the Lentz method, alongside Python implementations (`derive.py`, `derive_direct.py`) and a Mathematica notebook (`math_research.ipynb`).

## Related Concepts

- [[Continued Fractions]]
- [[Jenkins Transform]]
- [[entangled-continued-fractions]]

## Sources

- `raw/LaTeX/WJ Lentz/jenkins_transform_lentz.tex`
- `raw/LaTeX/WJ Lentz/derive.py`
- `raw/LaTeX/WJ Lentz/derive_direct.py`
