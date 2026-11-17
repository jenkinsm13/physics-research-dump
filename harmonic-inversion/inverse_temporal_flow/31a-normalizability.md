# 31a — Mechanism A — Normalizability / Sturm–Liouville Mode Count

**Question addressed.** (b) TERMINATION, attempted by *mode counting*: does the field
equation of note 16 admit only a **finite** number of normalizable charged modes on the
ordinal half-line, and if so does the deepest one sit at the desert depth
$n_e=107.08$ (note 30)? The honest outcome below is **no** — the operator yields a
**continuum**, not a finite tower, so it places neither $107$ nor the cross-check depths.
This revision upgrades the verdict from *asserted* to *computed*: the one calculation the
original note only gestured at — the **Floquet monodromy** of the reduced Hill equation —
is now performed, and it lands the pinned eigenvalue squarely **inside a stability band**
($\operatorname{tr}M=-1.5696$, $|\operatorname{tr}M|=1.57<2$, $\det M=1$, multipliers on
the unit circle, $\operatorname{Re}\mu=0$ to machine precision). The bulk therefore cannot
grow; the continuum is **forced, not chosen**. Reproduced in
`verify/verify_normalizability.py` (exit 0, residuals + monodromy inline).

## Set-up: strip the rotor, get a Hill equation

Take note 16 on $k\in[0,\infty)$ with the UV (Planck) boundary at $k=0$:
$$(D_k^2+M^2)\Psi=0,\quad D_k^2=\partial_k^2-\tfrac{2}{\varphi}K\partial_k+\tfrac{1}{\varphi^2}I,\quad M^2=\mathrm{osc}(k)^2,$$
with $K^2=I$, eigenvalues $s=\pm1$ ($\mathbf n_{-1}=(1,1)$ retarded $e^{-k/\varphi}$;
$\mathbf n_{+1}=(1,-1)$ advanced $e^{+k/\varphi}$), $\varphi=\tfrac{1+\sqrt5}2$,
$\ln\varphi=0.481212$, $1/\varphi=0.618034$, and
$\mathrm{osc}(k)=1/(1+\cos^2(2k\ln\varphi))\in[\tfrac12,1]$, so $\mathrm{osc}^2\in[\tfrac14,1]$.

In a $K$-eigenstate the vector equation is scalar:
$$\Psi_s''-\tfrac{2s}{\varphi}\Psi_s'+\tfrac{1}{\varphi^2}\Psi_s+\mathrm{osc}(k)^2\Psi_s=0.$$
Strip the **exact** rotor envelope $\Psi_s=e^{sk/\varphi}u_s(k)$. Using
$\Psi_s''=e^{sk/\varphi}\!\big(u''+\tfrac{2s}{\varphi}u'+\tfrac1{\varphi^2}u\big)$ and
$s^2=1$, the drift term *and* the constant $1/\varphi^2$ mass cancel **identically**:
$$\boxed{\,u_s''+\mathrm{osc}(k)^2\,u_s=0\,}\qquad\Longleftrightarrow\qquad u_s''=-W(k)\,u_s,\;\;W=\mathrm{osc}^2.$$
This is a **Hill equation** with eigenvalue pinned to $0$ and a strictly positive,
periodic potential $W(k)=\mathrm{osc}(k)^2\in[\tfrac14,1]$, period $L=\pi/(2\ln\varphi)=3.26425$.
The verify script confirms this reduction directly: the full operator applied to
$e^{sk/\varphi}u$ matches $e^{sk/\varphi}(u''+\mathrm{osc}^2u)$ to a finite-difference
**relative residual $3.6\times10^{-7}$** ($s=-1$) and $2.0\times10^{-7}$ ($s=+1$). The
envelope is not an approximation — it absorbs the entire first-order/constant-mass
structure exactly. **This exact reduction is the easy part (the bait); the spectrum is the
hook, and it turns entirely on the Floquet structure and the inner product below.**

## The decisive invariant: Floquet monodromy (now computed, not asserted)

Because the eigenvalue is **pinned to $0$** (there is no spectral parameter $\lambda$ left
to tune), the entire "continuum vs. discrete / does the bulk grow?" question collapses onto
a **single conjugacy invariant**: the trace of the one-period monodromy matrix $M$ of
$u''=-W(k)u$, $W=\mathrm{osc}^2$, period $L=\pi/(2\ln\varphi)$.

* $|\operatorname{tr}M|<2$ — **stable band**: multipliers $\rho_\pm$ on the unit circle,
  Floquet exponents $\mu=\ln\rho/L$ **pure imaginary**, $u_s$ bounded-oscillatory with
  **zero intrinsic growth**. The *only* attenuation in $\Psi_s=e^{sk/\varphi}u_s$ is then
  the explicit rotor envelope → continuum.
* $|\operatorname{tr}M|>2$ — **instability tongue**: a real $\mu$ exists; retarded
  normalizability would hinge on $\mu<1/\varphi$, and *that* competition could in principle
  have produced a discrete selection.

The original note merely *claimed* the bands are "thin" and never computed which case
holds. The monodromy (RK4 over one period, two fundamental solutions) gives — verified in
STEP 2b —
$$\operatorname{tr}M=-1.5696,\qquad |\operatorname{tr}M|=1.57<2,\qquad \det M=1.0000,$$
phase-independent across start-phases $k_0=0,0.7,1.6$ (as a conjugacy invariant must be:
all three give $-1.56956$). Hence
$\rho_\pm=\tfrac12\!\big(-1.5696\pm i\sqrt{4-1.5696^2}\big)$ with $|\rho_\pm|=1.000$,
$\operatorname{Re}\mu=-8.5\times10^{-18}$ (machine zero), $\operatorname{Im}\mu=\pm0.7576$
per shell.

**This is the crux of the knob-hunt.** A *too-easy* negative would hide a knob by
*choosing* an inner product or boundary that erases discrete structure. Here the absence of
discrete structure is **forced**: the pinned ray lands well *inside* a stability band (not
at a band edge, not in a tongue), so the bulk has no real Floquet exponent to compete with
$1/\varphi$ and no growing solution to quantize. The continuum is not a modelling choice —
it is the spectral fact.

## Where finiteness would have to come from — and why it doesn't

A *discrete, finite* Sturm–Liouville tower needs a **confining well with two turning
points**, so bound states quantize and eventually run out. Here
$W=\mathrm{osc}^2>0$ **everywhere** (verified $\min W=0.250000$, $\max W=1.000000$ on
$[0,200]$), so $u_s''=-(\text{positive})\,u_s$ is in the **oscillatory** sign class with
**no turning point**, and — now *computed* — Floquet-**stable** at the pinned eigenvalue
($|\operatorname{tr}M|=1.57<2$). The reduced solution is bounded-oscillatory: shooting from
the Planck boundary ($u(0)=0,u'(0)=1$) gives $|u|_{\max}=1.367$ and $|u(150)|=0.392$ — it
never decays on its own. The *only* decay/growth in $\Psi_s=e^{sk/\varphi}u_s$ is the
explicit envelope. This is exactly **Trap (i)** of the pre-registration: a periodic mass
gives Bloch/Floquet structure, never a finite discrete count, unless an envelope or
boundary confines — and the envelope here does not *confine*, it merely *attenuates a
whole sector uniformly*.

**Normalizability needs an inner product (the operator is non-Hermitian).** Two
defensible explicit choices on $k\in[0,\infty)$:

* **(i) plain weighted $L^2$:** $\;\|\Psi_s\|^2=\int_0^\infty e^{2sk/\varphi}|u_s|^2\,dk.$
 With $u_s=O(1)$: for $s=-1$ (retarded) the integrand $\sim e^{-2k/\varphi}$
 **converges** — verified $\|\Psi\|^2=0.423$ for the shot $u$ and $0.847$ for a *totally
 different* bounded $u=\cos(2.1k)+\tfrac12$, i.e. finite for *every* bounded profile. For
 $s=+1$ (advanced) the integrand $\sim e^{+2k/\varphi}$ **diverges**.
* **(ii) bi-orthogonal $\langle L|R\rangle$:** pairing $s=-1$ with $s=+1$ at weight $1$
 gives integrand $\sim e^{(-1+1)k/\varphi}|u|^2=|u|^2=O(1)$ → **diverges**.

In (i) the **entire retarded sector is normalizable** — *every* bounded $u_s$ qualifies,
for any $k$-content — so the normalizable charged modes form a **continuum** with no
quantization condition and no deepest member. In (ii) **nothing** is normalizable.
Neither choice yields a finite discrete tower; **no "deepest normalizable mode" exists.**

The only route to a number is to **impose an amplitude cutoff** $e^{-K^\*/\varphi}=T$,
giving $K^\*=-\varphi\ln T$. Landing on $107.08$ demands $T=e^{-107.08/\varphi}=1.8\times10^{-29}$ (verified) — a threshold with **no independent justification**. That is a
pure free knob.

## PRE-REGISTERED DISOWNMENT TEST (D1–D5)

* **(D1) NO FREE KNOB — FAIL.** The bulk problem produces *no number at all*: the computed
 Floquet trace ($|\operatorname{tr}M|=1.57<2$) puts the pinned eigenvalue in a stable band,
 so the spectrum is a continuum. A depth appears only after inserting an amplitude threshold
 $T$ (equivalently a Floquet-exponent cutoff) chosen to land near $107$ — the forbidden knob.
* **(D2) MANDATORY CROSS-CHECK — FAIL (decisive).** The mechanism yields a *continuum*,
 i.e. **no discrete depths**. It therefore reproduces **neither** the muon ($63$), **nor**
 the tau ($102$), **nor** the proton ($92$) — it places nothing. A rule that predicts no
 discrete depth cannot match an untuned one. This alone is fatal.
* **(D3) CONSISTENCY WITH THE TOWER — vacuously violated.** With a continuum, $63$ and
 $102$ are "inside" only trivially; there is no boundary to respect because there is no
 discrete spectrum. The mechanism cannot certify the tower because it cannot *generate*
 the tower.
* **(D4) ROBUSTNESS — stays NEGATIVE, and the knob is exposed.** Two independent stress
 tests. (a) *Inner product*: choice (ii) drops the count from "continuum" to "empty" —
 still no finite tower. (b) *Cutoff anchor*: under defensible alternative thresholds the
 number is nowhere near $107$ — $T=10^{-16}\Rightarrow K^\*\approx59.6$;
 $T=10^{-17}\Rightarrow K^\*\approx63.3$; one e-fold $T=1/e\Rightarrow K^\*=\varphi=1.62$;
 Green's-fn e-fold per comb step likewise $K^\*=1.62$. The number swings across $\sim1.6$–$75$
 with a hand-picked $T$; reaching $107$ needs $T=1.8\times10^{-29}$ chosen for no reason but
 the target. The Floquet result removes the last escape hatch — a real instability exponent
 that might have quantized — because there *is none* ($\operatorname{Re}\mu=0$). Whether one
 reads the spectrum as a Floquet-stable continuum (here) or hypothesises a band-restricted
 continuum, "no finite discrete tower, no unique deepest mode" is robust. **$107$ survives
 none of these defensible choices.**
* **(D5) $N_\star/\varphi^2=111.5$ FAILURE FLAG — not triggered, reported.** The
 mechanism produces no finite number, so it does not drift onto $\sim111$; the soft
 attractor is not the failure mode here. The failure mode is **non-finiteness** itself.

## Verdict

**negative — and now structurally PROVEN, not asserted.** Stripping the rotor envelope
reduces note 16 *exactly* (FD residual $\sim10^{-7}$) to a Hill equation
$u''=-\mathrm{osc}^2u$ whose strictly positive, periodic potential $W\in[\tfrac14,1]$ has
**no turning point**, and whose one-period monodromy has $\det M=1$,
$|\operatorname{tr}M|=1.57<2$ — the pinned eigenvalue sits **inside a Floquet stability
band**, so $u$ is bounded-oscillatory with $\operatorname{Re}\mu=0$ and the bulk cannot
grow. The envelope $e^{-k/\varphi}$ then makes the **whole** retarded sector normalizable
in plain $L^2$ — a **continuum**, not a discrete finite tower — while the advanced sector
and the bi-orthogonal pairing are non-normalizable. No deepest normalizable mode emerges;
any depth (including $107$) requires a free amplitude/stability knob (fails D1), swings from
$1.6$ to $75$ under defensible anchors (fails D4), and the rule places none of $63/102/92$
(fails D2). Normalizability is the **wrong door** for the desert depth — exactly as note 30
anticipated when it asked for "a dynamical boundary … that makes $107$ the deepest stable
charged mode." The Sturm–Liouville count is not that boundary, and the Floquet trace proves
it can never be.

## Extension — the precise structural ingredient that WOULD select 107

The Floquet calculation does more than close this door: it tells us **exactly what is
missing**. A finite Sturm–Liouville tower requires the *pinned* eigenvalue to fall in an
**instability gap** with a *graded* real exponent $\mu(k)$ that **crosses** the envelope
rate $1/\varphi$ at one place. Concretely, the missing ingredient is a **slow modulation of
the period or amplitude of $W$** — an $\varepsilon k$-drift, $W(k)=\mathrm{osc}^2(k)\,[1+\varepsilon\,g(k)]$,
or a chirp $\cos^2\!\big(2k\ln\varphi\cdot(1+\varepsilon k)\big)$ — that drags the pinned ray
across a band edge into a tongue at a depth set by $\varepsilon$. There $u\sim e^{\mu(k)k}$
with real $\mu(k)$, and the *retarded normalizability boundary* $\mu(K^\*)=1/\varphi$ becomes
a genuine, **parameter-free** turning point: the deepest normalizable mode sits where the
intrinsic Floquet growth first overtakes the envelope decay. For this to land at $107$
**without** a tuned knob, the drift $\varepsilon$ would itself have to be fixed by the
framework — the natural candidate is the **adiabatic off-shell defect**
$R(k)=\mathrm{osc}''+\mathrm{osc}^3$ (RMS $0.66$, worst *at* the comb), precisely the quantity
note 16 reports as the bulk's failure to be exactly on-shell. If $R(k)$ sources a secular
drift of $W$'s band structure, the band edge it pushes the pinned ray through is a candidate
for a *derived* termination depth. That is the one calculation that could turn this door
from "wrong" to "right" — and it is **absent** in the static (period-locked) Hill equation
studied here, which the trace above proves to be Floquet-stable and therefore non-quantizing.
Whether the derived depth of a *modulated* problem is $107$ (vs. tau-$102$, or the
$N_\star/\varphi^2=111.5$ attractor flagged in D5) is an open, falsifiable question for note
31b+.

**Falsifier.** Exhibit a *parameter-free* inner product (or a framework-fixed band-edge
drift $\varepsilon$) in which the field operator of note 16 has a **discrete** spectrum that
is **finite in number**, whose deepest normalizable eigenvalue is $107\pm1$, **and** which
keeps the tau ($102$) and muon ($63$) inside the normalizable set — without choosing any
threshold, anchor, or boundary condition to land there. The Floquet trace
$|\operatorname{tr}M|=1.57<2$ rules this out for the *static* Hill equation; the falsifier
must therefore live in a *modulated* one.
