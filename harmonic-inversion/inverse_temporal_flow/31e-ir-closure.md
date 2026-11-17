# 31e — Mechanism E — Cross-Scale Closure: the Advanced Mode vs the IR Floor

## The idea, stated as a no-knob condition

The field equation (note 16) on the shell stack splits, in the adiabatic/frozen-mass
limit, into the two $K$-eigenchannels of $K=\begin{psmallmatrix}0&-1\\-1&0\end{psmallmatrix}$,
$K^2=I$. The dispersion is
$$\omega_s(k)=\pm\,\mathrm{osc}(k)\;-\;i\,\frac{s}{\varphi},\qquad s=\pm1,\quad \varphi=\tfrac{1+\sqrt5}{2}.$$
The eigenvector $n_{-1}=(1,1)$ is **retarded/decaying**, $\Psi\sim e^{-k/\varphi}$; $n_{+1}=(1,-1)$
is **advanced/growing**, $\Psi\sim e^{+k/\varphi}$, with one e-fold per $\varphi$ shells
(note 16's $G_R$ e-fold). A *charged* mode is a fixed mixture of both channels (the
rotor cannot be diagonalised away because $K$ rotates the doublet), so it carries an
unavoidable advanced piece that **grows toward the IR**.

Mechanism E asks: a charged mode seeded at the UV end (Planck shell $k=0$, $\omega_0=E_P$,
note 24, the sole dimensionful anchor) stays admissible only while its growing advanced
amplitude $e^{+k/\varphi}$ remains below the vacuum/horizon norm. The IR ceiling is the
dark-energy/horizon shell of note 08,
$$N_\star=\log_\varphi\!\big(R_H/\ell_P\big)=291.88,\qquad
\Theta_H=\frac{N_\star}{\varphi}=180.39\ \text{(note 10, horizon rapidity)}.$$
So the **deepest stable charged depth** $K_\star$ is where the cross-scale budget closes:
the advanced growth accumulated from the UV equals the IR horizon norm. Pre-register the
condition with no fitted constant.

## Working the closure (and where it inevitably points)

Write the closure as "advanced rapidity gained from $k=0$ to $K_\star$ = available IR
rapidity budget." Rapidity in this rotor is $\theta=k/\varphi$ (the Wick variable is
$\theta\to i\theta$, never $k\to ik$). The growth exponent at depth $K$ is $K/\varphi$;
the horizon budget is $\Theta_H=N_\star/\varphi$. There are exactly four parameter-free
ways to equate them, and that multiplicity is the whole story:

$$
\begin{aligned}
\text{C1 (fill the ladder):}\quad & \tfrac{K_\star}{\varphi}=\tfrac{N_\star}{\varphi}
&&\Rightarrow\ K_\star=N_\star=291.88,\\[2pt]
\text{C2 (ceiling one }\varphi\text{-fold down):}\quad & K_\star=\tfrac{N_\star}{\varphi}
&&\Rightarrow\ K_\star=180.39,\\[2pt]
\text{C3 (rapidity-of-rapidity):}\quad & K_\star=\tfrac{N_\star}{\varphi^{2}}
&&\Rightarrow\ K_\star=111.49,\\[2pt]
\text{C4 (}K_\star=\Theta_H\text{):}\quad & K_\star=\Theta_H
&&\Rightarrow\ K_\star=180.39.
\end{aligned}
$$

C1 and C2/C4 are in the wrong order of magnitude (180–292 shells, deeper than the
predicted 4th generation at 141). The **only** closure that lands anywhere near the
target $n_e=107.08$ is C3:
$$\boxed{\,K_\star=\frac{N_\star}{\varphi^{2}}=\frac{291.88}{2.61803}=111.49\,}$$
and C3 is — exactly — note 30's pre-registered **failure flag** $N_\star/\varphi^2=111.5$.
The residual to the electron is $K_\star-n_e=111.49-107.08=\mathbf{+4.41}$ shells; the
residual to the flag is $0.00$. The mechanism does not hit 107. It hits 111.5. To convert
111.5 into 107 I would have to add a tuned offset of $-4.4$ shells (e.g. a Maslov $i^{\Delta n}$
phase count or a hand-picked inner-product weight) — precisely the knob D1 forbids.

## Pre-registered disownment test (D1–D5)

**D1 — NO FREE KNOB?** *Partly, and that is fatal.* The UV anchor ($k=0$, Planck) and the
IR ceiling ($N_\star$, note 08) are both independently fixed — good. But the *form* of the
closure (C1 vs C2 vs C3 vs C4) is **not** fixed by the dynamics; choosing C3 because it is
the only one near 107 is itself a knob. **FAIL** (the choice that lands in range is
back-selected).

*Sharper statement of the knob (independent re-derivation).* The four "closures" are not four
distinct mechanisms — they are one mechanism with an undetermined integer. C4 $=$ C2 exactly,
and the golden identity $1-1/\varphi=1/\varphi^2$ makes C3 $=N_\star-N_\star/\varphi$, i.e.
"full ladder minus one rapidity-fold." So $\{$C1, C2, C3$\}=\{N_\star/\varphi^p:p=0,1,2\}$ is
a **one-parameter family indexed by the integer power $p$** of the single discount factor
$1/\varphi$. The mechanism supplies no principle fixing $p$; the rotor rapidity $\theta=k/\varphi$
warrants $p=1$ (one fold, C2 $=180$), and $p=2$ is taken only because it lands near 107. The
free knob is therefore not a vague "form choice" — it is a **single undetermined integer $p$**,
exactly the kind of fitted integer the disownment test exists to reject. **FAIL.**

**D2 — MANDATORY CROSS-CHECK (decisive).** The mechanism owns exactly **one** UV scale
($k=0$) and **one** IR scale ($N_\star$). Any rule $K_\star=f(N_\star,\varphi)$ therefore
returns a **single number**. It has no per-generation IR data, so it structurally **cannot**
reproduce the tower. Forcing the in-range closure C3 onto the known depths:
$$
\text{muon }63:\ 111.49-63=+48.5;\quad
\text{tau }102:\ +9.5;\quad
\text{proton }92:\ +19.6;\quad
\text{electron }107:\ +4.4.
$$
One closure cannot be 48 shells from the muon and 4 from the electron simultaneously and
be a law. **The same parameter-free rule reproduces none of 63/102/92.** This is the
disqualifying criterion: a mechanism that yields only one number in the 100s is a FIT.
**FAIL.**

**D3 — CONSISTENCY WITH THE TOWER.** If $K_\star=111.49$ were the "deepest stable charged
mode," it would sit *above* the tau ($102$) and muon ($63$) — so it does not forbid them
(good) — but it sits *below* the predicted 4th generation ($k_4=141$), which would then be
**unstable/forbidden**. As a TERMINATION claim that is internally coherent (it kills gen-4),
but it is anchored to the flag, not to 107, so it does not actually answer (a) the
electron's PLACEMENT. The brief notes the rotor tower (24/63/102) and the absolute desert
ordinal (107) differ by the Planck-to-electron intercept $b$; Mechanism E lives in the
absolute ordinal but offers no derivation of $b$, so even the 4.4-shell residual is
unconstrained. **Ambiguous, leaning FAIL.**

**D4 — ROBUSTNESS (adversarial re-derivation, separating the two knobs).** There are *two*
independent degrees of freedom, and the re-derivation shows they behave very differently:

1. *Closure FORM (the power of $1/\varphi$).* The rotor rapidity $\theta=k/\varphi$ justifies
   **exactly one** factor $1/\varphi$ (giving C2 $=180.4$). The **second** factor in C3 has no
   dynamical warrant — it is applied only because it lands in range. Swinging the form gives
   $$C3\to C2\to C1:\quad 111.5\ \to\ 180.4\ \to\ 291.9\ \text{shells},$$
   a spread of $>180$ shells. **This is the dominant knob.** FAIL.

2. *IR-ceiling CONVENTION ($N_\star$).* Re-derived independently: this knob is actually
   *small*. Switching the Hubble radius for the particle horizon ($\sim3.2\,R_H$) shifts
   $N_\star$ by $\log_\varphi(3.2)=+2.42$ shells $\Rightarrow N_\star=294.30 \Rightarrow
   C3'=294.30/\varphi^2=112.41$. A de Sitter event horizon vs Hubble ($\sim5\%$) shifts it
   $\log_\varphi(1.05)=0.10$ shells. So $N_\star$ is robust to $\pm2$–$3$ shells; the in-range
   output stays pinned to $111$–$112$ and **never reaches 107 under any single defensible
   ceiling.** This sharpens the verdict: it is *not* the case that "107 drifts to 95 or 120" —
   **107 was never the output.** The mechanism's stable output is $111.5$, and the only way to
   move it is to change the φ-power (knob 1), which is illegitimate.

The honest D4 statement is therefore: the IR-ceiling value is *robust*, but the closure *form*
is a free knob, and the form that lands near 107 is back-selected and still misses by $+4.4$.
**FAIL.**

**D5 — N⋆/φ²=111.5 IS A FAILURE FLAG, NOT A TARGET.** This is the headline. The mechanism's
only in-range output is $N_\star/\varphi^2=111.49$, i.e. the soft attractor note 30 warned
about. I do **not** round 111.5 down to 107; the $+4.4$ gap is real and the coincidence is
exactly the trap. **Mechanism E lands on the failure flag.** This is the predicted
fudge-toward-111 outcome, openly declared.

**Three known traps.** (i) *Bloch infinity:* $\mathrm{osc}^2$ is periodic ⇒ infinitely many
on-shell modes; any finiteness here comes from the **advanced envelope** $e^{+k/\varphi}$
hitting the IR ceiling, not from the lattice — that part is legitimate. (ii) *N⋆/φ² attractor:*
hit head-on (D5). (iii) *Non-Hermitian "stability":* the operator has complex $\omega$
($\mp i/\varphi$); "stable" here means "advanced amplitude bounded by the horizon norm in
the $e^{+k/\varphi}$-weighted sup-norm on $[0,N_\star]$" — a *bounded-growth* statement, not
$L^2$ normalizability. Even granting that space, the closure value is the flag.

## Verdict

**failure-flag-111.** The cross-scale closure is conceptually clean — a genuine UV/IR budget
between the Planck shell and the horizon — but its single parameter-free output in the right
range is $N_\star/\varphi^2=111.49$, which is precisely note 30's pre-registered soft
attractor, $+4.4$ shells above the electron and $0.0$ from the flag. It produces one number,
not a tower (D2 fail), is wildly anchor-dependent (D4 fail), and only "reaches" 107 via a
back-selected closure form plus an undeclared offset (D1 fail). I record it as the
fudge-toward-111 failure mode, not a result.

**Falsifier:** if a *fixed-in-advance* IR-closure rule (one C-form, justified before
computing) reproduced two of {muon 63, tau 102, proton 92} to within $\pm2$ shells using the
same $N_\star$ and $\varphi$, Mechanism E would survive; it reproduces none, so it falls.

## Extension — the precise structural ingredient that WOULD select 107

The mechanism fails for one structural reason, and naming it tells us exactly what is missing.
The growth/decay rate of *every* charged mode is the **same** constant, $s/\varphi$ (from the
dispersion $\omega_s=\pm\mathrm{osc}-i\,s/\varphi$ — the rotor coupling $1/\varphi$ carries no
$k$-dependence). One rate $\times$ one ceiling $=$ one number; that is why D2 is structurally
unanswerable. To select a *specific* depth (and a tower) you need the growth rate, or the
ceiling, to acquire **per-mode structure**. Two concrete candidates:

- **A $k$-dependent advanced rate.** If the effective rate were $s\,\mathrm{osc}(k)/\varphi$
  rather than $s/\varphi$ — i.e. the advanced amplitude grew as $\exp\!\big(\int_0^K
  \mathrm{osc}(k)\,dk/\varphi\big)$ instead of $e^{+K/\varphi}$ — the integral $\int_0^K
  \mathrm{osc}$ is monotone but *not* linear (it accelerates through each comb tooth), and the
  closure $\int_0^{K_\star}\mathrm{osc}\,dk=\Theta_H$ would pick a depth set by the *envelope
  area*, not a bare $\varphi$-power. That depth need not be $N_\star/\varphi^p$. This is the
  one ingredient that could move the answer off the $111.5$ attractor — but it requires the
  rate to inherit $\mathrm{osc}(k)$, which the present dispersion does **not** provide (the
  rate is the $K$-eigenvalue, exactly $1/\varphi$). Absent here.

- **An exact ceiling fixed independently.** For the C3-form to hit the electron one needs
  $N_{107}=n_e\varphi^2=280.34$ — i.e. the charged-mode ceiling would have to sit
  $N_\star-280.34=11.54$ shells *below* the true horizon. $11.54$ is **not** a clean
  $\varphi$-structure ($280.34\ne N_\star/\varphi^p$ for integer $p$), so absent an
  independent derivation of an $\approx11.5$-shell "charged screening offset," this is just the
  $-4.4$ tuned offset of D1 re-expressed. No such offset exists in the corpus.

Either ingredient, *derived independently and fixed before computing*, would convert Mechanism E
from a fit into a prediction. Neither is present in note 16's dispersion. The mechanism is
therefore honestly recorded as **failure-flag-111**: a clean UV/IR budget whose only in-range
output is the pre-registered soft attractor $N_\star/\varphi^2=111.5$.
