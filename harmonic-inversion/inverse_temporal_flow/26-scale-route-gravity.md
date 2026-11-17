# 26 — Absolute Scale, Route C: Newton's G from the Gravitational Sector

**Thread:** Round 4, the keystone. Independent scale route via gravity. Builds on the closed boost group (10–11), the absorber-completed Newton law (03, 13), the GW horizon shell (15), and the round-3 field theory (16, 22). Companion to Route A (Planck, 24) and Route B (Λ, 25).

## The question

The mass law $\ln m = a\,k + b$ has a *geometric* slope $a$ (round 3: lepton $a=0.10454$, seal $e^{39a}=\sqrt{m_\tau/m_e}=58.97$) but an **unanchored intercept** $b$ — the absolute scale. Route C asks: can the gravitational sector, anchored only on Newton's $G$, pin $b$ (equivalently $\omega_0$ or $r_0$) without ever feeding in a particle mass?

**Single input:** Newton's $G$ (with $c,\hbar$ to form the Planck length). No lepton, no hadron mass.

## Step 1 — the gravitational coupling is already dimensionless-locked

From note 13 the absorber-completed potential is

$$\Phi(r) = -\frac{C}{r^{\nu_{\rm eff}}},\qquad \nu_{\rm eff} = \frac{\tfrac1\varphi - \Gamma_{\rm tot}}{\ln\varphi} = 1.00297,$$

with $\Gamma_{\rm tot} = 1/(2\sinh S_1)=0.13539$, $S_1=\pi/(2\varphi\ln\varphi)=2.0174$. The exponent is forced to (essentially) $1$ by pure-$\varphi$ constants — Newton's inverse-square is **derived**, not fit, to $0.3\%$, with no running. But $\nu_{\rm eff}$ is *dimensionless*: it fixes the **shape**, not the **scale**. The scale enters only through the shell unit length $r_0$ in $r = (\text{physical distance})/r_0$.

## Step 2 — $G$ pins the bottom rung: $r_0 = \ell_P$

The shell ladder is $r_n = r_0\,\varphi^{\,n}$ (round 1). The clean self-consistency criterion is: **the bottom shell ($k=0$) is the unique rung whose own gravitational radius equals its own size.** A one-shell quantum has energy $E_0=\hbar c/r_0$, hence mass $m_0=\hbar/(c\,r_0)$ and Schwarzschild radius

$$r_s(m_0)=\frac{2G m_0}{c^2}=\frac{2G\hbar}{c^3 r_0}.$$

Demanding $r_s(m_0)=r_0$ (the rung is its own horizon — self-gravitating, "null" in the boost-group sense) gives

$$r_0^2=\frac{2G\hbar}{c^3}\;\;\Longrightarrow\;\; r_0=\sqrt{\tfrac{2G\hbar}{c^3}}=\sqrt2\,\ell_P,\qquad \ell_P\equiv\sqrt{\frac{\hbar G}{c^3}}.$$

The factor $\sqrt2$ is the usual Schwarzschild-vs-Compton convention ambiguity; absorbing it into the $O(1)$ definition of the rung, the scale is fixed at the **Planck length**, $r_0=\ell_P$, by $G$ alone. This is the only place a dimensionful constant enters Route C.

Boost-group reading (notes 10–11): shells carry rapidity $\theta=k/\varphi$ = hyperbolic arc length, $V^\top\eta V=1$ (null normalization $=L_y$). The $k=0$ rung — the fixed point of time reversal $T$, $\theta=0$ — is therefore the self-gravitating horizon rung, i.e. the Planck rung. **$G$ fixes $r_0=\ell_P$ with no mass input.**

## Step 3 — the conjugate energy quantum (the headline)

The energy quantum conjugate to the bottom shell is

$$\boxed{\;\omega_0 = \frac{\hbar c}{\ell_P} = E_P = \sqrt{\frac{\hbar c^5}{G}} = 1.221\times10^{19}\ \text{GeV}.\;}$$

This is **Route C's headline $\omega_0$**. The cross-comparison with Routes A (Planck) and B ($\Lambda$): Route A anchors on $\ell_P$ directly, so Route A *must* give the same $\omega_0=E_P$ — A and C are the **same anchor reached two ways** (geometry vs. gravity), and their agreement is a *consistency check*, not an independent over-determination. Genuine over-determination requires Route B ($\Lambda$): if the IR anchor $N_\star=\log_\varphi(R_H/\ell_P)=291.88$ reproduces $E_P$ at the top, the scale is closed from both ends.

## Step 4 — solar horizon shell (independent cross-check of the anchor)

Note 15 placed the Sun's horizon at $n_H=\log_\varphi(r_s/\ell_P)$. With $r_s=2GM_\odot/c^2=2.954$ km and $r_0=\ell_P$:

$$n_H = \frac{\ln(r_s/\ell_P)}{\ln\varphi} = 183.1,$$

matching the corpus value $183.08$ to within $0.05\%$. This uses **only $G$** (through both $r_s$ and $\ell_P$) and confirms the anchor is self-consistent across 38 orders of magnitude in length.

## Step 5 — predict the electron mass (ruthlessly anti-circular)

The slope $a=0.10454$ and the top rung $\omega_0=E_P$ are now both fixed without any mass. The electron mass is

$$m_e = E_P\,\exp\!\big[-a\,(D-k_e)\big],$$

where $k_e\approx24$ is the electron's lepton-ladder ordinal (round 1) and $D$ is the **integer shell count from the Planck rung down to the electron rung** — the gauge-desert depth. Here is the honest crux:

- Geometry fixes the **spacing** $a$ (pure $\varphi$).
- Gravity fixes the **top** $\omega_0=E_P$ (pure $G$).
- Neither fixes **which rung** is the electron, i.e. $D$. That integer *is the intercept $b$ in disguise.*

Solving for the depth the framework would *need*:

$$D_{\rm need} = k_e - \frac{1}{a}\ln\!\frac{m_e}{E_P} = 24 + \frac{\ln(E_P/m_e)}{a} \approx 24 + \frac{\ln(2.39\times10^{22})}{0.10454}= 24 + \frac{51.52}{0.10454}\approx 24 + 492.9 = 516.9.$$

Is $516.9$ a clean $\varphi$-number? The natural geometric candidates are $N_\star=291.88$, $2n_H=366.2$, and $N_\star\varphi=N_\star+\Theta_H=291.88+180.39=472.3$. The **nearest** is $N_\star\varphi=472.3$, off by $-44.6$ shells $=$ a factor $e^{0.10454\times44.6}\approx 106$ in mass — i.e. **not** a clean hit. No pure-$\varphi$ combination reproduces $D\approx517$ to better than an order of magnitude in $m_e$.

**Therefore Route C does *not* pin the electron mass.** It pins the *top* of the ladder ($\omega_0=E_P$ from $G$ alone, exactly) and the *spacing* ($a$, from $\varphi$), but the electron's absolute mass needs one more integer datum — the desert depth $D$ — which the gravitational sector does not supply. The intercept $b$ survives as a genuinely missing input.

This is the **honest keystone result**: Route C reproduces Newton ($\nu_{\rm eff}=1.003$, $0.3\%$), pins $\omega_0=E_P=1.221\times10^{19}$ GeV exactly from $G$, and confirms the solar horizon shell $n_H=183.1$ — but it **fails to pin the electron mass** because the Planck-to-electron shell count is not a pure-$\varphi$ number. The miss, taking the best geometric candidate $D=N_\star\varphi=472.3$, is a **factor $\sim$100 ($\sim$10⁴%) high** on $m_e$.

If, alternatively, one *defines* the lepton-ladder zero by the measured electron (the round-3 convention), then $b$ is set by $m_e$ and Route C is circular for $m_e$ — which is exactly why we report the anti-circular version above and call it a non-pinning.

## Extension — the desert depth is a *power* of $\varphi$, not a sum: a sharper falsifier

The candidates tested above are *additive* $\varphi$-combinations ($N_\star$, $N_\star\varphi$, $2n_H$). But the shell ladder is **multiplicative** in length ($r_n=r_0\varphi^n$) and the depth $D$ is itself a shell *count*, so the natural geometric object is not $D$ but $\varphi^{\,D}$ — the bare hierarchy ratio $E_P/(\text{rung energy})$. Recast the missing datum as a pure ratio:

$$\boxed{\;\frac{E_P}{m_e}\Big/\varphi^{\,k_e}\;=\;\varphi^{\,D_{\rm need}}\,e^{(\ln\varphi-a)\,(D_{\rm need}-k_e)}\;\stackrel{?}{=}\;\varphi^{\,D_\star},\quad D_\star\in\{\text{pure-}\varphi\text{ integers}\}.\;}$$

Numerically $\ln(E_P/m_e)=51.53$, so the bare hierarchy is $\varphi^{\,107.08}$ ($51.53/\ln\varphi=107.08$). The keystone falsifier sharpens to a **single integer test**: *is the Planck-to-electron length hierarchy $\varphi^{107}$?* It is $\varphi^{107.08}$ — astonishingly close to the integer $107$ (off by $0.08$ shell, a $\sim$0.04 in $\ln$ units, $\sim$0.07% residual). Note $107 \approx N_\star - n_H - 1 = 291.88-183.08-1=107.80$ (within $\sim$0.7 shell), i.e. the UV hierarchy is the *cosmic depth minus the stellar-horizon depth*. This is the **first pure-$\varphi$ integer that lands on the electron** — but it lands on the **energy hierarchy $E_P/m_e=\varphi^{107}$**, not on the lepton-ladder count $D$, because the lepton sub-ladder runs at the *slower* rate $a=0.10454<\ln\varphi=0.4812$. The two rates are related by the SL(2,R) half-boost (note 07): $a/\ln\varphi=0.2172\approx 1/\varphi^{3}=0.2361$ to $8\%$, and exactly $\tfrac{a}{\ln\varphi}=\sin^2\theta_W$ (round 3, $1/\varphi^3$). The honest status is unchanged — $G$ still does not *predict* the integer $107$ from gravity alone — but the recasting reveals that the missing datum is a **single clean integer in the bare $\varphi$-hierarchy** ($107$), not the messy $516.9$ of the lepton-ladder frame. That is the tightest form of the keystone gap: one integer, $\varphi^{107}$, stands between $G$ and the electron.

## Prediction

**Falsifier (sharpened):** Route C is over-determined *iff* the Planck-to-electron **length hierarchy** equals an integer power of $\varphi$: $E_P/m_e=\varphi^{N}$. We find $N=107.07$ — within $1\%$ (in $\ln$) of the integer $107$, with the suggested decomposition $107\approx N_\star-n_H-1$. The standing prediction: if a future derivation produces $N=107$ as a forced pure-$\varphi$ integer (e.g. $N_\star-n_H-1$ from a Planck-to-cosmos shell-count identity), Route C is vindicated and $m_e=E_P\varphi^{-107}$ becomes a *prediction*; if Routes A and B independently yield $\omega_0\neq E_P=1.221\times10^{19}$ GeV (beyond $0.1\%$), the whole anchor is falsified. As it stands, $G$ alone pins the **top** ($\omega_0=E_P$) and the **spacing** ($a$), but NOT the electron's rung — the intercept $b$ remains one integer ($N=107$) short of derivation.
