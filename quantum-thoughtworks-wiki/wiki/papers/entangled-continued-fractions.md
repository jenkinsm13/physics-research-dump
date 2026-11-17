---
title: "The Entangled Continued Fractions Theorem"
author: Michael C. Jenkins (as Metamer)
created: 2026-04-06
updated: 2026-04-06
tags: [paper, continued-fractions, entanglement, number-theory, convergents]
sources:
  - "raw/LaTeX/Continued Fractions/entanglement.tex"
  - "raw/LaTeX/Continued Fractions/entanglement-expanded.tex"
  - "raw/LaTeX/Continued Fractions/excerpt.tex"
---

# The Entangled Continued Fractions Theorem

**Metamer, the Seeker of Mathematic Mysteries** (Michael C. Jenkins)

## The Theorem

**Theorem (Entangled Continued Fractions).** Let $A = [a_0; a_1, a_2, a_3, \ldots]$ and $B = [b_0; b_1, b_2, b_3, \ldots]$ be two continued fractions such that $A \times B = 1$ identically. Then, a modification in a term of $A$ necessitates a compensatory modification in the corresponding term of $B$ to maintain $A \times B = 1$. This relationship is akin to quantum entanglement, where a change to one element of an entangled pair induces a compensatory change in the other, irrespective of distance.

## Proof Outline

The proof uses the convergent recursion relations:

$$P_n = a_n P_{n-1} + P_{n-2}, \quad Q_n = a_n Q_{n-1} + Q_{n-2}$$

Since $A \times B = 1$, the convergent sequences are reciprocally linked. Modifying any $a_k$ in $A$ changes $P_n/Q_n$ for all $n \geq k$, forcing compensatory changes in $B$'s convergents to maintain the identity.

## Significance

This establishes an analogy between:
- **Mathematical structure**: Reciprocal continued fractions are "entangled" -- changing one requires compensatory changes in the other
- **Quantum physics**: Entangled quantum states exhibit non-local correlations

This connection underpins the use of [[Continued Fractions|continued fraction methods]] throughout the [[Matryoshka-Chronon Framework]].

---

## Related Concepts

- [[Continued Fractions]]
- [[Jenkins Transform]]
- [[DivideByZero]]
