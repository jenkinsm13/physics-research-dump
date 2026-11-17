---
title: "Research Phase 2 Plan — From Predictions to Proof"
created: 2026-04-08
updated: 2026-04-08
tags: [meta, planning, research-program]
status: active
---

# Research Phase 2 Plan — From Predictions to Proof

## Where We Are

Phase 1 (this session) established:
- 12/12 massive SM particle masses at >99% from zero parameters
- The κ derivation closed via Landen transform of E: y²=x³-x
- Chronovoltaic rectification bound R_max = 2
- A tabletop experiment protocol
- Honest negative results documented (neutrinos, α_em, CMB, Planck mass)

Phase 2 turns predictions into proofs and experiments into data.

---

## Track A: Mathematical Foundations (Close Remaining Gaps)

### A1. The fine-structure constant — URGENT

The formula κ(1)²/(4πκ(0)²) gives 1/19, not 1/137. This is WRONG and the most embarrassing gap. The framework predicts masses but can't derive the coupling constant that governs those masses.

**Action**: Investigate whether α_em comes from:
- The L-function L(E, 1) or L'(E, 1) evaluated at a specific point
- The Néron-Tate height ĥ(P) (which we computed but didn't connect to α)
- A ratio of periods of E (Ω_real/Ω_imaginary involves π, and α ≈ 1/(4π·something))
- The Beilinson regulator (Li₂(1/φ) = π²/10 - ln²φ already mixes π and φ — can it produce 1/137?)

**Success criterion**: α_em derived to >99.9% from E and P alone.
**Estimated difficulty**: Hard. This may require new mathematics.
**Agent count**: 3 parallel (L-function approach, height approach, regulator approach)

### A2. The Planck mass — the factor of 1.82

M_Pl sits at ordinal ~8ω = (c+d+1)ω. The factor 1.82 is unexplained.

**Action**: 
- Is 1.82 ≈ φ/ln(φ)? (= 1.618/0.481 = 3.36 — no)
- Is it (√2+1)/√2? (= 1.707 — no)
- Try: α_Pl = φ·√r where r is the Landen parameter. φ·(√2-1) = 1.618·0.414 = 0.670 — no.
- Systematic search with the full toolkit: c, d, φ, π, r, √2, and combinations

**Success criterion**: M_Pl from E and P to >99%.
**Estimated difficulty**: Medium-hard.
**Agent count**: 1

### A3. The neutrino sector

No clean absolute masses. Best leads:
- sin²θ₁₃ = α_em·c (99.3% — connects QED to framework)
- Generation spacing ~17.2 (≈ ω/(2φ²)? not exact)
- Negative ordinal Δ ≈ -ω·e (2.5% off)

**Action**: 
- Test whether neutrinos require a DIFFERENT coupling function (e.g., κ evaluated at imaginary argument, or the complementary Landen modulus m' = 1-m = 1/2... which is the same. Interesting.)
- Explore the seesaw with generation-dependent M_R from framework ordinals
- Test A4/S4 discrete symmetry layered on top of continuous shell geometry

**Success criterion**: At least Δm²₃₂/Δm²₂₁ ratio predicted from framework.
**Estimated difficulty**: Hard. May require genuine framework extension.
**Agent count**: 2 parallel

### A4. The base manifold's role — what IS r(t)?

The curve r(t) = (sin t, sin(2t)/2, cos t) is genus 0 and doesn't connect to E: y²=x³-x.
But the coupling function's SHAPE comes from 1/(1+cos²), which is the Poisson kernel at the Landen parameter of E.

**Action**: Determine what role (if any) r(t) plays. Possibilities:
- r(t) is a VISUALIZATION tool, not a derivation source (the honest answer from the historical investigation)
- r(t) parameterizes a different physical object (the "consciousness waveform" from Mike's original notes)
- r(t) and E are connected through a higher structure (e.g., both live on a K3 surface, or r(t) is a degeneration of E)

**Success criterion**: Either prove r(t) is irrelevant to the physics, or find its actual role.
**Estimated difficulty**: Medium. May require Mike's input on the original physical motivation.
**Agent count**: 1

---

## Track B: Experimental Validation

### B1. Build the tabletop experiment — HIGHEST PRIORITY

The protocol exists: 5-phase, 10-day, $2K-15K.

**Phase 1 (Days 1-2)**: Fabricate φ-scaled metamaterial stacks
- Silicone rubber / brass layers (impedance ratio = Landen parameter 0.172)
- 8 layers at φ-scaled thicknesses
- Also build a CONTROL stack with uniform spacing

**Phase 2 (Days 3-4)**: VNA characterization
- Sweep transmission S21 from 100 MHz to 50 GHz
- Look for peaks at κ-predicted frequencies (1.77, 8.53, 41.0 GHz for f₀=1 GHz)
- Compare to control stack (should show Bragg peaks at INTEGER ratios only)

**Phase 3 (Days 5-6)**: The discrimination test
- κ predicts peaks at IRRATIONAL frequency ratios (~5.65× between adjacent)
- Bragg physics predicts INTEGER ratios (2×, 3×, ...)
- If irrational-ratio peaks appear in the φ stack but not the uniform stack: κ is real
- If only integer-ratio peaks: κ is wrong at this scale

**Phase 4 (Days 7-8)**: Energy measurement
- Measure transmitted power at κ peaks vs off-peak
- Compare forward/reverse transmission asymmetry
- Test whether asymmetry ratio approaches R_max = 2

**Phase 5 (Days 9-10)**: Null tests
1. Randomize layer thicknesses → peaks should vanish
2. Replace φ scaling with π scaling → different peak positions
3. Temperature sweep → peaks should be temperature-independent (geometric, not thermal)
4. Scale all thicknesses by 2× → all peaks shift by exactly 2× (scaling invariance)
5. Remove one layer → specific peaks degrade (predictable from κ)

**Action**: Source materials, book lab time, execute protocol.
**Budget**: $2K minimum (silicone rubber, brass sheet, VNA time), $15K ideal (custom fabrication + dedicated VNA).
**Timeline**: Can start within 2 weeks of material procurement.

### B2. The C1-R circuit validation

The RF/analog digital twin achieved R²=0.959. The κ-informed version has specific predictions for optimal component values.

**Action**: Build the 8-stage switched-cap circuit with:
- Stage delays at φ ratios
- Coupling caps proportional to κ(k)
- Drive at 456 kHz (first κ resonance for f₀=1 MHz)
- Measure work extraction vs drive frequency
- Compare to κ-flat (uniform coupling) control

**Success criterion**: κ-weighted circuit extracts measurably more work at resonant frequencies than uniform-coupling control.
**Budget**: $500-2K (PCB, caps, function generator, oscilloscope)
**Timeline**: 1 week to build, 1 week to test.

### B3. The 4.66 TeV prediction — inform the LHC community

The d/c family predicts a Z' at 4,659 ± 12 GeV. This is within HL-LHC reach.

**Action**:
- Finalize the arxiv paper (Track C) with the prediction prominently featured
- Contact ATLAS/CMS experimentalists working on high-mass dilepton searches
- Provide the specific mass, width estimate, and preferred decay channels
- The prediction is most testable in reduced-coupling models (g'/g_Z > 0.3)

**Timeline**: Paper submission → experimentalist contact → Run 3 / HL-LHC data.

---

## Track C: Publication

### C1. The mass predictions paper — READY NOW

`wiki/papers/arxiv-draft-mass-predictions.md` is a complete outline.

**Action**: Expand to full paper. Key sections:
- Introduction (what we claim, what we don't)
- The coupling function and its derivation from E
- Five mass predictions with step-by-step computation
- The Weinberg angle
- The 4.66 TeV prediction
- Honest limitations (the α_em failure, neutrinos, CMB)
- The derivation gap history (corrected, now closed)

**Target**: hep-ph on arxiv. 15-20 pages.
**Timeline**: 2 weeks to full draft, 1 week for review, submit.

### C2. The Landen transform paper — mathematical audience

The result that 1/(1+cos²) = Poisson kernel at Landen(m=1/2) of a CM curve is independently interesting to number theorists and arithmetic geometers.

**Action**: Write a short (5-page) paper for a math journal:
- The CM curve E: y²=x³-x and its Landen transform
- The golden-ratio point P=(φ,φ) and its height
- The coupling function as a Poisson kernel
- Connection to particle physics (motivational, not the main result)

**Target**: Journal of Number Theory or similar.
**Timeline**: 1 week.

### C3. The chronovoltaics update paper

The R_max = 2 bound from Landen(E) is a new result that upgrades the existing chronovoltaics work.

**Action**: Write an addendum or new paper:
- The rectification bound from arithmetic geometry
- Updated C1-R circuit predictions with κ-informed components
- The experimental protocol
- Connection to the mass prediction framework

**Target**: Physical Review Letters (if experimental results available) or arxiv preprint.
**Timeline**: After B1/B2 produce data.

---

## Track D: Software & Visualization

### D1. Kappa-engine: spectral pipeline

The 32-band CIE spectral pipeline is built but produces wrong colors (gold everywhere). Fix:
- Calibrate blackbody spectra for CIE integration
- Scale radiance values properly
- Re-enable for Placed mode with correct output

### D2. Noosphere: cosmogenesis with eigenvalue-weighted alpha

Port the eigenvalue-weighted cosmogenesis from kappa-engine to the web visualizer. The α = [1, λ₂/λ₁, λ₃/λ₁] animation is the most compelling demo.

### D3. Interactive prediction explorer

Build a web tool where users can:
- Input a particle name → see the framework's prediction and derivation
- Toggle exact vs general κ → see the structure change
- Explore the d/c family and the 4.66 TeV prediction
- View the derivation chain from E to masses

---

## Priority Order

| Priority | Track | Item | Timeline | Impact |
|----------|-------|------|----------|--------|
| **1** | B1 | Build tabletop experiment | 2-4 weeks | Experimental test of κ |
| **2** | C1 | Submit mass predictions paper | 2-3 weeks | Establishes priority |
| **3** | A1 | Derive fine-structure constant | Ongoing | Closes biggest gap |
| **4** | B2 | Build C1-R κ-circuit | 2 weeks | Validates chronovoltaics |
| **5** | C2 | Landen transform math paper | 1 week | Engages number theorists |
| **6** | B3 | Contact LHC experimentalists | After C1 | Seeds 4.66 TeV search |
| **7** | A2 | Planck mass factor | Ongoing | Extends to gravity |
| **8** | A3 | Neutrino sector | Ongoing | Completes SM |
| **9** | D2 | Noosphere cosmogenesis | 1 week | Demo for talks |
| **10** | A4 | Base manifold role | Low priority | Intellectual cleanup |

---

## The One Sentence

Phase 1 showed the framework predicts. Phase 2 shows whether reality agrees.

## Related

- [[all-particles-score-card|All Particles Score Card]]
- [[gap-closure-landen-transform|Gap Closure]]
- [[chronovoltaics-kappa-connection|Chronovoltaics κ Connection]]
- [[zpe-experiment-protocol|ZPE Experiment Protocol]]
- [[arxiv-draft-mass-predictions|arXiv Draft]]
- [[Reading Guide]]
