# 24 — Absolute Scale, Route A: the Planck–Horizon Closure

**Thread:** Round 4, the keystone. The first of three scale routes (A = Planck/geometry here, B = Λ in note 25, C = Newton's $G$ in note 26). Builds on the closed boost group (10–11), the golden shell ladder $r_n=r_0\varphi^{\,n}$ (round 1, note 02), the cosmological depletion shell $N_\star=\log_\varphi(R_H/\ell_P)=291.88$ (note 08), and the round-3 field theory whose ZPE is UV-finite but whose quantum $\omega_0$ was left **unanchored** (note 22). Every number below is reproduced in `verify/verify_scale-route-planck.py`. $\varphi=1.6180339887$, $\ln\varphi=0.4812118251$.

## The keystone gap, restated

Everything through note 23 fixes *ordinals* and *ratios*. The boost group gives the rapidity ladder $\theta_n=n/\varphi$; the Casimir gives the mass-shell $M^2(k)=\mathrm{osc}^2(k)$; the lepton mass law (notes 04, 17) gives $\ln m = a\,k+b$ with a clean *geometric slope* $a=0.10454$ and the seal $e^{39a}=\sqrt{m_\tau/m_e}=58.97$. But the **intercept $b$** — the one number carrying dimensions, the absolute scale — was never derived. Route A pins it with a single geometric input: **shell $0$ lives at the Planck length**, $r_0=\ell_P$. Nothing else is fed in; $m_e$ is *not* used to set the scale. It is the thing we then try to predict.

## 1. The ladder is dimensionless except for one anchor

From note 02, lengths and energies live on the golden ladder
$$ r_n = r_0\,\varphi^{\,n}, \qquad \omega_n = \omega_0\,\varphi^{-n}, $$
energy descending as length ascends (UV at small $n$, IR at large $n$). The ladder is *purely dimensionless*: only the pair $(r_0,\omega_0)$ carries units, and they are conjugate, $\omega_0=\hbar c/r_0$, the natural quantum at the seed shell. So **one** anchor fixes both. We take
$$ \boxed{\,r_0 = \ell_P = 1.6163\times10^{-35}\,\text{m}\,} \;\Longrightarrow\; \boxed{\,\omega_0 = \frac{\hbar c}{\ell_P} = E_P = 1.2209\times10^{19}\,\text{GeV}.\,} $$
The round-trip $\hbar c/\ell_P$ reproduces the Planck energy to $1.2\times10^{-7}$ (numerical, from CODATA $\hbar,c,\ell_P$). This is the **headline number**: $\omega_0=E_P$, fixed from geometry with **zero mass input**. Note 26 reaches the identical $\omega_0$ from Newton's $G$; since $\ell_P=\sqrt{\hbar G/c^3}$, Routes A and C are the **same anchor reached two ways** (geometry vs. gravity) — their agreement is a consistency check, *not* independent over-determination. Genuine over-determination would require Route B ($\Lambda$, note 25) to reproduce $E_P$ from the IR end.

## 2. The horizon closes the ladder (note 08)

The depletion shell of note 08 measures the Planck$\to$Hubble hierarchy as a golden-shell count:
$$ N_\star = \log_\varphi\!\left(\frac{R_H}{\ell_P}\right)=291.88,\qquad \varphi^{N_\star}\approx 10^{61}. $$
The whole universe is $\approx 292$ golden shells deep. The deepest energy quantum is the horizon mode
$$ \omega_{N_\star}=E_P\,\varphi^{-N_\star}=1.2209\times10^{19}\,\text{GeV}\cdot\varphi^{-291.88}\approx 1.4\times10^{-42}\,\text{GeV}\;(\sim10^{-33}\,\text{eV}), $$
of order the present Hubble energy $\hbar H_0\sim 1.5\times10^{-33}\,$eV. I state the precision honestly: this is an **order-of-magnitude consistency check, not a sub-percent match** — $N_\star=291.88$ was itself *defined* as $\log_\varphi(R_H/\ell_P)$ (note 08), so $\omega_{N_\star}=\hbar c/R_H\sim\hbar H_0$ is, up to the $\mathcal O(1)$ factor relating $R_H$ to $c/H_0$, a definitional identity rather than an independent prediction. What is *not* circular is the **direction**: the IR cutoff falls *out* of the UV-anchored ladder rather than being inserted by hand. This is the same $\varphi^{N_\star}\approx10^{61}$ whose square gave $\Lambda\ell_P^2\sim10^{-122}$ in note 08.

## 3. Where does the electron sit? — the ruthless, anti-circular computation

Now the test. Demote $m_e$ to an *output*. On the energy ladder anchored at $E_P$, the electron occupies the energy shell
$$ n_e^{\rm exact}\equiv \log_\varphi\!\left(\frac{E_P}{m_e}\right)=\frac{\ln(1.2209\times10^{19}/5.110\times10^{-4})}{\ln\varphi}=\mathbf{107.079}. $$
For Route A to *pin* $m_e$, this $n_e$ must be a clean $\varphi$-lattice number derivable without $m_e$. The natural cosmological candidate is the depletion shell:
$$ \frac{n_e^{\rm exact}}{N_\star}=\frac{107.079}{291.88}=\mathbf{0.36686}. $$
**This is not $2/5$, not $3/8$, not any low-denominator fraction.** The most tempting simple anchor — "the electron sits $2/5$ of the way down the Planck$\to$Hubble ladder" — predicts $n_e=0.4N_\star=116.75$ and hence
$$ m_e^{\rm pred(2/5)}=E_P\,\varphi^{-0.4N_\star}=4.86\times10^{-6}\,\text{GeV},\qquad \text{miss }=\mathbf{-99.0\%}, $$
i.e. wrong by **two orders of magnitude**. There is no clean $\varphi$-combination here. (The closest numerical tease is $n_e\approx N_\star/e=107.38$, off by $0.30$ shell — a $-13.3\%$ mass miss — but $1/e$ is *not* a golden-ladder number: it has no low-denominator rational approximant inside lattice tolerance, so $N_\star/e$ is **disqualified as a derivation regardless of how close it lands**. The verify script enforces exactly this — it asserts the *disownment* of $N_\star/e$, not the magnitude of the coincidence. An earlier draft of that test rewarded the $\sim13\%$ near-miss as a passing check; that was a subtle fudge — locking in a number the prose itself calls non-physical — and has been removed.)

This is exactly, and independently, what Route C found by the *other* slope: solving for the desert depth the framework would need, $D_{\rm need}=24+\ln(E_P/m_e)/a=516.9$, versus the best $\varphi$-candidate $N_\star\varphi=472.3$ — a $44$-shell, factor-$\sim$100 miss (note 26 §5). **Two routes, two different slopes ($\ln\varphi$ here, $a$ there), same verdict:** the Planck-to-electron shell count is not a pure-$\varphi$ number.

## 4. The honest result

I will not dress this up.

1. **$\omega_0=E_P$ is genuinely pinned, with zero mass input.** The conjugate relation $\omega_0=\hbar c/r_0$ with $r_0=\ell_P$ fixes the absolute energy quantum from geometry alone, to $\sim10^{-7}$. *That is the deliverable headline*, and routes B/C can be compared against it directly. **The scale is pinned.**

2. **The electron mass is NOT pinned.** Anchoring at $\ell_P$ converts the dimensionless ladder to absolute energies, but it does **not** tell you *which rung* the electron occupies. That requires the integer shell-count $n_e=107.08$ — which is precisely the intercept $b$ in disguise — and $107.08$ is not produced by any pure-$\varphi$ lattice combination ($n_e/N_\star=0.367$, irreducible). The $2/5$ guess misses by $99\%$. **Route A pins the top of the ladder and the spacing; it leaves the desert depth as a genuinely missing input.**

3. **Why the honest non-pinning is the right answer.** Every Tier-2 near-miss in the round-3 audit (note 98) was a place where $\varphi$ cancels against an external mass. Route A explains *why*: the framework's geometry fixes the ladder's **unit** ($\omega_0=E_P$) and its **spacing** ($\varphi$ per shell, $a$ per ordinal), both parameter-free — but the **offset** (which shell is the electron) is one integer the boost group does not supply. The keystone gap is therefore *localized*, not closed: it is a single missing integer $n_e\in\mathbb Z$, not a continuous tuning. A future derivation that produces $107$ as a forced $\varphi$-lattice count would close it; until then, $b$ stays open.

## 5. Cross-check: the slope is independent of the intercept

Route A touches only $b$ (the absolute scale). The slope $a$ (note 17) is untouched and still independently seals the *ratios*: $e^{39a}=58.97=\sqrt{m_\tau/m_e}$ (residual $\sim7\times10^{-15}$). So Route A and the mass law are orthogonal — one would fix where the ladder starts, the other fixes its rungs. The fact that they do **not** meet at the electron (the $\varphi$-count $107$ is not forced) is the precise, quantified statement of the keystone gap.

## Extension — the over-determination closure number $C_{AB}$

Routes A and C share the single anchor $\ell_P=\sqrt{\hbar G/c^3}$, so their agreement is built in, not earned. The only way to genuinely *over-determine* the scale is to reach $\omega_0$ from the **IR end** — to lift the present Hubble energy back up the ladder and ask whether it returns the Planck quantum. Define the **closure number**
$$ \boxed{\,C_{AB}\equiv \frac{\omega_0^{\rm (UV)}}{\omega_0^{\rm (IR)}} = \frac{E_P}{\big(\hbar H_0\big)\,\varphi^{+N_\star}}\,}, \qquad \ln C_{AB}\Big/\ln\varphi \;=\; \text{closure residual in shells}. $$
If the anchored ladder is exact, $C_{AB}=1$ identically: walking *down* $N_\star$ shells from $E_P$ and *up* $N_\star$ shells from $\hbar H_0$ must meet. Numerically, with $\hbar H_0\sim1.5\times10^{-33}$ eV and $N_\star=291.88$,
$$ \omega_0^{\rm (IR)}=\hbar H_0\,\varphi^{291.88}\approx 1.5\times10^{-33}\,\text{eV}\times10^{61}\approx 1.5\times10^{19}\,\text{GeV}\approx E_P, $$
so $C_{AB}\approx 1$ to within **less than one shell** ($|\ln C_{AB}/\ln\varphi|<1$, i.e. within a factor $\varphi$). This is the sharpest single number Route A produces: the UV anchor and the IR horizon are **the same point on the ladder, reached from opposite ends**, and the residual *is* the $N_\star$ rounding/$H_0$ slack — nothing more. The closure being trivially $\approx1$ here (because $N_\star$ was *defined* from $R_H/\ell_P$) is precisely why **only an independent $\Lambda$-derivation in note 25, one that fixes $N_\star$ from vacuum physics rather than from the horizon ratio, can turn $C_{AB}$ from a tautology into a genuine over-determination.** That is the live target.

## Prediction

**Falsifier (the honest, sharp one):** Route A pins $\omega_0=E_P=1.2209\times10^{19}$ GeV. *(i)* If Route B ($\Lambda$) or any independent IR derivation returns $\omega_0\neq E_P$ by more than $0.1\%$, the Planck anchor is falsified outright. *(ii)* The electron-mass closure is **predicted to fail**: the Planck-to-electron count $n_e=\log_\varphi(E_P/m_e)=107.08$ is asserted to be *not* a pure-$\varphi$ lattice number — if a first-principles derivation ever forces $n_e$ (or $D=516.9$) as an exact golden-lattice integer to $\lesssim1$ shell ($\lesssim10\%$ in $m_e$), Route A's non-pinning is overturned and the scale is closed; if instead the only "fits" remain transcendental teases like $N_\star/e$, the desert depth stays an irreducible input and $G$/$\ell_P$ alone provably cannot give $m_e$.
