# 30 — The Desert Depth: A Disciplined Negative

*Task 2: attack the one missing integer of the keystone verdict (note 97) — the
electron's desert depth $n_e=\log_\varphi(E_P/m_e)=107.08$ — by seeking a selection
principle that forces it. The discipline, stated in advance: any candidate must
survive the same disownment test that killed $N_\star/e$. The honest outcome is a
negative, and a clean one. Reproduced by `verify/verify_desert-depth.py`.*

---

## The test, fixed before searching

A candidate closed form $v$ for $n_e$ counts as a derivation only if it clears all
three criteria (note 24's audit, made mechanical):

- **(T1) Closure.** $|v-n_e|<0.10$ shell — the window reserved for a genuine hit.
- **(T2) No free knob.** $v$ is built from corpus constants with *no* integer or
  rational chosen to fit. A candidate that needs a fitted/arbitrary integer is
  FITTED, not derived.
- **(T3) Not an artifact.** A bare "round to 107", or a $1/e$-type
  non-low-denominator coincidence dressed as structure, is disqualified *regardless
  of closeness*.

## The search and its result

| candidate | value | $|{\rm resid}|$ | T1 | T2 | T3 | verdict |
|---|---|---|---|---|---|---|
| $\mathrm{round}(n_e)=107$ | 107.000 | 0.081 | Y | Y | **n** | fail |
| $N_\star/e$ | 107.366 | 0.285 | n | Y | n | fail |
| $\tfrac25 N_\star$ | 116.752 | 9.671 | n | Y | n | fail |
| $N_\star-n_H(M_\odot)-1$ | 107.671 | 0.590 | n | **n** | Y | fail |
| $k_\tau+5$ | 107.000 | 0.081 | Y | **n** | Y | fail |
| inversion shell $k_{33}$ | 106.144 | 0.937 | n | Y | Y | fail |
| best lepton-ladder combo | 108.000 | 0.919 | n | n | Y | fail |

**Zero candidates pass.** The two that close to $0.081$ are precisely the traps the
test exists to reject:

- $\mathrm{round}(n_e)=107$ closes trivially but is *just rounding* — it asserts an
  integer without a principle (fails T3).
- $k_\tau+5=107$ is seductive: the $\tau$ ordinal ($102$) plus the manifold's
  defining integer $5$ (from $\sqrt5$, the $5-3u$ curvature numerator). But the
  additive $5$ is a free knob — nothing in the structure selects $+5$ over $+3$ or
  $+8$, and "lepton ordinal plus a hand-picked integer" is exactly the kind of
  after-the-fact fit the discipline forbids (fails T2).

## One near-coincidence, recorded and not claimed

$n_e/N_\star = 107.08/291.88 = 0.3669$, which is within $4\%$ of $1/\varphi^2=0.3820$.
If exact, it would put the electron at $N_\star/\varphi^2=111.5$ — a $4.4$-shell miss,
failing T1 outright. It is logged here as a near-coincidence, explicitly **not** a
result, under the same rule that disowned $N_\star/e$.

## Verdict

**The desert depth is not derivable from any clean $\varphi$-selection principle
built from the corpus constants.** Neither the field-equation spectrum (the
inversion comb $k_n$ does not pass through $107$; nearest is $k_{33}=106.1$), nor
the cosmological ladder ($N_\star/\varphi^2$, $N_\star/e$ all miss or are
artifacts), nor the lepton ladder (no integer combination of $\{24,39,3\}$ lands in
the window without a fitted coefficient) supplies it. The one missing integer
remains a genuine input.

## Why this is the right answer, not a failure

This negative *sharpens* the keystone verdict rather than weakening it. The
framework is a theory of **dimensionless structure**: it forces ratios, ordinals,
angles, and couplings ($\sin^2\theta_W=1/\varphi^3$, $\theta_{13}=|\delta\theta_g|$,
$z_t=1/\varphi$, the $e^{\pi/2}$ comb, three colors $=$ three dimensions). A
dimensionless theory has *no business* predicting a dimensionful mass from nothing,
and the disciplined search confirms it does not sneak one in. The absolute matter
scale requires exactly one external datum — the electron mass, equivalently the
desert depth — and once that single integer is supplied, every mass *ratio* the
framework predicts becomes an absolute mass.

The live question is therefore not "what closed form equals 107" (the wrong
question, and a numerology magnet) but "is there a *dynamical* boundary — a
normalizability or anomaly condition on the field equation of note 16 — that makes
$107$ the deepest stable charged mode?" That is a structural question, not a
curve-fit, and it is the only honest way the desert depth could ever be closed.
Until such a boundary is exhibited, the corpus stands at: dimensionless structure
fully determined, one dimensionful integer genuinely open.

**Update (note 31): the dynamical question is now answered — also negative, and now
*proven*.** Five dynamical mechanisms (normalizability, WKB breakdown, lifetime,
rotor winding, IR closure) were tested against a pre-registered disownment test;
none selects $107$ (genuine $=0$, partial $=0$). The decisive result: the field
equation reduces exactly to a period-locked Hill equation whose one-period Floquet
monodromy is *stable* ($|\mathrm{tr}\,M|=1.57<2$, $\mathrm{Re}\,\mu=0$), so the
static operator **cannot quantize** — it has a continuum, not a discrete tower.
Being translation-covariant in the ordinal, the static equation has only rates, no
preferred depth; a depth needs a charged-sector IR scale the framework does not
supply (importing the cosmological $N_\star$ forces the $N_\star/\varphi^2=111.5$
attractor, not $107$). Even the tempting "three generations" from rotor winding is
threshold-dependent, not a prediction. The honest path forward is a single
parameter-free computation on a *modulated* Hill equation (candidate modulation
source: the off-shell defect $R(k)=\osc''+\osc^3$), not another closed-form search.
See note 31.
