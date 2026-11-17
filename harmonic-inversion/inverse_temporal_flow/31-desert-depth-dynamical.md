# 31 — Is There a Dynamical Boundary Selecting $n_e\approx107$? Five Mechanisms, One Answer

*The direct attack on the open question from the keystone verdict (note 97) and the
closed-form negative (note 30): does the field equation of note 16 have a
**dynamical** boundary — normalizability, WKB breakdown, lifetime, rotor winding, or
IR closure — that selects the electron's desert depth $n_e=107.08$ without a free
knob? Five mechanisms (31a–31e), each developed and then adversarially knob-hunted
against a pre-registered disownment test (D1–D5). Final verdict: **no — and now
proven, not merely asserted.** All five are negatives or the flagged attractor. But
the five negatives converge on one precise, theorem-grade obstruction, which is the
real result. Reproduced by
`verify/verify_{normalizability,wkb-breakdown,lifetime-stability,rotor-winding,ir-closure}.py`
(all exit 0).*

---

## The pre-registered test (fixed before computing)

A dynamical mechanism counts as genuine only if: **(D1)** no free knob; **(D2)** the
*same* rule reproduces an independently-known depth (muon 63, tau 102, proton 92) —
the decisive criterion; **(D3)** it leaves the tau and muon stable; **(D4)** the
number survives a different-but-reasonable choice; **(D5)** landing on $\sim111$ is
the $N_\star/\varphi^2=111.5$ *failure flag*, not a hit.

## The five mechanisms and their verdicts

| # | Mechanism | Gives | D2 cross-check | Verdict |
|---|---|---|---|---|
| 31a | Normalizability (Sturm–Liouville) | a continuum — no discrete tower | fails (places none) | **negative (proven)** |
| 31b | WKB / adiabatic breakdown | a $\Delta k$-periodic comb, no depth | fails | **negative** |
| 31c | Lifetime / $Q$ threshold | depth-independent $\tau=\varphi$ | fails | **negative** |
| 31d | Rotor winding / generation count | re-states input comb; cap is knob-dependent | fails | **negative** |
| 31e | IR closure (advanced vs horizon) | $111.49=N_\star/\varphi^2$ | fails | **failure-flag-111** |

**genuine = 0, partial = 0, negative/flagged = 5.** Every mechanism that produced a
number did so only through a knob the audit exposed.

### 31a — the decisive structural negative (now proven)

The field equation reduces *exactly* (envelope $\Psi_s=e^{sk/\varphi}u_s$) to the
period-locked Hill equation $u''=-\osc^2(k)\,u$ with eigenvalue pinned to $0$. The
one-period Floquet monodromy was computed (RK4): $\det M=1.000$,
$\mathrm{tr}\,M=-1.5696$, $|\mathrm{tr}|<2$ — the pinned ray sits **inside a
stability band**, $\mathrm{Re}\,\mu=0$. So the bulk *cannot* quantize: the spectrum
is a continuum, there is no deepest normalizable mode, and any depth requires a
forced amplitude cutoff $T$ with $107.08$ demanding $T=1.8\times10^{-29}$ (pure
knob; robust anchors give $59.6$, $63.3$, $1.6$ — never $107$). The periodic mass
$\osc^2$ *provably* gives Bloch bands, not a tower. This is the load-bearing result.

### 31e — why $111.5$ keeps haunting us

The most instructive negative. "Advanced growth $e^{+k/\varphi}$ meets the horizon
ceiling at $N_\star$" gives, under its most natural choice,
$$k_*=N_\star-\Theta_H=N_\star-\frac{N_\star}{\varphi}=\frac{N_\star}{\varphi^2}=111.49,$$
**exactly** the note-30 failure-flag attractor — because $1-1/\varphi=1/\varphi^2$ is
a golden identity, *any* closure built from the advanced rate $1/\varphi$ and the
only available IR rapidity $\Theta_H=N_\star/\varphi$ is forced onto $111.5$. The
four "closures" collapse to one one-parameter family $\{N_\star/\varphi^p\}$; the
power $p$ is a fitted integer. The attractor is structural, and it is **not** $107$.

### 31d — the generation-count question, and why it is also a knob

The rotor mechanism is the most tempting, because it *looks* like a forward
prediction. The charged-lepton tower is the orbit of $R(\delta\theta_g)$,
$\delta\theta_g=78\ln\varphi-12\pi=-0.16459$, step $39$ — so by construction it
re-states the known tower $24\to63\to102$ and an *allowed* 4th tooth at $k_4=141$.
But terminating the tower requires a threshold on the cumulative rotor defect, and
the knob-hunt found the cap $N_{\max}$ swings across **0, 2, 5, 7, 9, 12, 19** as the
threshold ranges over defensible corpus constants ($|\delta\theta_g|$, $\ln\varphi$,
$1/\varphi$, $\pi/4$, $\pi/3$, $\pi/2$). The unique window giving exactly $3$,
$[0.247,0.329)$ rad, **contains no corpus constant**; and even the *criterion* is a
second knob (a "fall off the tooth at half-spacing" rule gives $9$). So "three
generations" is not derived — it is a number the mechanism can be tuned to, like all
the others. Honest verdict: negative. (The rule does correctly say $k_4=141$ is an
*allowed* ladder point, not a near-closure — but that is a re-statement, not a
prediction.)

## The convergent finding: a theorem-grade obstruction

Mechanisms 31a, 31b, 31c, and 31e independently arrive at the *same* structural
fact. The bulk field equation is **translation-covariant in the ordinal** — the mass
$\osc^2$ is exactly $\Delta k$-periodic — so by Floquet it possesses **only rates**
($1/\varphi$, $\Delta k$) and **no preferred depth or origin**. A desert depth is a
*ratio of two external masses* ($E_P/m_e$); it can enter only through boundary data
or an external scale, which is the very datum one is trying to derive (31b's
circularity argument). And the static operator is Floquet-*stable* (31a,
$|\mathrm{tr}\,M|=1.57<2$, $\mathrm{Re}\,\mu=0$), so it cannot host a discrete tower
at all.

$$\boxed{\;\text{The static, period-locked field equation cannot select a depth: it
is Floquet-stable and translation-covariant.}\;}$$

This is strictly sharper than note 30's "no closed form." It is an obstruction
theorem: not "we failed to find the principle," but "the principle cannot exist in
the *static* equation." Every mechanism that produced a number had to import the
*cosmological* scale $N_\star$ — the wrong sector, which forces $111.5$, not $107$,
and is itself a knob for the charged tower.

## What would be needed (the one constructive path)

All five extensions name the same missing ingredient: the exact $\Delta k$-periodicity
must be broken by a **framework-fixed slow modulation**
$$\osc^2(k)\;\longrightarrow\;\osc^2(k)\,[1+\epsilon\,g(k)],$$
opening an instability gap where a *graded* Floquet exponent $\mu(k)$ crosses the
envelope rate $1/\varphi$ at exactly one depth $K_*$ — the genuine, knob-free
turning point (deepest normalizable mode = where intrinsic growth first overtakes
envelope decay). For $K_*$ to be untuned, $\epsilon$ must itself be framework-fixed.
The natural candidate is the off-shell defect $R(k)=\osc''+\osc^3$ of note 16 §2
(RMS $0.66$, worst at the comb), which sources a secular drift of the band structure.

## Verdict

**No dynamical boundary in the current field equation selects $n_e\approx107$** —
proven, because the static operator is Floquet-stable and translation-covariant and
therefore cannot quantize. The desert depth remains a genuine external input. The
framework is, as the keystone verdict held, a theory of dimensionless structure that
correctly refuses to manufacture a dimensionful scale — and the disciplined search
confirms it does not sneak one in under any of five dynamical guises.

The probe's real yield is not the (expected) negative but its *sharpness*: (1) a
theorem-grade reason — translation-covariance + Floquet stability — that $107$ is not
derivable from the static equation; (2) the precise constructive target that could
close it (a framework-fixed modulation of the Hill equation, candidate source
$R(k)$); (3) an explanation of the persistent $111.5$ attractor as a forced golden
identity; (4) a clean demonstration that even the seductive "three generations" is
threshold-dependent, not a prediction.

## Falsifier / next step

The one parameter-free computation that remains: derive the modulation $\epsilon g(k)$
from $R(k)=\osc''+\osc^3$, compute the Floquet exponent of the *modulated* Hill
equation, and check whether $\mu(K_*)=1/\varphi$ lands on $107$ — versus the tau
($102$) or the $111.5$ attractor. If the modulated band-edge is *not* $107$ within
the closure window, the dynamical route is closed for good and the desert depth is
irreducibly external. That is the honest next move — a sharp computation, not another
search for a closed form.

**This computation is now done (note 32): the modulation route is also a knob.** $R(k)$
turns out to be exactly $\Delta k$-periodic, so it cannot break translation-covariance
at all; the only symmetry-breaking modulation is an aperiodic chirp whose rate
$\epsilon$ is fixed by no corpus quantity, and the resulting boundary $K_*(\epsilon)$
sweeps continuously through the tau ($102$), the electron target ($107$), and the
$111.5$ attractor — the $\epsilon$ values span only $\sim9\%$, so the knob cannot even
resolve the electron from the tau. The same rule reproduces none of the tower (D2
fails). The desert depth is now established as **irreducibly external** by three
disciplined negatives (closed form 30, static dynamics 31, modulated dynamics 32).
