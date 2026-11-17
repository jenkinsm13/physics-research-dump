# 31d — Mechanism D — Charged = Rotor-Coupled; a Winding/Anomaly Bound (and tower TERMINATION)

**Status.** Forward-prediction attempt: can a rotor winding / equidistribution bound CAP the number of charged
generations? Built on the field equation (note 16), the rotor U(1) (note 18), the comb (note 04), and the rotor
defect $\delta\theta_g=78\ln\varphi-12\pi$ (note 17). **This note addresses question (b), TERMINATION** — the
count $3$ vs $4$ — and only secondarily question (a). I keep the two ordinal conventions strictly separate.

## 1. Setup: charge = rotor coupling, and the two ordinals

A mode is *charged* iff it carries nonzero eigenvalue $q$ of the compact phase rotor $J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$
(note 18). The rotor advances the internal phase by $\ln\varphi$ per shell, so a unit-charge mode at rotor-ordinal
$k$ has accumulated phase $\theta(k)=k\ln\varphi$ and winding number $w(k)=k\ln\varphi/2\pi$.

Two ordinals, never conflated:
- **Rotor ordinal** $k$: leptons at $k_e=24,\ k_\mu=63,\ k_\tau=102$, step $\Delta n=39$ (note 04). Zero point is the rotor's, not the Planck scale.
- **Absolute–Planck ordinal** $n$: $n_e=\log_\varphi(E_P/m_e)=107.08$ (note 30). Related by $n=k+b/\!\ln\varphi$, where $b$ is the mass-law intercept $\ln m=ak+b$. The offset is fixed by the Planck anchor (note 24); it is **not** what this mechanism predicts. The generation *count* (3 vs 4) is a statement about $\Delta n=39$ steps in the rotor ordinal and says nothing directly about the value $107$.

## 2. The winding per generation

**Phase convention, stated up front.** The corpus rotor (notes 04/18) lives on the *doubled* spectroscopic phase
$\theta(k)=2k\ln\varphi \bmod \pi$, with defect $\delta\theta_g=78\ln\varphi-12\pi=-0.16459$/gen. The *winding
number* of a unit-charge mode is the natural object on the *single* phase $\Theta_1(k)=k\ln\varphi$,
$w(k)=k\ln\varphi/2\pi$. These are two different circles; I use $w(k)$ throughout and note that its per-generation
defect is **exactly half** the corpus $\delta\theta_g$ by construction ($\Theta_1=\theta/2$) — not a smuggled
factor of 2:

$$ \theta_{\rm gen}=39\ln\varphi=18.7673\ \mathrm{rad}=2\pi\cdot 2.98690,\qquad w_{\rm gen}=2.98690\approx 3. $$

So each generation is **three rotor turns minus a defect**:
$$ \delta_{\rm gen}=3\cdot2\pi-39\ln\varphi=18.8496-18.7673=+0.08229\ \mathrm{rad/gen}=\tfrac12|\delta\theta_g|. $$
Because $39\ln\varphi/2\pi$ is **irrational** ($\ln\varphi$ irrational), the fractional winding $\{w(k)\}$ is
**Weyl-equidistributing** on the circle — there is no exact resonance, ever.

## 3. The candidate termination bound (and why it is a knob)

The conjecture (note 18 §5): the tower terminates when the *accumulated* defect exceeds a threshold,
$|N\,\delta_{\rm gen}|>\Theta$. Setting $\Theta=\pi/2$ (a "quarter-turn loses comb identification") gives
$N_{\max}=\lfloor (\pi/2)/0.0823\rfloor=\lfloor 19.08\rfloor=19$ — **nineteen** generations, not three. To force
$N_{\max}=3$ one needs $\Theta\in(0.247,0.329)$ rad, a window with **no independent justification**. Choosing
$\Theta\approx0.25$ to land on $3$ is precisely the prohibited move.

An anomaly-cancellation reading fares no better. The clean topological fact is $w_{\rm gen}\approx3$: each
generation is ~3 windings, and three generations close one "meta-cycle" of $\sim9$ windings — but $\approx$ is
not $=$ (defect $0.0823$/gen, equidistributing), so nothing **forbids** a 4th. The 4th lepton would sit at
$k_4=141$, winding $141\ln\varphi/2\pi=10.798$ turns: a perfectly ordinary, allowed comb tooth.

## 4. THE MANDATORY CROSS-CHECK (D2) — decisive

A genuine rule must reproduce an *independently known* depth I did not tune to. The rotor-winding rule is
**parameter-free for placement of the teeth** (the comb of note 04), so I test it honestly:

| mode | $k$ | $2k\ln\varphi/\pi$ | nearest half-int (miss) | winding $k\ln\varphi/2\pi$ |
|------|-----|--------------------|-------------------------|----------------------------|
| $e$    | 24  | 7.35238  | 7.5 (off 0.148) | 1.8381 |
| $\mu$  | 63  | 19.29998 | 19.5 (off 0.200)| 4.8250 |
| $\tau$ | 102 | 31.24759 | 31.5 (off 0.248)| 7.8119 |
| 4th    | 141 | 43.19520 | 43.5 (off 0.305)| 10.7988 |

The comb-tooth condition $2k\ln\varphi=(2n-1)\pi/2$ is satisfied only *approximately* and the miss grows
monotonically (0.148→0.200→0.248→0.305) — the same equidistribution drift, $0.0823$/gen per pair of $k$-steps. So the rule **does**
reproduce the tower 24/63/102 with step 39 (✓, but this is the *input* comb, not a fresh prediction). Crucially,
the SAME rule with NO new parameter produces a clean, allowed 4th tooth at 141. **It does not yield 107, 92, or
any absolute depth at all** — the winding count is dimensionless and ordinal-agnostic. A mechanism that does not
even speak about $107$ cannot be said to derive it. On the count question, the rule's parameter-free output is
"the tower never terminates"; "3" requires a hand-chosen threshold.

## 5. Pre-registered disownment test (D1–D5)

- **D1 NO FREE KNOB — FAIL.** "$N_{\max}=3$" requires a defect threshold $\Theta\approx0.25$ rad picked to land on 3. Parameter-free, the bound is $N_{\max}=19$ (for $\Theta=\pi/2$) or $\infty$ (no threshold).
- **D2 CROSS-CHECK — FAIL as a derivation.** The rule reproduces 24/63/102/step-39 (because that *is* the comb it is built on) but predicts an **allowed** 4th at 141 and yields **no** absolute depth (no 107, no 92). It is consistent with the tower but does not independently predict any new depth.
- **D3 CONSISTENCY — would be VIOLATED by any "3" bound.** Any $\Theta$ small enough to forbid the 4th (k=141, *cumulative rotor defect* $0.3292$, distinct from the §4 comb-tooth miss $0.305$) lies just above the tau's accumulated defect ($0.2469$ at gen 3) — the margin is one defect step. The bound that kills generation 4 sits a hair above the tau; a slightly tighter $\Theta$ forbids the tau. This is the fragility D3 warns against.
- **D4 ROBUSTNESS — FAIL (two independent knobs, adversarially re-derived).** *Knob 1, the threshold.* Threshold $\pi/2\Rightarrow19$; $\pi/3\Rightarrow12$; $\pi/4\Rightarrow9$; $1/\varphi\Rightarrow7$; $\ln\varphi\Rightarrow5$; $|\delta\theta_g|\Rightarrow2$; "3 windings exact" ($\Theta\to0$) $\Rightarrow0$. The number swings across the whole range $0$–$19$ under equally defensible choices. The *only* window giving exactly 3 is $\Theta\in[0.2468,0.3290)$ rad (independently recomputed: $[3\delta_{\rm gen},4\delta_{\rm gen})$), and it has **no preimage in any corpus constant** — not $1/\varphi=0.618$, not $\ln\varphi=0.481$, not $|\delta\theta_g|=0.165$, not $\pi/\varphi^2=1.20$, not $\pi/4=0.785$, nothing. *Knob 2, the breakdown criterion itself.* Replace "cumulative rotor defect $>\Theta$" with the equally natural "mode falls off its comb tooth when the tooth-miss reaches a half-spacing ($0.5$ on the $2k\ln\varphi/\pi$ axis)": the miss drifts $\approx0.052$/gen there, giving an entirely different cap. The count is hostage not just to *where* the threshold sits but to *which* quantity is thresholded. Exposed knob, twice over.
- **D5 FAILURE-FLAG-111 — not triggered.** The mechanism produces counts (3, 19, ∞), never $\sim111$; it does not drift to the $N_\star/\varphi^2$ attractor because it never addresses the absolute depth. (Good in that narrow sense, but only because it answers a different question.)

**The three traps:** (i) periodicity — fatal: the comb is infinite, finiteness needs an envelope/boundary the
winding count cannot supply. (ii) attractor — avoided (different question): the rule emits dimensionless **counts**
($3/9/12/19/\infty$), never an absolute depth, so it has no path toward $107$ or the $N_\star/\varphi^2=111.5$
soft-attractor. (iii) non-Hermitian "stability" — not invoked; I make no normalizability claim, so no
inner-product is owed.

## 6. The structural ingredient that WOULD select 3 (what is missing)

The knob-hunt makes precise *what a genuine cap would require*. A tunable angular threshold $\Theta$ can never be
parameter-free, and a winding *count* is ordinal-agnostic, so neither can ever produce a protected "$3$." The only
object that could is a **topological / spectral multiplicity** — an integer that is what it is with nothing to dial:

1. **A self-adjoint reduction with a stated inner product.** The operator $D_k^2+M^2(k)$ is non-Hermitian
   (complex $\omega$, §dispersion). To *count* charged sectors one must first pick the functional space and pairing
   in which "charged rotor mode" is a discrete spectral datum. The natural candidate is the biorthogonal
   $\langle u_L|u_R\rangle$ of the $\mathcal{PT}$-like rotor pair $n_{\pm1}=(1,\mp1)$; the count would then be the
   number of $\langle\cdot|\cdot\rangle$-normalizable rotor sectors the envelope $osc^2(k)$ admits. **This pairing is
   never constructed here** — without it, "3" has no carrier. (This is exactly trap iii, named and left open.)
2. **The envelope, not the lattice, must do the cutting.** $osc^2$ is periodic ⇒ infinitely many teeth (trap i).
   A real cap needs the *amplitude* envelope (the $e^{\pm k/\varphi}$ rotor growth/decay, or a confining IR wall,
   note 31e) to render only finitely many rotor sectors normalizable in the inner product of (1). The winding phase
   alone is unit-modulus and cannot suppress anything.
3. **The integer would have to be $\lfloor w_{\rm gen}\rfloor=3$ *forced*, not coincidental.** $w_{\rm gen}=2.9869$
   rounds to $3$, but rounding is not a selection rule. A genuine derivation would show the multiplicity of (1)
   equals $\lfloor 39\ln\varphi/2\pi\rfloor$ for a reason — e.g. a Maslov index $i^{\Delta n}$ over one generation's
   $\Delta n=39$ reversals returning to the identity sector after exactly $3$ phase windings, with the $0.0823$-rad
   defect accumulating into the *first* non-trivial holonomy at generation $\sim$ the normalizable count. That index
   computation is the missing link; it is not done in any current note. Until it is, the cap is a wish, not a result.

## 7. The one honest positive

The single parameter-free, falsifiable statement the winding picture *does* make: a 4th charged lepton, if it
exists, sits at $k_4=141$ (winding $10.80$), an ordinary allowed tooth — i.e. the framework **does not forbid**
generation 4 (bare-affine mass $\approx159$ GeV, matching note 04's affine extrapolation). That is a real (if
unwelcome) prediction, opposite to the desired "termination."

## Verdict

**negative** (verdict *survives* an independent adversarial re-derivation). The rotor-winding/anomaly idea
reproduces the *input* comb but cannot terminate the tower without a hand-tuned defect threshold (knob → D1/D4
fail), any "3" bound dangerously brushes the tau (D3), and the mechanism yields no absolute depth, so it says
nothing about $107$. The knob-hunt **strengthens** the disownment: there are *two* exposed knobs, not one — the
threshold value ($N_{\max}\in\{0,2,5,7,9,12,19\}$ across $\{|\delta\theta_g|,\ln\varphi,1/\varphi,\pi/4,\pi/3,\pi/2\}$)
*and* the choice of which quantity is thresholded (cumulative defect vs comb-tooth fall-off give different counts).
The only window yielding exactly 3, $\Theta\in[0.247,0.329)$ rad, contains no corpus constant. Its sole
parameter-free output is that a 4th generation at $k_4=141$ is **allowed**, not forbidden. §7 names the precise
missing structural ingredient — a self-adjoint (biorthogonal) reduction whose spectral multiplicity *forces* the
integer — without which "3" has no carrier.

**Falsifier:** discovery of a 4th charged lepton at the bare-affine mass $\ln m_4 = a\cdot141+b$ ($a=0.104538$, least-squares intercept $b=-2.762$; note 04), $m_4\approx159$ GeV — upper end of note 04's $1.4$–$160$ GeV bracket (the ordinal $k_4=141$ is pinned hard, the mass only loosely) — would *confirm* the no-termination reading; its definitive absence, with no rotor threshold ever derived parameter-free, leaves the 3-generation count unexplained by this mechanism.
